(() => {
  'use strict';
  const filterBox = document.querySelector('[data-filtros-archivo]');
  const seasonFilter = document.getElementById('archivo-temporada');
  const rivalFilter = document.getElementById('archivo-rival');
  const clearButton = document.querySelector('[data-limpiar-archivo]');
  const count = document.querySelector('[data-recuento-archivo]');
  const rows = [...document.querySelectorAll('.tabla-comparador tbody tr[data-jornada]')];
  const selectA = document.getElementById('comparar-jornada-a');
  const selectB = document.getElementById('comparar-jornada-b');
  const shareButton = document.querySelector('[data-compartir-comparacion]');
  const compareState = document.querySelector('[data-estado-comparacion]');
  const downloadControls = document.querySelector('[data-controles-descarga]');
  const formatSelect = document.getElementById('formato-comparacion');
  const metricsToggle = document.querySelector('[data-incluir-metricas]');
  const captionToggle = document.querySelector('[data-incluir-pie]');
  const storiesNote = document.querySelector('[data-aviso-stories]');
  const carouselNote = document.querySelector('[data-aviso-carrusel]');
  const carouselContextControls = document.querySelector('[data-controles-contexto-carrusel]');
  const carouselContextInput = document.getElementById('frase-carrusel');
  const carouselExamples = document.getElementById('ejemplos-frase-carrusel');
  const carouselContextCount = document.querySelector('[data-contador-frase-carrusel]');
  const carouselPreview = document.querySelector('[data-preview-carrusel]');
  const carouselPreviewImage = document.querySelector('[data-preview-carrusel-img]');
  const noHeaderToggle = document.querySelector('[data-sin-cabecera]');
  const brandToggle = document.querySelector('[data-mostrar-marca]');
  const individualDownloads = document.querySelector('[data-descargas-individuales]');
  const carouselDownloads = document.querySelector('[data-descargas-carrusel]');
  let carouselPreviewUrl = null;
  const rounds = new Map(rows.map(row => [row.dataset.comparisonId, row]));

  function syncFiltersToUrl() {
    const url = new URL(window.location.href);
    if (seasonFilter.value) url.searchParams.set('temporada', seasonFilter.value);
    else url.searchParams.delete('temporada');
    if (rivalFilter.value) url.searchParams.set('rival', rivalFilter.value);
    else url.searchParams.delete('rival');
    window.history.replaceState(null, '', url);
  }

  function updateFilters() {
    let visible = 0;
    rows.forEach(row => {
      const show = (!seasonFilter.value || row.dataset.temporada === seasonFilter.value)
        && (!rivalFilter.value || row.dataset.rival === rivalFilter.value);
      row.hidden = !show;
      if (show) visible += 1;
    });
    count.textContent = `${visible} ${visible === 1 ? 'jornada' : 'jornadas'}`;
    count.setAttribute('aria-live', 'polite');
    syncFiltersToUrl();
  }

  function appendText(parent, tag, className, value) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    element.textContent = value;
    parent.append(element);
    return element;
  }

  function renderCard(slot, row, includeMetrics) {
    const round = row.dataset.jornada.padStart(2, '0');
    const card = document.querySelector(`[data-panel-comparacion="${slot}"]`);
    card.replaceChildren();
    const image = document.createElement('img');
    image.src = `../assets/ilustraciones/archivo-jornadas/${row.dataset.assetStem}.png`;
    image.width = 1200;
    image.height = 630;
    image.loading = 'lazy';
    image.alt = `Marcador de J${round} ante ${row.dataset.rival}`;
    card.append(image);
    appendText(card, 'figcaption', '', `J${round} · ${row.dataset.rival} · ${row.dataset.fechaPartido} · ${row.dataset.temporada}`);
    if (includeMetrics && row.dataset.posesion) {
      appendText(card, 'p', 'comparacion-estadisticas', `Posesión ${row.dataset.posesion.replace('.', ',')} % · tiros ${row.dataset.tirosZaragoza}–${row.dataset.tirosRival}`);
    } else {
      appendText(card, 'p', 'comparacion-estadisticas', 'Las métricas aparecerán cuando ambas jornadas tengan ficha completa.');
    }
  }

  function updateComparison(changed) {
    if (!selectA || !selectB) return;
    if (selectA.value === selectB.value && rounds.size > 1) {
      const other = [...rounds.keys()].find(round => round !== (changed === 'a' ? selectA.value : selectB.value));
      if (changed === 'a') selectB.value = other;
      else selectA.value = other;
    }
    const rowA = rounds.get(selectA.value);
    const rowB = rounds.get(selectB.value);
    if (!rowA || !rowB) return;
    const includeMetrics = rowA.dataset.completa === '1' && rowB.dataset.completa === '1';
    if (metricsToggle) {
      metricsToggle.disabled = !includeMetrics;
      if (!includeMetrics) metricsToggle.checked = false;
    }
    renderCard('a', rowA, includeMetrics);
    renderCard('b', rowB, includeMetrics);
    if (changed) {
      const url = new URL(window.location.href);
      url.searchParams.set('jornada_a', selectA.value);
      url.searchParams.set('jornada_b', selectB.value);
      window.history.replaceState(null, '', url);
    }
    compareState.textContent = includeMetrics
      ? 'Las dos fichas tienen cobertura completa: se muestran posesión y tiros de cada jornada.'
      : 'Se comparan los marcadores. La cobertura no permite comparar métricas en las dos jornadas.';
    updateCarouselPreview();
  }

  function xml(value) {
    return String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[char]));
  }

  function comparisonSvg(rowA, rowB, format, includeMetrics, includeCaption, includeHeader, showBrand, singleRow = null, contextText = '') {
    const layouts = {
      apaisado: {width:1200,height:630,header:148,panels:[{x:54,y:190,w:528,h:365},{x:618,y:190,w:528,h:365}],titleSize:42,titleY:111,brandY:54,captionY:582,domainY:606},
      cuadrado: {width:1080,height:1080,header:180,panels:[{x:80,y:220,w:920,h:350},{x:80,y:610,w:920,h:350}],titleSize:40,titleY:128,brandY:65,captionY:1010,domainY:1056},
      vertical: {width:1080,height:1350,header:190,panels:[{x:80,y:235,w:920,h:465},{x:80,y:755,w:920,h:465}],titleSize:40,titleY:134,brandY:64,captionY:1258,domainY:1326},
      historias: {width:1080,height:1920,header:395,panels:[{x:80,y:430,w:920,h:430},{x:80,y:900,w:920,h:430}],titleSize:40,titleY:348,brandY:274,captionY:1500,domainY:1560},
      carrusel: {width:1080,height:1080,header:190,panels:[{x:80,y:260,w:920,h:540}],titleSize:40,titleY:130,brandY:66,captionY:930,domainY:1056,single:true}
    };
    const baseLayout = layouts[format] || layouts.apaisado;
    const panelShift = !includeHeader && format !== 'historias' ? Math.max(0, baseLayout.header - 105) : 0;
    const layout = {...baseLayout, header:includeHeader ? baseLayout.header : 0, panels:baseLayout.panels.map(panel => ({...panel,y:panel.y-panelShift}))};
    const displayRows = singleRow ? [singleRow] : [rowA, rowB];
    const cards = displayRows.map((row, index) => {
      const panel = layout.panels[index];
      const {x,y,w,h} = panel;
      const home = row.dataset.sede === 'Casa' ? 'Real Zaragoza' : row.dataset.rival;
      const away = row.dataset.sede === 'Casa' ? row.dataset.rival : 'Real Zaragoza';
      const homeGoals = row.dataset.sede === 'Casa' ? row.dataset.golesZaragoza : row.dataset.golesRival;
      const awayGoals = row.dataset.sede === 'Casa' ? row.dataset.golesRival : row.dataset.golesZaragoza;
      const round = row.dataset.jornada.padStart(2, '0');
      const seasonLabel = xml(row.dataset.temporada);
      const cardMetrics = includeMetrics && row.dataset.completa === '1';
      const metrics = cardMetrics
        ? `Posesión ${xml(row.dataset.posesion.replace('.', ','))}% · tiros ${xml(row.dataset.tirosZaragoza)}–${xml(row.dataset.tirosRival)}`
        : '';
      const center=x+w/2, pad=Math.min(32,w*.06), nameWidth=w*.38;
      const metaY=y+44, labelY=y+h*.34, namesY=y+h*.45, scoreY=y+h*.70, metricY=y+h-36;
      return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="22" fill="#fff" stroke="#d4ded6" stroke-width="2"/><path d="M${x} ${y+h-8}h${w}" stroke="#ff7a2f" stroke-width="8"/><text x="${x+pad}" y="${metaY}" fill="#536257" font-family="Arial,sans-serif" font-size="${w<600?19:23}" font-weight="700" letter-spacing="1.2">${seasonLabel} · J${round} · ${xml(row.dataset.fechaPartido)}</text><text x="${x+pad}" y="${labelY}" fill="#536257" font-family="Arial,sans-serif" font-size="${w<600?17:19}" font-weight="700">LOCAL</text><text x="${x+w-pad}" y="${labelY}" text-anchor="end" fill="#536257" font-family="Arial,sans-serif" font-size="${w<600?17:19}" font-weight="700">VISITANTE</text><text x="${x+pad}" y="${namesY}" fill="#163e28" font-family="Arial,sans-serif" font-size="${w<600?24:30}" font-weight="700" textLength="${nameWidth}" lengthAdjust="spacingAndGlyphs">${xml(home)}</text><text x="${x+w-pad}" y="${namesY}" text-anchor="end" fill="#163e28" font-family="Arial,sans-serif" font-size="${w<600?24:30}" font-weight="700" textLength="${nameWidth}" lengthAdjust="spacingAndGlyphs">${xml(away)}</text><text x="${center}" y="${scoreY}" text-anchor="middle" fill="#163e28" font-family="Arial,sans-serif" font-size="${w<600?78:92}" font-weight="800">${xml(homeGoals)} <tspan fill="#ff7a2f" font-size="${w<600?56:64}">–</tspan> ${xml(awayGoals)}</text>${metrics?`<text x="${center}" y="${metricY}" text-anchor="middle" fill="#536257" font-family="Arial,sans-serif" font-size="${w<600?17:19}">${metrics}</text>`:''}`;
    }).join('');
    const title = singleRow
      ? `Jornada ${singleRow.dataset.jornada} · ${singleRow.dataset.rival} · ${singleRow.dataset.temporada}`
      : `Comparativa J${rowA.dataset.jornada}–J${rowB.dataset.jornada} · ${rowA.dataset.temporada} / ${rowB.dataset.temporada}`;
    const homeAway = row => row.dataset.sede === 'Casa'
      ? {home:'Real Zaragoza',away:row.dataset.rival,homeGoals:row.dataset.golesZaragoza,awayGoals:row.dataset.golesRival}
      : {home:row.dataset.rival,away:'Real Zaragoza',homeGoals:row.dataset.golesRival,awayGoals:row.dataset.golesZaragoza};
    const scores=displayRows.map(row => ({row,score:homeAway(row)}));
    const caption=includeCaption
      ? `<text x="${layout.width/2}" y="${layout.captionY}" text-anchor="middle" fill="#536257" font-family="Arial,sans-serif" font-size="17" font-weight="700">Primera Federación · ${scores.map(({row,score})=>`J${row.dataset.jornada.padStart(2,'0')} ${score.homeGoals}–${score.awayGoals}`).join(' · ')}</text>`
      : '';
    const storiesDesc=format==='historias'?' La composición reserva espacio superior e inferior para no quedar debajo de los controles de las historias.':'';
    const brandY=baseLayout.brandY ?? 54;
    const contextY=includeHeader?baseLayout.titleY+38:Math.max(brandY+58,baseLayout.header-62);
    const header=`${includeHeader?`<path d="M0 0h${layout.width}v${baseLayout.header}H0z" fill="#103b24"/><path d="M0 ${baseLayout.header-5}h${layout.width}" stroke="#ff7a2f" stroke-width="7"/>`:''}${showBrand?`<text x="54" y="${brandY}" fill="${includeHeader?'#bed8c4':'#163e28'}" font-family="Arial,sans-serif" font-size="17" font-weight="700" letter-spacing="3">LÍNEA DE PASE · ARCHIVO VISUAL</text>`:''}${includeHeader?`<text x="54" y="${baseLayout.titleY}" fill="#f7f8f4" font-family="Arial,sans-serif" font-size="${baseLayout.titleSize}" font-weight="800">${singleRow?`J${singleRow.dataset.jornada.padStart(2,'0')} · ${xml(singleRow.dataset.rival)}`:'Dos jornadas, frente a frente'}</text>`:''}${singleRow&&contextText?`<text x="54" y="${contextY}" fill="${includeHeader?'#e0e9e2':'#536257'}" font-family="Arial,sans-serif" font-size="19" font-weight="600">${xml(contextText)}</text>`:''}`;
    const description = singleRow
      ? `Resultado del Real Zaragoza ante ${xml(singleRow.dataset.rival)}, temporada ${xml(singleRow.dataset.temporada)}.`
      : `Marcadores del Real Zaragoza frente a ${displayRows.map(row=>xml(row.dataset.rival)).join(' y ')}.`;
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${layout.width}" height="${layout.height}" viewBox="0 0 ${layout.width} ${layout.height}" role="img" aria-labelledby="titulo descripcion"><title id="titulo">${xml(title)}</title><desc id="descripcion">${description} La posesión y los tiros se incluyen solo si se seleccionan y las dos fichas están completas.${xml(storiesDesc)}</desc><rect width="${layout.width}" height="${layout.height}" fill="#f3f5ef"/>${header}${cards}${caption}${showBrand?`<text x="${layout.width-50}" y="${layout.domainY}" text-anchor="end" fill="#64766b" font-family="Arial,sans-serif" font-size="15">lineadepase.com</text>`:''}</svg>`;
  }

  function updateCarouselPreview() {
    const active = formatSelect?.value === 'carrusel';
    if (carouselContextControls) carouselContextControls.hidden = !active;
    if (carouselPreview) carouselPreview.hidden = !active;
    if (!active) {
      if (carouselPreviewUrl) URL.revokeObjectURL(carouselPreviewUrl);
      carouselPreviewUrl = null;
      return;
    }
    const rowA = rounds.get(selectA?.value);
    const rowB = rounds.get(selectB?.value);
    if (!rowA || !rowB || !carouselPreviewImage) return;
    if (carouselContextInput && carouselContextInput.value.length > 72) carouselContextInput.value = carouselContextInput.value.slice(0,72);
    if (carouselContextCount && carouselContextInput) carouselContextCount.textContent = `${carouselContextInput.value.length}/72 caracteres`;
    const metrics = rowA.dataset.completa === '1' && rowB.dataset.completa === '1' && Boolean(metricsToggle?.checked);
    const svg = comparisonSvg(rowA,rowB,'carrusel',metrics,Boolean(captionToggle?.checked),!Boolean(noHeaderToggle?.checked),Boolean(brandToggle?.checked),rowA,carouselContextInput?.value.trim().slice(0,72) || '');
    const oldUrl=carouselPreviewUrl, nextUrl=URL.createObjectURL(new Blob([svg],{type:'image/svg+xml;charset=utf-8'}));
    carouselPreviewUrl=nextUrl;
    carouselPreviewImage.onload=()=>{if(oldUrl)URL.revokeObjectURL(oldUrl);carouselPreviewImage.onload=null;};
    carouselPreviewImage.onerror=()=>{if(oldUrl)URL.revokeObjectURL(oldUrl);carouselPreviewImage.onerror=null;};
    carouselPreviewImage.src=nextUrl;
  }

  function saveBlob(blob, filename) {
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.href = url;
    link.download = filename;
    document.body.append(link);
    link.click();
    link.remove();
    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  function zipStored(files) {
    const encoder = new TextEncoder();
    const crc32 = bytes => {
      let crc=0xffffffff;
      for(const byte of bytes){crc^=byte;for(let bit=0;bit<8;bit++)crc=(crc>>>1)^((crc&1)?0xedb88320:0);}
      return (crc^0xffffffff)>>>0;
    };
    const local=[], central=[]; let offset=0;
    for(const file of files){
      const name=encoder.encode(file.name), data=file.bytes, crc=crc32(data);
      const header=new Uint8Array(30+name.length), view=new DataView(header.buffer);
      view.setUint32(0,0x04034b50,true);view.setUint16(4,20,true);view.setUint16(6,0x0800,true);view.setUint16(8,0,true);
      view.setUint32(14,crc,true);view.setUint32(18,data.length,true);view.setUint32(22,data.length,true);view.setUint16(26,name.length,true);header.set(name,30);
      local.push(header,data);
      const record=new Uint8Array(46+name.length), cview=new DataView(record.buffer);
      cview.setUint32(0,0x02014b50,true);cview.setUint16(4,20,true);cview.setUint16(6,20,true);cview.setUint16(8,0x0800,true);cview.setUint16(10,0,true);
      cview.setUint32(16,crc,true);cview.setUint32(20,data.length,true);cview.setUint32(24,data.length,true);cview.setUint16(28,name.length,true);cview.setUint32(42,offset,true);record.set(name,46);
      central.push(record);offset+=header.length+data.length;
    }
    const centralSize=central.reduce((sum,part)=>sum+part.length,0), end=new Uint8Array(22), endView=new DataView(end.buffer);
    endView.setUint32(0,0x06054b50,true);endView.setUint16(8,files.length,true);endView.setUint16(10,files.length,true);endView.setUint32(12,centralSize,true);endView.setUint32(16,offset,true);
    return new Blob([...local,...central,end],{type:'application/zip'});
  }

  function svgToRaster(svg, mimeType) {
    return new Promise((resolve,reject)=>{
      const sourceUrl=URL.createObjectURL(new Blob([svg],{type:'image/svg+xml;charset=utf-8'}));
      const image=new Image();
      image.onload=()=>{
        const canvas=document.createElement('canvas');canvas.width=image.naturalWidth;canvas.height=image.naturalHeight;
        canvas.getContext('2d').drawImage(image,0,0);
        canvas.toBlob(blob=>{URL.revokeObjectURL(sourceUrl);if(!blob)reject(new Error('No se pudo rasterizar la tarjeta.'));else resolve(blob);},mimeType,mimeType==='image/webp'?0.86:undefined);
      };
      image.onerror=()=>{URL.revokeObjectURL(sourceUrl);reject(new Error('No se pudo preparar la tarjeta.'));};
      image.src=sourceUrl;
    });
  }

  async function downloadComparison(format) {
    const rowA = rounds.get(selectA.value);
    const rowB = rounds.get(selectB.value);
    if (!rowA || !rowB) return;
    const size = formatSelect?.value || 'apaisado';
    const metricsAvailable = rowA.dataset.completa === '1' && rowB.dataset.completa === '1';
    const includeMetrics = Boolean(metricsAvailable && metricsToggle?.checked);
    const includeCaption = Boolean(captionToggle?.checked);
    const includeHeader = !Boolean(noHeaderToggle?.checked);
    const showBrand = Boolean(brandToggle?.checked);
    const carouselContext = carouselContextInput?.value.trim().slice(0,72) || '';
    const safeName = value => value.replace(/[^0-9a-z]+/gi, '-').replace(/^-|-$/g, '');
    const stem = `comparativa-${size}-${safeName(rowA.dataset.comparisonId)}-${safeName(rowB.dataset.comparisonId)}`;
    if(size==='carrusel'){
      const mimeType={svg:'image/svg+xml',png:'image/png',webp:'image/webp'}[format];
      const extension=format;
      const files=[];
      for(const [index,row] of [rowA,rowB].entries()){
        const svg=comparisonSvg(rowA,rowB,'carrusel',includeMetrics,includeCaption,includeHeader,showBrand,row,index===0?carouselContext:'');
        let blob=format==='svg'?new Blob([svg],{type:'image/svg+xml;charset=utf-8'}):await svgToRaster(svg,mimeType);
        if(format==='webp'&&blob.type!=='image/webp')throw new Error('Este navegador no ofrece exportación WebP; puedes elegir PNG o SVG.');
        files.push({name:`diapositiva-${index+1}-jornada-${row.dataset.jornada.padStart(2,'0')}.${extension}`,bytes:new Uint8Array(await blob.arrayBuffer())});
      }
      saveBlob(zipStored(files),`${stem}-${format}.zip`);
      compareState.textContent=`Carrusel ZIP con dos diapositivas ${format.toUpperCase()} descargado${includeCaption?' con pie':' sin pie'}${carouselContext?' y frase de portada':' y sin frase de portada'}${includeHeader?' con cabecera':' sin cabecera'}${showBrand?' y con marca':' sin marca'}.`;
      return;
    }
    const svg=comparisonSvg(rowA,rowB,size,includeMetrics,includeCaption,includeHeader,showBrand);
    if(format==='svg')saveBlob(new Blob([svg],{type:'image/svg+xml;charset=utf-8'}),`${stem}.svg`);
    else {
      const mimeType=format==='webp'?'image/webp':'image/png';
      const blob=await svgToRaster(svg,mimeType);
      if(format==='webp'&&blob.type!=='image/webp')throw new Error('Este navegador no ofrece exportación WebP; puedes elegir PNG o SVG.');
      saveBlob(blob,`${stem}.${format}`);
    }
    compareState.textContent=`Tarjeta ${size} ${format.toUpperCase()} descargada${includeCaption?' con pie':' sin pie'}${includeHeader?' con cabecera':' sin cabecera'}${showBrand?' y con marca':' sin marca'}.`;
  }

  if (filterBox && seasonFilter && rivalFilter && count && rows.length) {
    const params = new URLSearchParams(window.location.search);
    const requestedSeason = params.get('temporada');
    const requestedRival = params.get('rival');
    if ([...seasonFilter.options].some(option => option.value === requestedSeason)) seasonFilter.value = requestedSeason;
    if ([...rivalFilter.options].some(option => option.value === requestedRival)) rivalFilter.value = requestedRival;
    seasonFilter.addEventListener('change', updateFilters);
    rivalFilter.addEventListener('change', updateFilters);
    clearButton.addEventListener('click', () => {
      seasonFilter.value = '';
      rivalFilter.value = '';
      updateFilters();
      seasonFilter.focus();
    });
    filterBox.hidden = false;
    updateFilters();
  }
  if (selectA && selectB && rounds.size) {
    selectA.addEventListener('change', () => updateComparison('a'));
    selectB.addEventListener('change', () => updateComparison('b'));
    const params = new URLSearchParams(window.location.search);
    const requestedA = params.get('jornada_a');
    const requestedB = params.get('jornada_b');
    if (rounds.has(requestedA) && rounds.has(requestedB) && requestedA !== requestedB) {
      selectA.value = requestedA;
      selectB.value = requestedB;
    }
    shareButton?.addEventListener('click', async () => {
      const url = new URL(window.location.href);
      url.searchParams.set('jornada_a', selectA.value);
      url.searchParams.set('jornada_b', selectB.value);
      try {
        await navigator.clipboard.writeText(url.toString());
        compareState.textContent = 'Enlace de la comparación copiado.';
      } catch {
        window.prompt('Copia el enlace de la comparación:', url.toString());
      }
    });
    const updateFormatGuidance = () => {
      if (storiesNote) storiesNote.hidden = formatSelect?.value !== 'historias';
      if (carouselNote) carouselNote.hidden = formatSelect?.value !== 'carrusel';
      if (individualDownloads) individualDownloads.hidden = formatSelect?.value === 'carrusel';
      if (carouselDownloads) carouselDownloads.hidden = formatSelect?.value !== 'carrusel';
      updateCarouselPreview();
    };
    formatSelect?.addEventListener('change', updateFormatGuidance);
    carouselContextInput?.addEventListener('input', updateCarouselPreview);
    carouselExamples?.addEventListener('change', () => {
      if (!carouselContextInput) return;
      carouselContextInput.value = carouselExamples.value;
      updateCarouselPreview();
    });
    [metricsToggle,captionToggle,noHeaderToggle,brandToggle].forEach(control=>control?.addEventListener('change',updateCarouselPreview));
    updateFormatGuidance();
    if (downloadControls) downloadControls.hidden = false;
    document.querySelectorAll('[data-descargar-comparacion]').forEach(button => {
      button.addEventListener('click', async () => {
        try {
          await downloadComparison(button.dataset.descargarComparacion);
        } catch (error) {
          compareState.textContent = error instanceof Error ? error.message : 'No se pudo preparar la descarga.';
        }
      });
    });
    updateComparison('');
  }
})();
