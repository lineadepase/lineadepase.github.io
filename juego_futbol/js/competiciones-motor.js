/* Competiciones ficticias: dos ligas independientes y Copa Unión. */
(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory;else root.MotorCompeticiones=factory(root.ClubMotor,root.ClubProyectos);})(typeof globalThis!=='undefined'?globalThis:this,(M,P)=>{
 'use strict';const FECHAS=[4,8,12,16,20],RONDAS=['Previa','Octavos','Cuartos','Semifinales','Final'],DIA=86400000;
 const orden=(a,b)=>b.puntos-a.puntos||(b.gf-b.gc)-(a.gf-a.gc)||b.gf-a.gf||a.nombre.localeCompare(b.nombre,'es');
 const tabla=(s,d)=>s.equipos.filter(e=>(e.division||1)===d).slice().sort(orden);
 const hash=s=>[...String(s)].reduce((a,c)=>(Math.imul(a,31)+c.charCodeAt(0))>>>0,7);
 function sorteo(ids,seed){let n=hash(seed),a=ids.slice();for(let i=a.length-1;i>0;i--){n=(Math.imul(n,1664525)+1013904223)>>>0;const j=n%(i+1);[a[i],a[j]]=[a[j],a[i]];}return a;}
 function copa(s){return {semilla:sorteo(s.equipos.map(e=>e.id),'copa-'+s.temporada),rondas:[],vivos:s.equipos.map(e=>e.id),campeon:null};}
 function iniciar(s){if(!s?.equipos)return s;if(s.competiciones===undefined)s.competiciones={version:1,activa:s.equipos.length===24,inicio:Date.UTC(s.fechaActual.year,s.fechaActual.month-1,s.fechaActual.day),copa:s.equipos.length===24?copa(s):null,historial:[]};return s;}
 function calendario(equipos,robin){return [1,2].map(d=>robin(equipos.filter(e=>e.division===d).map(e=>e.nombre))).reduce((a,b)=>a.map((round,i)=>[...round,...b[i]]));}
 const pendiente=s=>!!s?.competiciones?.activa&&s.competiciones.copa.rondas.length<5&&s.jornadaActual>=FECHAS[s.competiciones.copa.rondas.length];
 function participantes(c){if(!c.rondas.length)return c.semilla.slice(8);if(c.rondas.length===1)return [...c.semilla.slice(0,8),...c.rondas[0].partidos.map(p=>p.ganador)];return c.rondas.at(-1).partidos.map(p=>p.ganador);}
 function validar(s){try{const c=s.competiciones;if(!c||c.version!==1||typeof c.activa!=='boolean'||!Number.isFinite(c.inicio)||!Array.isArray(c.historial)||c.historial.length>20)return false;
  if(!c.historial.every(h=>h&&Number.isInteger(h.temporada)&&['campeonLiga','campeonSegunda','copa'].every(k=>h[k]===null||typeof h[k]==='string')&&['ascendidos','descendidos'].every(k=>Array.isArray(h[k])&&h[k].length<=2&&h[k].every(n=>typeof n==='string'&&n.length<=80))))return false;
  for(const e of s.equipos){if(e.gestion.balances.some(b=>['operacion','premios'].some(k=>b[k]!==undefined&&(!Number.isFinite(b[k])||b[k]<0))))return false;for(const j of e.plantilla)if(j.copa&&(!['goles','partidos','minutos'].every(k=>Number.isInteger(j.copa[k])&&j.copa[k]>=0&&j.copa[k]<=1e8)||!Number.isFinite(j.copa.xg)||j.copa.xg<0))return false;}
  if(!c.activa)return [4,12].includes(s.equipos.length)&&c.copa===null;
  if(s.equipos.length!==24||![1,2].every(d=>s.equipos.filter(e=>e.division===d).length===12))return false;
  const ids=new Set(s.equipos.map(e=>e.id)),cup=c.copa;if(!cup||!Array.isArray(cup.semilla)||cup.semilla.length!==24||new Set(cup.semilla).size!==24||!cup.semilla.every(id=>ids.has(id))||!Array.isArray(cup.rondas)||cup.rondas.length>5||!Array.isArray(cup.vivos))return false;
  let expected=cup.semilla.slice(8),winners=[];
  for(let i=0;i<cup.rondas.length;i++){const r=cup.rondas[i];if(!r||r.ronda!==i||!Array.isArray(r.partidos)||r.partidos.length!==[8,8,4,2,1][i])return false;const played=r.partidos.flatMap(p=>[p.local,p.visitante]);if(new Set(played).size!==expected.length||!expected.every(id=>played.includes(id)))return false;
   for(const p of r.partidos){if(![p.local,p.visitante].includes(p.ganador)||!['gl','gv','rematesLocal','rematesVisitante'].every(k=>Number.isInteger(p[k])&&p[k]>=0&&p[k]<=30)||!['xgLocal','xgVisitante'].every(k=>Number.isFinite(p[k])&&p[k]>=0&&p[k]<=30))return false;if(p.gl===p.gv){if(!Array.isArray(p.penaltis)||p.penaltis.length!==2||!p.penaltis.every(n=>Number.isInteger(n)&&n>=0&&n<=20)||p.penaltis[0]===p.penaltis[1]||p.ganador!==(p.penaltis[0]>p.penaltis[1]?p.local:p.visitante))return false;}else if(p.ganador!==(p.gl>p.gv?p.local:p.visitante)||p.penaltis!==null)return false;}
   winners=r.partidos.map(p=>p.ganador);expected=i===0?[...cup.semilla.slice(0,8),...winners]:winners;
  }
  const vivos=cup.rondas.length?expected:s.equipos.map(e=>e.id);if(cup.vivos.length!==vivos.length||new Set(cup.vivos).size!==vivos.length||!vivos.every(id=>cup.vivos.includes(id)))return false;
  return cup.rondas.length===5?cup.campeon===winners[0]:cup.campeon===null;
 }catch(_){return false;}}
 const activos=e=>{const on=e.plantilla.filter(j=>j.titular&&!j.lesionado);return [...on,...e.plantilla.filter(j=>!j.titular&&!j.lesionado).sort((a,b)=>b.media-a.media)].slice(0,11);};
 function tirar(e,rival,rng){const ps=activos(e),qs=activos(rival),f=ps.reduce((a,j)=>a+j.media*(1-j.cansancio/200)*j.moral/100,0)/11,def=qs.reduce((a,j)=>a+j.media*(1-j.cansancio/200)*j.moral/100,0)/11,count=9+Math.floor(rng()*6),goals=new Map();let gf=0,xgf=0;
  for(let i=0;i<count&&ps.length;i++){const attackers=ps.filter(j=>j.posicion==='DEL'||j.posicion==='CEN'),pool=attackers.length?attackers:ps,j=pool[Math.min(pool.length-1,Math.floor(rng()*pool.length))],xg=Math.max(.02,Math.min(.4,.05+rng()*.18+(f-def)/700));if(!j.copa)j.copa={goles:0,xg:0,partidos:0,minutos:0};j.copa.xg+=xg;xgf+=xg;if(rng()<xg){gf++;j.copa.goles++;goals.set(j.jugador_id,(goals.get(j.jugador_id)||0)+1);}}
  for(const j of ps){if(!j.copa)j.copa={goles:0,xg:0,partidos:0,minutos:0};j.copa.partidos++;j.copa.minutos+=90;}
  return {goles:gf,xg:Number(xgf.toFixed(2)),remates:ps.length?count:0,goals};
 }
 const salario=e=>[...e.plantilla,...e.gestion.cantera.filter(j=>j.equipoB)].reduce((a,j)=>a+j.salario,0);
 const operacion=e=>Math.round(e.aforo*.9+salario(e)*.25+(e.division===2?15000:45000));
 function penaltis(rng){let a=0,b=0;for(let i=0;i<5;i++){if(rng()<.73)a++;if(rng()<.73)b++;}for(let i=0;i<5&&a===b;i++){if(rng()<.73)a++;if(rng()<.73)b++;}if(a===b){if(rng()<.5)a++;else b++;}return [a,b];}
 function resolver(s,rng=Math.random){if(!pendiente(s))throw Error('No hay ronda de copa pendiente.');const c=s.competiciones.copa,index=c.rondas.length,ids=sorteo(participantes(c),s.temporada+'-ronda-'+index),byId=new Map(s.equipos.map(e=>[e.id,e])),rows=new Map();
  // Todos los clubes pagan nómina también durante una semana de copa, incluso eliminados o exentos.
  for(const e of s.equipos){const salarios=salario(e),empleados=M.sueldoStaff(e),mantenimiento=P.efectos(e).mantenimiento,operativos=operacion(e),neto=-salarios-empleados-mantenimiento-operativos;const row={temporada:s.temporada,jornada:s.jornadaActual,ronda:index+1,competicion:'copa',asistentes:0,entradas:0,extras:0,publicidad:0,salarios,empleados,primas:0,mantenimiento,operacion:operativos,premios:0,neto};e.presupuesto+=neto;e.gestion.balances.unshift(row);e.gestion.balances=e.gestion.balances.slice(0,30);rows.set(e.id,row);e.plantilla.forEach(j=>{j.cansancio=Math.max(0,j.cansancio-10);if(j.lesionado)j.lesionado--;});}
  const partidos=[];for(let i=0;i<ids.length;i+=2){const a=byId.get(ids[i]),b=byId.get(ids[i+1]),qa=tirar(a,b,rng),qb=tirar(b,a,rng),pens=qa.goles===qb.goles?penaltis(rng):null,winner=qa.goles===qb.goles?(pens[0]>pens[1]?a:b):(qa.goles>qb.goles?a:b),q=M.estimarTaquilla(a,b),row=rows.get(a.id);row.asistentes=q.asistentes;row.entradas=q.entradas;row.extras=q.extras;row.neto+=q.total;a.presupuesto+=q.total;
   for(const [e,score,opp] of [[a,qa,qb],[b,qb,qa]]){const r=rows.get(e.id),g=e.gestion;const ads=Object.entries(g.publicidad).reduce((sum,[space,p])=>sum+(!p?0:(space==='camiseta'?1:.45*(1+P.efectos(e).publicidad))*(p.tipo==='fijo'?60000:p.tipo==='victoria'?(winner===e?125000:15000):20000+score.goles*35000)),0),primas=e.plantilla.reduce((sum,j)=>sum+j.contrato.primaGol*(score.goals.get(j.jugador_id)||0),0);r.publicidad=Math.round(ads);r.primas=primas;r.neto+=r.publicidad-primas;e.presupuesto+=r.publicidad-primas;}
   for(const e of [a,b])activos(e).forEach(j=>j.cansancio=Math.min(100,j.cansancio+12));
   const premio=[25000,50000,100000,200000,500000][index];winner.presupuesto+=premio;rows.get(winner.id).premios=premio;rows.get(winner.id).neto+=premio;partidos.push({local:a.id,visitante:b.id,gl:qa.goles,gv:qb.goles,xgLocal:qa.xg,xgVisitante:qb.xg,rematesLocal:qa.remates,rematesVisitante:qb.remates,penaltis:pens,ganador:winner.id});
  }
  c.rondas.push({ronda:index,partidos});c.vivos=index===0?[...c.semilla.slice(0,8),...partidos.map(p=>p.ganador)]:partidos.map(p=>p.ganador);if(index===4)c.campeon=c.vivos[0];M.noticia(s,'Copa Unión · '+RONDAS[index]+' disputada'+(c.campeon?': campeón '+byId.get(c.campeon).nombre:'.'));return c.rondas.at(-1);
 }
 function cerrarTemporada(s){if(!s.competiciones?.activa)return;const a=tabla(s,1),b=tabla(s,2),asc=b.slice(0,2),desc=a.slice(-2),cup=s.competiciones.copa;s.competiciones.historial.unshift({temporada:s.temporada,campeonLiga:a[0].nombre,campeonSegunda:b[0].nombre,copa:s.equipos.find(e=>e.id===cup.campeon)?.nombre||null,ascendidos:asc.map(e=>e.nombre),descendidos:desc.map(e=>e.nombre)});s.competiciones.historial=s.competiciones.historial.slice(0,20);asc.forEach(e=>{e.division=1;e.presupuesto+=500000;});desc.forEach(e=>e.division=2);M.noticia(s,'Ascensos: '+asc.map(e=>e.nombre).join(', ')+'. Descensos: '+desc.map(e=>e.nombre).join(', ')+'.');}
 function nuevaTemporada(s){const history=s.competiciones?.historial||[];s.competiciones={version:1,activa:s.equipos.length===24,inicio:Date.UTC(s.fechaActual.year,s.fechaActual.month-1,s.fechaActual.day),copa:s.equipos.length===24?copa(s):null,historial:history};s.equipos.forEach(e=>e.plantilla.forEach(j=>{j.copa={goles:0,xg:0,partidos:0,minutos:0};}));}
 function fechaJornada(s,i){return s.competiciones.inicio+(i+Math.min(5,Math.floor(i/4)))*7*DIA;}
 return {iniciar,tabla,orden,calendario,validar,pendiente,resolver,cerrarTemporada,nuevaTemporada,fechaJornada,operacion,FECHAS,RONDAS};
});
