/* Pantallas con páginas reales: no se recorta información ni se clona el estado.
 * Los nodos originales conservan eventos, identificadores y formularios. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const sections = new Map();
  let currentSection = 'clasificacion', pages = [], pageIndex = 0, scheduled = 0, ready = false;
  let observer;
  function addTab(id, label) {
    const button = document.createElement('button');
    button.id = `pestana-${id}`; button.className = 'tab-btn'; button.type = 'button';
    button.setAttribute('role','tab'); button.setAttribute('aria-controls',`tab-${id}`);
    button.setAttribute('aria-selected','false'); button.tabIndex = -1; button.textContent = label;
    button.onclick = () => cambiarPestana(id, button);
    document.querySelector('nav').append(button);
  }
  function makeView(section, node, title) {
    const view = document.createElement('div'); view.className = 'screen-view';
    view.dataset.title = title; view.hidden = true;
    node.parentNode.insertBefore(view,node); view.append(node);
    sections.get(section).views.push(view);
  }
  function titleFor(node, index) {
    return node.getAttribute('aria-label') || node.querySelector('.panel-title,h2,h3,summary')?.textContent.trim() || `Opciones ${index+1}`;
  }
  function observe() {
    observer.observe(document.querySelector('main'),{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:['hidden','open','class']});
  }
  function requestLayout() {
    if (!ready || scheduled) return;
    scheduled = requestAnimationFrame(() => { scheduled = 0; layout(); });
  }
  function selectView(index, focus = false) {
    const state = sections.get(currentSection);
    state.index = Number(index); pageIndex = 0;
    $('screen-view').value = String(state.index);
    layout();
    if (focus) $('screen-heading').focus({preventScroll:true});
  }
  function showSection(id) {
    if (!sections.has(id)) return;
    currentSection = id; pageIndex = 0;
    const state = sections.get(id), select = $('screen-view');
    select.replaceChildren(...state.views.map((view,i) => new Option(view.dataset.title,String(i))));
    select.value = String(state.index);
    $('screen-section').textContent = $('pestana-'+id).textContent;
    layout();
  }
  // Se puede llevar una acción directamente a su pantalla, sin scrollIntoView.
  window.abrirPantallaJuego = id => {
    const node = $(id), view = node?.closest('.screen-view');
    if (!view) return;
    const section = view.closest('.tab-content').id.replace('tab-','');
    cambiarPestana(section,$('pestana-'+section));
    selectView(sections.get(section).views.indexOf(view));
    const target=$(id);
    const page=pages.findIndex(items=>items.some(item=>item===target||item.contains(target)||target.contains(item)));
    if(page>=0){pageIndex=page;layout();}
  };
  function layout() {
    if (!ready) return;
    observer.disconnect();
    const state = sections.get(currentSection);
    if(state.views[state.index].firstElementChild?.hidden && state.views.length>1){
      state.index=(state.index+1)%state.views.length;pageIndex=0;$('screen-view').value=String(state.index);
    }
    for (const [id,data] of sections) data.views.forEach((view,i) => {view.hidden = id !== currentSection || i !== state.index;});
    const root = state.views[state.index];
    root.querySelectorAll('.page-away').forEach(n => n.classList.remove('page-away'));
    root.querySelectorAll('.flow-split').forEach(n => n.classList.remove('flow-split'));
    root.querySelectorAll('table').forEach(table => {
      const labels = [...table.querySelectorAll('thead th')].map(n => n.textContent.trim());
      table.querySelectorAll('tbody tr').forEach(row => [...row.children].forEach((cell,i) => { if(cell.dataset.label !== labels[i]) cell.dataset.label = labels[i] || ''; }));
    });
    const limit = Math.max(80,root.clientHeight - 8);
    root.style.setProperty('--pitch-height',`${Math.max(80,limit-100)}px`);
    const units = [], branches = [];
    function divide(node) {
      if (!(node instanceof Element) || node.hidden || getComputedStyle(node).display === 'none') return;
      if(node.getBoundingClientRect().height>limit-32&&node.children.length&&!node.matches('button,select,svg,canvas,input,label,.reading-fragment')){
        [...node.childNodes].filter(n=>n.nodeType===Node.TEXT_NODE&&n.textContent.trim()).forEach(text=>{
          const span=document.createElement('span');span.className='reading-fragment';text.replaceWith(span);span.append(text);
        });
      }
      const children = [...node.children].filter(n => n instanceof Element && !n.hidden && getComputedStyle(n).display !== 'none');
      if ((node.getBoundingClientRect().height > limit - 32 || node.matches('.panel,.match-board,.swipe-card')) && children.length && !node.matches('button,select,svg,canvas,input')) {
        node.classList.add('flow-split'); branches.push(node); children.forEach(divide);
      } else units.push(node);
    }
    [...root.children].forEach(divide);
    const candidates = [...units,...branches];
    function paint(items) {
      const visible = new Set();
      items.forEach(item => {for(let n=item;n && n!==root;n=n.parentElement) visible.add(n);});
      candidates.forEach(n => n.classList.toggle('page-away',!visible.has(n)));
    }
    // Si un bloque aislado tampoco cabe, se divide de nuevo contando el espacio
    // de todos sus antecesores. Así también funciona con zoom y en pantallas bajas.
    const queue=[...units], fitted=[];
    while(queue.length){
      const unit=queue.shift(); paint([unit]);
      if(root.scrollHeight>root.clientHeight+1 && unit.matches('p,li,span') && unit.textContent.length>45 && !unit.querySelector('button,a,input,select')){
        const words=unit.textContent.split(/\s+/),fragments=[];let text='';
        words.forEach(word=>{if(text.length+word.length>40){fragments.push(text+' ');text='';}text+=word+' ';});
        if(text)fragments.push(text);
        unit.replaceChildren(...fragments.map(text=>{const span=document.createElement('span');span.className='reading-fragment';span.textContent=text;return span;}));
      }
      const children=[...unit.children].filter(n=>!n.hidden&&getComputedStyle(n).display!=='none');
      if(root.scrollHeight>root.clientHeight+1&&children.length&&!unit.matches('button,select,svg,canvas,input,label')){
        unit.classList.add('flow-split');branches.push(unit);candidates.push(...children);queue.unshift(...children);
      }else fitted.push(unit);
    }
    // Medimos la disposición real, incluidas tablas, márgenes y texto envuelto.
    pages = []; let batch = [];
    for (const unit of fitted) {
      batch.push(unit); paint(batch);
      if (root.scrollHeight > root.clientHeight + 1 && batch.length > 1) {
        batch.pop(); pages.push(batch); batch = [unit];
      }
    }
    if(batch.length) pages.push(batch);
    if(!pages.length) pages = [[]];
    pageIndex = Math.min(pageIndex,pages.length-1); paint(pages[pageIndex]);
    const rows=[...new Set(pages[pageIndex].map(n=>n.closest('tr')).filter(Boolean))];
    const person=rows.length===1?rows[0].querySelector('[data-label="Jugador"],[data-label="Equipo"]')?.textContent.trim():'';
    $('screen-view').selectedOptions[0].textContent=root.dataset.title+(person?' · '+person:'');
    $('screen-page').textContent = `Página ${pageIndex+1} de ${pages.length}`;
    $('screen-previous').disabled = pageIndex === 0; $('screen-next').disabled = pageIndex === pages.length-1;
    $('screen-heading').textContent = root.dataset.title;
    root.dataset.pageCount = String(pages.length);
    observe();
  }
  async function initialize() {
    // onload carga las plantillas de forma asíncrona; no sustituimos su arranque.
    if (!estadoJuego) { setTimeout(initialize,50); return; }
    document.body.classList.add('screen-mode');
    addTab('entrenamiento','🏋️ Entrenador'); addTab('ajustes','⚙️ Ajustes y ayuda');
    $('pestana-tactica').textContent='📋 Plantilla · Táctica';
    $('pestana-mercado').textContent='🔎 Secretaría · Fichajes';
    const nav=document.querySelector('nav');
    ['clasificacion','tactica','mercado','entrenamiento','partido','finanzas','estadio','ajustes'].forEach(id=>{const b=$('pestana-'+id);if(b)nav.append(b);});
    const settings = document.createElement('section'); settings.id='tab-ajustes'; settings.className='tab-content';
    settings.setAttribute('role','tabpanel'); settings.setAttribute('aria-labelledby','pestana-ajustes'); settings.setAttribute('aria-hidden','true');
    const settingsPanel=document.createElement('div'); settingsPanel.className='panel';
    settingsPanel.innerHTML='<h2>Tu carrera y tus copias</h2><p class="hint-box">Guarda en este navegador o exporta una copia para recuperarla en otro dispositivo.</p>';
    const stats=document.querySelector('.top-stats');
    [...stats.querySelectorAll('button,input,#estado-guardado')].forEach(n=>settingsPanel.append(n));
    settingsPanel.append($('lbl-salarios').closest('.stat-pill'));
    settings.append(settingsPanel,$('guia-rapida'),document.querySelector('.sim-disclaimer'));
    document.querySelector('main').append(settings);
    $('guia-rapida').open=true;
    const tools=document.createElement('div'); tools.className='screen-tools';
    tools.innerHTML='<label>Ver <select id="screen-view" aria-label="Pantalla de esta sección"></select></label><span id="screen-section" class="screen-badge"></span>';
    document.querySelector('main').prepend(tools);
    const heading=document.createElement('h2'); heading.id='screen-heading'; heading.tabIndex=-1;
    heading.className='sr-only'; heading.style.cssText='position:absolute;width:1px;height:1px;clip-path:inset(50%);overflow:hidden';
    tools.append(heading);
    const footer=document.createElement('footer'); footer.className='screen-footer';
    footer.innerHTML='<div class="page-controls" aria-label="Páginas de información"><button id="screen-previous" type="button">← Anterior</button><span id="screen-page" role="status" aria-live="polite"></span><button id="screen-next" type="button">Siguiente →</button></div>';
    footer.append($('floating-cta')); document.body.append(footer);
    // Accesos directos a lo que antes quedaba al final de un panel largo.
    const calendar=document.createElement('div');calendar.id='club-calendar';calendar.className='panel';
    $('reigns-panel').after(calendar);actualizarUI();
    const board=document.querySelector('.match-board');
    function matchPanel(title,nodes){
      const panel=document.createElement('div');panel.className='panel';
      const h=document.createElement('h2');h.textContent=title;h.className='panel-title';panel.append(h,...nodes.filter(Boolean));board.after(panel);
    }
    matchPanel('Poderes tácticos',[$('power-cards').previousElementSibling,$('power-cards'),$('power-feedback')]);
    matchPanel('Plan de partido y jugadas',[board.querySelector('.video-action-shortcuts'),board.querySelector('.match-quick-actions'),$('match-decision-feedback')]);
    const sponsors=document.createElement('div');sponsors.className='panel';
    const sponsorOptions=$('sponsor-options'),finance=sponsorOptions.closest('.panel');
    sponsors.append(sponsorOptions.previousElementSibling,sponsorOptions,$('sponsor-status'));finance.after(sponsors);
    if($('tab-finanzas'))$('tab-finanzas').append(finance,sponsors);
    // Cada panel importante obtiene un destino explícito; se mantienen sus nodos.
    document.querySelectorAll('main > .tab-content').forEach(section => {
      const id=section.id.replace('tab-',''); sections.set(id,{views:[],index:0});
      section.querySelectorAll('.grid-2,.tactics-layout,.training-layout').forEach(grid => grid.replaceWith(...grid.children));
      [...section.children].forEach((node,i) => makeView(id,node,titleFor(node,i)));
    });
    // El despacho se regenera al cambiar estado; su calendario se pagina junto a la decisión.
    const names={'primeros-pasos':'Primeros pasos','reigns-panel':'Decisiones y calendario','retos-mister':'Retos y recompensas','tbody-clasificacion':'Clasificación','tbody-historial-temporadas':'Archivo de temporadas','tbody-goleadores':'Goleadores','tbody-plantilla':'Alineación y jugadores','canvas-pizarra':'Campo · cambios directos','canvas-match-live':'Partido en directo','tbody-mercado':'Lista de fichajes','tbody-ventas':'Vender jugadores','swipe-card':'Ojeador · fichar o pasar','sponsor-options':'Finanzas y patrocinadores','svg-pase':'Ejercicio táctico','pase-intentos':'Progreso de entrenamiento'};
    Object.entries(names).forEach(([id,title])=>{const view=$(id)?.closest('.screen-view');if(view)view.dataset.title=title;});
    const titles={'club-calendar':'Calendario de temporada','reigns-panel':'Decisiones del despacho','finance-budget':'Finanzas del club','sponsor-options':'Patrocinadores','match-log':'Crónica del partido','canvas-shotmap':'Estadísticas y balance','lbl-cartel-partido':'Previa y resultado','replay-heading':'Repeticiones','chiri-feed':'Noticias de la afición'};
    Object.entries(titles).forEach(([id,title])=>{$(id).closest('.screen-view').dataset.title=title;});
    document.querySelector('.sim-disclaimer').closest('.screen-view').dataset.title='Sobre la simulación';
    sections.get('mercado').index=sections.get('mercado').views.indexOf($('swipe-card').closest('.screen-view'));
    $('screen-view').onchange=e=>selectView(e.target.value,true);
    $('screen-previous').onclick=()=>{pageIndex--;layout();if(pageIndex===0)$('screen-next').focus({preventScroll:true});};
    $('screen-next').onclick=()=>{pageIndex++;layout();if(pageIndex===pages.length-1)$('screen-previous').focus({preventScroll:true});};
    const original=cambiarPestana;
    cambiarPestana=function(id,button){original(id,button);showSection(id);};
    observer=new MutationObserver(requestLayout); ready=true;
    window.addEventListener('resize',requestLayout); new ResizeObserver(requestLayout).observe(document.querySelector('main'));
    showSection('clasificacion');
    // Si ya se cerró la introducción, el despacho es el punto de entrada.
    if($('centro-control')) window.abrirPantallaJuego('centro-control');
    else if($('primeros-pasos').hidden) selectView(1);
  }
  initialize();
})();
