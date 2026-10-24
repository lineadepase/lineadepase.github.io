/* Departamentos del club: interfaz y adaptación de partidas anteriores. */
(() => {
 'use strict';
 const M=window.ClubMotor,$=id=>document.getElementById(id),esc=s=>escaparHTML(String(s));
 const money=n=>Math.round(n).toLocaleString('es-ES')+' €';
 const crear=crearEstadoInicial,normalizar=normalizarEstadoPartida,validar=estadoPartidaValido,ui=actualizarUI;
 crearEstadoInicial=()=>M.normalizar(crear());
 normalizarEstadoPartida=s=>M.normalizar(normalizar(s));
 estadoPartidaValido=s=>validar(s)&&M.validar(s);
 const birthdays=procesarCumpleanosEnRango;
 procesarCumpleanosEnRango=function(desde,hasta,equipos=estadoJuego?.equipos||[],mercado=estadoJuego?.mercado||[]){
  const personas=[...new Set([...equipos.flatMap(e=>[...e.plantilla,...(e.gestion?.cantera||[])]),...mercado])];
  return birthdays(desde,hasta,[],personas);
 };
 window.ldpProcesarCumpleanos=procesarCumpleanosEnRango;
 const panel=(id,title,html)=>{const n=document.createElement('div');n.className='panel club-panel';n.id=id;n.innerHTML=`<h2 class="panel-title">${title}</h2>${html}`;return n;};
 function department(id,label){
  const n=document.createElement('section');n.id='tab-'+id;n.className='tab-content';n.setAttribute('role','tabpanel');n.setAttribute('aria-labelledby','pestana-'+id);n.setAttribute('aria-hidden','true');n.tabIndex=0;document.querySelector('main').append(n);
  const b=document.createElement('button');b.id='pestana-'+id;b.className='tab-btn';b.type='button';b.textContent=label;b.setAttribute('role','tab');b.setAttribute('aria-controls',n.id);b.setAttribute('aria-selected','false');b.tabIndex=-1;b.onclick=()=>cambiarPestana(id,b);document.querySelector('nav').append(b);return n;
 }
 const finances=department('finanzas','💶 Finanzas'),stadium=department('estadio','🏟️ Estadio');
 const feedback='<p id="club-feedback" class="club-feedback" role="status" aria-live="polite">Los importes y las reglas son ficticios. Cada operación se aplica al instante.</p>';
 finances.append(panel('club-tickets','Entradas y abonos',`<p>El precio, el rival y el transporte cambian la asistencia. Los abonados no pagan otra entrada.</p><div id="ticket-preview" class="club-metrics"></div><form id="ticket-form"><label>Entrada (€)<input id="ticket-price" type="number" min="5" max="120" value="20"></label><label>Abono de temporada (€)<input id="season-price" type="number" min="20" max="1500" value="150"></label><button>Guardar precios</button></form><button id="sell-season-tickets" type="button">Abrir campaña de abonos</button><p id="season-ticket-status" class="hint-box"></p>`),panel('club-ads','Camiseta y vallas',`<p>Firma un acuerdo por espacio hasta final de temporada. La respuesta es inmediata.</p><p>Fijo: 60.000 €/partido. Victoria: 125.000 € al ganar, 15.000 € en otro resultado. Goles: 20.000 € + 35.000 € por gol. Las vallas pagan el 45 %.</p><form id="ads-form"><label>Espacio<select id="ads-space"><option value="camiseta">Camiseta</option><option value="vallas">Vallas</option></select></label><label>Propuesta<select id="ads-type"><option value="fijo">Panadería del Cierzo · fijo</option><option value="victoria">Transportes Sendero · victorias</option><option value="goles">Huerta y Gol · goles</option></select></label><button>Firmar acuerdo</button></form><div id="ads-status"></div>`),panel('club-ledger','Balance de cada partido','<p>Ingresos y gastos separados para saber qué decisiones funcionan.</p><div class="table-wrap"><table><thead><tr><th>Jornada</th><th>Asistencia</th><th>Entradas</th><th>Servicios</th><th>Publicidad</th><th>Salarios</th><th>Empleados</th><th>Primas</th><th>Mantenimiento</th><th>Operación</th><th>Premios</th><th>Neto</th></tr></thead><tbody id="club-ledger-rows"></tbody></table></div>'));
 stadium.append(panel('club-ground','Tu estadio, grada por grada',`<svg id="stadium-plan" viewBox="0 0 600 300" role="img" aria-label="Gradas y obras del estadio"></svg><p>Ampliar una grada añade 1.000 localidades. Cuesta 250.000 € y tarda dos jornadas oficiales. El aforo aumenta al terminar.</p><form id="stand-form"><label>Grada<select id="stand-sector"><option value="norte">Norte</option><option value="sur">Sur</option><option value="este">Este</option><option value="oeste">Oeste</option></select></label><button>Ampliar · 250.000 €</button></form><div id="stadium-works"></div>`),panel('club-services','Servicios del estadio',`<p>Comida, tienda y parking generan ingresos por asistente. El transporte aumenta la demanda. Cada servicio tiene tres niveles; una mejora tarda dos jornadas.</p><div id="service-levels" class="club-metrics"></div><form id="service-form"><label>Servicio<select id="service-type"><option value="comida">Bares y puestos de comida</option><option value="tienda">Tiendas y merchandising</option><option value="parking">Parking</option><option value="transporte">Transporte público</option></select></label><button>Encargar mejora</button></form><p id="service-price" class="hint-box"></p>`));
 $('tab-entrenamiento').append(panel('club-staff','Empleados del club',`<p>Médico: reduce fatiga y, desde nivel 2, una jornada adicional de lesión. Psicólogo: recupera moral. Entrenador de cantera: acelera el desarrollo. Comercial: mejora la recaudación un 3 % por nivel.</p><div id="staff-current"></div><form id="staff-form"><label>Puesto<select id="staff-role"><option value="medico">Médico</option><option value="psicologo">Psicólogo</option><option value="cantera">Entrenador de cantera</option><option value="comercial">Director comercial</option></select></label><label>Nivel<select id="staff-level"><option value="0">Sin empleado</option><option value="1">1 · 2.000 €/jornada</option><option value="2">2 · 6.000 €/jornada</option><option value="3">3 · 12.000 €/jornada</option></select></label><button>Contratar o cambiar nivel</button></form><p>Alta: 20.000 € por nivel que se sube. Bajar nivel no devuelve el alta.</p>`));
 $('tab-tactica').append(panel('club-youth','Cantera y promesas',`<p>Ojea futbolistas ficticios de 17–18 años y promociona a quienes necesites. La escuela y el filial comparten 24 plazas de desarrollo, con un máximo de 12 en cada grupo; el primer equipo admite 25.</p><button id="scout-youth" type="button">Ojear promesa · 10.000 €</button><div class="table-wrap"><table><thead><tr><th>Jugador</th><th>Edad</th><th>Pos</th><th>Media</th><th>Potencial</th><th>Salario/j</th><th>Acción</th></tr></thead><tbody id="youth-rows"></tbody></table></div>`),panel('club-evolution','Evolución y relevos generacionales','<p>Menores de 25: hasta +3 de media por temporada si juegan al menos el 55 % de las jornadas. Desde los 31 años hay desgaste; los porteros empiezan a los 34. Retirada entre 35 y 40 según su perfil. El relevo conserva el potencial y perfil original, pero comienza con habilidad y salario de promesa.</p><p id="youth-threshold"></p><div id="career-news"></div>'));
 $('tab-mercado').append(panel('club-contracts','Ficha del jugador y negociación',`<label>Jugador<select id="contract-player" aria-label="Jugador para consultar o negociar"></select></label><div id="player-dossier"></div><form id="contract-form"><label>Traspaso al club (€)<input id="offer-fee" type="number" min="0" value="0"></label><label>Salario por jornada (€)<input id="offer-wage" type="number" min="100" value="1000"></label><label>Temporadas<input id="offer-years" type="number" min="1" max="5" value="3"></label><label>Cláusula (€)<input id="offer-release" type="number" min="0" value="1000000"></label><label>Prima por gol (€)<input id="offer-bonus" type="number" min="0" max="1000000" value="0"></label><button>Presentar oferta</button></form><p id="offer-response" role="status" aria-live="polite"></p><div class="club-actions"><button id="load-counter" type="button" disabled>Cargar contraoferta</button><button id="sign-contract" type="button" disabled>Firmar condiciones</button></div><p>Una cláusula por encima del triple del valor exige un 25 % más de sueldo. Una cláusula inferior al 65 % del valor permite que un rival pague y se lleve al jugador en el mercado.</p>`));
 $('tab-clasificacion').append(panel('club-messages','Noticias y avisos del club',feedback+'<div id="club-notices"></div>'));
 const detail=document.createElement('button');detail.id='roster-detail-toggle';detail.type='button';detail.textContent='Mostrar atributos';detail.setAttribute('aria-pressed','false');document.querySelector('.roster-controls').append(detail);
 detail.onclick=()=>{const show=document.body.classList.toggle('show-player-details');detail.textContent=show?'Vista resumida':'Mostrar atributos';detail.setAttribute('aria-pressed',String(show));window.dispatchEvent(new Event('resize'));};
 const mode=document.createElement('div');mode.className='club-match-mode';mode.innerHTML='<label>Cómo jugar<select id="club-match-mode"><option value="dirigir">Dirigir · decisiones y visionado 2D</option><option value="jugar">Jugar ocasiones 2D · teclado o táctil</option></select></label><button type="button" id="practice-arcade">Probar controles 2D</button><p class="hint-box">En modo jugable controlarás dos ataques clave del partido. Puedes moverte, pasar y disparar; sus goles cuentan en el marcador.</p>';
 const modePanel=panel('club-play-mode','Cómo jugar y práctica 2D','');modePanel.append(mode);document.querySelector('.match-board').before(modePanel);
 const mentality=panel('club-live-orders','Órdenes durante el partido','<label>Mentalidad: <strong id="mentality-label">Equilibrada · 50</strong><input id="club-mentality" type="range" min="0" max="100" value="50"></label><p>Defender reduce espacios; atacar adelanta las líneas y crea más peligro, pero expone la defensa.</p><button type="button" id="ask-goal">¡Pedir gol! · volcarse una vez</button><p id="live-order-feedback" role="status">La orden cambia el ataque y la defensa desde la siguiente jugada.</p>');
 document.querySelector('.match-board').after(mentality);
 const negotiate=document.createElement('button');negotiate.type='button';negotiate.id='open-negotiation';negotiate.textContent='Negociar sueldo y cláusula';$('swipe-card').append(negotiate);
 negotiate.onclick=()=>{const j=estadoJuego.mercado[0];if(!j)return;$('contract-player').value='mercado:'+j.jugador_id;dossier();window.abrirPantallaJuego?.('contract-player');};
 let response=null;
 function action(fn){try{if(partidoEnCurso)throw Error('Termina el partido antes de realizar operaciones del club. Las órdenes tácticas sí están disponibles.');const result=fn();guardarPartidaLocal(false);actualizarUI();notify(typeof result==='string'?result:'Operación realizada.');}catch(e){notify(e.message,true);}}
 function notify(text,error=false){const n=$('club-feedback');n.textContent=text;n.dataset.error=String(error);window.abrirPantallaJuego?.('club-feedback');}
 function selection(){const value=$('contract-player').value,renew=value.startsWith('propio:');const id=value.slice(value.indexOf(':')+1);return {id,renew,j:(renew?obtenerMiEquipo().plantilla:estadoJuego.mercado).find(j=>j.jugador_id===id)};}
 function formOffer(){return {precio:Number($('offer-fee').value),salario:Number($('offer-wage').value),anos:Number($('offer-years').value),clausula:Number($('offer-release').value),primaGol:Number($('offer-bonus').value)};}
 function setOffer(o){[['offer-fee','precio'],['offer-wage','salario'],['offer-years','anos'],['offer-release','clausula'],['offer-bonus','primaGol']].forEach(([id,k])=>$(id).value=o[k]);}
 function dossier(reset=true){
  const {j,renew}=selection();if(!j){$('player-dossier').textContent='No hay jugadores disponibles.';return;}
  $('player-dossier').innerHTML=`<div class="dossier-heading">${avatarJugadorHTML(j.nombre,j.posicion)}<div><h3>${esc(j.nombre)}</h3><p>${j.edad} años · ${j.posicion} · ${renew?'Tu plantilla':'Mercado'}</p></div><strong class="overall">${Math.round(j.media)}<small>MEDIA</small></strong></div><div class="dossier-values"><p>Potencial: ${j.desarrollo.potencial}/100</p><p>Contrato: ${j.contrato.anos} temporadas</p><p>Sueldo: ${money(j.salario)}/j</p><p>Cláusula: ${money(j.contrato.clausula)}</p><p>Partidos: ${j.desarrollo.partidos} · Minutos: ${j.desarrollo.minutos}</p></div><p class="hint-box">${j.contrato.clausula<j.precio*.65?'Cláusula vulnerable: un rival puede llevárselo pagando esa cantidad.':'Renueva para ajustar sueldo, años, primas y cláusula.'}</p>`;
  if(reset){setOffer({precio:renew?0:j.precio,salario:j.salario,anos:3,clausula:j.contrato.clausula,primaGol:j.contrato.primaGol});response=null;$('offer-response').textContent='Presenta una propuesta para recibir respuesta inmediata.';$('sign-contract').disabled=true;$('load-counter').disabled=true;}
 }
 function syncMarket(){
  const retired=new Set([...estadoJuego.carrera.retirados.map(j=>j.id),...estadoJuego.carrera.bajasBase]),own=new Set(obtenerMiEquipo().plantilla.map(j=>j.jugador_id));
  estadoJuego.mercado=estadoJuego.mercado.filter(j=>!retired.has(j.jugador_id)&&!own.has(j.jugador_id));
  estadoJuego.mercado=estadoJuego.mercado.map(j=>{
   const actual=estadoJuego.equipos.flatMap(e=>e.plantilla).find(p=>p.jugador_id===j.jugador_id);
   if(actual&&actual!==j){for(const k of ['media','edad','precio','salario','moral','cansancio','lesionado','goles','xg'])j[k]=actual[k];j.atributos={...actual.atributos};j.contrato={...actual.contrato};j.desarrollo={...actual.desarrollo,baseAtributos:{...actual.desarrollo.baseAtributos}};}
   return j;
  });
  estadoJuego.mercado.forEach(j=>{if(!j.desarrollo)M.normalizar(estadoJuego);});
 }
 function render(){
  if(!estadoJuego?.carrera)return;syncMarket();const eq=obtenerMiEquipo(),g=eq.gestion;
  const fixture=estadoJuego.calendario[estadoJuego.jornadaActual]?.find(pair=>pair.includes(eq.nombre));
  const quote=M.estimarTaquilla(eq,estadoJuego.equipos.find(e=>e!==eq&&fixture?.includes(e.nombre)));
  $('ticket-preview').innerHTML=`<p>Aforo <strong>${eq.aforo.toLocaleString('es-ES')}</strong></p><p>Asistencia orientativa <strong>${quote.asistentes.toLocaleString('es-ES')}</strong></p><p>Recaudación orientativa <strong>${money(quote.total)}</strong></p>`;
  if(document.activeElement!==$('ticket-price'))$('ticket-price').value=g.entrada;if(document.activeElement!==$('season-price'))$('season-price').value=g.abono;
  $('season-ticket-status').textContent=`${g.abonados.toLocaleString('es-ES')} abonados. ${g.abonosTemporada===estadoJuego.temporada?'Campaña ya realizada.':'Disponible antes de la primera jornada.'}`;
  $('sell-season-tickets').disabled=estadoJuego.jornadaActual!==0||g.abonosTemporada===estadoJuego.temporada;
  $('ads-status').innerHTML=Object.entries(g.publicidad).map(([k,c])=>`<p>${k==='camiseta'?'Camiseta':'Vallas'}: ${c?esc(c.nombre)+' · '+c.tipo:'libre'}</p>`).join('');
  $('club-ledger-rows').innerHTML=g.balances.length?g.balances.map(b=>`<tr><td>T${b.temporada} · ${b.competicion==='copa'?'Copa R'+b.ronda:'J'+b.jornada}</td><td>${b.asistentes}</td>${['entradas','extras','publicidad','salarios','empleados','primas','mantenimiento','operacion','premios','neto'].map(k=>`<td>${money(b[k]||0)}</td>`).join('')}</tr>`).join(''):'<tr><td colspan="12">El balance aparecerá después del primer partido.</td></tr>';
  const rects={norte:[120,10,360,45],sur:[120,245,360,45],oeste:[10,65,100,170],este:[490,65,100,170]};
  $('stadium-plan').innerHTML='<rect x="120" y="65" width="360" height="170" rx="8" fill="#166534" stroke="#e2e8f0"/><path d="M300 65v170" stroke="white"/><circle cx="300" cy="150" r="32" fill="none" stroke="white"/>'+Object.entries(rects).map(([k,r])=>`<g><rect x="${r[0]}" y="${r[1]}" width="${r[2]}" height="${r[3]}" rx="6" fill="${g.obras.some(o=>o.objetivo===k)?'#a16207':'#1d4ed8'}"/><text x="${r[0]+r[2]/2}" y="${r[1]+r[3]/2-2}" text-anchor="middle" fill="white" font-size="13">${k.toUpperCase()}</text><text x="${r[0]+r[2]/2}" y="${r[1]+r[3]/2+14}" text-anchor="middle" fill="white" font-size="13">${g.gradas[k]}</text></g>`).join('');
  $('stadium-works').innerHTML=g.obras.length?g.obras.map(o=>`<p>🚧 ${o.objetivo}: ${o.restante} jornada(s) para terminar.</p>`).join(''):'<p>Sin obras pendientes.</p>';
  $('service-levels').innerHTML=Object.entries(g.servicios).map(([k,v])=>`<p>${k}: <strong>${v}/3</strong></p>`).join('');
  $('service-price').textContent='Coste del siguiente nivel: '+money(100000*(g.servicios[$('service-type').value]+1));
  $('staff-current').innerHTML=Object.entries(g.staff).map(([k,n])=>`<p>${({medico:'Médico',psicologo:'Psicólogo',cantera:'Cantera',comercial:'Comercial'})[k]}: nivel ${n}</p>`).join('')+`<p><strong>Nómina del staff: ${money(M.sueldoStaff(eq))}/jornada.</strong></p>`;
  $('youth-rows').innerHTML=g.cantera.filter(j=>!j.equipoB).map(j=>`<tr><td class="left">${esc(j.nombre)}</td><td>${j.edad}</td><td>${j.posicion}</td><td><strong>${Math.round(j.media)}</strong></td><td>${j.desarrollo.potencial}</td><td>${money(j.salario)}</td><td><button type="button" data-promote="${esc(j.jugador_id)}">Promocionar</button></td></tr>`).join('');
  $('youth-threshold').textContent=`Esta liga tiene ${estadoJuego.calendario.length} jornadas: se exigen ${Math.ceil(estadoJuego.calendario.length*.55)} partidos oficiales para progresar hasta +3.`;
  $('career-news').innerHTML=g.ultimoCierre.length?g.ultimoCierre.map(t=>'<p>'+esc(t)+'</p>').join(''):'<p>Al cerrar la temporada verás aquí las mejoras, el desgaste, las retiradas y los relevos.</p>';
  $('club-notices').innerHTML=estadoJuego.carrera.noticias.slice(0,12).map(t=>'<p>'+esc(t)+'</p>').join('')||'<p>El club está listo para empezar.</p>';
  const select=$('contract-player'),previous=select.value,opts=[...eq.plantilla.map(j=>({value:'propio:'+j.jugador_id,label:'Renovar · '+j.nombre})),...estadoJuego.mercado.map(j=>({value:'mercado:'+j.jugador_id,label:'Fichar · '+j.nombre}))];
  if(JSON.stringify(opts.map(o=>o.value))!==select.dataset.options){select.replaceChildren(...opts.map(o=>new Option(o.label,o.value)));select.dataset.options=JSON.stringify(opts.map(o=>o.value));if(opts.some(o=>o.value===previous))select.value=previous;dossier();}else dossier(false);
  $('club-match-mode').value=estadoJuego.carrera.modoPartido;
  const mentalidad=estadoJuego.carrera.mentalidad??50;$('club-mentality').value=mentalidad;$('mentality-label').textContent=(mentalidad<35?'Defensiva':mentalidad>65?'Ofensiva':'Equilibrada')+' · '+mentalidad;
  $('ask-goal').disabled=!partidoEnCurso||Boolean(window.ldpMatchMods?.pedirGol);
 }
 actualizarUI=function(){if(estadoJuego){M.normalizar(estadoJuego);syncMarket();}ui();render();};
 const save=guardarPartidaLocal;
 guardarPartidaLocal=function(show=true){if(estadoJuego){M.normalizar(estadoJuego);syncMarket();}return save(show);};
 function form(id,fn){$(id).addEventListener('submit',e=>{e.preventDefault();action(fn);});}
 form('ticket-form',()=>{M.precios(obtenerMiEquipo(),Number($('ticket-price').value),Number($('season-price').value));return 'Precios actualizados. Consulta la asistencia orientativa en Finanzas.';});
 $('sell-season-tickets').onclick=()=>action(()=>`Campaña cerrada: ${money(M.abonos(estadoJuego,obtenerMiEquipo()))} ingresados.`);
 form('ads-form',()=>{M.publicidad(estadoJuego,obtenerMiEquipo(),$('ads-space').value,$('ads-type').value);return 'Patrocinio firmado hasta final de temporada.';});
 form('stand-form',()=>{M.obra(obtenerMiEquipo(),'grada',$('stand-sector').value,estadoJuego);return 'Ampliación encargada: '+obtenerMiEquipo().gestion.obras.at(-1).restante+' semanas.';});
 form('service-form',()=>{M.obra(obtenerMiEquipo(),'servicio',$('service-type').value,estadoJuego);return 'Servicio encargado: '+obtenerMiEquipo().gestion.obras.at(-1).restante+' semanas.';});
 $('service-type').onchange=render;
 $('ticket-form').addEventListener('input',()=>{
  const eq=obtenerMiEquipo(),entrada=Number($('ticket-price').value);if(entrada<5||entrada>120)return;
  const fixture=estadoJuego.calendario[estadoJuego.jornadaActual]?.find(pair=>pair.includes(eq.nombre));
  const rival=estadoJuego.equipos.find(e=>e!==eq&&fixture?.includes(e.nombre));
  const q=M.estimarTaquilla({...eq,gestion:{...eq.gestion,entrada}},rival);
  $('ticket-preview').innerHTML=`<p>Propuesta sin guardar: ${entrada} €</p><p>Asistencia orientativa <strong>${q.asistentes.toLocaleString('es-ES')}</strong></p><p>Recaudación orientativa <strong>${money(q.total)}</strong></p>`;
 });
 form('staff-form',()=>{M.contratarStaff(obtenerMiEquipo(),$('staff-role').value,Number($('staff-level').value));return 'Personal actualizado. Su nómina se descuenta en cada partido oficial.';});
 $('scout-youth').onclick=()=>action(()=>{const j=M.ojear(estadoJuego,obtenerMiEquipo());return `Ojeador: ${j.nombre}, ${j.edad} años, media ${j.media}, potencial ${j.desarrollo.potencial}.`;});
 $('youth-rows').onclick=e=>{const b=e.target.closest('[data-promote]');if(b)action(()=>{const j=M.promocionar(obtenerMiEquipo(),b.dataset.promote);convocarOnceAutomatico(obtenerMiEquipo());return `${j.nombre} ya pertenece al primer equipo.`;});};
 $('contract-player').onchange=()=>dossier();
 $('contract-form').onsubmit=e=>{e.preventDefault();try{const {j,renew}=selection();response=M.evaluarOferta(estadoJuego,obtenerMiEquipo(),j,formOffer(),renew);$('offer-response').textContent=response.texto;$('load-counter').disabled=response.estado!=='contraoferta';$('sign-contract').disabled=response.estado!=='aceptada';window.abrirPantallaJuego?.(response.estado==='aceptada'?'sign-contract':response.estado==='contraoferta'?'load-counter':'offer-response');}catch(e){$('offer-response').textContent=e.message;$('sign-contract').disabled=true;}};
 $('load-counter').onclick=()=>{if(response?.contra){setOffer(response.contra);$('offer-response').textContent='Contraoferta cargada. Preséntala para confirmar la respuesta.';$('sign-contract').disabled=true;window.abrirPantallaJuego?.('contract-form');}};
 $('contract-form').addEventListener('input',()=>{$('sign-contract').disabled=true;});
 $('sign-contract').onclick=()=>action(()=>{const {id,renew}=selection();M.firmar(estadoJuego,obtenerMiEquipo(),id,formOffer(),renew);estadoJuego.equipos.forEach(convocarOnceAutomatico);response=null;return 'Contrato firmado. Los nuevos importes ya están en la ficha y el presupuesto.';});
 $('club-match-mode').onchange=e=>{estadoJuego.carrera.modoPartido=e.target.value;guardarPartidaLocal(false);};
 $('practice-arcade').onclick=()=>window.jugarOcasion2D?.(true);
 $('club-mentality').oninput=e=>{const n=Number(e.target.value);estadoJuego.carrera.mentalidad=n;$('mentality-label').textContent=(n<35?'Defensiva':n>65?'Ofensiva':'Equilibrada')+' · '+n;guardarPartidaLocal(false);};
 $('ask-goal').onclick=()=>{const mods=window.ldpMatchMods;if(!partidoEnCurso||!mods||mods.pedirGol)return;mods.pedirGol=true;mods.attack+=10;mods.defense-=5;$('ask-goal').disabled=true;$('live-order-feedback').textContent='¡Todos arriba! +10 de ataque y −5 de defensa hasta el final. Aumenta el peligro; no garantiza gol.';};
 const fuerzas=calcularFuerzas;
 calcularFuerzas=function(eq){const f=fuerzas(eq);if(partidoEnCurso&&eq===obtenerMiEquipo()){
  const n=estadoJuego.carrera?.mentalidad??50;f.ataque=f.ataque*(.8+n*.004)+(window.ldpMatchMods?.attack||0);f.defensa=Math.max(1,f.defensa*(1.15-n*.003)+(window.ldpMatchMods?.defense||0));
 }return f;};
 window.ClubManager={
  liquidarPartido(local,vis,gL,gV){M.normalizar(estadoJuego);return M.liquidar(estadoJuego,local,vis,gL,gV).taquilla;},
  cerrarTemporada(){M.evolucionar(estadoJuego,estadoJuego.calendario.length);},
  mercado(){M.normalizar(estadoJuego);syncMarket();},
  finJornada(){
   const key=estadoJuego.temporada+':'+estadoJuego.jornadaActual;
   if(estadoJuego.ventanaMercadoAbierta&&estadoJuego.carrera.ultimoMercado!==key){M.clausulas(estadoJuego);estadoJuego.carrera.ultimoMercado=key;estadoJuego.equipos.forEach(convocarOnceAutomatico);}
  },
  render,
 };
})();
