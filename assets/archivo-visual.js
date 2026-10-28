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
  const favoriteButton = document.querySelector('[data-guardar-comparacion]');
  const resetOptionsButton = document.querySelector('[data-restablecer-opciones]');
  const copyImageButton = document.querySelector('[data-copiar-imagen]');
  const presetSelect = document.querySelector('[data-preset-selector]');
  const presetNameInput = document.getElementById('nombre-preset');
  const savePresetButton = document.querySelector('[data-guardar-preset]');
  const deletePresetButton = document.querySelector('[data-borrar-preset]');
  const paletteSelect = document.querySelector('[data-paleta-visual]');
  const contrastNotice = document.querySelector('[data-aviso-contraste]');
  const framingSelect = document.querySelector('[data-encuadre-visual]');
  const densitySelect = document.querySelector('[data-densidad-visual]');
  const safeZoneToggle = document.querySelector('[data-guia-zonas]');
  const stylePreviewControls = ['a','b'].map(side => ({
    framing: document.querySelector(`[data-vista-encuadre="${side}"]`),
    density: document.querySelector(`[data-vista-densidad="${side}"]`),
    image: document.querySelector(`[data-vista-estilo="${side}"]`)
  }));
  const altTextInput = document.querySelector('[data-texto-alternativo]');
  const generateAltTextButton = document.querySelector('[data-generar-texto-alternativo]');
  const copyAltTextButton = document.querySelector('[data-copiar-texto-alternativo]');
  const socialKitFormat = document.querySelector('[data-formato-kit]');
  const socialKitButton = document.querySelector('[data-descargar-kit]');
  const socialKitStatus = document.querySelector('[data-estado-kit]');
  const contactSheetButtons = [...document.querySelectorAll('[data-hoja-plantilla]')];
  const seasonPosterSelect = document.querySelector('[data-temporada-mapa]');
  const seasonPosterFormat = document.querySelector('[data-formato-mapa]');
  const seasonPosterType = document.querySelector('[data-tipo-mapa]');
  const seasonPosterButton = document.querySelector('[data-descargar-mapa]');
  const seasonPosterStatus = document.querySelector('[data-estado-mapa]');
  const seasonPosterSheet = document.querySelector('[data-lamina-mapa]');
  const seasonPosterAlt = document.querySelector('[data-texto-mapa]');
  const resetSeasonPosterAlt = document.querySelector('[data-restablecer-texto-mapa]');
  const seasonPosterPreview = document.querySelector('[data-preview-mapa-img]');
  const seasonPosterPreviewCaption = document.querySelector('[data-preview-mapa-caption]');
  const kitEstimates = document.querySelector('[data-kit-estimaciones]');
  const formatThumbnailButtons = [...document.querySelectorAll('[data-miniatura-formato]')];
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
  let altTextCustomized = false;
  let seasonPosterAltCustomized = false;
  let estimateTimer = 0;
  let estimateRun = 0;
  const rounds = new Map(rows.map(row => [row.dataset.comparisonId, row]));
  const preferencesKey = 'lineadepase:archivo-visual:preferencias:v1';
  const favoriteKey = 'lineadepase:archivo-visual:pareja-favorita:v1';
  const personalPresetsKey = 'lineadepase:archivo-visual:plantillas:v1';
  const palettes = {
    clasica: {background:'#f3f5ef',panel:'#ffffff',header:'#103b24',headerText:'#ffffff',brand:'#bed8c4',contextHeader:'#e0e9e2',foreground:'#163e28',muted:'#536257',border:'#d4ded6',accent:'#ff7a2f',domain:'#64766b'},
    contraste: {background:'#ffffff',panel:'#ffffff',header:'#111827',headerText:'#ffffff',brand:'#ffffff',contextHeader:'#ffffff',foreground:'#111827',muted:'#334155',border:'#111827',accent:'#b45309',domain:'#334155'},
    papel: {background:'#f4efe5',panel:'#fffcf5',header:'#203744',headerText:'#ffffff',brand:'#dce7e2',contextHeader:'#f0f4ed',foreground:'#1e2f38',muted:'#43505a',border:'#aab7b3',accent:'#ad4523',domain:'#43505a'}
  };
  const builtInPresets = {
    portada: {format:'apaisado',metrics:true,caption:true,noHeader:false,brand:true,framing:'equilibrado',density:'completa'},
    'comparacion-limpia': {format:'cuadrado',metrics:true,caption:false,noHeader:true,brand:false,framing:'equilibrado',density:'completa'},
    historia: {format:'historias',metrics:true,caption:false,noHeader:false,brand:true,framing:'equilibrado',density:'completa'},
    'social-cuadrada': {format:'cuadrado',metrics:false,caption:false,noHeader:true,brand:true,framing:'protagonista',density:'esencial'},
    'social-vertical': {format:'vertical',metrics:false,caption:false,noHeader:true,brand:true,framing:'protagonista',density:'esencial'}
  };

  function activePalette() { return palettes[paletteSelect?.value] || palettes.clasica; }

  function luminance(hex) {
    const channels = hex.slice(1).match(/.{2}/g).map(value => parseInt(value,16)/255).map(value => value <= .04045 ? value/12.92 : ((value+.055)/1.055)**2.4);
    return .2126*channels[0]+.7152*channels[1]+.0722*channels[2];
  }

  function updateContrastNotice() {
    if (!contrastNotice) return;
    const palette = activePalette();
    const pairs = [
      [palette.foreground,palette.background],[palette.muted,palette.background],
      [palette.foreground,palette.panel],[palette.muted,palette.panel],
      [palette.headerText,palette.header],[palette.brand,palette.header],
      [palette.contextHeader,palette.header]
    ];
    const minimum = Math.min(...pairs.map(([textColor,backgroundColor]) => {
      const a=luminance(textColor), b=luminance(backgroundColor);
      return (Math.max(a,b)+.05)/(Math.min(a,b)+.05);
    }));
    const passes = minimum >= 4.5;
    contrastNotice.textContent = passes ? `Contraste correcto · mínimo ${minimum.toFixed(1)}:1` : `Contraste bajo · mínimo ${minimum.toFixed(1)}:1; elige otra paleta`;
    contrastNotice.classList.toggle('contraste-bajo',!passes);
    contrastNotice.classList.toggle('contraste-correcto',passes);
  }

  function readStorage(key) {
    try { return JSON.parse(window.localStorage.getItem(key) || 'null'); }
    catch { return null; }
  }

  function writeStorage(key, value) {
    try { window.localStorage.setItem(key, JSON.stringify(value)); return true; }
    catch { return false; }
  }

  function restoreVisualPreferences() {
    const saved = readStorage(preferencesKey);
    if (!saved || typeof saved !== 'object') return;
    if (formatSelect && [...formatSelect.options].some(option => option.value === saved.format)) formatSelect.value = saved.format;
    if (metricsToggle && typeof saved.metrics === 'boolean') metricsToggle.checked = saved.metrics;
    if (captionToggle && typeof saved.caption === 'boolean') captionToggle.checked = saved.caption;
    if (noHeaderToggle && typeof saved.noHeader === 'boolean') noHeaderToggle.checked = saved.noHeader;
    if (brandToggle && typeof saved.brand === 'boolean') brandToggle.checked = saved.brand;
    if (paletteSelect && [...paletteSelect.options].some(option => option.value === saved.palette)) paletteSelect.value = saved.palette;
    if (framingSelect && [...framingSelect.options].some(option => option.value === saved.framing)) framingSelect.value = saved.framing;
    if (densitySelect && [...densitySelect.options].some(option => option.value === saved.density)) densitySelect.value = saved.density;
  }

  function saveVisualPreferences() {
    return writeStorage(preferencesKey, {
      format: formatSelect?.value || 'apaisado',
      metrics: Boolean(metricsToggle?.checked),
      caption: Boolean(captionToggle?.checked),
      noHeader: Boolean(noHeaderToggle?.checked),
      brand: brandToggle?.checked !== false,
      palette: paletteSelect?.value || 'clasica',
      framing: framingSelect?.value || 'equilibrado',
      density: densitySelect?.value || 'completa'
    });
  }

  function updateFavoriteButton() {
    if (!favoriteButton || !selectA || !selectB) return false;
    const saved = readStorage(favoriteKey);
    const isSaved = saved?.a === selectA.value && saved?.b === selectB.value;
    favoriteButton.textContent = isSaved ? 'Quitar pareja guardada' : 'Guardar pareja';
    favoriteButton.setAttribute('aria-pressed', String(Boolean(isSaved)));
    return Boolean(isSaved);
  }

  function currentVisualSettings() {
    return {
      format: formatSelect?.value || 'apaisado',
      metrics: Boolean(metricsToggle?.checked),
      caption: Boolean(captionToggle?.checked),
      noHeader: Boolean(noHeaderToggle?.checked),
      brand: brandToggle?.checked !== false,
      palette: paletteSelect?.value || 'clasica',
      framing: framingSelect?.value || 'equilibrado',
      density: densitySelect?.value || 'completa'
    };
  }

  function readPersonalPresets() {
    const saved = readStorage(personalPresetsKey);
    if (!Array.isArray(saved)) return [];
    return saved.filter(item => item && typeof item.id === 'string' && typeof item.name === 'string' && item.settings && typeof item.settings === 'object').slice(0,6);
  }

  function refreshPresetSelector(selectedValue = presetSelect?.value || '') {
    if (!presetSelect) return;
    let group = presetSelect.querySelector('[data-personal-presets]');
    if (!group) {
      group = document.createElement('optgroup');
      group.label = 'Mis plantillas';
      group.dataset.personalPresets = '';
      presetSelect.append(group);
    }
    group.replaceChildren();
    readPersonalPresets().forEach(preset => {
      const option = document.createElement('option');
      option.value = `personal:${preset.id}`;
      option.textContent = preset.name;
      group.append(option);
    });
    presetSelect.value = [...presetSelect.options].some(option => option.value === selectedValue) ? selectedValue : '';
    if (deletePresetButton) deletePresetButton.disabled = !presetSelect.value.startsWith('personal:');
  }

  function applyVisualSettings(settings) {
    if (formatSelect && [...formatSelect.options].some(option => option.value === settings.format)) formatSelect.value = settings.format;
    if (metricsToggle && typeof settings.metrics === 'boolean') metricsToggle.checked = settings.metrics;
    if (captionToggle && typeof settings.caption === 'boolean') captionToggle.checked = settings.caption;
    if (noHeaderToggle && typeof settings.noHeader === 'boolean') noHeaderToggle.checked = settings.noHeader;
    if (brandToggle && typeof settings.brand === 'boolean') brandToggle.checked = settings.brand;
    if (paletteSelect && palettes[settings.palette]) paletteSelect.value = settings.palette;
    if (framingSelect && ['equilibrado','protagonista'].includes(settings.framing)) framingSelect.value = settings.framing;
    if (densitySelect && ['completa','resultado','esencial'].includes(settings.density)) densitySelect.value = settings.density;
    formatSelect?.dispatchEvent(new Event('change',{bubbles:true}));
    saveVisualPreferences();
    updateComparison('');
  }

  function updateFormatThumbnails() {
    const rowA = rounds.get(selectA?.value);
    const rowB = rounds.get(selectB?.value);
    if (!rowA || !rowB) return;
    const metrics = rowA.dataset.completa === '1' && rowB.dataset.completa === '1' && Boolean(metricsToggle?.checked);
    formatThumbnailButtons.forEach(button => {
      const format = button.dataset.miniaturaFormato;
      if (!format) return;
      const isCarousel = format === 'carrusel';
      const svg = comparisonSvg(rowA,rowB,format,metrics,Boolean(captionToggle?.checked),!Boolean(noHeaderToggle?.checked),Boolean(brandToggle?.checked),isCarousel?rowA:null,isCarousel?carouselContextInput?.value.trim().slice(0,72) || '':'',densitySelect?.value,framingSelect?.value,altTextInput?.value.trim() || '');
      const image = button.querySelector('img');
      if (image) image.src = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
      button.setAttribute('aria-pressed',String(formatSelect?.value === format));
    });
  }

  function describeRows(rowsToDescribe, density, includeMetrics) {
    const mixedSeasons = new Set(rowsToDescribe.map(row => row.dataset.temporada)).size > 1;
    const results = rowsToDescribe.map(row => {
      const home = row.dataset.sede === 'Casa' ? 'Real Zaragoza' : row.dataset.rival;
      const away = row.dataset.sede === 'Casa' ? row.dataset.rival : 'Real Zaragoza';
      const homeGoals = row.dataset.sede === 'Casa' ? row.dataset.golesZaragoza : row.dataset.golesRival;
      const awayGoals = row.dataset.sede === 'Casa' ? row.dataset.golesRival : row.dataset.golesZaragoza;
      const context = density === 'esencial' ? '' : ` ${mixedSeasons ? `${row.dataset.temporada} ` : ''}${row.dataset.fechaPartido.split('-').reverse().join('/')}`;
      return `J${row.dataset.jornada}${context}: ${home} ${homeGoals}–${awayGoals} ${away}`;
    });
    const statistics = includeMetrics && density === 'completa'
      ? rowsToDescribe.filter(row => row.dataset.completa === '1').map(row => `J${row.dataset.jornada}: posesión Zaragoza ${row.dataset.posesion.replace('.', ',')} %, tiros ${row.dataset.tirosZaragoza}–${row.dataset.tirosRival}`)
      : [];
    return `Marcadores del Real Zaragoza: ${results.join('; ')}.${statistics.length ? ` ${statistics.join('; ')}.` : ''}`.slice(0,240);
  }

  function updateGeneratedAltText() {
    if (!altTextInput || altTextCustomized) return;
    const rowA = rounds.get(selectA?.value);
    const rowB = rounds.get(selectB?.value);
    if (!rowA || !rowB) return;
    const rowsToDescribe = formatSelect?.value === 'carrusel' ? [rowA] : [rowA,rowB];
    const metrics = densitySelect?.value === 'completa' && Boolean(metricsToggle?.checked) && rowA.dataset.completa === '1' && rowB.dataset.completa === '1';
    altTextInput.value = describeRows(rowsToDescribe,densitySelect?.value || 'completa',metrics);
  }

  function updateStyleComparisons() {
    const rowA = rounds.get(selectA?.value);
    const rowB = rounds.get(selectB?.value);
    if (!rowA || !rowB || stylePreviewControls.some(item => !item.image)) return;
    const format = formatSelect?.value === 'carrusel' ? 'cuadrado' : formatSelect?.value || 'apaisado';
    const metrics = rowA.dataset.completa === '1' && rowB.dataset.completa === '1' && Boolean(metricsToggle?.checked);
    stylePreviewControls.forEach(({framing,density,image}) => {
      const previewDensity = density?.value || 'completa';
      const previewAltText = altTextCustomized ? altTextInput?.value.trim() || '' : describeRows([rowA,rowB],previewDensity,metrics);
      const svg = comparisonSvg(rowA,rowB,format,metrics,Boolean(captionToggle?.checked),!Boolean(noHeaderToggle?.checked),Boolean(brandToggle?.checked),null,'',previewDensity,framing?.value || 'equilibrado',previewAltText);
      image.src = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
    });
  }

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
      metricsToggle.disabled = !includeMetrics || densitySelect?.value !== 'completa';
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
    updateFavoriteButton();
    updateGeneratedAltText();
    updateCarouselPreview();
    updateContactSheet();
    scheduleKitEstimates();
  }

  function xml(value) {
    return String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[char]));
  }

  function comparisonSvg(rowA, rowB, format, includeMetrics, includeCaption, includeHeader, showBrand, singleRow = null, contextText = '', density = densitySelect?.value || 'completa', framing = framingSelect?.value || 'equilibrado', altText = altTextInput?.value.trim() || '') {
    const layouts = {
      apaisado: {width:1200,height:630,header:148,panels:[{x:54,y:190,w:528,h:365},{x:618,y:190,w:528,h:365}],titleSize:42,titleY:111,brandY:54,captionY:582,domainY:606},
      cuadrado: {width:1080,height:1080,header:180,panels:[{x:80,y:220,w:920,h:350},{x:80,y:610,w:920,h:350}],titleSize:40,titleY:128,brandY:65,captionY:1010,domainY:1056},
      vertical: {width:1080,height:1350,header:190,panels:[{x:80,y:235,w:920,h:465},{x:80,y:755,w:920,h:465}],titleSize:40,titleY:134,brandY:64,captionY:1258,domainY:1326},
      historias: {width:1080,height:1920,header:520,panels:[{x:80,y:555,w:920,h:420},{x:80,y:1030,w:920,h:420}],titleSize:40,titleY:450,brandY:375,captionY:1520,domainY:1570},
      carrusel: {width:1080,height:1080,header:190,panels:[{x:80,y:260,w:920,h:540}],titleSize:40,titleY:130,brandY:66,captionY:930,domainY:1056,single:true}
    };
    const baseLayout = layouts[format] || layouts.apaisado;
    const palette = activePalette();
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
      const metrics = cardMetrics && density === 'completa'
        ? `Posesión ${xml(row.dataset.posesion.replace('.', ','))}% · tiros ${xml(row.dataset.tirosZaragoza)}–${xml(row.dataset.tirosRival)}`
        : '';
      const center=x+w/2, pad=Math.min(32,w*.06), nameWidth=w*.38;
      const metaY=y+44, labelY=y+h*.34, namesY=y+h*.45, scoreY=y+h*.70, metricY=y+h-36;
      const scoreSize = framing === 'protagonista' ? (w<600?100:122) : (w<600?78:92);
      const separatorSize = framing === 'protagonista' ? (w<600?62:82) : (w<600?56:64);
      const meta = density === 'esencial' ? '' : `<text x="${x+pad}" y="${metaY}" fill="${palette.muted}" font-family="Arial,sans-serif" font-size="${w<600?19:23}" font-weight="700" letter-spacing="1.2">${seasonLabel} · J${round} · ${xml(row.dataset.fechaPartido)}</text>`;
      return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="22" fill="${palette.panel}" stroke="${palette.border}" stroke-width="2"/><path d="M${x} ${y+h-8}h${w}" stroke="${palette.accent}" stroke-width="8"/>${meta}<text x="${x+pad}" y="${labelY}" fill="${palette.muted}" font-family="Arial,sans-serif" font-size="${w<600?17:19}" font-weight="700">LOCAL</text><text x="${x+w-pad}" y="${labelY}" text-anchor="end" fill="${palette.muted}" font-family="Arial,sans-serif" font-size="${w<600?17:19}" font-weight="700">VISITANTE</text><text x="${x+pad}" y="${namesY}" fill="${palette.foreground}" font-family="Arial,sans-serif" font-size="${w<600?24:30}" font-weight="700" textLength="${nameWidth}" lengthAdjust="spacingAndGlyphs">${xml(home)}</text><text x="${x+w-pad}" y="${namesY}" text-anchor="end" fill="${palette.foreground}" font-family="Arial,sans-serif" font-size="${w<600?24:30}" font-weight="700" textLength="${nameWidth}" lengthAdjust="spacingAndGlyphs">${xml(away)}</text><text x="${center}" y="${scoreY}" text-anchor="middle" fill="${palette.foreground}" font-family="Arial,sans-serif" font-size="${scoreSize}" font-weight="800">${xml(homeGoals)} <tspan fill="${palette.accent}" font-size="${separatorSize}">–</tspan> ${xml(awayGoals)}</text>${metrics?`<text x="${center}" y="${metricY}" text-anchor="middle" fill="${palette.muted}" font-family="Arial,sans-serif" font-size="${w<600?17:19}">${metrics}</text>`:''}`;
    }).join('');
    const title = singleRow
      ? `Jornada ${singleRow.dataset.jornada} · ${singleRow.dataset.rival} · ${singleRow.dataset.temporada}`
      : `Comparativa J${rowA.dataset.jornada}–J${rowB.dataset.jornada} · ${rowA.dataset.temporada} / ${rowB.dataset.temporada}`;
    const homeAway = row => row.dataset.sede === 'Casa'
      ? {home:'Real Zaragoza',away:row.dataset.rival,homeGoals:row.dataset.golesZaragoza,awayGoals:row.dataset.golesRival}
      : {home:row.dataset.rival,away:'Real Zaragoza',homeGoals:row.dataset.golesRival,awayGoals:row.dataset.golesZaragoza};
    const scores=displayRows.map(row => ({row,score:homeAway(row)}));
    const caption=includeCaption && density === 'completa'
      ? `<text x="${layout.width/2}" y="${layout.captionY}" text-anchor="middle" fill="${palette.muted}" font-family="Arial,sans-serif" font-size="17" font-weight="700">Primera Federación · ${scores.map(({row,score})=>`J${row.dataset.jornada.padStart(2,'0')} ${score.homeGoals}–${score.awayGoals}`).join(' · ')}</text>`
      : '';
    const storiesDesc=format==='historias'?' La composición reserva espacio superior e inferior para no quedar debajo de los controles de las historias.':'';
    const brandY=baseLayout.brandY ?? 54;
    const contextY=includeHeader?baseLayout.titleY+38:Math.max(brandY+58,baseLayout.header-62);
    const header=`${includeHeader?`<path d="M0 0h${layout.width}v${baseLayout.header}H0z" fill="${palette.header}"/><path d="M0 ${baseLayout.header-5}h${layout.width}" stroke="${palette.accent}" stroke-width="7"/>`:''}${showBrand?`<text x="54" y="${brandY}" fill="${includeHeader?palette.brand:palette.foreground}" font-family="Arial,sans-serif" font-size="17" font-weight="700" letter-spacing="3">LÍNEA DE PASE · ARCHIVO VISUAL</text>`:''}${includeHeader?`<text x="54" y="${baseLayout.titleY}" fill="${palette.headerText}" font-family="Arial,sans-serif" font-size="${baseLayout.titleSize}" font-weight="800">${singleRow?`J${singleRow.dataset.jornada.padStart(2,'0')} · ${xml(singleRow.dataset.rival)}`:'Dos jornadas, frente a frente'}</text>`:''}${singleRow&&contextText?`<text x="54" y="${contextY}" fill="${includeHeader?palette.contextHeader:palette.muted}" font-family="Arial,sans-serif" font-size="19" font-weight="600">${xml(contextText)}</text>`:''}`;
    const description = altText || describeRows(displayRows,density,includeMetrics);
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${layout.width}" height="${layout.height}" viewBox="0 0 ${layout.width} ${layout.height}" role="img" aria-labelledby="titulo descripcion"><title id="titulo">${xml(title)}</title><desc id="descripcion">${xml(description)}${xml(storiesDesc)}</desc><rect width="${layout.width}" height="${layout.height}" fill="${palette.background}"/>${header}${cards}${caption}${showBrand?`<text x="${layout.width-50}" y="${layout.domainY}" text-anchor="end" fill="${palette.domain}" font-family="Arial,sans-serif" font-size="15">lineadepase.com</text>`:''}</svg>`;
  }

  function updateContactSheet() {
    const rowA=rounds.get(selectA?.value), rowB=rounds.get(selectB?.value);
    if(!rowA||!rowB)return;
    contactSheetButtons.forEach(button=>{
      const name=button.dataset.hojaPlantilla, settings=builtInPresets[name], image=button.querySelector('img');
      if(!settings||!image)return;
      const metrics=settings.metrics&&rowA.dataset.completa==='1'&&rowB.dataset.completa==='1';
      const svg=comparisonSvg(rowA,rowB,settings.format,metrics,settings.caption, !settings.noHeader, settings.brand,null,'',settings.density,settings.framing,describeRows([rowA,rowB],settings.density,metrics));
      image.src=`data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
      button.setAttribute('aria-pressed',String(presetSelect?.value===name));
    });
  }

  function seasonPosterRows(season) {
    return rows.filter(row=>row.dataset.temporada===season).sort((a,b)=>Number(a.dataset.jornada)-Number(b.dataset.jornada));
  }

  function seasonPosterLayout(format) {
    const layouts={cuadrado:{width:1080,height:1080,top:175,bottom:82},vertical:{width:1080,height:1350,top:190,bottom:90},historias:{width:1080,height:1920,top:380,bottom:300}};
    return layouts[format]||layouts.cuadrado;
  }

  function seasonPosterPageSize(format) {
    const layout=seasonPosterLayout(format), usable=layout.height-layout.top-layout.bottom, minCard=74, gap=12;
    return Math.max(1,Math.floor((usable+gap)/(minCard+gap)));
  }

  function seasonPosterPages(season,format) {
    const seasonRows=seasonPosterRows(season), perPage=seasonPosterPageSize(format);
    return Array.from({length:Math.ceil(seasonRows.length/perPage)},(_,index)=>seasonRows.slice(index*perPage,(index+1)*perPage));
  }

  function posterOutcome(row) {
    const goals=Number(row.dataset.golesZaragoza), against=Number(row.dataset.golesRival);
    if(goals>against)return {label:'VICTORIA',color:'#176b3a'};
    if(goals<against)return {label:'DERROTA',color:'#a33028'};
    return {label:'EMPATE',color:'#49515c'};
  }

  function seasonPosterDescription(season,format,pageIndex=0) {
    const pages=seasonPosterPages(season,format), pageRows=pages[pageIndex]||[], records=pageRows.map(row=>{
      const result=posterOutcome(row).label.toLocaleLowerCase('es');
      return `J${row.dataset.jornada} ${row.dataset.sede.toLocaleLowerCase('es')} ante ${row.dataset.rival}: ${row.dataset.golesZaragoza}–${row.dataset.golesRival}, ${result}`;
    });
    return `Real Zaragoza, temporada ${season}, lámina ${pageIndex+1} de ${Math.max(1,pages.length)}. ${records.join('; ')}`.slice(0,1000);
  }

  function seasonPosterSvg(season,format,pageIndex=0,customAlt='') {
    const layout=seasonPosterLayout(format), palette=activePalette(), pages=seasonPosterPages(season,format), seasonRows=seasonPosterRows(season), pageRows=pages[pageIndex]||[];
    if(!seasonRows.length||!pageRows.length)return '';
    const usable=layout.height-layout.top-layout.bottom, gap=12, cardHeight=Math.min(112,(usable-gap*(pageRows.length-1))/pageRows.length);
    const total=cardHeight*pageRows.length+gap*(pageRows.length-1), startY=layout.top+(usable-total)/2;
    const cards=pageRows.map((row,index)=>{
      const y=startY+index*(cardHeight+gap), home=row.dataset.sede==='Casa'?'Real Zaragoza':row.dataset.rival, away=row.dataset.sede==='Casa'?row.dataset.rival:'Real Zaragoza';
      const homeGoals=row.dataset.sede==='Casa'?row.dataset.golesZaragoza:row.dataset.golesRival, awayGoals=row.dataset.sede==='Casa'?row.dataset.golesRival:row.dataset.golesZaragoza;
      const date=row.dataset.fechaPartido.split('-').slice(1).reverse().join('/'), outcome=posterOutcome(row);
      const metric=row.dataset.completa==='1'?`<text x="${layout.width/2}" y="${y+cardHeight*.88}" text-anchor="middle" fill="${palette.muted}" font-family="Arial,sans-serif" font-size="13">Posesión ${xml(row.dataset.posesion.replace('.',','))}% · tiros ${xml(row.dataset.tirosZaragoza)}–${xml(row.dataset.tirosRival)}</text>`:'';
      const badgeWidth=130, badgeX=layout.width-36-badgeWidth;
      return `<rect x="36" y="${y}" width="${layout.width-72}" height="${cardHeight}" rx="18" fill="${palette.panel}" stroke="${palette.border}" stroke-width="2"/><path d="M36 ${y+cardHeight-6}h${layout.width-72}" stroke="${outcome.color}" stroke-width="7"/><text x="64" y="${y+cardHeight*.32}" fill="${palette.muted}" font-family="Arial,sans-serif" font-size="16" font-weight="700">J${row.dataset.jornada.padStart(2,'0')} · ${xml(date)} · ${row.dataset.sede==='Casa'?'CASA':'FUERA'}</text><rect x="${badgeX}" y="${y+8}" width="${badgeWidth}" height="26" rx="13" fill="${outcome.color}"/><text x="${badgeX+badgeWidth/2}" y="${y+26}" text-anchor="middle" fill="#ffffff" font-family="Arial,sans-serif" font-size="13" font-weight="700">${outcome.label}</text><text x="${layout.width/2}" y="${y+cardHeight*.62}" text-anchor="middle" fill="${palette.foreground}" font-family="Arial,sans-serif" font-size="21" font-weight="700" textLength="${layout.width-150}" lengthAdjust="spacingAndGlyphs">${xml(home)} ${xml(homeGoals)}–${xml(awayGoals)} ${xml(away)}</text>${metric}`;
    }).join('');
    const seasonCounts=seasonRows.reduce((counts,row)=>{
      const key=row.dataset.sede==='Casa'?'casa':'fuera', outcome=posterOutcome(row).label;
      counts[key][outcome]++; return counts;
    },{casa:{VICTORIA:0,EMPATE:0,DERROTA:0},fuera:{VICTORIA:0,EMPATE:0,DERROTA:0}});
    const metricless=seasonRows.filter(row=>row.dataset.completa!=='1').length;
    const totals=`Casa ${seasonCounts.casa.VICTORIA}V–${seasonCounts.casa.EMPATE}E–${seasonCounts.casa.DERROTA}D · Fuera ${seasonCounts.fuera.VICTORIA}V–${seasonCounts.fuera.EMPATE}E–${seasonCounts.fuera.DERROTA}D`;
    const pageText=`Lámina ${pageIndex+1} de ${pages.length} · Jornadas ${pageRows[0].dataset.jornada.padStart(2,'0')}–${pageRows.at(-1).dataset.jornada.padStart(2,'0')}`;
    const note=`${seasonRows.length} jornadas · ${seasonRows.length-metricless} con ficha validada · ${metricless} sin métricas`;
    const safeTop=format==='historias'?220:0, safeBottom=format==='historias'?220:0;
    const alt=customAlt||seasonPosterDescription(season,format,pageIndex);
    const footerY=layout.height-safeBottom-54;
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${layout.width}" height="${layout.height}" viewBox="0 0 ${layout.width} ${layout.height}" role="img" aria-labelledby="mapa-titulo mapa-desc"><title id="mapa-titulo">Real Zaragoza · ${xml(season)} · mapa de resultados</title><desc id="mapa-desc">${xml(alt)}. ${xml(totals)}. ${xml(note)}.</desc><rect width="100%" height="100%" fill="${palette.background}"/><path d="M0 ${safeTop}h${layout.width}v${layout.height-safeTop-safeBottom}H0z" fill="${palette.header}"/><text x="54" y="${safeTop+62}" fill="${palette.brand}" font-family="Arial,sans-serif" font-size="18" font-weight="700" letter-spacing="3">LÍNEA DE PASE · REAL ZARAGOZA</text><text x="54" y="${safeTop+120}" fill="${palette.headerText}" font-family="Arial,sans-serif" font-size="42" font-weight="800">Mapa de la temporada</text><text x="54" y="${safeTop+163}" fill="${palette.contextHeader}" font-family="Arial,sans-serif" font-size="26">${xml(season)} · ${xml(pageText)}</text>${cards}<text x="54" y="${footerY}" fill="${palette.brand}" font-family="Arial,sans-serif" font-size="16">${xml(totals)}</text><text x="54" y="${footerY+24}" fill="${palette.brand}" font-family="Arial,sans-serif" font-size="15">${xml(note)}</text></svg>`;
  }

  function updateSeasonPosterPreview() {
    if(!seasonPosterPreview||!seasonPosterSelect)return;
    const season=seasonPosterSelect.value, format=seasonPosterFormat?.value||'cuadrado', pages=seasonPosterPages(season,format), pageIndex=Math.min(Number(seasonPosterSheet?.value||0),Math.max(0,pages.length-1));
    const sheetControl=seasonPosterSheet?.parentElement;
    if(sheetControl){sheetControl.hidden=pages.length<2;}
    if(seasonPosterSheet){
      const current=String(pageIndex), options=pages.map((page,index)=>`<option value="${index}">Lámina ${index+1} · J${page[0].dataset.jornada.padStart(2,'0')}–J${page.at(-1).dataset.jornada.padStart(2,'0')}</option>`).join('');
      seasonPosterSheet.innerHTML=options;
      seasonPosterSheet.value=current;
    }
    if(seasonPosterAlt&&!seasonPosterAltCustomized)seasonPosterAlt.value=seasonPosterDescription(season,format,pageIndex);
    const alt=seasonPosterAlt?.value.trim()||seasonPosterDescription(season,format,pageIndex), svg=seasonPosterSvg(season,format,pageIndex,alt);
    seasonPosterPreview.src=`data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
    seasonPosterPreview.alt=alt;
    if(seasonPosterPreviewCaption)seasonPosterPreviewCaption.textContent=`Vista previa · lámina ${pageIndex+1} de ${Math.max(1,pages.length)} · ${format==='cuadrado'?'1080 × 1080':format==='vertical'?'1080 × 1350':'1080 × 1920'}`;
  }

  async function downloadSeasonPoster() {
    const season=seasonPosterSelect?.value, format=seasonPosterFormat?.value||'cuadrado', type=seasonPosterType?.value||'png';
    const pages=seasonPosterPages(season,format), alt=seasonPosterAlt?.value.trim()||'';
    if(!pages.length)throw new Error('No hay jornadas disponibles para esa temporada.');
    const files=[]; let singleBlob=null;
    for(let index=0;index<pages.length;index++){
      const svg=seasonPosterSvg(season,format,index,alt);
      const blob=type==='svg'?new Blob([svg],{type:'image/svg+xml;charset=utf-8'}):await svgToRaster(svg,type==='webp'?'image/webp':'image/png');
      if(type==='webp'&&blob.type!=='image/webp')throw new Error('Este navegador no ofrece exportación WebP.');
      if(pages.length===1)singleBlob=blob;
      else files.push({name:`lamina-${String(index+1).padStart(2,'0')}.${type}`,bytes:new Uint8Array(await blob.arrayBuffer())});
    }
    const safeSeason=season.replace(/[^0-9a-z]+/gi,'-').replace(/^-|-$/g,'');
    if(singleBlob){saveBlob(singleBlob,`mapa-temporada-${safeSeason}-${format}.${type}`);if(seasonPosterStatus)seasonPosterStatus.textContent=`Mapa ${season} descargado · ${format} · ${(singleBlob.size/1024).toFixed(1)} KB.`;}
    else {const zip=zipStored(files);saveBlob(zip,`mapa-temporada-${safeSeason}-${format}-${type}.zip`);if(seasonPosterStatus)seasonPosterStatus.textContent=`ZIP con ${pages.length} láminas ${format} descargado · ${(zip.size/1024).toFixed(1)} KB.`;}
  }

  function scheduleKitEstimates() {
    if(!kitEstimates)return;
    window.clearTimeout(estimateTimer);
    const run=++estimateRun;
    kitEstimates.textContent='Calculando tamaños para la pareja seleccionada…';
    estimateTimer=window.setTimeout(async()=>{
      const rowA=rounds.get(selectA?.value),rowB=rounds.get(selectB?.value);
      if(!rowA||!rowB)return;
      const metrics=rowA.dataset.completa==='1'&&rowB.dataset.completa==='1'&&Boolean(metricsToggle?.checked);
      const alt=altTextCustomized?altTextInput?.value.trim()||'':describeRows([rowA,rowB],densitySelect?.value||'completa',metrics);
      const formats=[['cuadrado',1080,1080],['vertical',1080,1350],['historias',1080,1920]];
      const output=[], sizeMap={};
      try {
        for(const [size,width,height] of formats){
          const svg=comparisonSvg(rowA,rowB,size,metrics,Boolean(captionToggle?.checked),!Boolean(noHeaderToggle?.checked),Boolean(brandToggle?.checked),null,'',densitySelect?.value,framingSelect?.value,alt);
          const svgBytes=new TextEncoder().encode(svg).length;
          const png=await svgToRaster(svg,'image/png');
          const webp=await svgToRaster(svg,'image/webp');
          if(run!==estimateRun)return;
          sizeMap[size]={svg:svgBytes,png:png.size,webp:webp.type==='image/webp'?webp.size:null};
          output.push(`<tr><th scope="row">${size==='cuadrado'?'Cuadrado':size==='vertical'?'Vertical':'Historias'}<br><small>${width} × ${height}</small></th><td>${(svgBytes/1024).toFixed(1)} KB</td><td>${(png.size/1024).toFixed(1)} KB</td><td>${webp.type==='image/webp'?(webp.size/1024).toFixed(1)+' KB':'No disponible'}</td></tr>`);
        }
        if(run!==estimateRun)return;
        const zipType=socialKitFormat?.value||'png', extension=zipType;
        const zipFiles=['cuadrado','vertical','historias'].map(size=>({name:`${size}.${extension}`,bytes:sizeMap[size][zipType]}));
        zipFiles.push({name:'texto-alternativo.txt',bytes:new TextEncoder().encode(alt).length});
        const zipSize=zipFiles.reduce((sum,file)=>sum+(file.bytes??0)+76+2*new TextEncoder().encode(file.name).length,22);
        kitEstimates.innerHTML=`<div class="archivo-tabla-pesos"><table><thead><tr><th>Formato</th><th>SVG</th><th>PNG</th><th>WebP</th></tr></thead><tbody>${output.join('')}</tbody></table></div><p class="nota">ZIP del formato elegido (${zipType.toUpperCase()}): ${(zipSize/1024).toFixed(1)} KB, incluido el texto alternativo.</p>`;
      } catch {
        if(run===estimateRun)kitEstimates.textContent='No se pudieron calcular todos los tamaños en este navegador.';
      }
    },450);
  }

  function updateCarouselPreview() {
    const active = formatSelect?.value === 'carrusel';
    if (carouselContextControls) carouselContextControls.hidden = !active;
    if (carouselPreview) carouselPreview.hidden = !active;
    if (!active) {
      if (carouselPreviewUrl) URL.revokeObjectURL(carouselPreviewUrl);
      carouselPreviewUrl = null;
      updateFormatThumbnails();
      updateStyleComparisons();
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
    updateFormatThumbnails();
    updateStyleComparisons();
  }

  function updateSafeZoneGuide() {
    const frame = document.querySelector('[data-miniatura-zonas]');
    frame?.classList.toggle('mostrar-zonas-seguras',formatSelect?.value === 'historias' && Boolean(safeZoneToggle?.checked));
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
        const slideAltText=altTextCustomized?altTextInput?.value.trim() || '':describeRows([row],densitySelect?.value || 'completa',includeMetrics);
        const svg=comparisonSvg(rowA,rowB,'carrusel',includeMetrics,includeCaption,includeHeader,showBrand,row,index===0?carouselContext:'',densitySelect?.value,framingSelect?.value,slideAltText);
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

  async function downloadSocialKit() {
    const rowA = rounds.get(selectA?.value);
    const rowB = rounds.get(selectB?.value);
    if (!rowA || !rowB) return;
    const format = socialKitFormat?.value || 'png';
    const mimeType = {svg:'image/svg+xml',png:'image/png',webp:'image/webp'}[format];
    if (!mimeType) return;
    const metricsAvailable = rowA.dataset.completa === '1' && rowB.dataset.completa === '1';
    const includeMetrics = metricsAvailable && Boolean(metricsToggle?.checked);
    const includeCaption = Boolean(captionToggle?.checked);
    const includeHeader = !Boolean(noHeaderToggle?.checked);
    const showBrand = Boolean(brandToggle?.checked);
    const density = densitySelect?.value || 'completa';
    const framing = framingSelect?.value || 'equilibrado';
    const alternativeText = altTextCustomized ? altTextInput?.value.trim() || '' : describeRows([rowA,rowB],density,includeMetrics);
    const safeName = value => value.replace(/[^0-9a-z]+/gi, '-').replace(/^-|-$/g, '');
    const stem = `kit-social-${safeName(rowA.dataset.comparisonId)}-${safeName(rowB.dataset.comparisonId)}`;
    const files = [];
    for (const size of ['cuadrado','vertical','historias']) {
      const svg = comparisonSvg(rowA,rowB,size,includeMetrics,includeCaption,includeHeader,showBrand,null,'',density,framing,alternativeText);
      const blob = format === 'svg' ? new Blob([svg],{type:'image/svg+xml;charset=utf-8'}) : await svgToRaster(svg,mimeType);
      if (format === 'webp' && blob.type !== 'image/webp') throw new Error('Este navegador no ofrece exportación WebP; elige PNG o SVG.');
      files.push({name:`${size}.${format}`,bytes:new Uint8Array(await blob.arrayBuffer())});
    }
    files.push({name:'texto-alternativo.txt',bytes:new TextEncoder().encode(alternativeText)});
    saveBlob(zipStored(files),`${stem}-${format}.zip`);
    if (socialKitStatus) socialKitStatus.textContent = `ZIP listo: cuadrado, vertical e historias en ${format.toUpperCase()}, más el texto alternativo.`;
  }

  async function copyComparisonImage() {
    if (!navigator.clipboard?.write || typeof ClipboardItem === 'undefined') {
      compareState.textContent = 'Este navegador no permite copiar imágenes directamente. Puedes descargar la tarjeta en PNG.';
      return;
    }
    const rowA = rounds.get(selectA?.value);
    const rowB = rounds.get(selectB?.value);
    if (!rowA || !rowB) return;
    const size = formatSelect?.value || 'apaisado';
    const includeMetrics = rowA.dataset.completa === '1' && rowB.dataset.completa === '1' && Boolean(metricsToggle?.checked);
    const includeCaption = Boolean(captionToggle?.checked);
    const includeHeader = !Boolean(noHeaderToggle?.checked);
    const showBrand = Boolean(brandToggle?.checked);
    const svg = size === 'carrusel'
      ? comparisonSvg(rowA,rowB,'carrusel',includeMetrics,includeCaption,includeHeader,showBrand,rowA,carouselContextInput?.value.trim().slice(0,72) || '')
      : comparisonSvg(rowA,rowB,size,includeMetrics,includeCaption,includeHeader,showBrand);
    const png = await svgToRaster(svg,'image/png');
    await navigator.clipboard.write([new ClipboardItem({'image/png':png})]);
    compareState.textContent = size === 'carrusel'
      ? 'Primera diapositiva del carrusel copiada como imagen PNG.'
      : `Tarjeta ${size} copiada como imagen PNG.`;
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
    restoreVisualPreferences();
    refreshPresetSelector();
    const favorite = readStorage(favoriteKey);
    if (rounds.has(favorite?.a) && rounds.has(favorite?.b) && favorite.a !== favorite.b) {
      selectA.value = favorite.a;
      selectB.value = favorite.b;
    }
    selectA.addEventListener('change', () => updateComparison('a'));
    selectB.addEventListener('change', () => updateComparison('b'));
    const params = new URLSearchParams(window.location.search);
    const requestedA = params.get('jornada_a');
    const requestedB = params.get('jornada_b');
    if (rounds.has(requestedA) && rounds.has(requestedB) && requestedA !== requestedB) {
      selectA.value = requestedA;
      selectB.value = requestedB;
    }
    favoriteButton?.addEventListener('click', () => {
      if (updateFavoriteButton()) {
        try { window.localStorage.removeItem(favoriteKey); } catch {}
        compareState.textContent = 'Pareja guardada eliminada.';
      } else if (writeStorage(favoriteKey,{a:selectA.value,b:selectB.value})) {
        compareState.textContent = 'Pareja guardada en este navegador.';
      } else {
        compareState.textContent = 'No se pudo guardar la pareja en este navegador.';
      }
      updateFavoriteButton();
    });
    [formatSelect,metricsToggle,captionToggle,noHeaderToggle,brandToggle].forEach(control=>control?.addEventListener('change',saveVisualPreferences));
    [framingSelect,densitySelect].forEach(control=>control?.addEventListener('change',() => {
      updateFormatGuidance();
      updateComparison('');
      saveVisualPreferences();
    }));
    safeZoneToggle?.addEventListener('change',updateSafeZoneGuide);
    stylePreviewControls.forEach(({framing,density}) => {
      framing?.addEventListener('change',updateStyleComparisons);
      density?.addEventListener('change',updateStyleComparisons);
    });
    altTextInput?.addEventListener('input',() => {
      altTextCustomized = true;
      updateFormatThumbnails();
      updateCarouselPreview();
      updateContactSheet();
      scheduleKitEstimates();
    });
    generateAltTextButton?.addEventListener('click',() => {
      altTextCustomized = false;
      updateGeneratedAltText();
      updateCarouselPreview();
    });
    copyAltTextButton?.addEventListener('click',async () => {
      const text = altTextInput?.value.trim() || '';
      if (!text) return;
      try {
        await navigator.clipboard.writeText(text);
        compareState.textContent = 'Texto alternativo copiado.';
      } catch {
        altTextInput?.focus();
        altTextInput?.select();
        compareState.textContent = 'Selecciona el texto alternativo y cópialo.';
      }
    });
    contactSheetButtons.forEach(button=>button.addEventListener('click',()=>{
      const name=button.dataset.hojaPlantilla;
      if(!builtInPresets[name])return;
      if(presetSelect)presetSelect.value=name;
      applyVisualSettings(builtInPresets[name]);
      compareState.textContent=`Plantilla «${button.querySelector('span')?.textContent||name}» aplicada.`;
    }));
    const availableSeasons=[...new Set(rows.map(row=>row.dataset.temporada))].sort((a,b)=>b.localeCompare(a,'es'));
    availableSeasons.forEach(season=>{const option=document.createElement('option');option.value=season;option.textContent=season;seasonPosterSelect?.append(option);});
    if(seasonPosterSelect)seasonPosterSelect.value=availableSeasons[0]||'';
    seasonPosterButton?.addEventListener('click',async()=>{if(seasonPosterStatus)seasonPosterStatus.textContent='Preparando el mapa…';try{await downloadSeasonPoster();}catch(error){if(seasonPosterStatus)seasonPosterStatus.textContent=error instanceof Error?error.message:'No se pudo preparar el mapa.';}});
    [seasonPosterSelect,seasonPosterFormat,seasonPosterType].forEach(control=>control?.addEventListener('change',()=>{updateSeasonPosterPreview();if(seasonPosterStatus)seasonPosterStatus.textContent='El mapa está listo para descargar.';}));
    seasonPosterSheet?.addEventListener('change',updateSeasonPosterPreview);
    seasonPosterAlt?.addEventListener('input',()=>{seasonPosterAltCustomized=true;updateSeasonPosterPreview();});
    resetSeasonPosterAlt?.addEventListener('click',()=>{seasonPosterAltCustomized=false;updateSeasonPosterPreview();if(seasonPosterStatus)seasonPosterStatus.textContent='Texto alternativo actualizado con los resultados.';});
    updateSeasonPosterPreview();
    socialKitFormat?.addEventListener('change',scheduleKitEstimates);
    socialKitButton?.addEventListener('click',async () => {
      if (socialKitStatus) socialKitStatus.textContent = 'Preparando tres formatos…';
      try { await downloadSocialKit(); }
      catch (error) {
        if (socialKitStatus) socialKitStatus.textContent = error instanceof Error ? error.message : 'No se pudo preparar el kit social.';
      }
    });
    resetOptionsButton?.addEventListener('click', () => {
      if (formatSelect) formatSelect.value = 'apaisado';
      if (metricsToggle) metricsToggle.checked = true;
      if (captionToggle) captionToggle.checked = true;
      if (noHeaderToggle) noHeaderToggle.checked = false;
      if (brandToggle) brandToggle.checked = true;
      if (paletteSelect) paletteSelect.value = 'clasica';
      if (framingSelect) framingSelect.value = 'equilibrado';
      if (densitySelect) densitySelect.value = 'completa';
      if (safeZoneToggle) safeZoneToggle.checked = false;
      if (carouselContextInput) carouselContextInput.value = '';
      if (carouselExamples) carouselExamples.value = '';
      if (presetSelect) presetSelect.value = '';
      if (deletePresetButton) deletePresetButton.disabled = true;
      saveVisualPreferences();
      updateFormatGuidance();
      updateComparison('');
      compareState.textContent = 'Opciones visuales restablecidas.';
    });
    copyImageButton?.addEventListener('click', async () => {
      try { await copyComparisonImage(); }
      catch { compareState.textContent = 'No se pudo copiar la imagen. Puedes descargar la tarjeta en PNG.'; }
    });
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
      if (copyImageButton) copyImageButton.textContent = formatSelect?.value === 'carrusel' ? 'Copiar primera diapositiva' : 'Copiar imagen';
      if (captionToggle) captionToggle.disabled = densitySelect?.value !== 'completa';
      updateSafeZoneGuide();
      updateGeneratedAltText();
      updateCarouselPreview();
      updateContrastNotice();
    };
    presetSelect?.addEventListener('change', () => {
      const value = presetSelect.value;
      if (builtInPresets[value]) {
        applyVisualSettings(builtInPresets[value]);
        compareState.textContent = `Plantilla «${presetSelect.selectedOptions[0].textContent}» aplicada.`;
        return;
      }
      const personalId = value.startsWith('personal:') ? value.slice('personal:'.length) : '';
      const personal = readPersonalPresets().find(preset => preset.id === personalId);
      if (personal) {
        applyVisualSettings(personal.settings);
        compareState.textContent = `Plantilla «${personal.name}» aplicada.`;
      }
      if (deletePresetButton) deletePresetButton.disabled = !personal;
    });
    savePresetButton?.addEventListener('click', () => {
      const name = presetNameInput?.value.trim().slice(0,28) || '';
      if (!name) {
        compareState.textContent = 'Escribe un nombre breve para guardar la plantilla.';
        presetNameInput?.focus();
        return;
      }
      const presets = readPersonalPresets();
      const existing = presets.find(preset => preset.name.toLocaleLowerCase() === name.toLocaleLowerCase());
      if (!existing && presets.length >= 6) {
        compareState.textContent = 'Ya hay 6 plantillas personales. Borra una antes de guardar otra.';
        return;
      }
      const preset = {id:existing?.id || `p-${Date.now().toString(36)}`,name,settings:currentVisualSettings()};
      const next = existing ? presets.map(item => item.id === existing.id ? preset : item) : [...presets,preset];
      if (!writeStorage(personalPresetsKey,next)) {
        compareState.textContent = 'No se pudo guardar la plantilla en este navegador.';
        return;
      }
      presetNameInput.value = '';
      refreshPresetSelector(`personal:${preset.id}`);
      compareState.textContent = `Plantilla «${name}» guardada en este navegador.`;
    });
    deletePresetButton?.addEventListener('click', () => {
      const personalId = presetSelect?.value.startsWith('personal:') ? presetSelect.value.slice('personal:'.length) : '';
      if (!personalId) return;
      const presets = readPersonalPresets();
      const target = presets.find(preset => preset.id === personalId);
      if (!writeStorage(personalPresetsKey,presets.filter(preset => preset.id !== personalId))) {
        compareState.textContent = 'No se pudo borrar la plantilla.';
        return;
      }
      refreshPresetSelector('');
      compareState.textContent = target ? `Plantilla «${target.name}» borrada.` : 'Plantilla borrada.';
    });
    formatSelect?.addEventListener('change', updateFormatGuidance);
    paletteSelect?.addEventListener('change', () => {
      updateFormatGuidance();
      saveVisualPreferences();
      updateContactSheet();
      scheduleKitEstimates();
      updateSeasonPosterPreview();
    });
    formatThumbnailButtons.forEach(button => button.addEventListener('click', () => {
      if (!formatSelect || ![...formatSelect.options].some(option => option.value === button.dataset.miniaturaFormato)) return;
      formatSelect.value = button.dataset.miniaturaFormato;
      formatSelect.dispatchEvent(new Event('change',{bubbles:true}));
      saveVisualPreferences();
    }));
    carouselContextInput?.addEventListener('input', updateCarouselPreview);
    carouselExamples?.addEventListener('change', () => {
      if (!carouselContextInput) return;
      carouselContextInput.value = carouselExamples.value;
      updateCarouselPreview();
    });
    [metricsToggle,captionToggle,noHeaderToggle,brandToggle].forEach(control=>control?.addEventListener('change',() => {
      updateGeneratedAltText();
      updateCarouselPreview();
      scheduleKitEstimates();
    }));
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
    scheduleKitEstimates();
  }
})();
