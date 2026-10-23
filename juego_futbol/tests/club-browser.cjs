const {chromium}=require('playwright'),assert=require('node:assert/strict');
const {installScreenNavigation}=require('./screen-navigation.cjs');
const fs=require('node:fs/promises'),path=require('node:path');
(async()=>{
 const browser=await chromium.launch({headless:true}),out=path.join(__dirname,'test-artifacts');await fs.mkdir(out,{recursive:true});
 try{for(const [mode,width,height] of [['desktop',1366,900],['mobile',390,844]]){
  const page=await browser.newPage({viewport:{width,height}}),errors=[];installScreenNavigation(page);
  page.on('pageerror',e=>errors.push(e.message));page.on('dialog',d=>d.accept());
  await page.goto('http://127.0.0.1:8765/juego_futbol/');await page.waitForSelector('.screen-mode');
  const migration=await page.evaluate(()=>{
   const s=JSON.parse(JSON.stringify(estadoJuego)),cash=s.equipos[0].presupuesto,ids=s.equipos[0].plantilla.map(j=>j.jugador_id);
   delete s.carrera;s.equipos.forEach(e=>{delete e.gestion;e.plantilla.forEach(j=>{delete j.contrato;delete j.desarrollo;});});s.mercado.forEach(j=>{delete j.contrato;delete j.desarrollo;});localStorage.setItem('ldp_manager_save',JSON.stringify(s));return {cash,ids};
  });
  await page.reload();await page.waitForSelector('.screen-mode');
  assert.equal(await page.evaluate(()=>estadoPartidaValido(estadoJuego)),true);
  assert.deepEqual(await page.evaluate(()=>({cash:obtenerMiEquipo().presupuesto,ids:obtenerMiEquipo().plantilla.map(j=>j.jugador_id)})),migration);
  await page.locator('#roster-detail-toggle').click();
  await page.locator('#tbody-plantilla [data-player-detail]').first().scrollIntoViewIfNeeded();
  assert.equal(await page.locator('#roster-detail-toggle').getAttribute('aria-pressed'),'true');
  await page.locator('#roster-detail-toggle').click();
  const aforo=await page.evaluate(()=>obtenerMiEquipo().aforo);
  await page.locator('#stand-sector').selectOption('norte');await page.locator('#stand-form button').click();
  assert.equal(await page.evaluate(()=>obtenerMiEquipo().aforo),aforo);
  assert.equal(await page.evaluate(()=>obtenerMiEquipo().gestion.obras[0].restante),4);
  await page.locator('#service-type').selectOption('comida');await page.locator('#service-form button').click();
  await page.locator('#staff-role').selectOption('medico');await page.locator('#staff-level').selectOption('2');await page.locator('#staff-form button').click();
  assert.equal(await page.evaluate(()=>ClubMotor.sueldoStaff(obtenerMiEquipo())),6000);
  await page.locator('#ticket-price').fill('35');await page.locator('#season-price').fill('100');await page.locator('#ticket-form button').click();
  assert.equal(await page.evaluate(()=>obtenerMiEquipo().gestion.entrada),35);
  await page.locator('#sell-season-tickets').click();assert.ok(await page.evaluate(()=>obtenerMiEquipo().gestion.abonados>0));
  await page.locator('#ads-space').selectOption('camiseta');await page.locator('#ads-type').selectOption('fijo');await page.locator('#ads-form button').click();
  await page.locator('#scout-youth').click();await page.locator('#scout-start').click();await page.evaluate(()=>{simularJornada();VideoActionTrigger.close();if(eventoVestuarioActual)resolverEventoVestuario(0);});await page.locator('[data-scout-sign]').first().click();const youth=await page.evaluate(()=>obtenerMiEquipo().gestion.cantera.at(-1).jugador_id);
  await page.locator(`[data-promote="${youth}"]`).click();assert.ok(await page.evaluate(id=>obtenerMiEquipo().plantilla.some(j=>j.jugador_id===id),youth));
  const player=await page.evaluate(()=>{const j=obtenerMiEquipo().plantilla[0];return {id:j.jugador_id,salario:j.salario,precio:j.precio};});
  await page.locator('#contract-player').selectOption('propio:'+player.id);
  await page.locator('#offer-wage').fill(String(Math.floor(player.salario*.9)));await page.locator('#contract-form button').click();
  assert.match(await page.locator('#offer-response').textContent(),/mejorar/);
  await page.locator('#load-counter').click();await page.locator('#contract-form button').click();await page.locator('#sign-contract').click();
  assert.equal(await page.evaluate(id=>obtenerMiEquipo().plantilla.find(j=>j.jugador_id===id).contrato.anos,player.id),3);
  await page.evaluate(()=>{for(let i=0;i<4;i++){simularJornada();if(eventoVestuarioActual)resolverEventoVestuario(0);}});
  assert.equal(await page.evaluate(()=>obtenerMiEquipo().aforo),aforo+1000);
  assert.equal(await page.evaluate(()=>obtenerMiEquipo().gestion.servicios.comida),1);
  assert.equal(await page.evaluate(()=>obtenerMiEquipo().gestion.balances.length),5);
  assert.ok(await page.evaluate(()=>obtenerMiEquipo().plantilla.some(j=>j.desarrollo.partidos>0)));
  await page.evaluate(()=>VideoActionTrigger.close());
  await page.locator('#pestana-estadio').click();await page.locator('#screen-view').selectOption('0');await page.screenshot({path:path.join(out,`club-estadio-${mode}.png`)});
  // Primera ocasión con controles reales; la segunda fija un gol para comprobar
  // que el marcador oficial usa el resultado arcade, sin otra tirada aleatoria.
  await page.evaluate(()=>{
   if(eventoVestuarioActual)resolverEventoVestuario(0);VideoActionTrigger.close();estadoJuego.carrera.modoPartido='jugar';window.__testMatchSpeed=1;window.__disableRandomVAR=true;
   const original=window.jugarOcasion2D;let calls=0;window.jugarOcasion2D=(...args)=>++calls===1?original(...args):Promise.resolve({controlledGoal:true,success:true,player:obtenerMiEquipo().plantilla.find(j=>j.titular&&!j.lesionado)});
   vivirJornada();
  });
  await page.waitForSelector('#arcade-modal.open',{timeout:40000});
  const bounds=await page.locator('.arcade-dialog').evaluate(n=>n.getBoundingClientRect().toJSON());assert.ok(bounds.top>=0&&bounds.bottom<=height+1);
  const imageBefore=await page.locator('#arcade-pitch').evaluate(n=>n.toDataURL());
  await page.keyboard.down('ArrowRight');await page.waitForTimeout(250);await page.keyboard.up('ArrowRight');
  assert.notEqual(await page.locator('#arcade-pitch').evaluate(n=>n.toDataURL()),imageBefore);
  await page.locator('#arcade-pass').click();await page.locator('#arcade-shoot').click();await page.screenshot({path:path.join(out,`club-arcade-${mode}.png`)});await page.locator('#arcade-exit').click();
  await page.waitForFunction(()=>!partidoEnCurso,null,{timeout:60000});
  assert.ok(await page.evaluate(()=>eventosPartidoActual.some(e=>Number(e.minuto)===66&&e.esGol)), 'el gol jugable entra en las estadísticas oficiales');
  assert.equal(await page.evaluate(()=>estadoPartidaValido(estadoJuego)),true);
  await page.evaluate(()=>{if(eventoVestuarioActual)resolverEventoVestuario(0);while(estadoJuego.jornadaActual<estadoJuego.calendario.length){simularJornada();if(eventoVestuarioActual)resolverEventoVestuario(0);}iniciarNuevaTemporada();});
  assert.equal(await page.evaluate(()=>estadoJuego.temporada),2);assert.equal(await page.evaluate(()=>estadoPartidaValido(estadoJuego)),true);
  const cash=await page.evaluate(()=>{guardarPartidaLocal(false);return obtenerMiEquipo().presupuesto;});await page.reload();await page.waitForSelector('.screen-mode');
  assert.equal(await page.evaluate(()=>obtenerMiEquipo().presupuesto),cash);assert.equal(await page.evaluate(()=>estadoJuego.temporada),2);
  assert.deepEqual(errors,[]);console.log(`${mode}: migración, precios, abonos, obras, empleados, cantera, contratos, 2D oficial y temporada correctos`);await page.close();
 }}finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
