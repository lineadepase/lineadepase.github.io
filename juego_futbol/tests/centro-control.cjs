const {chromium}=require('playwright'),assert=require('node:assert/strict');
const {installScreenNavigation}=require('./screen-navigation.cjs');
(async()=>{const browser=await chromium.launch({headless:true});try{
 for(const [width,height] of [[1366,900],[390,844]]){
  const p=await browser.newPage({viewport:{width,height}});installScreenNavigation(p);const errors=[];p.on('pageerror',e=>errors.push(e.message));
  await p.goto('http://127.0.0.1:8765/juego_futbol/');await p.waitForSelector('.screen-mode');
  assert.equal(await p.locator('#screen-view option:checked').textContent(),'Centro de control');
  await p.locator('[data-open="club-tickets"]').click();assert.equal(await p.locator('#screen-view option:checked').textContent(),'Entradas y abonos');
  await p.evaluate(()=>{const e=obtenerMiEquipo();e.plantilla.find(j=>j.titular).cansancio=90;e.presupuesto=-100;e.gestion.balances=Array.from({length:8},(_,i)=>({temporada:1,jornada:8-i,neto:(8-i)*100,asistentes:0,entradas:0,extras:0,publicidad:0,salarios:0,empleados:0,primas:0}));actualizarUI();abrirPantallaJuego('control-alerts');});
  assert.match(await p.locator('#control-alerts').textContent(),/descanso/);assert.match(await p.locator('#control-alerts').textContent(),/déficit/);
  assert.match(await p.locator('#control-finance').textContent(),/J8/);assert.doesNotMatch(await p.locator('#control-finance').textContent(),/J1/);
  await p.locator('[data-open="btn-rotar-fatigados"]').click();assert.match(await p.locator('#screen-view option:checked').textContent(),/^Alineación y jugadores/);
  await p.locator('#open-compare').click();await p.locator('#compare-first').selectOption({index:2});await p.locator('#compare-second').selectOption({index:3});
  const expected=await p.evaluate(()=>obtenerMiEquipo().plantilla[2].nombre);assert.match(await p.locator('#compare-summary').textContent(),new RegExp(expected));
  await p.locator('#compare-contract').click();assert.ok((await p.locator('#contract-player option:checked').textContent()).startsWith('Renovar · '+expected+' · '));assert.match(await p.locator('#player-dossier').textContent(),new RegExp(expected));
  const theme=await p.locator('#offer-wage').evaluate(n=>({bg:getComputedStyle(n).backgroundColor,fg:getComputedStyle(n).color}));assert.equal(theme.bg,'rgb(16, 23, 37)');assert.equal(theme.fg,'rgb(229, 234, 244)');
  assert.deepEqual(errors,[]);console.log(`${width}: resumen, alertas, accesos, comparación, contrato y tema nocturno correctos`);await p.close();
 }
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
