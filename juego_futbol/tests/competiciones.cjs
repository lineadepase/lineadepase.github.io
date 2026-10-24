const {chromium}=require('playwright');
const assert=require('node:assert/strict');
(async()=>{const browser=await chromium.launch({headless:true});try{
for(const viewport of [{width:1440,height:900},{width:390,height:844}]){
 const page=await browser.newPage({viewport});const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('dialog',d=>d.accept());
 await page.goto('http://127.0.0.1:8765/juego_futbol/');await page.waitForSelector('.screen-mode');
 const result=await page.evaluate(()=>{
  const s=estadoJuego,C=ClubCompeticiones,league=()=>s.equipos.map(e=>[e.pj,e.puntos,e.gf,e.gc,...e.plantilla.map(j=>j.goles)]);
  const edge=JSON.parse(JSON.stringify(s));edge.jornadaActual=4;const pk=C.resolver(edge,()=>.99);if(!pk.partidos.every(p=>p.gl===p.gv&&p.penaltis&&p.penaltis[0]!==p.penaltis[1]))throw Error('Desempate por penaltis inválido');
  const initial={valid:estadoPartidaValido(s),teams:s.equipos.length,divisions:[C.tabla(s,1).length,C.tabla(s,2).length],rounds:s.calendario.length};
  for(let i=0;i<4;i++){simularJornada();if(eventoVestuarioActual)resolverEventoVestuario(0);}
  const before=JSON.stringify(league()),date=s.fechaActual,ms=Date.UTC(date.year,date.month-1,date.day),cash=s.equipos.map(e=>e.presupuesto);
  simularJornada();const after=s.fechaActual;
  const first={unchanged:before===JSON.stringify(league()),round:s.jornadaActual,cup:s.competiciones.copa.rondas.length,days:(Date.UTC(after.year,after.month-1,after.day)-ms)/86400000,ledger:s.equipos.every((e,i)=>Math.abs(e.presupuesto-cash[i]-e.gestion.balances[0].neto)<.001),rows:s.equipos.every(e=>e.gestion.balances[0].competicion==='copa')};
  const filter=document.getElementById('analysis-division');filter.value='2';filter.dispatchEvent(new Event('input'));const filtered=document.querySelectorAll('#analysis-chart [data-analysis-club]').length;filter.value='0';filter.dispatchEvent(new Event('input'));
  const frozen=JSON.stringify(s);let blocked=false;try{C.resolver(s)}catch(_){blocked=true}const duplicate=blocked&&JSON.stringify(s)===frozen;
  const damaged=JSON.parse(JSON.stringify(s));damaged.competiciones.copa.semilla[0]=damaged.competiciones.copa.semilla[1];const rejects=!estadoPartidaValido(damaged);
  let calls=0;while(s.jornadaActual<22&&calls++<40){simularJornada();if(eventoVestuarioActual)resolverEventoVestuario(0);}
  const cup=s.competiciones.copa,complete={valid:estadoPartidaValido(s),cupRounds:cup.rondas.length,matches:cup.rondas.reduce((n,r)=>n+r.partidos.length,0),allPlayed:s.equipos.every(e=>e.pj===22),winner:!!cup.campeon};
  const top=C.tabla(s,2).slice(0,2).map(e=>e.id),bottom=C.tabla(s,1).slice(-2).map(e=>e.id);iniciarNuevaTemporada();
  const next={valid:estadoPartidaValido(s),season:s.temporada,history:s.competiciones.historial.length,promoted:top.every(id=>s.equipos.find(e=>e.id===id).division===1),relegated:bottom.every(id=>s.equipos.find(e=>e.id===id).division===2),reset:s.competiciones.copa.rondas.length===0&&s.equipos.every(e=>e.plantilla.every(j=>!j.copa||Object.values(j.copa).every(n=>n===0)))};
  guardarPartidaLocal(false);return {initial,first,filtered,duplicate,rejects,complete,next};
 });
 assert.deepEqual(result.initial,{valid:true,teams:24,divisions:[12,12],rounds:22});assert.deepEqual(result.first,{unchanged:true,round:4,cup:1,days:7,ledger:true,rows:true});assert.equal(result.filtered,12);assert.equal(result.duplicate,true);assert.equal(result.rejects,true);assert.deepEqual(result.complete,{valid:true,cupRounds:5,matches:23,allPlayed:true,winner:true});assert.deepEqual(result.next,{valid:true,season:2,history:1,promoted:true,relegated:true,reset:true});
 await page.reload();await page.waitForSelector('.screen-mode');assert.equal(await page.evaluate(()=>estadoJuego.temporada===2&&estadoPartidaValido(estadoJuego)),true);
 await page.evaluate(()=>abrirPantallaJuego('competition-overview'));await page.screenshot({path:'juego_futbol/tests/test-artifacts/competiciones-'+viewport.width+'.png'});
 assert.deepEqual(errors,[]);await page.close();console.log('Competiciones: calendario, copa, caja, estadísticas, ascensos y persistencia correctos en '+viewport.width);
}
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
