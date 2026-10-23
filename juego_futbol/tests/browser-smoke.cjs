// Prueba integral con navegador real: el workflow sirve el HTML y genera capturas.
// Repito los flujos en ordenador y en un viewport táctil con tamaño de iPhone.
const { chromium, devices } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const errors = [];
  const artifactDir = require('node:path').join(__dirname, 'test-artifacts');
  await fs.mkdir(artifactDir, { recursive: true });
  try {
    // Uso el mismo recorrido para detectar diferencias entre escritorio y móvil.
    for (const mode of ['desktop', 'mobile']) {
      const context = await browser.newContext(mode === 'mobile'
        ? { ...devices['iPhone 13'], viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true }
        : { viewport: { width: 1366, height: 900 } });
      const page = await context.newPage();
      page.on('pageerror', err => errors.push(mode + ': ' + err.message));
      page.on('console', message => {
        if (message.type() === 'error') errors.push(mode + ' consola: ' + message.text());
      });
      page.on('dialog', dialog => dialog.accept());
      // La web presenta el juego en el catálogo y ofrece una explicación real de xG.
      await page.goto('http://127.0.0.1:8765/proyectos/', { waitUntil: 'load' });
      const ctaJuego = page.getByRole('link', { name: 'Probar el juego web' });
      assert.equal(await ctaJuego.getAttribute('href'), '../juego_futbol/index.html',
        'el catálogo enlaza al juego web y no promete una descarga móvil');
      await ctaJuego.click();
      await page.waitForURL('**/juego_futbol/index.html');
      const enlaceXg = page.getByRole('link', { name: 'Aprende qué mide el xG y cómo interpretarlo' });
      assert.equal(await enlaceXg.getAttribute('href'), '../proyectos/xg/index.html',
        'el aviso del simulador enlaza a la explicación de xG existente');
      await enlaceXg.click();
      await page.waitForURL('**/proyectos/xg/index.html');
      assert.match(await page.locator('h1').innerText(), /xG/i, 'la explicación enlazada se puede abrir');
      await page.goto('http://127.0.0.1:8765/juego_futbol/', { waitUntil: 'load' });
      if (mode === 'mobile') assert.equal(await page.evaluate(() => window.innerWidth), 390, 'ancho de pantalla móvil esperado');
      await page.emulateMedia({ reducedMotion: 'reduce' });
      const movimientoReducido = await page.evaluate(() => ({
        preferencia: matchMedia('(prefers-reduced-motion: reduce)').matches,
        animacionPanel: parseFloat(getComputedStyle(document.querySelector('.tab-content')).animationDuration),
        transicionPestana: parseFloat(getComputedStyle(document.querySelector('.tab-btn')).transitionDuration)
      }));
      assert.equal(movimientoReducido.preferencia, true, 'el navegador puede solicitar movimiento reducido');
      assert.ok(movimientoReducido.animacionPanel <= 0.001, 'los paneles reducen su animación');
      assert.ok(movimientoReducido.transicionPestana <= 0.001, 'las pestañas reducen su transición');
      await page.emulateMedia({ reducedMotion: 'no-preference' });
      try {
        await page.waitForFunction(() => typeof estadoJuego !== 'undefined' && !!estadoJuego.equipos);
      } catch (error) {
        throw new Error(`${error.message}; errores de página: ${JSON.stringify(errors)}`);
      }
      // Compruebo que el simulador arranca con las plantillas paródicas separadas de sus clubes reales.
      const integridadPlantillas = await page.evaluate(() => ({
        temporada: PLANTILLAS_DB.temporada,
        equipos: PLANTILLAS_DB.equipos.map(e => e.nombre_parodico),
        tamaños: PLANTILLAS_DB.equipos.map(e => e.jugadores.length),
        jugadores: PLANTILLAS_DB.equipos.map(e => e.jugadores.map(j => j.nombre)),
        consistencia: PLANTILLAS_DB.equipos.every(e => e.jugadores.every(j =>
          j.avatar_ia && j.avatar_ia.includes('assets/ia/avatares/') &&
          ['RAS','TOZ','CHI','RET','ALM'].every(k => Number.isInteger(j.atributos[k])))),
        control: obtenerMiEquipo().nombre,
        panelActivo: document.querySelector('[role="tabpanel"][aria-hidden="false"]')?.id
      }));
      assert.equal(integridadPlantillas.temporada, '2026/27');
      assert.deepEqual(integridadPlantillas.equipos, [
        'Real Magras de Madrid', 'Balompié del Somontano',
        'Atlético Colchonico de la Ribera', 'Athletic de la Tronca'
      ]);
      assert.ok(integridadPlantillas.tamaños.every(n => n >= 14), 'cada club tiene fondo de plantilla para rotar');
      assert.equal(integridadPlantillas.consistencia, true, 'cada jugador declara caricatura IA y cinco atributos paródicos');
      const nombresImprescindibles = [
        'Kylian Embozado', 'Vini de la Cadiera', 'Jude el Campanero', 'Fede Chispazo', 'Thibaut el Muro',
        'Lamine el Almendrón', 'Dani Pasapúes', 'Raphinha el Abentau', 'Gavi Rompetrastes',
        'Pedri de la Acequia', 'Pau Tozudo', 'Julián la Araña Baturra', 'Alexander el Picador',
        'Jan Cerrojo', 'Nico Remolino', 'Iñaki el Trillo', 'Oihan el Zagal'
      ];
      assert.ok(nombresImprescindibles.every(nombre => integridadPlantillas.jugadores.flat().includes(nombre)),
        'la base incluye las parodias solicitadas de los cuatro equipos');
      assert.equal(integridadPlantillas.control, 'Real Magras de Madrid');
      assert.equal(integridadPlantillas.panelActivo, 'tab-clasificacion', 'la vista inicial coincide con Despacho Míster');
      const impactoAtributos = await page.evaluate(() => {
        const jugador = obtenerMiEquipo().plantilla.find(j => !j.lesionado && j.atributos.CHI < 99);
        const original = jugador.atributos.CHI;
        const inicial = rendimientoReal(jugador);
        jugador.atributos.CHI = 99;
        const mejorado = rendimientoReal(jugador);
        jugador.atributos.CHI = original;
        return { inicial, mejorado };
      });
      assert.ok(impactoAtributos.mejorado > impactoAtributos.inicial,
        'los atributos paródicos influyen en el rendimiento según la posición');
      await page.locator('#pestana-tactica').click();
      const anclajesMenu = await page.evaluate(() => {
        const nav = document.querySelector('nav[role="tablist"]');
        const cta = document.getElementById('floating-cta');
        return { nav: getComputedStyle(nav).position, ctaVisible: !!cta && getComputedStyle(cta).position === 'fixed',
          separados: cta.getBoundingClientRect().bottom <= nav.getBoundingClientRect().top + 2 };
      });
      assert.equal(anclajesMenu.nav, 'fixed', 'la navegación inferior permanece fija');
      assert.equal(anclajesMenu.ctaVisible, true, 'el CTA de avance queda fijo y visible');
      assert.equal(anclajesMenu.separados, true, 'el CTA no queda debajo de la navegación');
      // La rotación manual es operable con teclado y comunica selección y bajas.
      const indicesRotacion = await page.evaluate(() => {
        const plantilla = obtenerMiEquipo().plantilla;
        return {
          titular: plantilla.findIndex(j => j.titular && j.lesionado === 0),
          suplente: plantilla.findIndex(j => !j.titular && j.lesionado === 0)
        };
      });
      assert.ok(indicesRotacion.titular >= 0 && indicesRotacion.suplente >= 0,
        'debe haber un titular y un suplente aptos para probar la rotación');
      if (mode === 'mobile') {
        const tablaPlantillaMovil = await page.evaluate(() => {
          const tabla = document.querySelector('.squad-table');
          const estilo = getComputedStyle(tabla.querySelector('tbody tr'));
          const campos = ['Cans', 'Goles', 'xG', 'Estado'].map(campo => {
            const celda = tabla.querySelector(`td[data-label="${campo}"]`);
            return { campo, visible: getComputedStyle(celda).display !== 'none', anchura: celda.getBoundingClientRect().width };
          });
          return { plantilla: tabla.scrollWidth <= tabla.clientWidth + 1, columnas: estilo.display,
            campos, anchoDocumento: document.documentElement.scrollWidth, anchoVentana: innerWidth };
        });
        assert.equal(tablaPlantillaMovil.plantilla, true,
          'la plantilla muestra todas sus columnas sin desplazamiento horizontal en móvil');
        assert.equal(tablaPlantillaMovil.columnas, 'grid', 'cada futbolista se organiza como ficha compacta en móvil');
        assert.ok(tablaPlantillaMovil.campos.every(campo => campo.visible && campo.anchura > 0),
          'fatiga, goles, xG y estado siguen visibles en móvil');
        assert.ok(tablaPlantillaMovil.anchoDocumento <= tablaPlantillaMovil.anchoVentana + 2,
          'la plantilla adaptable no ensancha la página móvil');
      }
      const selectorJugador = indice => `#tbody-plantilla .player-select-btn[data-player-index="${indice}"]`;
      const botonTitular = page.locator(selectorJugador(indicesRotacion.titular));
      assert.equal(await botonTitular.getAttribute('aria-pressed'), 'false', 'ningún jugador está seleccionado al cargar');
      await botonTitular.focus();
      await page.keyboard.press('Enter');
      assert.equal(await page.locator(selectorJugador(indicesRotacion.titular)).getAttribute('aria-pressed'), 'true',
        'Enter selecciona un jugador y expone el estado accesible');
      const botonSuplente = page.locator(selectorJugador(indicesRotacion.suplente));
      await botonSuplente.focus();
      await page.keyboard.press('Space');
      const rotacionTeclado = await page.evaluate(({ titular, suplente }) => ({
        titular: obtenerMiEquipo().plantilla[titular].titular,
        suplente: obtenerMiEquipo().plantilla[suplente].titular,
        seleccionCancelada: document.querySelector('.player-select-btn[aria-pressed="true"]') === null
      }), indicesRotacion);
      assert.deepEqual(rotacionTeclado, { titular: false, suplente: true, seleccionCancelada: true },
        'Espacio completa el intercambio y limpia la selección');
      const baja = await page.evaluate(indice => {
        const club = obtenerMiEquipo();
        const original = club.plantilla[indice].lesionado;
        club.plantilla[indice].lesionado = 1;
        actualizarUI();
        const boton = document.querySelector(`.player-select-btn[data-player-index="${indice}"]`);
        const resultado = { desactivado: boton.disabled, explicacion: boton.title };
        club.plantilla[indice].lesionado = original;
        actualizarUI();
        return resultado;
      }, indicesRotacion.titular);
      assert.deepEqual(baja, { desactivado: true, explicacion: 'Jugador lesionado' },
        'una baja no se puede elegir y el control explica por qué');
      await page.evaluate(({ titular, suplente }) => {
        const plantilla = obtenerMiEquipo().plantilla;
        plantilla[titular].titular = true;
        plantilla[suplente].titular = false;
        jugadorSeleccionadoIdx = null;
        guardarPartidaLocal(false);
        actualizarUI();
      }, indicesRotacion);
      // La ayuda de rotación solo releva con un suplente apto de la misma posición y menos fatiga.
      const escenarioRotacion = await page.evaluate(() => {
        const plantilla = obtenerMiEquipo().plantilla;
        const titular = plantilla.findIndex(j => j.titular && j.lesionado === 0 &&
          plantilla.some(s => !s.titular && s.lesionado === 0 && s.posicion === j.posicion));
        const suplente = plantilla.findIndex(j => !j.titular && j.lesionado === 0 &&
          j.posicion === plantilla[titular]?.posicion);
        const original = plantilla.map(j => ({ titular: j.titular, cansancio: j.cansancio }));
        plantilla.forEach(j => { j.cansancio = 10; });
        plantilla[titular].cansancio = 90;
        plantilla[suplente].cansancio = 20;
        actualizarUI();
        return { titular, suplente, nombreTitular: plantilla[titular].nombre,
          nombreSuplente: plantilla[suplente].nombre, original };
      });
      assert.ok(escenarioRotacion.titular >= 0 && escenarioRotacion.suplente >= 0,
        'la plantilla base debe incluir un relevo de la misma posición');
      await page.locator('#btn-rotar-fatigados').click();
      const cambioFatiga = await page.evaluate(({ titular, suplente }) => ({
        titular: obtenerMiEquipo().plantilla[titular].titular,
        suplente: obtenerMiEquipo().plantilla[suplente].titular,
        mensaje: document.getElementById('resultado-rotacion').textContent
      }), escenarioRotacion);
      assert.deepEqual({ titular: cambioFatiga.titular, suplente: cambioFatiga.suplente },
        { titular: false, suplente: true }, 'el relevo cambia a los dos jugadores sin alterar su posición');
      assert.match(cambioFatiga.mensaje,
        new RegExp(`Rotaciones aplicadas: ${escenarioRotacion.nombreTitular} por ${escenarioRotacion.nombreSuplente}`),
        'la herramienta anuncia el cambio concreto');
      await page.evaluate(({ original }) => {
        obtenerMiEquipo().plantilla.forEach((j, indice) => {
          j.titular = original[indice].titular;
          j.cansancio = original[indice].cansancio;
        });
        guardarPartidaLocal(false);
        actualizarUI();
      }, escenarioRotacion);
      await page.locator('#pestana-partido').click();
      await page.locator('[data-video-action="var"]').click();
      assert.equal(await page.locator('#microclip-backdrop').getAttribute('aria-hidden'), 'false',
        'el disparador VAR abre el reproductor/fallback visual');
      assert.match(await page.locator('#microclip-title').innerText(), /VAR de pueblo/);
      await page.locator('#microclip-close').click();
      // Navegación rediseñada, módulo Tinder, CTAs y finanzas.
      assert.deepEqual(await page.locator('button.tab-btn').allInnerTexts().then(xs=>xs.map(x=>x.trim())), [
        '🏠 Despacho Míster', '🔥 Tinder Fichajes', '📋 Táctica', '⚽ Partido'
      ], 'las cuatro secciones usan nombres y orden claros');
      await page.locator('#pestana-mercado').click();
      assert.ok(await page.locator('#swipe-card').isVisible(), 'se presenta la tarjeta de ojeo');
      assert.deepEqual(await page.locator('#tbody-mercado').locator('xpath=ancestor::table').locator('thead th').allInnerTexts(),
        ['Jugador', 'Pos', 'Rasgos', 'Precio', 'Salario/j', 'Acción'],
        'la tabla de mercado también expone los atributos paródicos en lugar de la media');
      const partidaAntesSwipe = await page.evaluate(() => JSON.parse(JSON.stringify(estadoJuego)));
      const swipeInicial = await page.locator('#swipe-name').innerText();
      await page.locator('#swipe-reject').click();
      assert.notEqual(await page.locator('#swipe-name').innerText(), swipeInicial, 'descartar avanza al siguiente candidato');
      assert.match(await page.locator('#swipe-feedback').innerText(), /cierzo|abrazo|propicio/i, 'el descarte responde con retranca');
      assert.equal(await page.locator('#microclip-backdrop').getAttribute('aria-hidden'), 'false',
        'el descarte abre la reacción visual preparada para el clip IA');
      assert.match(await page.locator('#video-action-status').innerText(), /clips IA se incorporarán/,
        'el fallback explica que el asset de vídeo aún no está generado');
      await page.locator('#microclip-close').click();
      const ficha = await page.evaluate(() => ({
        caricatura: document.getElementById('swipe-portrait').dataset.portraitId,
        clausula: document.getElementById('swipe-clause').textContent,
        etiquetas: [...document.querySelectorAll('#swipe-stats .swipe-stat')].length,
        atributos: document.querySelectorAll('#swipe-stats .attribute-pill').length,
        codigos: [...document.querySelectorAll('#swipe-stats .attribute-pill small')].map(e=>e.textContent)
      }));
      assert.match(ficha.caricatura, /^caricatura-/);
      assert.ok(ficha.clausula.length>20 && ficha.etiquetas>=4, 'ficha lista atributos, cláusula y placeholder de ilustración');
      assert.equal(ficha.atributos, 5, 'la carta ofrece los cinco atributos humorísticos');
      assert.deepEqual(ficha.codigos, ['RAS','TOZ','CHI','RET','ALM']);
      assert.ok(window.DATOS_ARAGONESES.equipos.includes('Real Magras de Madrid') &&
        window.DATOS_ARAGONESES.equipos.includes('Athletic de la Tronca'), 'el universo incluye clubes aragoneses ficticios');

      await page.locator('#pestana-clasificacion').click();
      assert.equal(await page.locator('.cta-card button').count(), 2, 'despacho ofrece dos acciones siguientes');
      await page.locator('#pestana-clasificacion').click();
      await page.locator('#tab-clasificacion details').last().evaluate(el => { el.open = true; });
      assert.match(await page.locator('#finance-budget').innerText(), /€/);
      assert.match(await page.locator('#finance-wages').innerText(), /€/);
      assert.equal(await page.locator('#sponsor-options .sponsor-card').count(), 3, 'hay tres contratos absurdos disponibles');
      await page.locator('[data-sponsor="cero-cero"]').click();
      assert.match(await page.locator('#sponsor-status').innerText(), /Contrato firmado/, 'la firma activa un objetivo y una prima');
      assert.equal(await page.locator('#floating-cta').isVisible(), true, 'la llamada a la acción permanece fija en pantalla');
      const candidatoLocalizado = await page.evaluate(() => {
        const j = estadoJuego.mercado[0];
        const rival = estadoJuego.equipos.find(eq => eq.plantilla.some(p => p.jugador_id === j.jugador_id));
        return { jugador: j.nombre, id: j.jugador_id, clubId: rival?.id };
      });
      await page.locator('#swipe-match').click();
      const rosterTrasMatch = await page.evaluate(({ id, clubId }) => ({
        fichado: obtenerMiEquipo().plantilla.filter(j => j.jugador_id === id).length,
        sigueEnOrigen: estadoJuego.equipos.find(eq => eq.id === clubId)?.plantilla.some(j => j.jugador_id === id) || false
      }), candidatoLocalizado);
      assert.equal(rosterTrasMatch.fichado, 1, 'el match incorpora al jugador exactamente una vez');
      assert.equal(rosterTrasMatch.sigueEnOrigen, false, 'el traspaso lo retira de su club de origen');
      await page.locator('#microclip-close').click();
      await page.evaluate(partida => { estadoJuego=partida; guardarPartidaLocal(false); actualizarUI(); }, partidaAntesSwipe);
      assert.equal(await page.locator('#finance-squad').innerText(), '14 jugadores · 11 titulares');
      await page.locator('#pestana-partido').click();
      assert.equal(await page.locator('#match-clock').innerText(), '00′');
      assert.equal(await page.locator('#sel-estilo').inputValue(), 'Equilibrado');
      await page.locator('[data-quick-plan="Ofensivo"]').click();
      assert.equal(await page.locator('#sel-estilo').inputValue(), 'Ofensivo', 'la decisión rápida actualiza el estilo del motor');
      assert.match(await page.locator('#match-decision-feedback').innerText(), /próxima jornada/);
      await page.locator('#pestana-tactica').click();
      await page.screenshot({ path: require('node:path').join(artifactDir, `juego-${mode}.png`), fullPage: true });
      // Identidad ficticia, aviso de métricas simuladas, avatares propios y modelo de ataque/defensa.
      assert.equal(await page.locator('.sim-disclaimer').count(), 1, 'aviso visible de simulación');
      assert.match(await page.locator('.sim-disclaimer').innerText(), /xG.*datos del juego/i);
      assert.match(await page.locator('#guia-rapida summary').innerText(), /Cómo jugar/);
      await page.locator('#guia-rapida summary').click();
      assert.match(await page.locator('#guia-rapida').innerText(), /una vez antes de cada jornada/);
      assert.match(await page.locator('#guia-rapida').innerText(), /seis jornadas/);
      await page.locator('#guia-rapida summary').click();
      assert.equal(await page.locator('#btn-simular-jornada').innerText(), '▶️ SIMULAR JORNADA EN VIVO');
      assert.equal(await page.evaluate(() => estadoJuego.equipos.length), 4);
      assert.equal(await page.locator('#tbody-match-breakdown tr').innerText(),
        'El balance aparecerá al terminar el partido.', 'la tabla explica cuándo estará disponible');
      assert.equal(await page.locator('#btn-exportar-balance').isDisabled(), true,
        'el CSV no se ofrece antes de tener un balance');
      const plantillasFicticias = await page.evaluate(() => ({
        clubes: estadoJuego.equipos.map(e => e.nombre),
        jugadores: estadoJuego.equipos.flatMap(e => e.plantilla.map(j => j.nombre)),
        mercado: estadoJuego.mercado.map(j => j.nombre),
        perfilesRivales: estadoJuego.equipos.slice(1).map(e => [e.formacion, e.estilo]),
        cabecera: document.querySelector('.club-brand h1')?.textContent.trim()
      }));
      assert.deepEqual(plantillasFicticias.clubes, [
        'Real Magras de Madrid', 'Balompié del Somontano', 'Atlético Colchonico de la Ribera', 'Athletic de la Tronca'
      ], 'todos los clubes deben ser ficticios');
      assert.equal(plantillasFicticias.cabecera, 'REAL MAGRAS DE MADRID', 'la cabecera debe usar la identidad ficticia');
      assert.ok(plantillasFicticias.jugadores.every(nombre => !/^(POR|DEF|CEN|DEL)_/.test(nombre)),
        'los rivales no deben mostrar identificadores internos como nombres');
      assert.ok(plantillasFicticias.jugadores.some(nombre => nombre === 'Kylian Embozado'));
      assert.deepEqual(plantillasFicticias.mercado, [
        "Dani del Sendero", "Yuri Espino", "Marcos de la Lumbre", "Frenkie de la Ronda", "Johnny el Rastrojo"
      ], 'el mercado sale de los candidatos declarados en la base actual');
      assert.deepEqual(plantillasFicticias.perfilesRivales, [
        ['4-3-3', 'Ofensivo'], ['4-3-3', 'Defensivo'], ['4-3-3', 'Equilibrado']
      ], 'los rivales deben presentar perfiles tácticos diferenciados');
      const perfilProximoRival = await page.evaluate(() => {
        const miEquipo = obtenerMiEquipo();
        const cruce = estadoJuego.calendario[estadoJuego.jornadaActual]
          .find(([local, visitante]) => local === miEquipo.nombre || visitante === miEquipo.nombre);
        const rival = estadoJuego.equipos.find(eq => eq.nombre === cruce.find(nombre => nombre !== miEquipo.nombre));
        const fuerzas = calcularFuerzas(rival);
        return {
          nombre: rival.nombre,
          formacion: rival.formacion,
          estilo: rival.estilo,
          juegaEnCasa: cruce[0] === miEquipo.nombre,
          disponibilidad: {
            aptos: miEquipo.plantilla.filter(j => j.lesionado === 0).length,
            total: miEquipo.plantilla.length,
            bajas: miEquipo.plantilla.filter(j => j.lesionado > 0).length,
            fatigados: miEquipo.plantilla.filter(j => j.lesionado === 0 && j.cansancio >= 75).length,
            titularesFatigados: miEquipo.plantilla.filter(j => j.titular && j.lesionado === 0 && j.cansancio >= 75).length
          },
          ataque: fuerzas.ataque.toFixed(1),
          defensa: fuerzas.defensa.toFixed(1),
          ataquePropio: calcularFuerzas(miEquipo).ataque.toFixed(1),
          defensaPropia: calcularFuerzas(miEquipo).defensa.toFixed(1)
        };
      });
      const textoPreviaRival = await page.locator('#match-preview').innerText();
      assert.ok(textoPreviaRival.includes(perfilProximoRival.nombre) &&
        textoPreviaRival.includes(`${perfilProximoRival.formacion} · ${perfilProximoRival.estilo}`) &&
        textoPreviaRival.includes(`Localía: ${perfilProximoRival.juegaEnCasa ? 'juegas en casa' : 'juegas fuera'} · el motor aplica +3 al ataque local si hay jugadores aptos`) &&
        textoPreviaRival.includes(`Plantilla: ${perfilProximoRival.disponibilidad.aptos}/${perfilProximoRival.disponibilidad.total} disponibles · ${perfilProximoRival.disponibilidad.bajas} bajas · ${perfilProximoRival.disponibilidad.fatigados} con fatiga ≥75 % (${perfilProximoRival.disponibilidad.titularesFatigados} titulares)`) &&
        textoPreviaRival.includes(`rival, ataque ${perfilProximoRival.ataque} / defensa ${perfilProximoRival.defensa}`) &&
        textoPreviaRival.includes(`tu ataque vs defensa rival ${perfilProximoRival.ataquePropio} vs ${perfilProximoRival.defensa}`) &&
        textoPreviaRival.includes(`tu defensa vs ataque rival ${perfilProximoRival.defensaPropia} vs ${perfilProximoRival.ataque}`) &&
        textoPreviaRival.includes('no predicen el resultado'),
        'la previa muestra ambos perfiles, los cruces de fuerzas y aclara que no es un pronóstico');
      const avatarCheck = await page.evaluate(() => {
        const avatares = [...document.querySelectorAll('#tbody-plantilla .player-avatar')];
        const avatarMercado = [...document.querySelectorAll('#tbody-mercado .player-avatar')];
        const muestra = avatarJugadorHTML('Kylian Embozado', 'POR');
        return {
          plantel: avatares.length,
          mercado: avatarMercado.length,
          decorativos: [...avatares, ...avatarMercado].every(svg => svg.getAttribute('aria-hidden') === 'true'),
          estables: muestra === avatarJugadorHTML('Kylian Embozado', 'POR'),
          distintos: muestra !== avatarJugadorHTML('Rita Remates', 'DEL'),
          sinRecursosExternos: [...avatares, ...avatarMercado].every(svg => !svg.querySelector('[href], image'))
        };
      });
      assert.equal(avatarCheck.plantel, 14, 'cada jugador de la plantilla tiene avatar vectorial');
      assert.equal(avatarCheck.mercado, 5, 'cada fichaje disponible tiene avatar vectorial');
      assert.equal(avatarCheck.decorativos, true, 'el avatar complementa el nombre sin duplicar lectura accesible');
      assert.equal(avatarCheck.estables, true, 'el mismo personaje conserva su avatar determinista');
      assert.equal(avatarCheck.distintos, true, 'nombres diferentes producen retratos diferenciados');
      assert.equal(avatarCheck.sinRecursosExternos, true, 'los retratos no cargan imágenes de terceros');
      const matchModelCheck = await page.evaluate(() => {
        const equilibrado = calcularPerfilAtaque(70, 70);
        const ventajaAtacante = calcularPerfilAtaque(82, 65);
        const defensaSuperior = calcularPerfilAtaque(65, 82);
        const extremos = [calcularPerfilAtaque(-10, 0), calcularPerfilAtaque(1000, 1)];
        return {
          ataqueCreaMasRemates: ventajaAtacante.probabilidadRemate > equilibrado.probabilidadRemate,
          defensaReduceRemates: defensaSuperior.probabilidadRemate < equilibrado.probabilidadRemate,
          ataqueMejoraCalidad: ventajaAtacante.ajusteXg > equilibrado.ajusteXg,
          defensaReduceCalidad: defensaSuperior.ajusteXg < equilibrado.ajusteXg,
          acotado: extremos.every(perfil => Number.isFinite(perfil.probabilidadRemate) &&
            perfil.probabilidadRemate >= 0.45 && perfil.probabilidadRemate <= 0.90 &&
            perfil.probabilidadOcasionClara >= 0.10 && perfil.probabilidadOcasionClara <= 0.50 &&
            perfil.ajusteXg >= -0.08 && perfil.ajusteXg <= 0.08)
        };
      });
      assert.deepEqual(matchModelCheck, {
        ataqueCreaMasRemates: true,
        defensaReduceRemates: true,
        ataqueMejoraCalidad: true,
        defensaReduceCalidad: true,
        acotado: true
      }, 'el motor debe reflejar ataque y defensa rivales al generar remates y xG');
      assert.equal(await page.evaluate(() => estadoJuego.jornadaActual), 0);
      // Verifico navegación completa y ausencia de desplazamiento horizontal en móvil.
      const tabs = ['mercado', 'tactica', 'partido', 'clasificacion'];
      for (const tab of tabs) {
        await page.locator('button.tab-btn').filter({
          hasText: tab === 'tactica' ? 'Táctica' :
            tab === 'partido' ? 'Partido' :
            tab === 'clasificacion' ? 'Despacho' : 'Fichajes'
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
      const accesibilidadTabs = await page.evaluate(() => ({
        total: document.querySelectorAll('[role="tab"]').length,
        seleccionadas: [...document.querySelectorAll('[role="tab"][aria-selected="true"]')].map(tab => tab.id),
        paneles: [...document.querySelectorAll('[role="tabpanel"]')].every(panel =>
          panel.getAttribute('aria-labelledby') && panel.hasAttribute('aria-hidden'))
      }));
      assert.equal(accesibilidadTabs.total, 4, 'la navegación expone cuatro pestañas accesibles');
      assert.deepEqual(accesibilidadTabs.seleccionadas, ['pestana-clasificacion']);
      assert.equal(accesibilidadTabs.paneles, true, 'cada pestaña identifica su panel');
      await page.locator('#pestana-clasificacion').focus();
      await page.keyboard.press('ArrowRight');
      assert.equal(await page.locator('#pestana-mercado').getAttribute('aria-selected'), 'true',
        'la flecha derecha avanza a Tinder Fichajes');
      assert.equal(await page.evaluate(() => document.activeElement.id), 'pestana-mercado');
      await page.keyboard.press('End');
      assert.equal(await page.locator('#pestana-partido').getAttribute('aria-selected'), 'true',
        'Fin selecciona la última pestaña');
      await page.keyboard.press('Home');
      assert.equal(await page.locator('#pestana-clasificacion').getAttribute('aria-selected'), 'true',
        'Inicio selecciona la primera pestaña');
      // Compruebo ejercicios, sus marcadores de progreso y la persistencia de cada modalidad.
      await page.locator('#pestana-clasificacion').click();
      await page.locator('#tab-clasificacion details').last().evaluate(el => { el.open = true; });
      const trainingBefore = await page.evaluate(() => ({
        opcion: retoPaseActual.opcionRecomendada,
        indice: retoPaseActual.indice,
        intentos: estadoJuego.entrenamiento.intentos,
        jugadores: obtenerMiEquipo().plantilla.map(j => [j.media, j.cansancio, j.moral])
      }));
      await page.locator(`#pase-opciones button[data-opcion-index="${trainingBefore.opcion}"]`).click();
      assert.match(await page.locator('#pase-feedback').innerText(), /^100\/100/,
        'la mejor decisión debe recibir la máxima valoración del ejercicio');
      const trainingAfter = await page.evaluate(() => ({
        intentos: estadoJuego.entrenamiento.intentos,
        puntos: estadoJuego.entrenamiento.puntos,
        mejor: estadoJuego.entrenamiento.mejorPuntuacion,
        jugadores: obtenerMiEquipo().plantilla.map(j => [j.media, j.cansancio, j.moral]),
        botonesBloqueados: [...document.querySelectorAll('#pase-opciones button')].every(b => b.disabled)
      }));
      assert.equal(trainingAfter.intentos, trainingBefore.intentos + 1);
      assert.equal(trainingAfter.puntos, 100);
      assert.equal(trainingAfter.mejor, 100);
      assert.deepEqual(trainingAfter.jugadores, trainingBefore.jugadores,
        'el ejercicio no altera atributos ni fatiga de la plantilla');
      assert.equal(trainingAfter.botonesBloqueados, true,
        'una misma situación no se puede puntuar varias veces');
      await page.locator('#btn-siguiente-pase').click();
      assert.notEqual(await page.evaluate(() => retoPaseActual.indice), trainingBefore.indice,
        'siguiente ejercicio presenta otro contexto');
      const corruptTraining = await page.evaluate(() => {
        const partida = crearEstadoInicial();
        partida.entrenamiento.mejorPuntuacion = 101;
        return estadoPartidaValido(partida);
      });
      assert.equal(corruptTraining, false, 'las estadísticas de entrenamiento se validan al importar');
      const corruptArchive = await page.evaluate(() => {
        const partida = crearEstadoInicial();
        partida.historialTemporadas = [{ temporada: 1, clasificacion: [], pichichi: null }];
        return estadoPartidaValido(partida);
      });
      assert.equal(corruptArchive, false, 'un resumen histórico incompleto se rechaza al importar');
      const legacyArchive = await page.evaluate(() => {
        const partida = crearEstadoInicial();
        partida.historialTemporadas = [{
          temporada: 1,
          clasificacion: partida.equipos.map(eq => ({ nombre: eq.nombre, puntos: 0, gf: 0, gc: 0 })),
          pichichi: { nombre: 'Kylian Embozado', equipo: 'Real Magras de Madrid', goles: 4, xg: 2.5 }
        }];
        const migrada = normalizarEstadoPartida(partida);
        return { valida: estadoPartidaValido(migrada), resumen: migrada.historialTemporadas[0] };
      });
      assert.equal(legacyArchive.valida, true, 'los resúmenes guardados con un único pichichi se migran');
      assert.equal(legacyArchive.resumen.goleadores[0].nombre, 'Kylian Embozado');
      assert.equal(Object.hasOwn(legacyArchive.resumen, 'pichichi'), false,
        'la migración deja el resumen histórico en el formato actual');
      assert.ok(legacyArchive.resumen.clasificacion.every(eq => eq.pj === 6 &&
        eq.remates === null && eq.xgf === null && eq.xgc === null),
        'la migración distingue las métricas históricas desconocidas de los ceros');
      const legacySave = await page.evaluate(() => {
        const partida = crearEstadoInicial();
        delete partida.entrenamiento;
        return estadoPartidaValido(partida);
      });
      assert.equal(legacySave, true, 'los guardados anteriores sin estadísticas de entrenamiento siguen siendo válidos');
      const passOnlySave = await page.evaluate(() => {
        const partida = crearEstadoInicial();
        partida.entrenamiento = { intentos: 1, puntos: 76, mejorPuntuacion: 76 };
        return estadoPartidaValido(partida);
      });
      assert.equal(passOnlySave, true, 'los guardados de la primera versión del laboratorio siguen siendo válidos');
      const inconsistentTraining = await page.evaluate(() => {
        const partida = crearEstadoInicial();
        partida.entrenamiento.porTipo.pase.intentos = 1;
        return estadoPartidaValido(partida);
      });
      assert.equal(inconsistentTraining, false, 'se rechazan contadores de entrenamiento incoherentes');
      await page.reload();
      assert.equal(await page.evaluate(() => estadoJuego.entrenamiento.intentos), 1,
        'el progreso del ejercicio se conserva al recargar');
      await page.locator('#pestana-clasificacion').click();
      await page.locator('#tab-clasificacion details').last().evaluate(el => { el.open = true; });
      await page.locator('#tipo-ejercicio').selectOption('presion');
      assert.match(await page.locator('#titulo-laboratorio').innerText(), /Presión coordinada/);
      const pressBoardState = await page.locator('#svg-presion').evaluate(el => ({
        active: el.classList.contains('active'),
        ariaHidden: el.getAttribute('aria-hidden'),
        display: getComputedStyle(el).display,
        visibility: getComputedStyle(el).visibility,
        width: el.getBoundingClientRect().width,
        height: el.getBoundingClientRect().height,
        tabActive: Boolean(document.querySelector('#tab-clasificacion details[open] #pase-opciones'))
      }));
      assert.ok(pressBoardState.active && pressBoardState.ariaHidden === 'false' &&
        pressBoardState.display !== 'none' && pressBoardState.visibility !== 'hidden' &&
        pressBoardState.width > 0 && pressBoardState.height > 0 && pressBoardState.tabActive,
        'la pizarra de presión se muestra al cambiar de ejercicio: ' + JSON.stringify(pressBoardState));
      const pressingChoice = await page.evaluate(() => retoPaseActual.opcionRecomendada);
      await page.locator(`#pase-opciones button[data-opcion-index="${pressingChoice}"]`).click();
      const pressingProgress = await page.evaluate(() => ({
        total: estadoJuego.entrenamiento.intentos,
        pass: estadoJuego.entrenamiento.porTipo.pase.intentos,
        pressure: estadoJuego.entrenamiento.porTipo.presion.intentos,
        pressureBest: estadoJuego.entrenamiento.porTipo.presion.mejorPuntuacion
      }));
      assert.deepEqual(pressingProgress, { total: 2, pass: 1, pressure: 1, pressureBest: 100 },
        'el ejercicio de presión guarda progreso separado y suma al total');
      await page.reload();
      assert.equal(await page.evaluate(() => estadoJuego.entrenamiento.porTipo.presion.intentos), 1,
        'el progreso de presión también se conserva al recargar');
      const olderPressureSave = await page.evaluate(() => {
        const partida = crearEstadoInicial();
        delete partida.entrenamiento.porTipo.espacio;
        delete partida.entrenamiento.porTipo.finalizacion;
        return estadoPartidaValido(partida);
      });
      assert.equal(olderPressureSave, true, 'los guardados de dos ejercicios siguen siendo válidos');
      await page.locator('#pestana-clasificacion').click();
      await page.locator('#tab-clasificacion details').last().evaluate(el => { el.open = true; });
      await page.locator('#tipo-ejercicio').selectOption('espacio');
      assert.match(await page.locator('#titulo-laboratorio').innerText(), /Lectura del espacio/);
      const spaceBoard = await page.locator('#svg-espacio').evaluate(el => ({
        active: el.classList.contains('active'),
        ariaHidden: el.getAttribute('aria-hidden'),
        display: getComputedStyle(el).display,
        width: el.getBoundingClientRect().width,
        height: el.getBoundingClientRect().height
      }));
      assert.ok(spaceBoard.active && spaceBoard.ariaHidden === 'false' && spaceBoard.display !== 'none' &&
        spaceBoard.width > 0 && spaceBoard.height > 0,
        'la pizarra de lectura del espacio debe renderizarse: ' + JSON.stringify(spaceBoard));
      const spaceChoice = await page.evaluate(() => retoPaseActual.opcionRecomendada);
      await page.locator(`#pase-opciones button[data-opcion-index="${spaceChoice}"]`).click();
      const spaceProgress = await page.evaluate(() => ({
        total: estadoJuego.entrenamiento.intentos,
        passes: estadoJuego.entrenamiento.porTipo.pase.intentos,
        pressure: estadoJuego.entrenamiento.porTipo.presion.intentos,
        space: estadoJuego.entrenamiento.porTipo.espacio.intentos,
        spaceBest: estadoJuego.entrenamiento.porTipo.espacio.mejorPuntuacion
      }));
      assert.deepEqual(spaceProgress, { total: 3, passes: 1, pressure: 1, space: 1, spaceBest: 100 },
        'lectura del espacio conserva progreso separado y suma al total');
      await page.reload();
      assert.equal(await page.evaluate(() => estadoJuego.entrenamiento.porTipo.espacio.intentos), 1,
        'el progreso de lectura del espacio se conserva al recargar');
      await page.locator('#pestana-clasificacion').click();
      await page.locator('#tab-clasificacion details').last().evaluate(el => { el.open = true; });
      await page.locator('#tipo-ejercicio').selectOption('finalizacion');
      assert.match(await page.locator('#titulo-laboratorio').innerText(), /Finalización/);
      const finishBoard = await page.locator('#svg-finalizacion').evaluate(el => ({
        active: el.classList.contains('active'),
        ariaHidden: el.getAttribute('aria-hidden'),
        display: getComputedStyle(el).display,
        width: el.getBoundingClientRect().width,
        height: el.getBoundingClientRect().height,
        visibleBoards: document.querySelectorAll('.pass-pitch.active').length
      }));
      assert.ok(finishBoard.active && finishBoard.ariaHidden === 'false' && finishBoard.display !== 'none' &&
        finishBoard.width > 0 && finishBoard.height > 0 && finishBoard.visibleBoards === 1,
        'la pizarra de finalización aparece sola y renderizada: ' + JSON.stringify(finishBoard));
      const finishChoice = await page.evaluate(() => retoPaseActual.opcionRecomendada);
      await page.locator(`#pase-opciones button[data-opcion-index="${finishChoice}"]`).click();
      const finishProgress = await page.evaluate(() => ({
        total: estadoJuego.entrenamiento.intentos,
        attempts: estadoJuego.entrenamiento.porTipo.finalizacion.intentos,
        best: estadoJuego.entrenamiento.porTipo.finalizacion.mejorPuntuacion,
        playerDataUnchanged: obtenerMiEquipo().plantilla.every(j => j.goles === 0 && j.xg === 0)
      }));
      assert.deepEqual(finishProgress, { total: 4, attempts: 1, best: 100, playerDataUnchanged: true },
        'finalización registra progreso sin alterar estadísticas reales del simulador');
      await page.reload();
      assert.equal(await page.evaluate(() => estadoJuego.entrenamiento.porTipo.finalizacion.intentos), 1,
        'el progreso de finalización se conserva al recargar');
      // Compruebo que lesiones y fatiga influyen en el once y que descanso solo se aplica una vez.
      await page.locator('button.tab-btn').filter({ hasText: 'Táctica' }).click();
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
      const restRecovery = await page.evaluate(() => {
        const player = obtenerMiEquipo().plantilla[0];
        const original = { lesionado: player.lesionado, cansancio: player.cansancio };
        const used = estadoJuego.preparacionUsada;
        estadoJuego.preparacionUsada = false;
        player.lesionado = 2;
        player.cansancio = 50;
        accionDescansar();
        const result = { lesionado: player.lesionado, cansancio: player.cansancio };
        Object.assign(player, original);
        estadoJuego.preparacionUsada = used;
        return result;
      });
      assert.deepEqual(restRecovery, { lesionado: 1, cansancio: 20 },
        'el descanso debe reducir la lesión y la fatiga');
      const repeatRest = await page.evaluate(() => {
        const player = obtenerMiEquipo().plantilla[0];
        const original = { lesionado: player.lesionado, cansancio: player.cansancio };
        const used = estadoJuego.preparacionUsada;
        estadoJuego.preparacionUsada = true;
        player.lesionado = 2;
        player.cansancio = 50;
        accionDescansar();
        const result = { lesionado: player.lesionado, cansancio: player.cansancio };
        Object.assign(player, original);
        estadoJuego.preparacionUsada = used;
        return result;
      });
      assert.deepEqual(repeatRest, { lesionado: 2, cansancio: 50 },
        'no se puede descansar dos veces en la misma jornada');
      const injuredRecovery = await page.evaluate(() => {
        const [home, away] = estadoJuego.equipos;
        const player = home.plantilla[0];
        const old = { lesionado: player.lesionado, cansancio: player.cansancio, titular: player.titular };
        player.lesionado = 2;
        player.cansancio = 31;
        player.titular = true;
        const canvas = document.getElementById('canvas-shotmap');
        simularPartidoIndividual(home, away, false, document.getElementById('match-log'),
          canvas.getContext('2d'), canvas.width, canvas.height);
        const result = { lesionado: player.lesionado, cansancio: player.cansancio };
        Object.assign(player, old);
        convocarOnceAutomatico(home);
        return result;
      });
      assert.deepEqual(injuredRecovery, { lesionado: 1, cansancio: 31 },
        'el lesionado se recupera sin acumular fatiga');
      // Una jornada mal formada, incluso en el futuro, no debe alterar el estado de liga.
      const invalidFixture = await page.evaluate(() => {
        const original = estadoJuego.calendario[estadoJuego.jornadaActual];
        const before = estadoJuego.jornadaActual;
        estadoJuego.calendario[before] = [[estadoJuego.equipos[0].nombre, estadoJuego.equipos[0].nombre]];
        try {
          simularJornada();
          return { before, after: estadoJuego.jornadaActual };
        } finally {
          estadoJuego.calendario[before] = original;
        }
      });
      assert.equal(invalidFixture.after, invalidFixture.before,
        'una jornada corrupta no debe simularse');
      const futureFixture = await page.evaluate(() => {
        const future = (estadoJuego.jornadaActual + 1) % estadoJuego.calendario.length;
        const original = estadoJuego.calendario[future];
        const before = estadoJuego.jornadaActual;
        const points = estadoJuego.equipos.map(e => e.puntos);
        estadoJuego.calendario[future] = [[estadoJuego.equipos[0].nombre, estadoJuego.equipos[0].nombre]];
        try {
          simularJornada();
          return { before, after: estadoJuego.jornadaActual,
            pointsUnchanged: estadoJuego.equipos.every((e, i) => e.puntos === points[i]) };
        } finally {
          estadoJuego.calendario[future] = original;
        }
      });
      assert.equal(futureFixture.after, futureFixture.before,
        'una jornada futura corrupta también debe impedir simular');
      assert.equal(futureFixture.pointsUnchanged, true,
        'no deben cambiar los puntos cuando el calendario es inválido');
      // El juego debe seguir arrancando si el navegador bloquea localStorage y señalar los fallos de guardado.
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
      assert.equal(await page.locator('#estado-guardado').textContent(), '⚠️ No guardado',
        'el fallo de autoguardado debe quedar visible');
      await page.evaluate(() => guardarPartidaLocal(false));
      assert.equal(await page.locator('#estado-guardado').textContent(), '✓ Guardado',
        'el indicador debe recuperarse tras guardar correctamente');
      await page.reload();
      assert.equal(await page.locator('#estado-guardado').textContent(), '✓ Partida recuperada',
        'al reabrir una partida guardada debe indicarse que se recuperó');
      // Exportar e importar debe conservar una partida válida y rechazar una copia corrupta sin sustituirla.
      const exportEvent = page.waitForEvent('download');
      await page.locator('header button').filter({ hasText: 'Exportar' }).click();
      const exportFile = await exportEvent;
      assert.match(exportFile.suggestedFilename(), /^linea-de-pase-temporada-1\.json$/,
        'la copia de seguridad se descarga con nombre de temporada');
      const exported = JSON.parse(await fs.readFile(await exportFile.path(), 'utf8'));
      assert.equal(exported.formato, 'linea-de-pase-partida');
      assert.equal(exported.version, 1);
      assert.equal(exported.partida.equipos.length, 4);
      const importCandidate = structuredClone(exported.partida);
      importCandidate.equipos.find(e => e.nombre === 'Real Magras de Madrid').presupuesto = -250000;
      await page.locator('#archivo-partida').setInputFiles({
        name: 'copia-linea-de-pase.json', mimeType: 'application/json',
        buffer: Buffer.from(JSON.stringify({ ...exported, partida: importCandidate }))
      });
      await page.waitForFunction(() => document.getElementById('estado-guardado').textContent === '✓ Copia importada');
      assert.equal(await page.evaluate(() => obtenerMiEquipo().presupuesto), -250000,
        'la importación conserva los presupuestos negativos válidos');
      const beforeInvalidImport = await page.evaluate(() => obtenerMiEquipo().presupuesto);
      const invalidImportDialog = page.waitForEvent('dialog');
      await page.locator('#archivo-partida').setInputFiles({
        name: 'copia-danada.json', mimeType: 'application/json',
        buffer: Buffer.from(JSON.stringify({ formato: 'linea-de-pase-partida', version: 99, partida: {} }))
      });
      await invalidImportDialog;
      assert.equal(await page.evaluate(() => obtenerMiEquipo().presupuesto), beforeInvalidImport,
        'una importación no válida no modifica la partida activa');
      const importSafety = await page.evaluate(() => {
        const partida = structuredClone(crearEstadoInicial());
        const nombreHostil = '<img src=x onerror="window.__xssHit=true">';
        partida.equipos[0].plantilla[0].nombre = nombreHostil;
        partida.equipos[0].plantilla[0].goles = 1;
        partida.equipos[0].plantilla[0].xg = 0.8;
        partida.mercado[0].nombre = nombreHostil;
        window.__xssHit = false;
        return {
          partida,
          nombreHostil,
          valid: estadoPartidaValido(partida),
          longNameRejected: (() => {
            const copia = structuredClone(partida);
            copia.equipos[0].plantilla[0].nombre = 'x'.repeat(81);
            return !estadoPartidaValido(copia);
          })()
        };
      });
      assert.equal(importSafety.valid, true,
        'los nombres importados se aceptan como texto ordinario, aunque contengan signos HTML');
      assert.equal(importSafety.longNameRejected, true,
        'se rechazan nombres excesivamente largos para proteger el renderizado');
      const safeImportStatus = page.waitForFunction(() =>
        document.getElementById('estado-guardado').textContent === '✓ Copia importada');
      await page.locator('#archivo-partida').setInputFiles({
        name: 'copia-nombres-especiales.json', mimeType: 'application/json',
        buffer: Buffer.from(JSON.stringify({ formato: 'linea-de-pase-partida', version: 1,
          partida: importSafety.partida }))
      });
      await safeImportStatus;
      await page.waitForTimeout(50);
      const safeRender = await page.evaluate(nombreHostil => ({
        plantelAsText: [...document.querySelectorAll('#tbody-plantilla strong')]
          .some(el => el.textContent === nombreHostil),
        marketAsText: [...document.querySelectorAll('#tbody-mercado strong')]
          .some(el => el.textContent === nombreHostil),
        scorerAsText: [...document.querySelectorAll('#tbody-goleadores strong')]
          .some(el => el.textContent === nombreHostil),
        injectedImages: document.querySelectorAll('tbody img').length,
        executed: window.__xssHit
      }), importSafety.nombreHostil);
      assert.equal(safeRender.plantelAsText, true, 'un nombre importado se muestra como texto en plantilla');
      assert.equal(safeRender.marketAsText, true, 'un nombre importado se muestra como texto en mercado');
      assert.equal(safeRender.scorerAsText, true, 'un nombre importado se muestra como texto en goleadores');
      assert.equal(safeRender.injectedImages, 0, 'un guardado no puede inyectar etiquetas en las tablas');
      assert.equal(safeRender.executed, false, 'un guardado no puede ejecutar atributos HTML');
      const resetIndicator = await page.evaluate(() => {
        const originalConfirm = window.confirm;
        window.confirm = () => true;
        try {
          reiniciarPartidaLocal();
          return document.getElementById('estado-guardado').textContent;
        } finally {
          window.confirm = originalConfirm;
        }
      });
      assert.equal(resetIndicator, 'Nueva partida sin guardar',
        'el reinicio debe indicar que la partida nueva no está guardada');
      // Verifico los límites deportivos y económicos que protegen los estados extremos.
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
        const before = [home, away].map(eq => ({ xgf: eq.xgf, remates: eq.remates }));
        const log = document.getElementById('match-log');
        const canvas = document.getElementById('canvas-shotmap');
        simularPartidoIndividual(home, away, false, log, canvas.getContext('2d'), canvas.width, canvas.height);
        const after = [home, away].map(eq => ({ xgf: eq.xgf, remates: eq.remates }));
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
      // Las compras/ventas válidas actualizan plantilla y presupuesto; las inválidas no hacen nada.
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
      const marketAffordance = await page.evaluate(() => {
        const club = obtenerMiEquipo();
        const presupuestoOriginal = club.presupuesto;
        const precio = estadoJuego.mercado[0].precio;
        club.presupuesto = precio - 1;
        actualizarUI();
        const sinFondos = document.querySelector('#tbody-mercado button');
        const resultadoSinFondos = {
          disabled: sinFondos.disabled,
          title: sinFondos.title,
          texto: sinFondos.innerText
        };
        club.presupuesto = presupuestoOriginal;
        actualizarUI();
        return resultadoSinFondos;
      });
      assert.deepEqual(marketAffordance, {
        disabled: true,
        title: 'Presupuesto insuficiente para este fichaje',
        texto: 'Sin presupuesto'
      }, 'el mercado explica y bloquea visualmente un fichaje fuera del presupuesto');
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
      const squadLimit = await page.evaluate(() => {
        const club = obtenerMiEquipo();
        const plantillaOriginal = club.plantilla;
        const antes = { presupuesto: club.presupuesto, mercado: estadoJuego.mercado.length };
        club.plantilla = Array.from({ length: MAX_PLANTILLA }, (_, i) => ({
          ...plantillaOriginal[i % plantillaOriginal.length], nombre: `Suplente de prueba ${i + 1}`, titular: false
        }));
        actualizarUI();
        const botonesBloqueados = [...document.querySelectorAll('#tbody-mercado button')].every(boton => boton.disabled);
        ficharJugador(0);
        const noHuboCompra = club.plantilla.length === MAX_PLANTILLA && club.presupuesto === antes.presupuesto &&
          estadoJuego.mercado.length === antes.mercado;
        club.plantilla = plantillaOriginal;
        actualizarUI();
        return { botonesBloqueados, noHuboCompra };
      });
      assert.deepEqual(squadLimit, { botonesBloqueados: true, noHuboCompra: true },
        'la plantilla de 25 jugadores bloquea visualmente y también impide fichajes');
      // Un partido determinista permite comparar el número de remates con mapa, crónica y repeticiones.
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
      await page.locator('button').filter({ hasText: 'Partido' }).click();
      const replayCheck = await page.evaluate(() => {
        const random = Math.random;
        const originalStats = obtenerMiEquipo().plantilla.map(j => [j.goles, j.xg]);
        try {
          Math.random = () => 0.1;
          limpiarRepeticionesPartido();
          const [home, away] = crearEstadoInicial().equipos;
          const canvas = document.getElementById('canvas-shotmap');
          dibujarCampoBase(canvas.getContext('2d'), canvas.width, canvas.height);
          simularPartidoIndividual(home, away, true, document.getElementById('match-log'),
            canvas.getContext('2d'), canvas.width, canvas.height);
          const selected = mostrarRepeticion(0);
          return {
            events: eventosPartidoActual.length,
            shots: [home.remates, away.remates],
            clearChances: [home, away].map(eq => eventosPartidoActual.filter(e => e.equipo === eq.nombre && e.esClara).length),
            breakdownRows: [...document.querySelectorAll('#tbody-match-breakdown tr')]
              .map(row => [...row.cells].map(cell => cell.textContent)),
            expectedBreakdownRows: [home, away].map(eq => {
              const diferencia = eq.gf - eq.xgf;
              return [eq.nombre, String(eq.gf), String(eq.remates), eq.xgf.toFixed(2),
                `${diferencia > 0 ? '+' : ''}${diferencia.toFixed(2)}`,
                String(eventosPartidoActual.filter(e => e.equipo === eq.nombre && e.esClara).length)];
            }),
            summary: document.getElementById('match-summary').textContent,
            summaryIsLive: document.getElementById('match-summary').getAttribute('aria-live'),
            controls: document.querySelectorAll('#replay-controls [data-replay-index]').length,
            logButtons: document.querySelectorAll('#match-log .replay-trigger').length,
            selected,
            finalSummary: [...document.querySelectorAll('#match-log p')]
              .find(line => line.textContent.includes('FINAL:'))?.textContent || '',
            pressed: document.querySelector('#replay-controls [data-replay-index="0"]')?.getAttribute('aria-pressed'),
            xg: document.getElementById('replay-xg').textContent,
            replayType: document.getElementById('replay-type').textContent,
            player: document.getElementById('replay-player').textContent,
            replayTypeMatchesEvent: document.getElementById('replay-type').textContent ===
              (eventosPartidoActual[0]?.esClara ? 'Ocasión clara' : 'Ocasión de menor peligro'),
            categorizedEvents: [...document.querySelectorAll('#match-log .log-goal, #match-log .log-chance')]
              .every(line => /Ocasión clara|Ocasión de menor peligro/.test(line.textContent)),
            simulatedLabel: document.getElementById('replay-status').textContent.includes('no vídeo real'),
            originalStatsUnchanged: obtenerMiEquipo().plantilla.every((j, i) =>
              j.goles === originalStats[i][0] && j.xg === originalStats[i][1])
          };
        } finally {
          Math.random = random;
        }
      });
      assert.equal(await page.locator('#microclip-backdrop').getAttribute('aria-hidden'), 'false', 'la repetición abre el microclip animado');
      await page.locator('#microclip-close').click();
      assert.equal(replayCheck.events, 18, 'el partido genera ocasiones en sus 18 ventanas de juego');
      assert.equal(replayCheck.shots.reduce((total, remates) => total + remates, 0), 18,
        'el contador de remates coincide con las ocasiones generadas');
      assert.deepEqual(replayCheck.breakdownRows, replayCheck.expectedBreakdownRows,
        'la tabla de partido compara los dos equipos con goles, remates, xG y ocasiones claras');
      assert.equal(await page.locator('#btn-exportar-balance').isDisabled(), false,
        'el informe CSV se activa al terminar el partido');
      const reportDownloadEvent = page.waitForEvent('download');
      await page.locator('#btn-exportar-balance').click();
      const reportDownload = await reportDownloadEvent;
      assert.match(reportDownload.suggestedFilename(), /^linea-de-pase-partido-temporada-1-jornada-1\.csv$/,
        'el informe usa un nombre de archivo en castellano con temporada y jornada');
      const csvReport = await fs.readFile(await reportDownload.path(), 'utf8');
      assert.equal(csvReport.charCodeAt(0), 0xFEFF, 'el CSV empieza con BOM para conservar tildes en hojas de cálculo');
      const csvRows = csvReport.slice(1).trimEnd().split(/\r?\n/);
      assert.deepEqual(csvRows.slice(1), replayCheck.expectedBreakdownRows.map(row =>
        row.map(value => `"${value.replace(/"/g, '""')}"`).join(';')),
      'el CSV contiene las mismas estadísticas que el balance visible');
      assert.equal(csvRows.length, 3, 'el archivo incluye cabecera y los dos equipos');
      if (mode === 'mobile') {
        const informeMovil = await page.evaluate(() => {
          const tabla = document.getElementById('match-breakdown');
          const campos = [...tabla.tBodies[0].rows].flatMap(fila => [...fila.cells])
            .filter(celda => celda.dataset.label)
            .map(celda => ({ etiqueta: celda.dataset.label, visible: getComputedStyle(celda).display !== 'none',
              ancho: celda.getBoundingClientRect().width }));
          return { sinDesbordamiento: tabla.scrollWidth <= tabla.clientWidth + 1,
            filasComoFicha: getComputedStyle(tabla.tBodies[0].rows[0]).display === 'grid', campos };
        });
        assert.equal(informeMovil.sinDesbordamiento, true,
          'el balance usa el ancho de móvil sin exigir desplazamiento lateral');
        assert.equal(informeMovil.filasComoFicha, true, 'cada equipo del balance se presenta como ficha móvil');
        assert.ok(informeMovil.campos.every(campo => campo.visible && campo.ancho > 0),
          'todos los datos del informe siguen visibles en móvil');
      }
      await page.screenshot({ path: require('node:path').join(artifactDir, `partido-${mode}.png`), fullPage: true });
      assert.ok(replayCheck.finalSummary.includes(`Remates: ${replayCheck.shots[0]} vs ${replayCheck.shots[1]}`) &&
        replayCheck.finalSummary.includes('xG:') &&
        replayCheck.finalSummary.includes(`ocasiones claras: ${replayCheck.clearChances[0]} vs ${replayCheck.clearChances[1]}`),
        'la crónica final compara remates, ocasiones claras y xG con los contadores del motor');
      assert.ok(replayCheck.summary.includes(`Remates: ${replayCheck.shots[0]} vs ${replayCheck.shots[1]}`) &&
        replayCheck.summary.includes('xG:') && replayCheck.summaryIsLive === 'polite' &&
        replayCheck.summary.includes(`ocasiones claras: ${replayCheck.clearChances[0]} vs ${replayCheck.clearChances[1]}`),
        'el resumen visual y accesible comunica el resultado, remates, ocasiones claras y xG');
      assert.equal(replayCheck.controls, replayCheck.events, 'cada ocasión tiene control para repetirla');
      assert.equal(replayCheck.logButtons, replayCheck.events, 'la crónica enlaza cada remate a su repetición');
      assert.equal(replayCheck.selected, true);
      assert.equal(replayCheck.pressed, 'true', 'la repetición seleccionada se anuncia a lectores de pantalla');
      assert.ok(Number.isFinite(Number(replayCheck.xg)) && replayCheck.player &&
        ['Ocasión clara', 'Ocasión de menor peligro'].includes(replayCheck.replayType),
        'la repetición indica la categoría interna de la ocasión seleccionada');
      assert.equal(replayCheck.replayTypeMatchesEvent, true,
        'la ficha de repetición muestra la categoría del evento seleccionado');
      assert.equal(replayCheck.categorizedEvents, true, 'la crónica clasifica cada ocasión de forma legible');
      assert.equal(replayCheck.simulatedLabel, true, 'la repetición se identifica como reconstrucción, no vídeo real');
      assert.equal(replayCheck.originalStatsUnchanged, true,
        'la prueba de repetición usa datos aislados y no altera la partida activa');
      await page.locator('button').filter({ hasText: 'SIMULAR JORNADA' }).click();
      await page.locator('[data-power="cierzo"]').click();
      assert.equal(await page.locator('[data-power="cierzo"]').getAttribute('class').then(c=>c.includes('used')), true,
        'el poder táctico se consume al lanzarlo durante el reloj');
      await page.waitForFunction(() => estadoJuego.jornadaActual === 1 &&
        document.getElementById('event-backdrop').classList.contains('open'), null, { timeout: 15000 });
      const eventoAntes = await page.evaluate(() => ({
        presupuesto: obtenerMiEquipo().presupuesto,
        moral: obtenerMiEquipo().plantilla[0].moral,
        opcion: eventoVestuarioActual.opciones[0],
        contrato: estadoJuego.patrocinadorActivo
      }));
      await page.locator('[data-event-choice="0"]').click();
      const eventoDespues = await page.evaluate(() => ({
        presupuesto: obtenerMiEquipo().presupuesto,
        moral: obtenerMiEquipo().plantilla[0].moral,
        pendiente: eventoVestuarioActual
      }));
      assert.equal(eventoAntes.contrato, null, 'el contrato se liquida tras la jornada');
      assert.equal(eventoDespues.presupuesto, Math.max(0, eventoAntes.presupuesto + eventoAntes.opcion.dinero),
        'el mini-evento altera y guarda las finanzas');
      assert.equal(eventoDespues.moral, Math.max(0, Math.min(100, eventoAntes.moral + eventoAntes.opcion.moral)),
        'el mini-evento modifica la moral del vestuario');
      assert.equal(eventoDespues.pendiente, null, 'la decisión cierra el popup');
      assert.equal(await page.evaluate(() => estadoJuego.jornadaActual), 1);
      await page.reload();
      assert.equal(await page.evaluate(() => estadoJuego.jornadaActual), 1, 'partida persistente');
      await page.evaluate(() => { for (let i = 1; i < 6; i++) simularJornada(); });
      assert.equal(await page.evaluate(() => estadoJuego.jornadaActual), 6);
      assert.equal(await page.locator('#match-preview').innerText(),
        'No hay rival pendiente: la temporada está cerrada.');
      assert.match(await page.locator('#btn-simular-jornada').innerText(), /CERRAR TEMPORADA Y CONTINUAR/,
        'el botón explica que empieza la gestión de la siguiente campaña');
      // Cierro una temporada para probar desempates, premios, reinicio estadístico y renovación del mercado.
      const empate = await page.evaluate(() => {
        const clubes = crearEstadoInicial().equipos;
        clubes.forEach(e => { e.puntos = 10; e.gf = 8; e.gc = 5; });
        clubes[0].gf = 9;
        clubes[1].gc = 4;
        return calcularPremiosClasificacion(clubes).map(e => e.nombre);
      });
      assert.equal(empate[0], 'Real Magras de Madrid',
        'a igualdad de puntos y diferencia de goles, mandan los goles a favor');
      const empateTotal = await page.evaluate(() => {
        const clubes = crearEstadoInicial().equipos;
        clubes.forEach(e => { e.puntos = 10; e.gf = 8; e.gc = 5; });
        return calcularPremiosClasificacion(clubes).map(e => e.nombre);
      });
      assert.deepEqual(empateTotal, [
        'Athletic de la Tronca', 'Atlético Colchonico de la Ribera',
        'Balompié del Somontano', 'Real Magras de Madrid'
      ], 'si puntos, diferencia y goles a favor empatan, el nombre ordena de forma estable');
      const temporadaIncompleta = await page.evaluate(() => {
        const actual = estadoJuego.jornadaActual;
        const temporada = estadoJuego.temporada;
        estadoJuego.jornadaActual = 5;
        try {
          iniciarNuevaTemporada();
          return estadoJuego.temporada === temporada && estadoJuego.jornadaActual === 5;
        } finally {
          estadoJuego.jornadaActual = actual;
        }
      });
      assert.equal(temporadaIncompleta, true,
        'no se debe cobrar premios ni iniciar temporada antes de la última jornada');
      const premios = await page.evaluate(() => {
        const ordenados = calcularPremiosClasificacion(estadoJuego.equipos);
        return ordenados.map(p => p.premio);
      });
      assert.deepEqual(premios, [5000000, 3500000, 2500000, 1500000],
        'los premios deben descender según la clasificación');
      const presupuestosAntes = await page.evaluate(() =>
        Object.fromEntries(estadoJuego.equipos.map(e => [e.nombre, e.presupuesto])));
      const premiosPorEquipo = await page.evaluate(() =>
        Object.fromEntries(calcularPremiosClasificacion(estadoJuego.equipos).map(p => [p.nombre, p.premio])));
      const mercadoAntesDeTemporada = await page.evaluate(() => ({
        cantidad: estadoJuego.mercado.length,
        nombres: estadoJuego.mercado.map(j => j.nombre)
      }));
      await page.evaluate(() => {
        estadoJuego.equipos.forEach(eq => eq.plantilla.forEach(j => { j.goles = 0; j.xg = 0; }));
        const goleadorLocal = obtenerMiEquipo().plantilla.find(j => j.nombre === 'Kylian Embozado');
        const goleadorVisitante = estadoJuego.equipos[1].plantilla.find(j => j.posicion === 'DEL');
        goleadorLocal.goles = 7;
        goleadorLocal.xg = 4.25;
        goleadorVisitante.goles = 7;
        goleadorVisitante.xg = 5.1;
      });
      await page.evaluate(() => iniciarNuevaTemporada());
      assert.equal(await page.evaluate(() => estadoJuego.temporada), 2);
      assert.match(await page.locator('#btn-simular-jornada').innerText(), /SIMULAR JORNADA EN VIVO/,
        'el botón vuelve a indicar que toca jugar una jornada');
      const archivoPrimeraTemporada = await page.evaluate(() => estadoJuego.historialTemporadas[0]);
      assert.equal(archivoPrimeraTemporada.temporada, 1, 'el cambio de temporada archiva la campaña que termina');
      assert.equal(archivoPrimeraTemporada.goleadores.length, 2,
        'el resumen conserva a todos los máximos goleadores empatados');
      assert.ok(archivoPrimeraTemporada.goleadores.some(j => j.nombre === 'Kylian Embozado'));
      assert.ok(archivoPrimeraTemporada.goleadores.some(j => j.equipo !== 'Real Magras de Madrid'));
      assert.ok(archivoPrimeraTemporada.goleadores.every(j => j.goles === 7),
        'el empate se resuelve por goles y no por xG');
      assert.ok(archivoPrimeraTemporada.clasificacion.every(eq => Number.isInteger(eq.pj) &&
        Number.isInteger(eq.remates) && Number.isFinite(eq.xgf) && Number.isFinite(eq.xgc)),
        'el archivo conserva partidos, remates y xG de los cuatro equipos');
      assert.match(await page.locator('#tbody-historial-temporadas tr').first().innerText(), /Empate:.*Kylian Embozado/,
        'el archivo anuncia el empate entre goleadores');
      const celdasArchivo = await page.locator('#tbody-historial-temporadas tr').first().locator('td').allInnerTexts();
      assert.equal(celdasArchivo[3].trim(), String(archivoPrimeraTemporada.clasificacion[0].pj),
        'la tabla histórica muestra los partidos jugados de la fila');
      assert.match(celdasArchivo[5], /^\d+-\d+$/);
      assert.match(celdasArchivo[6], /^\d+$/);
      assert.match(celdasArchivo[7], /^\d+\.\d{2}$/);
      const equipoArchivado = archivoPrimeraTemporada.clasificacion[0];
      const diferenciaEsperada = equipoArchivado.gf - equipoArchivado.xgf;
      assert.equal(celdasArchivo[8].trim(), `${diferenciaEsperada >= 0 ? '+' : ''}${diferenciaEsperada.toFixed(2)}`,
        'la diferencia entre goles y xG se calcula desde las métricas archivadas');
      assert.match(celdasArchivo[9], /^\d+\.\d{2}$/,
        'la tabla histórica muestra goles, remates y xG a favor, diferencia y en contra');
      assert.equal(await page.evaluate(() => estadoPartidaValido(estadoJuego)), true,
        'el nuevo historial cumple la validación de guardado');
      assert.equal(await page.locator('#tbody-historial-temporadas tr').count(), 4,
        'el archivo muestra la clasificación completa de la campaña');
      assert.deepEqual(await page.evaluate(() => estadoJuego.equipos.map(eq => eq.remates)), [0, 0, 0, 0],
        'los remates se reinician al comenzar la temporada');
      const presupuestosDespues = await page.evaluate(() =>
        Object.fromEntries(estadoJuego.equipos.map(e => [e.nombre, e.presupuesto])));
      for (const nombre of Object.keys(presupuestosAntes)) {
        assert.equal(presupuestosDespues[nombre] - presupuestosAntes[nombre], premiosPorEquipo[nombre],
          'cada club recibe exactamente su premio de clasificación');
      }

      assert.equal(await page.evaluate(() => estadoJuego.jornadaActual), 0);
      assert.equal(await page.evaluate(() => estadoJuego.calendario.length), 6);
      const mercadoRenovado = await page.evaluate(() => ({
        cantidad: estadoJuego.mercado.length,
        jugadores: estadoJuego.mercado.map(j => ({ nombre: j.nombre, posicion: j.posicion, goles: j.goles, xg: j.xg })),
        duplicados: new Set(estadoJuego.mercado.map(j => j.nombre.toLocaleLowerCase('es'))).size !== estadoJuego.mercado.length
      }));
      const incorporados = mercadoRenovado.jugadores.filter(j => !mercadoAntesDeTemporada.nombres.includes(j.nombre));
      assert.equal(mercadoRenovado.cantidad, Math.min(12, mercadoAntesDeTemporada.cantidad + 4),
        'la nueva temporada incorpora cuatro opciones de mercado hasta su límite');
      assert.equal(incorporados.length, 4,
        'los refuerzos generados son nuevos y ficticios');
      assert.deepEqual(incorporados.map(j => j.posicion).sort(), ['CEN', 'DEF', 'DEL', 'POR'],
        'la renovación anual cubre las cuatro posiciones');
      assert.equal(mercadoRenovado.duplicados, false, 'el mercado no duplica nombres');
      assert.ok(mercadoRenovado.jugadores.every(j => j.goles === 0 && j.xg === 0),
        'las estadísticas del mercado empiezan limpias cada temporada');
      await page.reload();
      assert.equal(await page.evaluate(() => estadoJuego.temporada), 2);
      assert.equal(await page.evaluate(() => estadoJuego.historialTemporadas[0].goleadores.length), 2,
        'el empate de goleadores se conserva al recargar la partida');
      const limiteMercado = await page.evaluate(() => {
        estadoJuego.jornadaActual = estadoJuego.calendario.length;
        iniciarNuevaTemporada();
        return { temporada: estadoJuego.temporada, cantidad: estadoJuego.mercado.length,
          distintos: new Set(estadoJuego.mercado.map(j => j.nombre.toLocaleLowerCase('es'))).size };
      });
      assert.deepEqual(limiteMercado, { temporada: 3, cantidad: 12, distintos: 12 },
        'el mercado renueva opciones sin crecer indefinidamente en temporadas largas');
      // El déficit es válido; además, este caso cubre la migración de guardados sin remates ni archivo histórico.
      await page.evaluate(() => {
        const partida = crearEstadoInicial();
        partida.equipos.find(e => e.nombre === 'Real Magras de Madrid').presupuesto = -250000;
        partida.equipos.forEach(e => { delete e.remates; });
        delete partida.historialTemporadas;
        localStorage.setItem('ldp_manager_save', JSON.stringify(partida));
      });
      await page.reload();
      assert.equal(await page.evaluate(() => obtenerMiEquipo().presupuesto), -250000,
        'una partida con déficit se recupera sin reiniciarse');
      assert.deepEqual(await page.evaluate(() => estadoJuego.equipos.map(eq => eq.remates)), [0, 0, 0, 0],
        'los guardados anteriores migran el contador de remates sin perder datos');
      assert.deepEqual(await page.evaluate(() => estadoJuego.historialTemporadas), [],
        'los guardados antiguos reciben un archivo vacío sin reiniciar la temporada');
      assert.match(await page.locator('#lbl-presupuesto').innerText(), /Déficit/,
        'el déficit se señala en la interfaz');
      const compraEnDeficit = await page.evaluate(() => {
        const club = obtenerMiEquipo();
        const antes = [club.presupuesto, club.plantilla.length, estadoJuego.mercado.length];
        const botonesBloqueados = [...document.querySelectorAll('#tbody-mercado button')].every(boton =>
          boton.disabled && boton.title === 'Presupuesto insuficiente para este fichaje');
        ficharJugador(0);
        return { antes, despues: [club.presupuesto, club.plantilla.length, estadoJuego.mercado.length], botonesBloqueados };
      });
      assert.deepEqual(compraEnDeficit.despues, compraEnDeficit.antes,
        'no se permite comprar jugadores con déficit');
      assert.equal(compraEnDeficit.botonesBloqueados, true,
        'el déficit desactiva las compras y explica el motivo');
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
      await page.evaluate(() => {
        const partida = crearEstadoInicial();
        partida.calendario[1] = partida.calendario[0];
        localStorage.setItem('ldp_manager_save', JSON.stringify(partida));
      });
      await page.reload();
      assert.equal(await page.evaluate(() => calendarioValido(estadoJuego.calendario, estadoJuego.equipos)), true,
        'calendario con enfrentamientos duplicados rechazado');
      await page.evaluate(() => {
        const partida = crearEstadoInicial();
        partida.equipos[0].plantilla[0].cansancio = 140;
        localStorage.setItem('ldp_manager_save', JSON.stringify(partida));
      });
      await page.reload();
      assert.equal(await page.evaluate(() => estadoJuego.equipos[0].plantilla[0].cansancio <= 100), true,
        'partida con fatiga fuera de rango rechazada');
      await page.evaluate(() => {
        const partida = crearEstadoInicial();
        partida.equipos[0].plantilla[0].salario = -500;
        localStorage.setItem('ldp_manager_save', JSON.stringify(partida));
      });
      await page.reload();
      assert.equal(await page.evaluate(() => estadoJuego.equipos[0].plantilla[0].salario >= 0), true,
        'partida con salario negativo rechazada');
      const safeMarkup = await page.evaluate(() =>
        escaparHTML('<img src=x onerror=alert(1)>') === '&lt;img src=x onerror=alert(1)&gt;');
      assert.equal(safeMarkup, true, 'los nombres mostrados en el registro deben escapar HTML');
      const malformedTeams = await page.evaluate(() =>
        calendarioValido(crearEstadoInicial().calendario, [null, {}, {}, {}]));
      assert.equal(malformedTeams, false, 'equipos malformados no deben provocar excepciones');
      const swappedCalendar = await page.evaluate(() => {
        const partida = crearEstadoInicial();
        // Intercambiar jornadas completas entre mitades conserva los doce
        // partidos, pero duplica parejas dentro de cada vuelta.
        const tmp = partida.calendario[0];
        partida.calendario[0] = partida.calendario[4];
        partida.calendario[4] = tmp;
        return calendarioValido(partida.calendario, partida.equipos);
      });
      assert.equal(swappedCalendar, false, 'la ida y vuelta no pueden mezclar enfrentamientos');
      await page.evaluate(() => {
        const partida = crearEstadoInicial();
        partida.equipos[0].nombre = 'Equipo inexistente';
        localStorage.setItem('ldp_manager_save', JSON.stringify(partida));
      });
      await page.reload();
      assert.equal(await page.evaluate(() => obtenerMiEquipo()?.nombre), 'Real Magras de Madrid',
        'una partida sin el equipo controlado se debe rechazar');
      await page.evaluate(() => localStorage.setItem('ldp_manager_save', '{bad json'));
      await page.reload();
      assert.equal(await page.evaluate(() => estadoJuego.temporada), 1);
      if (mode === 'mobile') {
        // Mido el documento completo después de todas las interacciones, no solo al cargar.
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
