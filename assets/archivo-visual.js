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

  function comparisonSvg(rowA, rowB) {
    const hasMetrics = rowA.dataset.completa === '1' && rowB.dataset.completa === '1';
    const cards = [rowA, rowB].map((row, index) => {
      const x = index ? 618 : 54;
      const home = row.dataset.sede === 'Casa' ? 'Real Zaragoza' : row.dataset.rival;
      const away = row.dataset.sede === 'Casa' ? row.dataset.rival : 'Real Zaragoza';
      const homeGoals = row.dataset.sede === 'Casa' ? row.dataset.golesZaragoza : row.dataset.golesRival;
      const awayGoals = row.dataset.sede === 'Casa' ? row.dataset.golesRival : row.dataset.golesZaragoza;
      const round = row.dataset.jornada.padStart(2, '0');
      const seasonLabel = xml(row.dataset.temporada);
      const metrics = hasMetrics
        ? `Posesión ${xml(row.dataset.posesion.replace('.', ','))}% · tiros ${xml(row.dataset.tirosZaragoza)}–${xml(row.dataset.tirosRival)}`
        : 'Métricas no comparables por falta de cobertura completa';
      const panel = `<rect x="${x}" y="190" width="528" height="365" rx="22" fill="#fff" stroke="#d4ded6" stroke-width="2"/><path d="M${x} 534h528" stroke="#ff7a2f" stroke-width="8"/><text x="${x+28}" y="234" fill="#536257" font-family="Arial,sans-serif" font-size="20" font-weight="700" letter-spacing="1.5">${seasonLabel} · J${round} · ${xml(row.dataset.fechaPartido)}</text><text x="${x+32}" y="312" fill="#536257" font-family="Arial,sans-serif" font-size="19" font-weight="700">LOCAL</text><text x="${x+496}" y="312" text-anchor="end" fill="#536257" font-family="Arial,sans-serif" font-size="19" font-weight="700">VISITANTE</text><text x="${x+32}" y="352" fill="#163e28" font-family="Arial,sans-serif" font-size="26" font-weight="700" textLength="210" lengthAdjust="spacingAndGlyphs">${xml(home)}</text><text x="${x+496}" y="352" text-anchor="end" fill="#163e28" font-family="Arial,sans-serif" font-size="26" font-weight="700" textLength="210" lengthAdjust="spacingAndGlyphs">${xml(away)}</text><text x="${x+264}" y="445" text-anchor="middle" fill="#163e28" font-family="Arial,sans-serif" font-size="86" font-weight="800">${xml(homeGoals)} <tspan fill="#ff7a2f" font-size="62">–</tspan> ${xml(awayGoals)}</text><text x="${x+264}" y="505" text-anchor="middle" fill="#536257" font-family="Arial,sans-serif" font-size="18">${metrics}</text>`;
      return panel;
    }).join('');
    const title = `Comparativa J${rowA.dataset.jornada}–J${rowB.dataset.jornada} · ${rowA.dataset.temporada} / ${rowB.dataset.temporada}`;
    return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-labelledby="titulo descripcion"><title id="titulo">${xml(title)}</title><desc id="descripcion">Marcadores del Real Zaragoza frente a ${xml(rowA.dataset.rival)} y ${xml(rowB.dataset.rival)}. La posesión y los tiros se incluyen solo con fichas completas en ambos partidos.</desc><rect width="1200" height="630" fill="#f3f5ef"/><path d="M0 0h1200v148H0z" fill="#103b24"/><path d="M0 143h1200" stroke="#ff7a2f" stroke-width="7"/><text x="54" y="54" fill="#bed8c4" font-family="Arial,sans-serif" font-size="17" font-weight="700" letter-spacing="3">LÍNEA DE PASE · ARCHIVO VISUAL</text><text x="54" y="111" fill="#f7f8f4" font-family="Arial,sans-serif" font-size="42" font-weight="800">Dos jornadas, frente a frente</text>${cards}<text x="1150" y="603" text-anchor="end" fill="#64766b" font-family="Arial,sans-serif" font-size="15">lineadepase.com</text></svg>`;
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
    const svg = comparisonSvg(rowA, rowB);
    const safeName = value => value.replace(/[^0-9a-z]+/gi, '-').replace(/^-|-$/g, '');
    const filename = `comparativa-${safeName(rowA.dataset.comparisonId)}-${safeName(rowB.dataset.comparisonId)}`;
    if (format === 'svg') {
      saveBlob(new Blob([svg], {type: 'image/svg+xml;charset=utf-8'}), `${filename}.svg`);
      compareState.textContent = 'Tarjeta comparativa SVG descargada.';
      return;
    }
    const sourceUrl = URL.createObjectURL(new Blob([svg], {type: 'image/svg+xml;charset=utf-8'}));
    const image = new Image();
    image.onload = () => {
      const canvas = document.createElement('canvas');
      canvas.width = 1200;
      canvas.height = 630;
      canvas.getContext('2d').drawImage(image, 0, 0);
      canvas.toBlob(blob => {
        URL.revokeObjectURL(sourceUrl);
        if (!blob) {
          compareState.textContent = 'No se pudo preparar la descarga PNG.';
          return;
        }
        saveBlob(blob, `${filename}.png`);
        compareState.textContent = 'Tarjeta comparativa PNG descargada.';
      }, 'image/png');
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
    document.querySelectorAll('[data-descargar-comparacion]').forEach(button => {
      button.addEventListener('click', () => downloadComparison(button.dataset.descargarComparacion));
    });
    updateComparison('');
  }
})();
