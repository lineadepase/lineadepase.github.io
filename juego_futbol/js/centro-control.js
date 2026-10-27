/* Resúmenes visuales calculados con los datos reales de la carrera. */
(() => {
 'use strict';
 const $=id=>document.getElementById(id),esc=s=>escaparHTML(String(s));
 const euros=n=>Math.round(n).toLocaleString('es-ES')+' €';
 const panel=document.createElement('section');panel.id='centro-control';panel.className='panel control-panel';
 panel.innerHTML='<h2 class="panel-title">Centro de control</h2><div id="control-metrics" class="control-metrics"></div><div id="control-next" class="control-next"></div><div id="control-alerts" class="control-alerts"></div><div class="control-shortcuts" aria-label="Accesos directos">'+[['tbody-plantilla','📋','Alineación'],['canvas-pizarra','⚽','Campo táctico'],['club-calendar','🗓','Calendario'],['club-youth','🌱','Cantera'],['club-tickets','🎟','Entradas'],['club-ledger','📊','Balance']].map(([id,icon,name])=>`<button type="button" data-open="${id}"><span aria-hidden="true">${icon}</span>${name}<span aria-hidden="true">↗</span></button>`).join('')+'</div><div id="control-finance"></div>';
 $('tab-clasificacion').prepend(panel);
 const analysis=document.createElement('section');analysis.id='visual-player';analysis.className='panel control-panel';
 analysis.innerHTML='<h2 class="panel-title">Comparar futbolistas</h2><div class="compare-selects"><label>Jugador<select id="compare-first"></select></label><label>Comparar con<select id="compare-second"></select></label></div><div id="compare-summary"></div><button id="compare-contract" type="button">Abrir ficha y contrato →</button><div class="compare-visual"><div id="compare-graph"></div><div id="compare-bars"></div></div>';
 $('tab-tactica').append(analysis);
 const compareButton=document.createElement('button');compareButton.id='open-compare';compareButton.type='button';compareButton.textContent='Comparar jugadores';
 compareButton.onclick=()=>{const selected=obtenerMiEquipo().plantilla[jugadorSeleccionadoIdx];if(selected){$('compare-first').value=selected.jugador_id;compare();}window.abrirPantallaJuego?.('compare-first');};
 document.querySelector('.roster-controls').append(compareButton);
 document.addEventListener('click',e=>{const b=e.target.closest('[data-open]');if(b)window.abrirPantallaJuego?.(b.dataset.open);});
 const mean=xs=>xs.reduce((a,b)=>a+b,0)/Math.max(1,xs.length);
 const level=n=>n>=70?'good':n>=40?'warn':'bad';
 function meter(label,n){return `<div class="visual-meter ${level(n)}"><span>${esc(label)}</span><strong>${Math.round(n)}/100</strong><span class="meter-track" aria-hidden="true"><i style="width:${Math.max(0,Math.min(100,n))}%"></i></span></div>`;}
 let players=[];
 function compare(){
  const a=players.find(j=>j.jugador_id===$('compare-first').value),b=players.find(j=>j.jugador_id===$('compare-second').value);if(!a||!b)return;
  const attrs=[['RAS','Determinación'],['TOZ','Fuerza'],['CHI','Regate'],['RET','Pase'],['ALM','Resistencia']];
  $('compare-summary').innerHTML=`<p><span class="legend-a">● ${esc(a.nombre)}</span> · ${a.posicion} · Media ${Math.round(a.media)} · ${a.edad} años</p><p><span class="legend-b">◆ ${esc(b.nombre)}</span> · ${b.posicion} · Media ${Math.round(b.media)} · ${b.edad} años</p>`;
  const point=(i,v)=>{const t=i*Math.PI*2/5-Math.PI/2;return [160+Math.cos(t)*v,135+Math.sin(t)*v];};
  const polygon=v=>attrs.map((_,i)=>point(i,v)).map(p=>p.join(',')).join(' ');
  const shape=j=>attrs.map(([k],i)=>point(i,j.atributos[k])).map(p=>p.join(',')).join(' ');
  $('compare-graph').innerHTML=`<svg viewBox="0 0 320 275" role="img" aria-label="Comparación de cinco atributos. Valores exactos debajo.">${[25,50,75,100].map(v=>`<polygon points="${polygon(v)}" fill="none" stroke="#3b4967"/>`).join('')}<polygon points="${shape(a)}" fill="#34d39922" stroke="#34d399" stroke-width="3"/><polygon points="${shape(b)}" fill="#5ac8fa11" stroke="#5ac8fa" stroke-width="3" stroke-dasharray="6 3"/>${attrs.map(([,label],i)=>{const [x,y]=point(i,123);return `<text x="${x}" y="${y}" text-anchor="middle" fill="#d5def0" font-size="10">${label}</text>`;}).join('')}</svg>`;
  $('compare-bars').innerHTML=attrs.map(([k,label])=>`<div class="attribute-compare"><span>${label}</span><strong class="legend-a">${a.atributos[k]}</strong><span class="compare-track" aria-hidden="true"><i style="width:${a.atributos[k]}%"></i><b style="width:${b.atributos[k]}%"></b></span><strong class="legend-b">${b.atributos[k]}</strong></div>`).join('');
 }
 $('compare-first').onchange=compare;$('compare-second').onchange=compare;
 $('compare-contract').onclick=()=>{const id=$('compare-first').value,own=obtenerMiEquipo().plantilla.some(j=>j.jugador_id===id);$('contract-player').value=(own?'propio:':'mercado:')+id;$('contract-player').dispatchEvent(new Event('change'));window.abrirPantallaJuego?.('player-dossier');};
 function render(){
  if(!estadoJuego?.carrera)return;const eq=obtenerMiEquipo(),g=eq.gestion;
  const ready=eq.plantilla.filter(j=>!j.lesionado).length,condition=mean(eq.plantilla.map(j=>100-j.cansancio)),morale=mean(eq.plantilla.map(j=>j.moral));
  $('control-metrics').innerHTML=`<article><small>Presupuesto disponible</small><strong class="${eq.presupuesto<0?'legend-bad':''}">${euros(eq.presupuesto)}</strong><span>Nómina: ${euros(masaSalarial(eq)+ClubMotor.sueldoStaff(eq))}/j</span></article><article><small>Plantilla disponible</small><strong>${ready}<small> / ${eq.plantilla.length}</small></strong><span>${eq.plantilla.length-ready} lesionados · ${eq.plantilla.filter(j=>j.cansancio>=75).length} fatigados</span></article><article>${meter('Condición física',condition)}</article><article>${meter('Moral del equipo',morale)}</article>`;
  const fixture=estadoJuego.calendario[estadoJuego.jornadaActual]?.find(p=>p.includes(eq.nombre)),opponent=fixture?.find(n=>n!==eq.nombre),rival=estadoJuego.equipos.find(e=>e.nombre===opponent);
  $('control-next').innerHTML=fixture?`<div><small>SIGUIENTE PARTIDO · J${estadoJuego.jornadaActual+1}</small><h3>${esc(eq.nombre)} <span>vs</span> ${esc(opponent)}</h3><p>${fixture[0]===eq.nombre?'En casa':'Fuera de casa'} · Rival: ${esc(rival.formacion)} · ${esc(rival.estilo)}</p></div><button type="button" data-open="canvas-match-live">Preparar partido →</button>`:'<h3>Temporada completada · revisa el archivo y cierra la campaña con el botón principal.</h3>';
  const alerts=[];
  if(ready<11)alerts.push(['bad','No hay once jugadores disponibles','tbody-plantilla']);
  const tired=eq.plantilla.filter(j=>j.titular&&j.cansancio>=75).length;
  if(tired)alerts.push(['warn',`${tired} titulares necesitan descanso`,'btn-rotar-fatigados']);
  if(eq.presupuesto<0)alerts.push(['bad','Presupuesto en déficit: revisa el balance','club-ledger']);
  if(estadoJuego.mister?.despachoPendiente)alerts.push(['warn','Decisión de la directiva pendiente','dispatch-card']);
  if(g.obras.length)alerts.push(['warn',`${g.obras.length} obras en marcha`,'stadium-works']);
  if(!alerts.length)alerts.push(['good','Equipo listo · consulta la alineación','tbody-plantilla']);
  $('control-alerts').innerHTML=alerts.slice(0,3).map(([kind,text,target])=>`<button class="control-alert ${kind}" type="button" data-open="${target}">${kind==='good'?'✓':'!'} ${esc(text)} <span aria-hidden="true">→</span></button>`).join('');
  const balances=g.balances.slice(0,6).reverse(),max=Math.max(1,...balances.map(b=>Math.abs(b.neto)));
  $('control-finance').innerHTML='<h3>Resultado económico · últimos partidos</h3>'+(balances.length?'<div class="finance-bars">'+balances.map(b=>`<div><span>${b.competicion==='copa'?'Copa '+b.ronda:'J'+b.jornada}</span><span class="finance-track" aria-hidden="true"><i class="${b.neto<0?'negative':''}" style="width:${Math.abs(b.neto)/max*100}%"></i></span><strong>${euros(b.neto)}</strong></div>`).join('')+'</div>':'<p class="empty-data">Sin partidos liquidados. Aquí verás el beneficio o la pérdida real después de jugar.</p>');
  players=[...eq.plantilla,...estadoJuego.mercado];
  for(const id of ['compare-first','compare-second']){const select=$(id),previous=select.value;select.replaceChildren(...players.map(j=>new Option(j.nombre+' · '+j.posicion,j.jugador_id)));if(players.some(j=>j.jugador_id===previous))select.value=previous;else if(id==='compare-second')select.selectedIndex=Math.min(1,players.length-1);}
  compare();
  $('tbody-plantilla').querySelectorAll('tr').forEach((row,i)=>{const j=eq.plantilla[i];if(!j)return;for(const [label,n] of [['Cans',j.cansancio],['Moral',j.moral]]){const cell=row.querySelector(`[data-label="${label}"]`);if(cell){cell.classList.add('visual-cell');cell.style.setProperty('--meter-value',n+'%');cell.dataset.tone=label==='Cans'?(n>=75?'bad':n>=40?'warn':'good'):level(n);}}});
 }
 const ui=actualizarUI;actualizarUI=function(){ui();render();};
})();
