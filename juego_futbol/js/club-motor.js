/* Reglas de carrera ficticias, independientes del DOM y comprobables con Node. */
(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.ClubMotor=api;})(typeof globalThis!=='undefined'?globalThis:this,()=>{
 'use strict';
 const ATTR=['RAS','TOZ','CHI','RET','ALM'],POS=['POR','DEF','CEN','DEL'];
 const SECTORES=['norte','sur','este','oeste'],SERVICIOS=['parking','comida','tienda','transporte'];
 const STAFF=['medico','psicologo','cantera','comercial'];
 const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
 const hash=s=>[...String(s)].reduce((n,c)=>(Math.imul(n,31)+c.charCodeAt(0))>>>0,7);
 const euros=n=>Math.round(n);
 const fin=(v,a,b)=>Number.isFinite(v)&&v>=a&&v<=b;
 function defaultPlayer(j){
  if(!j||typeof j!=='object')return;
  if(j.contrato===undefined)j.contrato={anos:3,clausula:euros(j.precio*1.8),primaGol:0};
  if(j.desarrollo===undefined)j.desarrollo={potencial:clamp(j.media+4+hash(j.jugador_id)%9,j.media,99),baseMedia:j.media,baseAtributos:{...j.atributos},partidos:0,minutos:0,retiro:35+hash(j.jugador_id)%4+(j.posicion==='POR'?2:0)};
 }
 function generar(estado,eq,posicion,edad=18,herencia=null){
  const id=`cantera-${estado.temporada}-${estado.carrera.secuencia++}`,seed=hash(id+eq.nombre);
  const nombres=['Darío','Álex','Hugo','Leo','Bruno','Izan','Gael','Nico','Pablo','Mario'];
  const apellidos=['del Olmo','Cierzo','del Río','Sendero','Valle','de la Vega','Sierra','Montes','Luna','Campos'];
  const potencial=herencia?.desarrollo.potencial||74+seed%22;
  const media=clamp(Math.round(potencial*.68)+(seed%7)-3,45,75);
  const j={jugador_id:id,nombre:nombres[seed%10]+' '+apellidos[Math.floor(seed/10)%10],jugador_real:'',equipo_origen:'Cantera ficticia',equipo_origen_parodia:eq.nombre,
   posicion,media,atributos:Object.fromEntries(ATTR.map((a,i)=>[a,clamp(media+((seed>>i)%13)-6,30,95)])),rasgo:'Promesa de la escuela',clausula:'Cantera propia',avatar_ia:'',reacciones_ia:{},edad,cumpleanos:`${String(1+seed%12).padStart(2,'0')}-${String(1+Math.floor(seed/12)%28).padStart(2,'0')}`,moral:80,cansancio:0,precio:media*7000,salario:Math.round(media*45),goles:0,xg:0,lesionado:0,titular:false};
  defaultPlayer(j);j.desarrollo.potencial=potencial;
  if(herencia){j.desarrollo.baseMedia=herencia.desarrollo.baseMedia;j.desarrollo.baseAtributos={...herencia.desarrollo.baseAtributos};j.desarrollo.origenRetirado=herencia.jugador_id;}
  return j;
 }
 function normalizar(s){
  if(!s||!Array.isArray(s.equipos))return s;
  if(s.carrera===undefined)s.carrera={version:1,secuencia:1,ultimaEvolucion:0,retirados:[],bajasBase:[],noticias:[],liquidados:[],modoPartido:'dirigir'};
  if(!s.carrera||typeof s.carrera!=='object')return s;
  if(s.carrera.bajasBase===undefined)s.carrera.bajasBase=[];
  if(s.carrera.mentalidad===undefined)s.carrera.mentalidad=50;
  s.equipos.forEach(eq=>{
   if(!eq||!Array.isArray(eq.plantilla))return;
   if(eq.gestion===undefined){
    const n=Math.floor(eq.aforo/4);
    eq.gestion={entrada:20,abono:150,abonados:0,abonosTemporada:0,gradas:{norte:n,sur:n,este:n,oeste:eq.aforo-3*n},servicios:Object.fromEntries(SERVICIOS.map(k=>[k,0])),staff:Object.fromEntries(STAFF.map(k=>[k,0])),obras:[],cantera:[],publicidad:{camiseta:null,vallas:null},balances:[],ultimoCierre:[]};
    for(const pos of ['POR','DEF','DEL'])eq.gestion.cantera.push(generar(s,eq,pos,17));
   }
   if(eq.gestion.modernizacion===undefined)eq.gestion.modernizacion=0;
   if(eq.gestion.filial===undefined)eq.gestion.filial={activo:false,jugados:0,victorias:0,empates:0,derrotas:0,ultimo:''};
   eq.plantilla.forEach(defaultPlayer);eq.gestion?.cantera?.forEach(defaultPlayer);
  });
  s.mercado?.forEach(defaultPlayer);
  return s;
 }
 function jugadorValido(j){
  return !!j&&typeof j.jugador_id==='string'&&/^[\p{L}\p{N}][\p{L}\p{N}_-]{0,100}$/u.test(j.jugador_id)&&typeof j.nombre==='string'&&j.nombre.length<=80&&POS.includes(j.posicion)&&fin(j.media,1,100)&&Number.isInteger(j.edad)&&fin(j.edad,16,99)&&
   j.atributos&&ATTR.every(k=>fin(j.atributos[k],0,100))&&fin(j.moral,0,100)&&fin(j.cansancio,0,100)&&fin(j.precio,0,1e10)&&fin(j.salario,0,1e7)&&fin(j.goles,0,1e7)&&fin(j.xg,0,1e9)&&Number.isInteger(j.lesionado)&&fin(j.lesionado,0,10000)&&typeof j.titular==='boolean'&&typeof j.avatar_ia==='string'&&typeof j.cumpleanos==='string'&&/^\d{2}-\d{2}$/.test(j.cumpleanos)&&(()=>{const [m,d]=j.cumpleanos.split('-').map(Number),date=new Date(Date.UTC(2028,m-1,d));return date.getUTCMonth()===m-1&&date.getUTCDate()===d;})()&&
   j.contrato&&Number.isInteger(j.contrato.anos)&&fin(j.contrato.anos,0,5)&&fin(j.contrato.clausula,0,1e10)&&fin(j.contrato.primaGol,0,1e6)&&
   j.desarrollo&&fin(j.desarrollo.potencial,1,100)&&fin(j.desarrollo.baseMedia,1,100)&&Number.isInteger(j.desarrollo.partidos)&&fin(j.desarrollo.partidos,0,10000)&&fin(j.desarrollo.minutos,0,1e7)&&Number.isInteger(j.desarrollo.retiro)&&fin(j.desarrollo.retiro,34,42)&&ATTR.every(k=>fin(j.desarrollo.baseAtributos?.[k],0,100));
 }
 function esGenerado(j){return /^cantera-\d+-\d+$/.test(j?.jugador_id||'')&&jugadorValido(j);}
 function validar(s){
  try{
   if(!s.carrera||s.carrera.version!==1||!Number.isInteger(s.carrera.secuencia)||!fin(s.carrera.secuencia,1,1e9)||!Number.isInteger(s.carrera.ultimaEvolucion)||!fin(s.carrera.ultimaEvolucion,0,s.temporada)||!['dirigir','jugar'].includes(s.carrera.modoPartido)||!Array.isArray(s.carrera.liquidados)||!Array.isArray(s.carrera.bajasBase)||s.carrera.bajasBase.length>1000||!Array.isArray(s.carrera.retirados)||s.carrera.retirados.length>200||!Array.isArray(s.carrera.noticias)||s.carrera.noticias.length>100)return false;
   if(!fin(s.carrera.mentalidad,0,100)||!s.carrera.noticias.every(t=>typeof t==='string'&&t.length<2000))return false;
   if(!s.carrera.retirados.every(r=>r&&typeof r.id==='string'&&typeof r.nombre==='string'&&fin(r.edad,16,99)&&Number.isInteger(r.temporada)&&typeof r.regen==='string')||!s.carrera.bajasBase.every(id=>typeof id==='string'&&id.length<=100)||s.carrera.liquidados.length>1000||!s.carrera.liquidados.every(k=>typeof k==='string'&&k.length<=300))return false;
   const ids=[];
   for(const e of s.equipos){const g=e.gestion,f=g?.filial;if(!Number.isInteger(g?.modernizacion)||!fin(g.modernizacion,0,3)||!f||typeof f.activo!=='boolean'||!['jugados','victorias','empates','derrotas'].every(k=>Number.isInteger(f[k])&&fin(f[k],0,100000))||f.jugados!==f.victorias+f.empates+f.derrotas||typeof f.ultimo!=='string'||f.ultimo.length>100)return false;if(g.cantera?.some(j=>j.equipoB!==undefined&&typeof j.equipoB!=='boolean')||g.cantera?.filter(j=>j.equipoB).length>12||(!f.activo&&g.cantera?.some(j=>j.equipoB)))return false;}
   for(const eq of s.equipos){
    const g=eq.gestion;
    if(!g||!fin(g.entrada,5,120)||!fin(g.abono,20,1500)||!Number.isInteger(g.abonados)||!fin(g.abonados,0,eq.aforo)||!fin(g.abonosTemporada,0,s.temporada)||!SECTORES.every(k=>Number.isInteger(g.gradas?.[k])&&fin(g.gradas[k],0,100000))||Object.values(g.gradas).reduce((a,b)=>a+b,0)!==eq.aforo||!SERVICIOS.every(k=>Number.isInteger(g.servicios?.[k])&&fin(g.servicios[k],0,3))||!STAFF.every(k=>Number.isInteger(g.staff?.[k])&&fin(g.staff[k],0,3))||!Array.isArray(g.cantera)||g.cantera.length>24||!Array.isArray(g.obras)||g.obras.length>8||!g.obras.every(o=>['grada','servicio','remodelacion'].includes(o.tipo)&&Number.isInteger(o.restante)&&fin(o.restante,1,52)&&(o.tipo==='remodelacion'?['estadio']:o.tipo==='grada'?SECTORES:SERVICIOS).includes(o.objetivo))||!Array.isArray(g.balances)||g.balances.length>30)return false;
    if(!Array.isArray(g.ultimoCierre)||g.ultimoCierre.length>100||!g.ultimoCierre.every(t=>typeof t==='string'&&t.length<=2000))return false;
    if(!g.balances.every(b=>b&&['asistentes','entradas','extras','publicidad','salarios','empleados','primas'].every(k=>fin(b[k],0,1e12))&&Number.isFinite(b.neto)&&Number.isInteger(b.temporada)&&Number.isInteger(b.jornada)))return false;
    if(!g.publicidad||!['camiseta','vallas'].every(k=>g.publicidad[k]===null||(['fijo','victoria','goles'].includes(g.publicidad[k].tipo)&&typeof g.publicidad[k].nombre==='string'&&g.publicidad[k].temporada===s.temporada)))return false;
    for(const j of [...eq.plantilla,...g.cantera]){if(!jugadorValido(j))return false;ids.push(j.jugador_id);}
   }
   const maxSeq=Math.max(0,...[...ids,...s.mercado.map(j=>j.jugador_id)].filter(id=>/^cantera-\d+-\d+$/.test(id)).map(id=>Number(id.split('-')[2])));
   return s.carrera.secuencia>maxSeq&&new Set(ids).size===ids.length&&s.mercado.length<=100&&s.mercado.every(jugadorValido);
  }catch(_){return false;}
 }
 function noticia(s,texto){s.carrera.noticias.unshift(String(texto));s.carrera.noticias=s.carrera.noticias.slice(0,100);}
 function pagar(eq,importe){if(!fin(importe,0,1e10)||eq.presupuesto<importe)throw Error('Presupuesto insuficiente.');eq.presupuesto-=importe;}
 function estimarTaquilla(eq,rival){
  const g=eq.gestion,calidad=(rival?.plantilla||eq.plantilla).reduce((v,j)=>v+j.media,0)/Math.max(1,(rival?.plantilla||eq.plantilla).length);
  const atractivo=.62+calidad/400+g.servicios.transporte*.025+g.modernizacion*.015;
  const demanda=clamp(atractivo*(1-(g.entrada-20)*.014),.08,1);
  const asistentes=Math.min(eq.aforo,Math.max(g.abonados,Math.round(eq.aforo*demanda)));
  const entradas=(asistentes-g.abonados)*g.entrada;
  const extras=Math.round(asistentes*(g.servicios.comida*.65+g.servicios.tienda*.55+g.servicios.parking*.35));
  return {asistentes,entradas,extras,total:Math.round((entradas+extras)*(1+g.staff.comercial*.03))};
 }
 function precios(eq,entrada,abono){if(!fin(entrada,5,120)||!fin(abono,20,1500))throw Error('Entradas: 5–120 €. Abonos: 20–1.500 €.');eq.gestion.entrada=entrada;eq.gestion.abono=abono;}
 function abonos(s,eq){
  if(s.jornadaActual!==0||eq.gestion.abonosTemporada===s.temporada)throw Error('La campaña de abonos se abre una vez, antes de la primera jornada.');
  const g=eq.gestion,locales=s.calendario.filter(j=>j.some(([a])=>a===eq.nombre)).length;
  g.abonados=Math.round(eq.aforo*clamp(.28*(g.entrada*Math.max(1,locales)/g.abono),.02,.55));
  g.abonosTemporada=s.temporada;const ingreso=g.abonados*g.abono;eq.presupuesto+=ingreso;
  noticia(s,`${eq.nombre}: ${g.abonados} abonos vendidos por ${ingreso.toLocaleString('es-ES')} €.`);return ingreso;
 }
 function obra(eq,tipo,objetivo){
  const g=eq.gestion,list=tipo==='grada'?SECTORES:SERVICIOS;
  if(g.obras.length>=8)throw Error('Ya hay ocho obras en curso. Espera a que termine alguna.');
  if(!['grada','servicio'].includes(tipo)||!list.includes(objetivo))throw Error('Obra no disponible.');
  if(g.obras.some(o=>o.tipo===tipo&&o.objetivo===objetivo))throw Error('Ya hay una obra en ese sector.');
  if(tipo==='grada'&&eq.aforo+(g.obras.filter(o=>o.tipo==='grada').length+1)*1000>150000)throw Error('Aforo máximo de 150.000 alcanzado, incluidas las obras pendientes.');
  if(tipo==='servicio'&&g.servicios[objetivo]>=3)throw Error('Servicio al máximo nivel.');
  const coste=tipo==='grada'?250000:100000*(g.servicios[objetivo]+1);
  pagar(eq,coste);g.obras.push({tipo,objetivo,restante:2,coste});return coste;
 }
 function contratarStaff(eq,puesto,nivel){
  if(!STAFF.includes(puesto)||!Number.isInteger(nivel)||!fin(nivel,0,3))throw Error('Puesto o nivel no válido.');
  if(eq.gestion.staff[puesto]===nivel)return 0;
  const coste=Math.max(0,nivel-eq.gestion.staff[puesto])*20000;pagar(eq,coste);eq.gestion.staff[puesto]=nivel;return coste;
 }
 const sueldoStaff=eq=>Object.values(eq.gestion.staff).reduce((a,n)=>a+[0,2000,6000,12000][n],0);
 function publicidad(s,eq,espacio,tipo){
  if(!['camiseta','vallas'].includes(espacio)||!['fijo','victoria','goles'].includes(tipo))throw Error('Acuerdo no válido.');
  if(eq.gestion.publicidad[espacio])throw Error('Ese espacio está contratado hasta final de temporada.');
  const nombres={fijo:'Panadería del Cierzo',victoria:'Transportes Sendero',goles:'Huerta y Gol'};
  eq.gestion.publicidad[espacio]={tipo,nombre:nombres[tipo],temporada:s.temporada};
 }
 function liquidar(s,local,vis,gL,gV){
  const key=`${s.temporada}:${local.id||local.nombre}:${vis.id||vis.nombre}`;
  if(s.carrera.liquidados.includes(key))return {duplicado:true,taquilla:0};
  s.carrera.liquidados.push(key);const estimate=estimarTaquilla(local,vis);
  for(const [eq,goles,contra,home] of [[local,gL,gV,true],[vis,gV,gL,false]]){
   const g=eq.gestion,ingresos=home?estimate.total:0;
   const publicidad=Object.entries(g.publicidad).reduce((sum,[espacio,c])=>sum+(!c?0:(espacio==='camiseta'?1:.45)*(c.tipo==='fijo'?60000:c.tipo==='victoria'?(goles>contra?125000:15000):20000+goles*35000)),0);
   const aptos=eq.plantilla.filter(j=>j.titular&&!j.lesionado);
   aptos.forEach(j=>{j.desarrollo.partidos++;j.desarrollo.minutos+=90;});
   const prima=eq.plantilla.reduce((sum,j)=>sum+j.contrato.primaGol*(j.goles-(j.desarrollo.golesLiquidados||0)),0);
   eq.plantilla.forEach(j=>{j.desarrollo.golesLiquidados=j.goles;});
   const salarios=[...eq.plantilla,...g.cantera.filter(j=>j.equipoB)].reduce((sum,j)=>sum+j.salario,0),empleados=sueldoStaff(eq);
   const neto=Math.round(ingresos+publicidad-salarios-empleados-Math.max(0,prima));eq.presupuesto+=neto;
   g.balances.unshift({temporada:s.temporada,jornada:s.jornadaActual+1,local:home,asistentes:home?estimate.asistentes:0,entradas:home?estimate.entradas:0,extras:home?estimate.extras:0,publicidad:Math.round(publicidad),salarios,empleados,primas:Math.max(0,prima),neto});g.balances=g.balances.slice(0,30);
   g.obras.forEach(o=>{o.restante--;if(o.restante===0){if(o.tipo==='grada'){g.gradas[o.objetivo]+=1000;eq.aforo+=1000;}else if(o.tipo==='remodelacion')g.modernizacion++;else g.servicios[o.objetivo]++;noticia(s,`${eq.nombre}: terminada la obra de ${o.objetivo}.`);}});g.obras=g.obras.filter(o=>o.restante>0);
   eq.plantilla.forEach(j=>{j.moral=clamp(j.moral+g.staff.psicologo,0,100);j.cansancio=clamp(j.cansancio-g.staff.medico*2,0,100);if(j.lesionado&&g.staff.medico>=2&&!globalThis.ClubOperaciones)j.lesionado=Math.max(0,j.lesionado-1);});
  }
  return {duplicado:false,taquilla:estimate.total};
 }
 function ojear(s,eq){
  if(eq.gestion.cantera.filter(j=>!j.equipoB).length>=12||eq.gestion.cantera.length>=24)throw Error('La cantera tiene doce plazas. Promociona jugadores antes de ojear.');
  pagar(eq,10000);const counts=Object.fromEntries(POS.map(p=>[p,eq.plantilla.filter(j=>j.posicion===p).length]));
  const pos=counts.POR<2?'POR':POS[(s.carrera.secuencia)%4];const j=generar(s,eq,pos,17+s.carrera.secuencia%2);eq.gestion.cantera.push(j);return j;
 }
 function promocionar(eq,id){
  if(eq.plantilla.length>=25)throw Error('El primer equipo ya tiene 25 jugadores.');
  const i=eq.gestion.cantera.findIndex(j=>j.jugador_id===id);if(i<0)throw Error('Juvenil no disponible.');
  const [j]=eq.gestion.cantera.splice(i,1);eq.plantilla.push(j);return j;
 }
 function evaluarOferta(s,eq,j,o,renovar=false){
  if(!j||!o||!fin(o.precio,0,1e10)||!fin(o.salario,100,1e7)||!Number.isInteger(o.anos)||!fin(o.anos,1,5)||!fin(o.clausula,0,1e10)||!fin(o.primaGol,0,1e6))throw Error('Revisa los importes y la duración (1–5 años).');
  const precio=renovar?0:j.precio;
  const salario=Math.round(Math.max(1000,j.salario)*(o.clausula>j.precio*3?1.25:1));
  const contra={precio,salario,anos:o.anos,clausula:Math.max(o.clausula,Math.round(j.precio*.5)),primaGol:o.primaGol};
  if(!renovar&&!s.ventanaMercadoAbierta)return {estado:'cerrado',texto:'El mercado abre en agosto y diciembre.'};
  if(!renovar&&eq.plantilla.length>=25)return {estado:'rechazo',texto:'Plantilla completa: máximo 25 futbolistas.'};
  if(eq.presupuesto<Math.max(precio,o.precio))return {estado:'rechazo',texto:'No hay presupuesto para pagar el traspaso.'};
  if(renovar&&o.precio!==0)return {estado:'rechazo',texto:'Una renovación no lleva traspaso: indica 0 € en ese campo.'};
  if(o.salario<salario*.65||o.precio<precio*.5)return {estado:'ruptura',texto:'La propuesta está demasiado lejos. El jugador rechaza estas condiciones.'};
  if(o.precio<precio||o.salario<salario||o.clausula<j.precio*.5)return {estado:'contraoferta',texto:'Pide mejorar estas condiciones. Puedes cargar la contraoferta o retirarte.',contra};
  return {estado:'aceptada',texto:'Oferta aceptada. Puedes firmar ahora; todavía no se ha cobrado nada.',contra};
 }
 function firmar(s,eq,id,o,renovar=false){
  const j=(renovar?eq.plantilla:s.mercado).find(j=>j.jugador_id===id);
  const response=evaluarOferta(s,eq,j,o,renovar);if(response.estado!=='aceptada')throw Error(response.texto);
  if(!renovar){
   const owner=s.equipos.find(e=>e.plantilla.some(p=>p.jugador_id===id));
   if(owner===eq)throw Error('El jugador ya está en tu club.');
   if(owner){owner.plantilla=owner.plantilla.filter(p=>p.jugador_id!==id);owner.presupuesto+=o.precio;reforzar(s,owner);}
   pagar(eq,o.precio);eq.plantilla.push(j);j.titular=false;s.mercado=s.mercado.filter(p=>p.jugador_id!==id);
  }
  j.salario=o.salario;j.contrato={anos:o.anos,clausula:o.clausula,primaGol:o.primaGol};
  noticia(s,`${j.nombre}: ${renovar?'renovación':'fichaje'} por ${o.anos} temporadas.`);return j;
 }
 function reforzar(s,eq){
  const objetivo={POR:2,DEF:4,CEN:4,DEL:2};
  for(const p of POS){while(eq.plantilla.filter(j=>j.posicion===p).length<objetivo[p]&&eq.plantilla.length<25){const i=eq.gestion.cantera.findIndex(j=>j.posicion===p);eq.plantilla.push(i>=0?eq.gestion.cantera.splice(i,1)[0]:generar(s,eq,p));}}
  while(eq.plantilla.length<14)eq.plantilla.push(generar(s,eq,POS[s.carrera.secuencia%4]));
 }
 function clausulas(s){
  const changes=[];
  for(const owner of s.equipos){
   const j=owner.plantilla.find(p=>p.contrato.clausula<p.precio*.65&&p.contrato.anos>0);
   if(!j)continue;
   const comprador=s.equipos.find(e=>e!==owner&&e.plantilla.length<25&&e.presupuesto>j.contrato.clausula+j.salario*6&&e.plantilla.filter(p=>p.posicion===j.posicion).length<6);
   if(!comprador)continue;
   const precio=j.contrato.clausula;comprador.presupuesto-=precio;owner.presupuesto+=precio;
   owner.plantilla=owner.plantilla.filter(p=>p!==j);comprador.plantilla.push(j);j.titular=false;j.contrato.clausula=Math.round(j.precio*1.8);reforzar(s,owner);
   changes.push(`${comprador.nombre} paga ${precio.toLocaleString('es-ES')} € de cláusula por ${j.nombre}.`);
  }
  changes.forEach(t=>noticia(s,t));return changes;
 }
 function evolucionar(s,totalPartidos){
  if(s.carrera.ultimaEvolucion>=s.temporada)return [];
  const umbral=Math.max(1,Math.ceil(totalPartidos*.55)),resumen=[];
  for(const eq of s.equipos){
   const g=eq.gestion;g.ultimoCierre=[];
   for(const j of [...eq.plantilla]){
    const d=j.desarrollo;let delta=0;
    if(j.edad>=d.retiro){
     eq.plantilla=eq.plantilla.filter(p=>p!==j);s.mercado=s.mercado.filter(p=>p.jugador_id!==j.jugador_id);
     const regen=generar(s,eq,j.posicion,18+hash(j.jugador_id+s.temporada)%7,j);
     if(g.cantera.length<12)g.cantera.push(regen);else eq.plantilla.push(regen);
     s.carrera.retirados.push({id:j.jugador_id,nombre:j.nombre,edad:j.edad,temporada:s.temporada,regen:regen.jugador_id});
     if(!j.jugador_id.startsWith('cantera-')&&!s.carrera.bajasBase.includes(j.jugador_id))s.carrera.bajasBase.push(j.jugador_id);
     g.ultimoCierre.push(`${j.nombre} se retira con ${j.edad} años. Relevo: ${regen.nombre} (${regen.edad}).`);continue;
    }
    if(j.edad<25&&d.partidos>=umbral)delta=Math.min(3,1+Math.floor(d.partidos/Math.max(1,totalPartidos)*2)+Math.floor(g.staff.cantera/2),Math.max(0,d.potencial-j.media));
    if(j.edad>(j.posicion==='POR'?33:30))delta=-Math.min(3,1+Math.floor((j.edad-31)/3));
    j.media=clamp(j.media+delta,1,100);ATTR.forEach(k=>j.atributos[k]=clamp(j.atributos[k]+delta,1,100));
    if(delta)g.ultimoCierre.push(`${j.nombre}: ${delta>0?'+':''}${delta} de media (${d.partidos}/${totalPartidos} partidos).`);
    j.precio=Math.round(j.media*15000*(j.edad<25?1.35:j.edad>30?.7:1));
    j.contrato.anos=Math.max(0,j.contrato.anos-1);
    if(j.contrato.anos===0){
     if(eq.nombre===s.equipoControlado){eq.plantilla=eq.plantilla.filter(p=>p!==j);j.precio=0;j.titular=false;if(!s.mercado.some(p=>p.jugador_id===j.jugador_id))s.mercado.push(j);g.ultimoCierre.push(`${j.nombre} termina contrato y queda libre.`);}
     else j.contrato.anos=2;
    }
    d.partidos=0;d.minutos=0;d.golesLiquidados=0;
   }
   g.cantera.forEach(j=>{const delta=Math.min(2+Math.floor(g.staff.cantera/2),j.desarrollo.potencial-j.media);j.media+=Math.max(0,delta);ATTR.forEach(k=>j.atributos[k]=clamp(j.atributos[k]+Math.max(0,delta),1,100));});
   const graduados=g.cantera.filter(j=>j.edad>24);g.cantera=g.cantera.filter(j=>j.edad<=24);
   graduados.forEach(j=>{j.precio=0;j.contrato.anos=0;if(s.mercado.length<100)s.mercado.push(j);});
   reforzar(s,eq);while(g.cantera.length<3)g.cantera.push(generar(s,eq,POS[s.carrera.secuencia%4],17));
   g.abonados=0;g.abonosTemporada=0;g.publicidad={camiseta:null,vallas:null};
   resumen.push(...g.ultimoCierre.map(t=>eq.nombre+': '+t));
  }
  const owned=new Set(s.equipos.flatMap(e=>e.plantilla.map(j=>j.jugador_id)));
  s.mercado=s.mercado.map(j=>{
   if(owned.has(j.jugador_id)||j.edad<j.desarrollo.retiro)return j;
   const regen=generar(s,s.equipos[0],j.posicion,18+hash(j.jugador_id)%7,j);
   s.carrera.retirados.push({id:j.jugador_id,nombre:j.nombre,edad:j.edad,temporada:s.temporada,regen:regen.jugador_id});
   if(!j.jugador_id.startsWith('cantera-')&&!s.carrera.bajasBase.includes(j.jugador_id))s.carrera.bajasBase.push(j.jugador_id);
   return regen;
  });
  s.mercado=s.mercado.slice(-100);
  s.carrera.ultimaEvolucion=s.temporada;s.carrera.liquidados=[];s.carrera.retirados=s.carrera.retirados.slice(-200);
  resumen.forEach(t=>noticia(s,t));return resumen;
 }
 return {normalizar,validar,jugadorValido,esGenerado,generar,estimarTaquilla,precios,abonos,obra,contratarStaff,sueldoStaff,publicidad,liquidar,ojear,promocionar,evaluarOferta,firmar,reforzar,clausulas,evolucionar,noticia,SECTORES,SERVICIOS,STAFF};
});
