(() => {
  'use strict';
  const root = document.documentElement;
  if(document.head&&document.currentScript?.src){
    const passportStyle=document.createElement('link');passportStyle.rel='stylesheet';passportStyle.href=new URL('pasaporte-cifra.css?v=20261027a',document.currentScript.src).href;document.head.append(passportStyle);
  }
  const sistema = matchMedia('(prefers-color-scheme: dark)');
  const oscuro = () => root.dataset.theme ? root.dataset.theme === 'dark' : sistema.matches;
  const nav = document.querySelector('.nav');
  if (nav) {
    const label = document.createElement('label'); label.className = 'selector-tema';
    const texto = document.createElement('span'); texto.className = 'selector-texto'; texto.textContent = 'Tema'; label.append(texto);
    const select = document.createElement('select'); select.setAttribute('aria-label','Tema de la web');
    [['auto','Sistema'],['light','Claro'],['dark','Oscuro']].forEach(([value,text]) => select.add(new Option(text,value)));
    select.value = root.dataset.theme || 'auto'; label.append(select); nav.after(label);
    select.addEventListener('change', () => {
      if (select.value === 'auto') delete root.dataset.theme; else root.dataset.theme=select.value;
      try { if (select.value==='auto') localStorage.removeItem('lineadepase-tema'); else localStorage.setItem('lineadepase-tema',select.value); } catch (_) {}
      document.dispatchEvent(new Event('tema-cambiado'));
    });
    sistema.addEventListener('change', () => { if (!root.dataset.theme) document.dispatchEvent(new Event('tema-cambiado')); });
  }
  const main = document.querySelector('main');
  if (main) {
    main.id ||= 'contenido';
    const skip = document.createElement('a'); skip.href='#'+main.id; skip.className='saltar'; skip.textContent='Saltar al contenido'; document.body.prepend(skip);
  }
  const informe = document.querySelector('[data-informe]');
  if (informe) {
    const index = document.createElement('nav'); index.className='indice'; index.setAttribute('aria-label','Índice del informe');
    const title = document.createElement('p'); title.className='etiqueta'; title.textContent='En este informe';index.append(title);
    const list = document.createElement('ul');
    informe.querySelectorAll('h2').forEach((h,n) => {
      h.id ||= 'apartado-'+(n+1); const li=document.createElement('li'),a=document.createElement('a');a.href='#'+h.id;a.textContent=h.textContent;li.append(a);list.append(li);
    });
    index.append(list); informe.querySelector('.cab-proyecto').after(index);
  }
  document.querySelectorAll('.racha').forEach(racha => {
    const result=document.createElement('p'); result.className='detalle-racha';result.setAttribute('aria-live','polite');result.textContent='Selecciona un partido para ver el resultado.';racha.after(result);
    racha.querySelectorAll('[title]').forEach(span => {
      const b=document.createElement('button');b.type='button';b.className=span.className;b.textContent=span.textContent;
      const detalle=span.title;b.setAttribute('aria-label',detalle);b.setAttribute('aria-pressed','false');
      b.addEventListener('click',()=>{racha.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));result.textContent=detalle;});span.replaceWith(b);
    });
  });
  const dialog = document.createElement('dialog');dialog.className='ampliacion';dialog.setAttribute('aria-labelledby','titulo-ampliacion');
  dialog.innerHTML='<div class="barra-ampliacion"><h2 id="titulo-ampliacion"></h2><div class="controles-ampliacion"><button type="button" data-zoom="menos" aria-label="Reducir gráfico">−</button><output aria-label="Nivel de ampliación">100 %</output><button type="button" data-zoom="mas" aria-label="Ampliar gráfico">+</button><button type="button" data-cerrar autofocus>Cerrar</button></div></div><div class="zona-ampliacion"><div class="contenido-ampliacion"></div></div>';
  document.body.append(dialog);
  const contenido=dialog.querySelector('.contenido-ampliacion'),nivel=dialog.querySelector('output');let zoom=100,origin;
  function ajustar() { contenido.style.width=zoom+'%';nivel.textContent=zoom+' %';dialog.querySelector('[data-zoom="menos"]').disabled=zoom<=100;dialog.querySelector('[data-zoom="mas"]').disabled=zoom>=250; }
  dialog.querySelector('[data-cerrar]').addEventListener('click',()=>dialog.close());
  dialog.querySelector('[data-zoom="menos"]').addEventListener('click',()=>{zoom=Math.max(100,zoom-50);ajustar();});
  dialog.querySelector('[data-zoom="mas"]').addEventListener('click',()=>{zoom=Math.min(250,zoom+50);ajustar();});
  dialog.addEventListener('close',()=>{document.body.classList.remove('modal-abierto');origin?.focus();});
  dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
  function ampliar(source,title,button,tipo) {
    if (!source) return;
    origin=button;contenido.replaceChildren();const copy=source.cloneNode(true);
    copy.querySelectorAll('[id]').forEach(e=>e.removeAttribute('id'));copy.removeAttribute('id');
    if(copy.tagName.toLowerCase()==='svg') {
      // Los gráficos responsivos ya definen su sistema de coordenadas en viewBox.
      if (!copy.hasAttribute('viewBox')) {
        const width=source.width.baseVal.value,height=source.height.baseVal.value;
        if (width>0&&height>0) copy.setAttribute('viewBox',`0 0 ${width} ${height}`);
      }
      copy.removeAttribute('width');copy.removeAttribute('height');copy.querySelectorAll('[tabindex]').forEach(e=>e.removeAttribute('tabindex'));
      // La ampliación es una vista de lectura; los filtros siguen en el gráfico original.
      copy.querySelectorAll('[role="button"]').forEach(e=>e.removeAttribute('role'));
    }
    dialog.querySelector('[data-zoom="menos"]').setAttribute('aria-label','Reducir '+tipo);
    dialog.querySelector('[data-zoom="mas"]').setAttribute('aria-label','Ampliar '+tipo);
    copy.setAttribute('aria-label',title);contenido.append(copy);dialog.querySelector('h2').textContent=title;zoom=100;ajustar();document.body.classList.add('modal-abierto');dialog.showModal();
  }
  document.querySelectorAll('.grafico,.figura img').forEach(source => {
    const dynamic=source.classList.contains('grafico');const holder=dynamic?source.parentElement:source.closest('figure');
    const tipo=!dynamic&&holder.matches('.foto,.foto-cabecera,.retrato')?'imagen':'gráfico';
    const title=dynamic?holder.querySelector('h3').textContent:source.alt;
    const b=document.createElement('button');b.type='button';b.className='ampliar-grafico';b.textContent='Ampliar '+tipo;b.setAttribute('aria-label','Ampliar '+tipo+': '+title);
    b.addEventListener('click',()=>ampliar(dynamic?source.querySelector('svg'):source,title,b,tipo));holder.append(b);
  });
  const metricDefinitions={
    'posesión':'Porcentaje de posesión según el proveedor de la ficha. Describe el tiempo o las secuencias con balón; no mide por sí solo el peligro creado.',
    'tiros a puerta':'Remates que el proveedor considera dirigidos a portería. El criterio puede variar entre servicios.',
    'tiros dentro del área':'Remates clasificados dentro del área por el proveedor; no pondera ángulo, oposición ni calidad.',
    'tiros':'Recuento de remates según el proveedor. No informa por sí solo de su calidad; algunos desgloses de partido pueden no coincidir.',
    'goles esperados (xg)':'Suma de probabilidades estimadas de gol para los tiros. El modelo cambia entre proveedores y un dato ausente no equivale a cero.',
    'xg':'Suma de probabilidades estimadas de gol para los tiros. El modelo cambia entre proveedores y un dato ausente no equivale a cero.',
    'ocasiones claras':'Categoría del proveedor para ocasiones de alta probabilidad. No existe un umbral universal entre servicios.',
    'puntos acumulados':'Suma de puntos de las jornadas incluidas hasta el corte indicado.',
    'puntos':'Tres puntos por victoria, uno por empate y ninguno por derrota.',
    'goles':'Goles anotados en el partido según la ficha de resultado.',
  };
  const contextMeta=document.querySelector('meta[name="grafico-contexto"]')?.content||document.querySelector('.corte-visible')?.textContent||'';
  const matchContext=document.querySelector('.ficha-marcador .mp-cab span')?.textContent.trim()||'';
  function passport(container,title,description,sample){
    if(!container||container.querySelector(':scope > .pasaporte-cifra'))return;
    const key=title.trim().toLocaleLowerCase('es');
    const details=document.createElement('details');details.className='pasaporte-cifra';
    const summary=document.createElement('summary');summary.textContent='Contexto de la cifra';details.append(summary);
    const content=document.createElement('div');content.className='pasaporte-cifra-contenido';
    const definition=Object.entries(metricDefinitions).find(([name])=>key.includes(name))?.[1]||description||'La ficha muestra el valor y el criterio aplicados en este análisis.';
    const measure=document.createElement('p');measure.innerHTML='<strong>Qué mide.</strong> ';measure.append(document.createTextNode(definition));content.append(measure);
    if(sample){const sampleLine=document.createElement('p');sampleLine.innerHTML='<strong>Muestra.</strong> ';sampleLine.append(document.createTextNode(sample));content.append(sampleLine);}
    const owner=container.closest('.tarjeta,.kpi')||container.parentElement;
    const sourceNote=owner?.querySelector('.mp-pie a,.fuentes a')||document.querySelector('.ficha-marcador')&&document.querySelector('.mp-pie a');
    if(matchContext){const cutoff=document.createElement('p');cutoff.innerHTML='<strong>Partido.</strong> ';cutoff.append(document.createTextNode(matchContext));content.append(cutoff);}
    else if(contextMeta){const cutoff=document.createElement('p');cutoff.innerHTML='<strong>Corte y fuente.</strong> ';cutoff.append(document.createTextNode(contextMeta));content.append(cutoff);}
    if(sourceNote){const source=document.createElement('p');source.innerHTML='<strong>Ficha de origen.</strong> ';const link=sourceNote.cloneNode(true);link.textContent=sourceNote.textContent.trim();source.append(link);content.append(source);}
    else {const method=document.querySelector('a[href*="#fuentes-metodo"],a[href*="#metodo-grupo"],a[href*="#metodo"]');if(method){const source=document.createElement('p');const link=method.cloneNode(true);link.textContent='Método y cobertura';source.append(link);content.append(source);}}
    if((key.includes('tiros')||key==='tiros')&&window.location.pathname.endsWith('/jornada-9.html')){
      const review=document.createElement('p');const link=document.createElement('a');link.href='/datos-en-revision/#tiros-j9';link.textContent='Consultar la diferencia entre fuentes de la J9';review.append(link);content.append(review);
    }
    details.append(content);container.append(details);
  }
  document.querySelectorAll('.mp-stat').forEach(row=>{
    const label=row.querySelector('dt');if(!label)return;
    passport(row,label.textContent.trim(),'', 'Un partido.');
  });
  document.querySelectorAll('.kpi').forEach(kpi=>{
    const label=kpi.querySelector('span');if(!label)return;
    const sample=document.querySelector('.ficha-marcador')?'Un partido.':'Acumulado en el periodo que se indica en la página.';
    passport(kpi,label.textContent.trim(),'',sample);
  });
  document.querySelectorAll('.grafico').forEach(graph=>{
    const owner=graph.closest('.tarjeta')||graph.parentElement;
    const title=owner?.querySelector('h2,h3')?.textContent.trim();if(!title)return;
    const note=owner.querySelector('.lectura-grafico,.nota')?.textContent.trim()||'';
    const count=owner.textContent.match(/\bn\s*[=:]\s*([\d.,]+)/i)?.[1];
    const sample=count?'n = '+count+' en la muestra indicada.':'La muestra sigue la selección y los filtros descritos en esta página.';
    passport(owner,title,note,sample);
  });
  const corte=document.querySelector('[data-corte]');
  if(corte)fetch('../../datos/zaragoza.json').then(r=>{if(!r.ok)throw Error();return r.json();}).then(d=>{
    corte.textContent='Datos del análisis hasta el '+new Date(d.corte+'T12:00:00').toLocaleDateString('es-ES')+' · Jornada '+d.jornada;
  }).catch(()=>{});
})();

// La previa mantiene su enlace como archivo después de la hora del encuentro.
document.querySelectorAll('[data-previa-hasta]').forEach(card=>{
  const inicio=Date.parse(card.dataset.previaHasta);
  if(Number.isFinite(inicio)&&Date.now()>=inicio){
    card.querySelector('.etiqueta').textContent='La previa · Jornada 8';
    document.querySelectorAll('[data-link-previa]').forEach(a=>a.textContent='Previa: Murcia – Zaragoza');
    const link=card.querySelector('a');if(link)link.textContent='Leer el análisis previo →';
  }
});
