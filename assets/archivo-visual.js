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
  }

  function xml(value) {
    return String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[char]));
  }

  function comparisonSvg(rowA, rowB, format, includeMetrics, includeCaption) {
    const layouts = {
      apaisado: {width:1200,height:630,header:148,panels:[{x:54,y:190,w:528,h:365},{x:618,y:190,w:528,h:365}],titleSize:42,titleY:111,brandY:54,captionY:582,domainY:606},
      cuadrado: {width:1080,height:1080,header:180,panels:[{x:80,y:220,w:920,h:350},{x:80,y:610,w:920,h:350}],titleSize:40,titleY:128,brandY:65,captionY:1010,domainY:1056},
      vertical: {width:1080,height:1350,header:190,panels:[{x:80,y:235,w:920,h:465},{x:80,y:755,w:920,h:465}],titleSize:40,titleY:134,brandY:64,captionY:1258,domainY:1326},
      historias: {width:1080,height:1920,header:395,panels:[{x:80,y:430,w:920,h:430},{x:80,y:900,w:920,h:430}],titleSize:40,titleY:348,brandY:274,captionY:1500,domainY:1560}
    };
    const layout = layouts[format] || layouts.apaisado;
    const cards = [rowA, rowB].map((row, index) => {
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
        : includeMetrics ? 'Métricas no comparables por falta de cobertura completa' : 'Métricas omitidas';
      const center=x+w/2, pad=Math.min(32,w*.06), nameWidth=w*.38;
      const metaY=y+44, labelY=y+h*.34, namesY=y+h*.45, scoreY=y+h*.70, metricY=y+h-36;
      return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="22" fill="#fff" stroke="#d4ded6" stroke-width="2"/><path d="M${x} ${y+h-8}h${w}" stroke="#ff7a2f" stroke-width="8"/><text x="${x+pad}" y="${metaY}" fill="#536257" font-family="Arial,sans-serif" font-size="${w<600?19:23}" font-weight="700" letter-spacing="1.2">${seasonLabel} · J${round} · ${xml(row.dataset.fechaPartido)}</text><text x="${x+pad}" y="${labelY}" fill="#536257" font-family="Arial,sans-serif" font-size="${w<600?17:19}" font-weight="700">LOCAL</text><text x="${x+w-pad}" y="${labelY}" text-anchor="end" fill="#536257" font-family="Arial,sans-serif" font-size="${w<600?17:19}" font-weight="700">VISITANTE</text><text x="${x+pad}" y="${namesY}" fill="#163e28" font-family="Arial,sans-serif" font-size="${w<600?24:30}" font-weight="700" textLength="${nameWidth}" lengthAdjust="spacingAndGlyphs">${xml(home)}</text><text x="${x+w-pad}" y="${namesY}" text-anchor="end" fill="#163e28" font-family="Arial,sans-serif" font-size="${w<600?24:30}" font-weight="700" textLength="${nameWidth}" lengthAdjust="spacingAndGlyphs">${xml(away)}</text><text x="${center}" y="${scoreY}" text-anchor="middle" fill="#163e28" font-family="Arial,sans-serif" font-size="${w<600?78:92}" font-weight="800">${xml(homeGoals)} <tspan fill="#ff7a2f" font-size="${w<600?56:64}">–</tspan> ${xml(awayGoals)}</text><text x="${center}" y="${metricY}" text-anchor="middle" fill="#536257" font-family="Arial,sans-serif" font-size="${w<600?17:19}">${metrics}</text>`;
    }).join('');
    const title = `Comparativa J${rowA.dataset.jornada}–J${rowB.dataset.jornada} · ${rowA.dataset.temporada} / ${rowB.dataset.temporada}`;
    const homeAway = row => row.dataset.sede === 'Casa'
      ? {home:'Real Zaragoza',away:row.dataset.rival,homeGoals:row.dataset.golesZaragoza,awayGoals:row.dataset.golesRival}
      : {home:row.dataset.rival,away:'Real Zaragoza',homeGoals:row.dataset.golesRival,awayGoals:row.dataset.golesZaragoza};
    const scoreA=homeAway(rowA), scoreB=homeAway(rowB);
    const caption=includeCaption
      ? `<text x="${layout.width/2}" y="${layout.captionY}" text-anchor="middle" fill="#536257" font-family="Arial,sans-serif" font-size="17" font-weight="700">Primera Federación · J${rowA.dataset.jornada.padStart(2,'0')} ${scoreA.homeGoals}–${scoreA.awayGoals} · J${rowB.dataset.jornada.padStart(2,'0')} ${scoreB.homeGoals}–${scoreB.awayGoals}</text>`
      : '';
    const storiesDesc=format==='historias'?' La composición reserva espacio superior e inferior para no quedar debajo de los controles de las historias.':'';
    const brandY=layout.brandY ?? 54;
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${layout.width}" height="${layout.height}" viewBox="0 0 ${layout.width} ${layout.height}" role="img" aria-labelledby="titulo descripcion"><title id="titulo">${xml(title)}</title><desc id="descripcion">Marcadores del Real Zaragoza frente a ${xml(rowA.dataset.rival)} y ${xml(rowB.dataset.rival)}. La posesión y los tiros se incluyen solo si se seleccionan y las dos fichas están completas.${xml(storiesDesc)}</desc><rect width="${layout.width}" height="${layout.height}" fill="#f3f5ef"/><path d="M0 0h${layout.width}v${layout.header}H0z" fill="#103b24"/><path d="M0 ${layout.header-5}h${layout.width}" stroke="#ff7a2f" stroke-width="7"/><text x="54" y="${brandY}" fill="#bed8c4" font-family="Arial,sans-serif" font-size="17" font-weight="700" letter-spacing="3">LÍNEA DE PASE · ARCHIVO VISUAL</text><text x="54" y="${layout.titleY}" fill="#f7f8f4" font-family="Arial,sans-serif" font-size="${layout.titleSize}" font-weight="800">Dos jornadas, frente a frente</text>${cards}${caption}<text x="${layout.width-50}" y="${layout.domainY}" text-anchor="end" fill="#64766b" font-family="Arial,sans-serif" font-size="15">lineadepase.com</text></svg>`;
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

  async function downloadComparison(format) {
    const rowA = rounds.get(selectA.value);
    const rowB = rounds.get(selectB.value);
    if (!rowA || !rowB) return;
    const size = formatSelect?.value || 'apaisado';
    const dimensions = {apaisado:[1200,630],cuadrado:[1080,1080],vertical:[1080,1350],historias:[1080,1920]}[size] || [1200,630];
    const metricsAvailable = rowA.dataset.completa === '1' && rowB.dataset.completa === '1';
    const includeMetrics = Boolean(metricsAvailable && metricsToggle?.checked);
    const includeCaption = Boolean(captionToggle?.checked);
    const svg = comparisonSvg(rowA, rowB, size, includeMetrics, includeCaption);
    const safeName = value => value.replace(/[^0-9a-z]+/gi, '-').replace(/^-|-$/g, '');
    const filename = `comparativa-${size}-${safeName(rowA.dataset.comparisonId)}-${safeName(rowB.dataset.comparisonId)}`;
    if (format === 'svg') {
      saveBlob(new Blob([svg], {type: 'image/svg+xml;charset=utf-8'}), `${filename}.svg`);
      compareState.textContent = `Tarjeta ${size} SVG descargada${includeMetrics?' con métricas':' sin métricas'}${includeCaption?' y con pie':' sin pie'}.`;
      return;
    }
    const sourceUrl = URL.createObjectURL(new Blob([svg], {type: 'image/svg+xml;charset=utf-8'}));
    const image = new Image();
    image.onload = () => {
      const canvas = document.createElement('canvas');
      canvas.width = dimensions[0];
      canvas.height = dimensions[1];
      canvas.getContext('2d').drawImage(image, 0, 0);
      const mimeType = format === 'webp' ? 'image/webp' : 'image/png';
      const extension = format;
      canvas.toBlob(blob => {
        URL.revokeObjectURL(sourceUrl);
        if (!blob || (format === 'webp' && blob.type !== 'image/webp')) {
          compareState.textContent = format === 'webp'
            ? 'Este navegador no ofrece exportación WebP; puedes descargar la tarjeta como PNG o SVG.'
            : 'No se pudo preparar la descarga PNG.';
          return;
        }
        saveBlob(blob, `${filename}.${extension}`);
        compareState.textContent = `Tarjeta ${size} ${extension.toUpperCase()} descargada${includeMetrics?' con métricas':' sin métricas'}${includeCaption?' y con pie':' sin pie'}.`;
      }, mimeType, format === 'webp' ? 0.86 : undefined);
    };
    image.onerror = () => {
      URL.revokeObjectURL(sourceUrl);
      compareState.textContent = 'No se pudo preparar la tarjeta comparativa.';
    };
    image.src = sourceUrl;
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
    };
    formatSelect?.addEventListener('change', updateFormatGuidance);
    updateFormatGuidance();
    if (downloadControls) downloadControls.hidden = false;
    document.querySelectorAll('[data-descargar-comparacion]').forEach(button => {
      button.addEventListener('click', () => downloadComparison(button.dataset.descargarComparacion));
    });
    updateComparison('');
  }
})();
