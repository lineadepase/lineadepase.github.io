const {chromium}=require('playwright'),assert=require('node:assert/strict');
const {installScreenNavigation}=require('./screen-navigation.cjs');
(async()=>{const b=await chromium.launch({headless:true});try{
 for(const [width,height] of [[1366,900],[390,844],[320,568],[844,390]]){
  const p=await b.newPage({viewport:{width,height}});installScreenNavigation(p);p.on('dialog',d=>d.accept());const errors=[];p.on('pageerror',e=>errors.push(e.message));
  await p.goto('http://127.0.0.1:8765/juego_futbol/');await p.waitForSelector('.screen-mode');
  await p.evaluate(()=>{const e=obtenerMiEquipo();while(e.plantilla.length<25)e.plantilla.push(ClubMotor.generar(estadoJuego,e,'DEF',20));actualizarUI();abrirPantallaJuego('alineacion-completa');});
  await p.waitForTimeout(100);assert.equal(await p.locator('.lineup-person:visible').count(),25);assert.equal(await p.locator('#screen-page').textContent(),'Página 1 de 1');
  const positions=await p.locator('.lineup-person:visible').evaluateAll(ns=>ns.map(n=>n.getBoundingClientRect().toJSON()));assert.ok(positions.every(r=>r.top>=0&&r.bottom<=height&&r.right<=width));
  const ids=await p.evaluate(()=>{const e=obtenerMiEquipo();return [e.plantilla.find(j=>j.titular).jugador_id,e.plantilla.find(j=>!j.titular&&!e.suplentesIds.includes(j.jugador_id)).jugador_id]});
  await p.locator(`[data-lineup-id="${ids[0]}"]`).click();await p.locator(`[data-lineup-id="${ids[1]}"]`).click();assert.equal(await p.evaluate(id=>obtenerMiEquipo().plantilla.find(j=>j.jugador_id===id).titular,ids[1]),true);
  // La creación del filial, el presupuesto y sus salarios se comprueban desde una carrera nueva.
  await p.evaluate(()=>{estadoJuego=crearEstadoInicial();actualizarUI();abrirPantallaJuego('club-filial');});
  const before=await p.evaluate(()=>obtenerMiEquipo().presupuesto);await p.locator('#create-bteam').click();assert.equal(await p.evaluate(()=>obtenerMiEquipo().gestion.cantera.filter(j=>j.equipoB).length),0);assert.equal(await p.evaluate(()=>obtenerMiEquipo().presupuesto),before-100000);
  // Plantilla de prueba para verificar amistosos y nóminas; las altas reales se cubren en scouting-datos.cjs.
  await p.evaluate(()=>{const e=obtenerMiEquipo();for(let i=0;i<11;i++){const j=ClubMotor.generar(estadoJuego,e,'CEN',18);j.equipoB=true;e.gestion.cantera.push(j);}actualizarUI();});
  await p.locator('#play-bteam').click();assert.equal(await p.evaluate(()=>obtenerMiEquipo().gestion.filial.jugados),1);assert.equal(await p.locator('#play-bteam').isDisabled(),true);
  await p.locator('#remodel-stadium').click();assert.equal(await p.evaluate(()=>obtenerMiEquipo().gestion.modernizacion),0);
  await p.evaluate(()=>{simularJornada();simularJornada();simularJornada();VideoActionTrigger.close();if(eventoVestuarioActual)resolverEventoVestuario(0);});
  assert.equal(await p.evaluate(()=>obtenerMiEquipo().gestion.modernizacion),1);
  assert.equal(await p.evaluate(()=>{const e=obtenerMiEquipo();return e.gestion.balances[0].salarios===masaSalarial(e)}),true);
  await p.evaluate(()=>abrirPantallaJuego('data-kpis'));assert.match(await p.locator('#data-sample').textContent(),/3 partidos/);assert.ok(await p.locator('#data-scatter circle').count()>0);
  await p.locator('#export-data').scrollIntoViewIfNeeded();const [download]=await Promise.all([p.waitForEvent('download'),p.click('#export-data')]);assert.match(download.suggestedFilename(),/^bigdata-liga/);
  await p.locator('#recruit-pos').selectOption('POR');assert.equal(await p.evaluate(()=>[...document.querySelectorAll('#recruit-results tbody tr')].every(tr=>tr.cells[1].textContent==='POR')),true);
  assert.equal(await p.evaluate(()=>estadoPartidaValido(estadoJuego)),true);await p.evaluate(()=>guardarPartidaLocal(false));await p.reload();await p.waitForSelector('.screen-mode');assert.equal(await p.evaluate(()=>obtenerMiEquipo().gestion.filial.activo),true);assert.equal(await p.evaluate(()=>estadoPartidaValido(estadoJuego)),true);
  assert.deepEqual(errors,[]);console.log(`${width}: 25 jugadores sin scroll, cambios, filial, nóminas, remodelación, Big Data, CSV y persistencia correctos`);await p.close();
 }
}finally{await b.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
