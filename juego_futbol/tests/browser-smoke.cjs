const { chromium, devices } = require('playwright');
const assert = require('node:assert/strict');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const errors = [];
  try {
    for (const mode of ['desktop', 'mobile']) {
      const context = await browser.newContext(mode === 'mobile'
        ? { ...devices['iPhone 13'], viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true }
        : { viewport: { width: 1366, height: 900 } });
      const page = await context.newPage();
      page.on('pageerror', err => errors.push(mode + ': ' + err.message));
      page.on('dialog', dialog => dialog.accept());
      await page.goto('http://127.0.0.1:8765/juego_futbol/', { waitUntil: 'load' });
      if (mode === 'mobile') assert.equal(await page.evaluate(() => window.innerWidth), 390, 'ancho de pantalla móvil esperado');
      await page.waitForFunction(() => typeof estadoJuego !== 'undefined' && !!estadoJuego.equipos);
      assert.equal(await page.locator('.sim-disclaimer').count(), 1, 'aviso visible de simulación');
      assert.match(await page.locator('.sim-disclaimer').innerText(), /xG.*datos del juego/i);
      assert.equal(await page.evaluate(() => estadoJuego.equipos.length), 4);
      assert.equal(await page.evaluate(() => estadoJuego.jornadaActual), 0);
      const tabs = ['tactica', 'partido', 'clasificacion', 'mercado'];
      for (const tab of tabs) {
        await page.locator('button.tab-btn').filter({
          hasText: tab === 'tactica' ? 'Pizarra Táctica' :
            tab === 'partido' ? 'Día de Partido' :
            tab === 'clasificacion' ? 'Clasificación' : 'Mercado'
        }).click();
        assert.equal(await page.locator('#tab-' + tab).evaluate(el => getComputedStyle(el).display !== 'none'), true,
          'pestaña visible: ' + tab);
        if (mode === 'mobile') {
          const widths = await page.evaluate(() => ({
            document: document.documentElement.scrollWidth,
            viewport: window.innerWidth
          }));
          assert.ok(widths.document <= widths.viewport + 2, 'desbordamiento en pestaña ' + tab);
        }
      }
      await page.locator('button.tab-btn').filter({ hasText: 'Pizarra Táctica' }).click();
      const availability = await page.locator('#resumen-disponibilidad').innerText();
      assert.match(availability, /Disponibles: \d+\/\d+/);
      assert.match(availability, /Lesionados: \d+/);
      assert.match(availability, /Fatigados/);
      const injuryCheck = await page.evaluate(() => {
        const club = obtenerMiEquipo();
        const player = club.plantilla.find(j => j.titular);
        player.lesionado = 2;
        const result = calcularFuerzas(club);
        const excluded = !club.plantilla.some(j => j.titular && j.lesionado > 0);
        player.lesionado = 0;
        convocarOnceAutomatico(club);
        return { result, excluded };
      });
      assert.equal(injuryCheck.excluded, true, 'los lesionados no forman parte del once calculado');
      assert.ok(Number.isFinite(injuryCheck.result.ataque) && Number.isFinite(injuryCheck.result.defensa));
      const injuredShot = await page.evaluate(() => {
        const club = obtenerMiEquipo();
        const target = club.plantilla.find(j => j.titular);
        const prev = target.xg;
        target.lesionado = 3;
        const rival = estadoJuego.equipos.find(e => e !== club);
        const log = document.getElementById('match-log');
        const canvas = document.getElementById('canvas-shotmap');
        simularPartidoIndividual(club, rival, false, log, canvas.getContext('2d'), canvas.width, canvas.height);
        const unchanged = target.xg === prev;
        target.lesionado = 0;
        convocarOnceAutomatico(club);
        return unchanged;
      });
      assert.equal(injuredShot, true, 'un lesionado no puede rematar');
      const blockedRead = await page.evaluate(() => {
        const original = Storage.prototype.getItem;
        Storage.prototype.getItem = function () { throw new Error('lectura bloqueada'); };
        try {
          window.onload();
          return estadoJuego.equipos.length;
        } finally {
          Storage.prototype.getItem = original;
        }
      });
      assert.equal(blockedRead, 4, 'el juego debe arrancar con almacenamiento bloqueado');
      const saveFailure = await page.evaluate(() => {
        const original = Storage.prototype.setItem;
        Storage.prototype.setItem = function () { throw new Error('almacenamiento bloqueado'); };
        try {
          return guardarPartidaLocal(false);
        } finally {
          Storage.prototype.setItem = original;
        }
      });
      assert.equal(saveFailure, false, 'el fallo de almacenamiento no debe bloquear el juego');
      const shortSquad = await page.evaluate(() => {
        const club = obtenerMiEquipo();
        const original = club.plantilla.map(j => j.lesionado);
        const full = calcularFuerzas(club).ataque;
        club.plantilla.forEach((j, i) => { j.lesionado = i < 6 ? 0 : 3; });
        const depleted = calcularFuerzas(club).ataque;
        club.plantilla.forEach((j, i) => { j.lesionado = original[i]; });
        convocarOnceAutomatico(club);
        return { full, depleted };
      });
      assert.ok(shortSquad.depleted < shortSquad.full,
        'las bajas deben reducir la fuerza del equipo');
      const noPlayers = await page.evaluate(() => {
        const [home, away] = estadoJuego.equipos;
        const original = [home, away].map(eq => eq.plantilla.map(j => j.lesionado));
        for (const eq of [home, away]) eq.plantilla.forEach(j => { j.lesionado = 4; });
        const before = [home, away].map(eq => eq.xgf);
        const log = document.getElementById('match-log');
        const canvas = document.getElementById('canvas-shotmap');
        simularPartidoIndividual(home, away, false, log, canvas.getContext('2d'), canvas.width, canvas.height);
        const after = [home, away].map(eq => eq.xgf);
        [home, away].forEach((eq, i) => eq.plantilla.forEach((j, k) => { j.lesionado = original[i][k]; }));
        convocarOnceAutomatico(home);
        convocarOnceAutomatico(away);
        return { before, after };
      });
      assert.deepEqual(noPlayers.after, noPlayers.before,
        'equipos sin jugadores aptos no generan ocasiones');
      const training = await page.evaluate(() => {
        const club = obtenerMiEquipo();
        const fatigueBefore = club.plantilla.map(j => j.cansancio);
        accionEntrenar();
        const fatigueAfter = club.plantilla.map(j => j.cansancio);
        accionDescansar();
        const fatigueAfterBlockedRest = club.plantilla.map(j => j.cansancio);
        return { fatigueBefore, fatigueAfter, fatigueAfterBlockedRest, used: estadoJuego.preparacionUsada };
      });
      assert.equal(training.used, true);
      assert.deepEqual(training.fatigueAfterBlockedRest, training.fatigueAfter,
        'no se puede descansar tras entrenar en la misma jornada');
      assert.ok(training.fatigueAfter.some((n, i) => n > training.fatigueBefore[i]),
        'el entrenamiento genera cansancio');
      await page.reload();
      assert.equal(await page.evaluate(() => estadoJuego.preparacionUsada), true,
        'preparación persistente tras recarga');
      const invalidMarket = await page.evaluate(() => {
        const club = obtenerMiEquipo();
        const before = { money: club.presupuesto, size: club.plantilla.length,
          available: estadoJuego.mercado.length };
        ficharJugador(9999);
        venderJugador(9999);
        return { before, after: { money: club.presupuesto, size: club.plantilla.length,
          available: estadoJuego.mercado.length } };
      });
      assert.deepEqual(invalidMarket.after, invalidMarket.before,
        'índices de mercado inválidos no alteran el estado');
      const market = await page.evaluate(() => {
        const club = obtenerMiEquipo();
        const before = { money: club.presupuesto, size: club.plantilla.length, available: estadoJuego.mercado.length };
        const price = estadoJuego.mercado[0].precio;
        ficharJugador(0);
        const assertMarket = { afterBuyMoney: club.presupuesto, afterBuySize: club.plantilla.length,
          afterBuyAvailable: estadoJuego.mercado.length, price, before };
        venderJugador(club.plantilla.length - 1);
        return { ...assertMarket, afterSellMoney: club.presupuesto,
          afterSellSize: club.plantilla.length, afterSellAvailable: estadoJuego.mercado.length };
      });
      assert.equal(market.afterBuyMoney, market.before.money - market.price);
      assert.equal(market.afterBuySize, market.before.size + 1);
      assert.equal(market.afterBuyAvailable, market.before.available - 1);
      assert.equal(market.afterSellSize, market.before.size);
      assert.equal(market.afterSellAvailable, market.before.available);
      assert.equal(market.afterSellMoney, market.before.money - market.price + Math.round(market.price * 0.8));
      const beforeReload = await page.evaluate(() => ({
        money: obtenerMiEquipo().presupuesto,
        squad: obtenerMiEquipo().plantilla.length,
        market: estadoJuego.mercado.length
      }));
      await page.reload();
      const afterReload = await page.evaluate(() => ({
        money: obtenerMiEquipo().presupuesto,
        squad: obtenerMiEquipo().plantilla.length,
        market: estadoJuego.mercado.length
      }));
      assert.deepEqual(afterReload, beforeReload, 'mercado y presupuesto guardados automáticamente');
      await page.locator('button').filter({ hasText: 'Día de Partido' }).click();
      await page.locator('button').filter({ hasText: 'SIMULAR JORNADA' }).click();
      assert.equal(await page.evaluate(() => estadoJuego.jornadaActual), 1);
      await page.reload();
      assert.equal(await page.evaluate(() => estadoJuego.jornadaActual), 1, 'partida persistente');
      await page.evaluate(() => { for (let i = 1; i < 6; i++) simularJornada(); });
      assert.equal(await page.evaluate(() => estadoJuego.jornadaActual), 6);
      await page.evaluate(() => iniciarNuevaTemporada());
      assert.equal(await page.evaluate(() => estadoJuego.temporada), 2);
      assert.equal(await page.evaluate(() => estadoJuego.jornadaActual), 0);
      assert.equal(await page.evaluate(() => estadoJuego.calendario.length), 6);
      await page.reload();
      assert.equal(await page.evaluate(() => estadoJuego.temporada), 2);
      await page.evaluate(() => localStorage.setItem('ldp_manager_save',
        JSON.stringify({ equipos: [], mercado: [], calendario: [], jornadaActual: 0, temporada: 1 })));
      await page.reload();
      assert.equal(await page.evaluate(() => estadoJuego.equipos.length), 4,
        'partida estructuralmente inválida rechazada');
      await page.evaluate(() => {
        const partida = crearEstadoInicial();
        partida.equipos[0].plantilla[0].media = 'incorrecta';
        localStorage.setItem('ldp_manager_save', JSON.stringify(partida));
      });
      await page.reload();
      assert.equal(await page.evaluate(() => typeof estadoJuego.equipos[0].plantilla[0].media), 'number',
        'partida con valoración de jugador corrupta rechazada');
      await page.evaluate(() => localStorage.setItem('ldp_manager_save', '{bad json'));
      await page.reload();
      assert.equal(await page.evaluate(() => estadoJuego.temporada), 1);
      if (mode === 'mobile') {
        const size = await page.evaluate(() => ({
          documentWidth: document.documentElement.scrollWidth,
          viewportWidth: window.innerWidth
        }));
        console.log('Mobile layout:', size);
        assert.ok(size.documentWidth <= size.viewportWidth + 2, 'desbordamiento horizontal móvil');
      }
      await context.close();
      console.log(mode + ': OK');
    }
    assert.deepEqual(errors, [], 'errores JS en navegador');
  } finally {
    await browser.close();
  }
})().catch(err => { console.error(err); process.exitCode = 1; });
