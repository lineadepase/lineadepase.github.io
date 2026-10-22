const { chromium, devices } = require('playwright');
const assert = require('node:assert/strict');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const errors = [];
  try {
    for (const mode of ['desktop', 'mobile']) {
      const context = await browser.newContext(mode === 'mobile'
        ? { ...devices['iPhone 13'], browserName: undefined }
        : { viewport: { width: 1366, height: 900 } });
      const page = await context.newPage();
      page.on('pageerror', err => errors.push(mode + ': ' + err.message));
      page.on('dialog', dialog => dialog.accept());
      await page.goto('http://127.0.0.1:8765/juego_futbol/', { waitUntil: 'load' });
      await page.waitForFunction(() => typeof estadoJuego !== 'undefined' && !!estadoJuego.equipos);
      assert.equal(await page.evaluate(() => estadoJuego.equipos.length), 4);
      assert.equal(await page.evaluate(() => estadoJuego.jornadaActual), 0);
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
