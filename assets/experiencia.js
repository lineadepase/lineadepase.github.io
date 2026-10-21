(() => {
  'use strict';
  document.querySelectorAll('.goles-portada').forEach(details=>details.addEventListener('toggle',()=>{if(details.open)window.dispatchEvent(new Event('resize'));}));
  const nav = document.querySelector('.cabecera .nav');
  if (nav) {
    const narrow = matchMedia('(max-width: 1100px)');
    const button = document.createElement('button');
    button.type='button'; button.className='boton-menu'; button.textContent='Menú';
    nav.id ||= 'navegacion-principal'; button.setAttribute('aria-controls',nav.id); button.setAttribute('aria-expanded','false');
    nav.before(button);
    function close() { button.setAttribute('aria-expanded','false'); nav.hidden=narrow.matches; }
    button.addEventListener('click',()=>{ const open=button.getAttribute('aria-expanded')!=='true'; button.setAttribute('aria-expanded',String(open)); nav.hidden=!open; });
    nav.addEventListener('click',event=>{ if(event.target.closest('a')&&narrow.matches) close(); });
    document.addEventListener('keydown',event=>{ if(event.key==='Escape'&&narrow.matches&&button.getAttribute('aria-expanded')==='true'){ close(); button.focus(); } });
    document.addEventListener('click',event=>{ if(narrow.matches&&!event.target.closest('.cabecera')) close(); });
    narrow.addEventListener('change',close); close();
    document.documentElement.classList.add('menu-preparado');
  }

  function wrapText(context, value, width) {
    const lines=[];
    value.split(/\s+/).forEach(word=>{
      if(lines.length&&context.measureText(lines[lines.length-1]+' '+word).width<=width) lines[lines.length-1]+=' '+word;
      else lines.push(word);
    });
    return lines;
  }
  function loadImage(url) {
    return new Promise((resolve,reject)=>{ const image=new Image(); image.onload=()=>resolve(image); image.onerror=()=>reject(Error('No se ha podido cargar la imagen.')); image.src=url; });
  }
  async function graphImage(source) {
    if (source.tagName.toLowerCase()==='img') {
      const url=new URL(source.currentSrc||source.src,location.href);
      if(url.origin!==location.origin) throw Error('Solo se descargan los gráficos de esta web.');
      return {image:await loadImage(url.href)};
    }
    const copy=source.cloneNode(true), originals=[source,...source.querySelectorAll('*')], copies=[copy,...copy.querySelectorAll('*')];
    originals.forEach((element,index)=>{
      const style=getComputedStyle(element);
      ['fill','stroke','stroke-width','font-family','font-size','font-weight','opacity','text-anchor','dominant-baseline'].forEach(key=>copies[index].style.setProperty(key,style.getPropertyValue(key).replace(/url\(["']?[^)]*#([^"')]+)["']?\)/g,'url(#$1)')));
      if(source.id==='minutos-svg'&&element.classList.contains('gol')) copies[index].style.opacity='1';
    });
    const references = new Set([...copy.outerHTML.matchAll(/url\(["']?#([^"')]+)["']?\)/g)].map(match=>match[1]));
    const defs=document.createElementNS('http://www.w3.org/2000/svg','defs');
    references.forEach(id=>{ if(!copy.querySelector('[id="'+CSS.escape(id)+'"]')){ const definition=document.getElementById(id); if(definition) defs.append(definition.cloneNode(true)); } });
    copy.prepend(defs);
    copy.setAttribute('xmlns','http://www.w3.org/2000/svg');
    const box=source.getBoundingClientRect();
    const view=source.viewBox.baseVal;
    copy.setAttribute('width',view.width||box.width); copy.setAttribute('height',view.height||box.height);
    if(!view.width) copy.setAttribute('viewBox','0 0 '+box.width+' '+box.height);
    const url=URL.createObjectURL(new Blob([new XMLSerializer().serializeToString(copy)],{type:'image/svg+xml;charset=utf-8'}));
    try { return {image:await loadImage(url),revoke:()=>URL.revokeObjectURL(url)}; }
    catch(error){ URL.revokeObjectURL(url); throw error; }
  }
  document.querySelectorAll('.grafico,figure.figura,#minutos').forEach(holder=>{
    const timeline=holder.id==='minutos';
    const dynamic=holder.classList.contains('grafico')||timeline;
    const image=dynamic?null:holder.querySelector('img');
    if(!dynamic&&(!image||/foto|retrato|statsbomb/i.test(image.getAttribute('src')||''))) return;
    const button=document.createElement('button'); button.type='button';button.className='descargar-grafico';button.textContent='Descargar gráfico (PNG)';
    const status=document.createElement('span');status.className='estado-descarga';status.setAttribute('role','status');
    const parent=dynamic&&!timeline?holder.parentElement:holder;
    parent.append(button,status);
    button.addEventListener('click',async()=>{
      let loaded;
      try {
        button.disabled=true;status.textContent='Preparando la imagen…';
        const source=dynamic?holder.querySelector('svg'):image;
        if(!source) throw Error('El gráfico aún no está disponible. Espera a que termine de cargar.');
        loaded=await graphImage(source);
        const title=((dynamic?parent.querySelector('h3,h2')?.textContent:holder.querySelector('figcaption')?.textContent||image.alt)||document.querySelector('h1').textContent).split(/\. (?:Elaboración|Fuente)/)[0];
        let meta=document.querySelector('meta[name="grafico-contexto"]')?.content||'Consulta las fuentes y el periodo en el análisis original.';
        const filter=dynamic?document.querySelector('[data-sede][aria-pressed="true"]'):null;
        if(filter) meta+=' · Sede: '+filter.textContent.trim()+'.';
        const note=dynamic?parent.querySelector(':scope > .nota')?.textContent:null;
        if(note) meta+=' '+note.trim();
        const legend=dynamic?[...parent.querySelectorAll('.leyenda span,.leyenda-min span')].map(item=>({label:item.textContent.trim(),color:getComputedStyle(item.querySelector('i')||item).backgroundColor,split:!!item.querySelector('.zgz-mitad')})):[];
        const canvas=document.createElement('canvas');const context=canvas.getContext('2d');
        const width=Math.max(1000,Math.min(1800,loaded.image.naturalWidth||1200));
        context.font='bold 30px Arial'; const titleLines=wrapText(context,title.trim(),width-96);
        context.font='20px Arial'; const sourceLines=wrapText(context,meta,width-96);
        const top=50+titleLines.length*38+(legend.length?40:0), chartHeight=Math.round((width-64)*loaded.image.naturalHeight/loaded.image.naturalWidth);
        const footer=112+sourceLines.length*28;
        canvas.width=width;canvas.height=top+chartHeight+footer;
        context.fillStyle='#ffffff';context.fillRect(0,0,width,canvas.height);
        context.fillStyle='#112b1d';context.font='bold 30px Arial';titleLines.forEach((line,i)=>context.fillText(line,48,44+i*38));
        let legendX=48;context.font='20px Arial';legend.forEach(item=>{context.fillStyle=item.split?'#213e96':item.color;context.fillRect(legendX,top-32,18,18);if(item.split){context.fillStyle='#ffffff';context.fillRect(legendX+9,top-32,9,18);context.strokeStyle='#213e96';context.strokeRect(legendX,top-32,18,18);}context.fillStyle='#112b1d';context.fillText(item.label,legendX+28,top-16);legendX+=context.measureText(item.label).width+70;});
        context.fillStyle=timeline?'#0f3d25':getComputedStyle(document.documentElement).getPropertyValue('--panel').trim()||'#ffffff';context.fillRect(32,top,width-64,chartHeight);
        context.drawImage(loaded.image,32,top,width-64,chartHeight);
        context.fillStyle='#4d6356';context.font='20px Arial';sourceLines.forEach((line,i)=>context.fillText(line,48,top+chartHeight+42+i*28));
        context.fillStyle='#1f6b3e';context.font='bold 24px Arial';context.fillText('Línea de pase · lineadepase.com',48,canvas.height-32);
        const blob=await new Promise((resolve,reject)=>canvas.toBlob(value=>value?resolve(value):reject(Error('No se ha podido preparar el PNG.')),'image/png'));
        const url=URL.createObjectURL(blob), link=document.createElement('a');link.href=url;
        link.download='linea-de-pase-'+title.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,'-').slice(0,80)+'.png';
        link.click();setTimeout(()=>URL.revokeObjectURL(url),30000);
        status.textContent='Imagen preparada con título, periodo, fuente y marca.';
      } catch(error) { status.textContent=error.message||'No se ha podido descargar el gráfico.'; }
      finally { loaded?.revoke?.();button.disabled=false; }
    });
  });
})();
