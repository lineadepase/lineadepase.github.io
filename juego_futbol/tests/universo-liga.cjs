const {chromium}=require('playwright');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
  const page=await browser.newPage();page.on('dialog',d=>d.accept());
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:8765/juego_futbol/');await page.waitForSelector('.screen-mode');
  const fresh=await page.evaluate(()=>({teams:estadoJuego.equipos.length,rounds:estadoJuego.calendario.length,valid:estadoPartidaValido(estadoJuego),ids:new Set(estadoJuego.equipos.flatMap(e=>e.plantilla.map(j=>j.jugador_id))).size,names:new Set(estadoJuego.equipos.flatMap(e=>e.plantilla.map(j=>j.nombre))).size,real:PLANTILLAS_DB.equipos.some(e=>e.club_real||e.jugadores.some(j=>j.jugador_real))}));
  assert.deepEqual(fresh,{teams:12,rounds:22,valid:true,ids:168,names:168,real:false});
  const migration=await page.evaluate(()=>{
   // Reproduce una carrera anterior con cuatro clubes y una jornada jugada.
   let s=crearEstadoInicial();s.equipos=s.equipos.slice(0,4);s.mercado=[];
   const old=s.equipos[0].nombre;s.equipos[0].nombre='Real Magras de Madrid';s.equipoControlado='Real Magras de Madrid';
   s.calendario=generarCalendario(s.equipos.map(e=>e.nombre));s.jornadaActual=1;delete s.universoVersion;
   s.equipos[0].presupuesto=1234567;s.equipos[0].plantilla[0].goles=3;
   s=normalizarEstadoPartida(JSON.parse(JSON.stringify(s)));
   const before={name:s.equipoControlado,teams:s.equipos.length,round:s.jornadaActual,cash:s.equipos[0].presupuesto,goals:s.equipos[0].plantilla[0].goles,valid:estadoPartidaValido(s)};
   estadoJuego=s;EQUIPO_CONTROLADO=s.equipoControlado;
   while(s.jornadaActual<s.calendario.length){simularJornada();if(eventoVestuarioActual)resolverEventoVestuario(0);}
   iniciarNuevaTemporada();
   return {before,after:{teams:s.equipos.length,rounds:s.calendario.length,season:s.temporada,valid:estadoPartidaValido(s),unique:new Set(s.equipos.flatMap(e=>e.gestion.cantera.map(j=>j.jugador_id))).size}};
  });
  assert.deepEqual(migration.before,{name:'Unión Valdoria',teams:4,round:1,cash:1234567,goals:3,valid:true});
  assert.deepEqual(migration.after,{teams:12,rounds:22,season:2,valid:true,unique:36});
  const weekly=await page.evaluate(()=>{const a=estadoJuego.fechaActual;const start=Date.UTC(a.year,a.month-1,a.day);simularJornada();if(eventoVestuarioActual)resolverEventoVestuario(0);const b=estadoJuego.fechaActual;return Date.UTC(b.year,b.month-1,b.day)-start;});
  assert.equal(weekly,7*86400000);assert.deepEqual(errors,[]);
  console.log('Universo original, calendario 22 jornadas, semana de 7 días y migración de carrera antigua: correctos');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
