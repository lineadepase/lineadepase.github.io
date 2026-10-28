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
  const socialPrintButton = document.querySelector('[data-imprimir-social]');
  const contactSheetPrintButton = document.querySelector('[data-imprimir-hoja-contacto]');
  const contactSheetPdfButton = document.querySelector('[data-imprimir-hoja-contacto-pdf]');
  const contactSheetDirectPrintButton = document.querySelector('[data-imprimir-hoja-directa]');
  const comparisonA5PdfButton = document.querySelector('[data-imprimir-comparacion-a5]');
  const comparisonTextButton = document.querySelector('[data-descargar-comparacion-texto]');
  const comparisonHtmlButton = document.querySelector('[data-abrir-comparacion-html]');
  const comparisonA5DirectPrintButton = document.querySelector('[data-imprimir-a5-directa]');
  const comparisonA5InkSelect = document.querySelector('[data-modo-impresion-a5]');
  const printPaperSelect = document.querySelector('[data-papel-impresion-social]');
  const printOrientationSelect = document.querySelector('[data-orientacion-hoja-social]');
  const contactSheetVariantSelect = document.querySelector('[data-variante-hoja-contacto]');
  const contactSheetPrintPreview = document.querySelector('[data-preview-hoja-contacto]');
  const contactSheetPrintPreviewCaption = document.querySelector('[data-caption-hoja-contacto]');
  const comparisonA5PrintPreview = document.querySelector('[data-preview-a5]');
  const comparisonA5PrintPreviewCaption = document.querySelector('[data-caption-a5]');
  const comparisonA5PreviewButton = document.querySelector('[data-ampliar-a5]');
  const comparisonA5Dialog = document.querySelector('[data-dialog-a5]');
  const comparisonA5DialogImage = document.querySelector('[data-preview-a5-ampliada]');
  const comparisonA5DialogClose = document.querySelector('[data-cerrar-vista-a5]');
  const printQuickButtons = [...document.querySelectorAll('[data-salto-impresion]')];
  const inkCoverageOutputs = Object.fromEntries(['color','monocromo','fotocopia'].map(mode=>[mode,document.querySelector(`[data-tinta-estimada="${mode}"]`)]));
  const resetPrintSettingsButton = document.querySelector('[data-restablecer-impresion]');
  const printSettingsStatus = document.querySelector('[data-estado-preferencias-impresion]');
  const socialPrintStatus = document.querySelector('[data-estado-impresion-social]');
  const contactSheetButtons = [...document.querySelectorAll('[data-hoja-plantilla]')];
  const seasonPosterSelect = document.querySelector('[data-temporada-mapa]');
  const seasonPosterRival = document.querySelector('[data-rival-mapa]');
  const seasonPosterFrom = document.querySelector('[data-desde-mapa]');
  const seasonPosterTo = document.querySelector('[data-hasta-mapa]');
  const seasonPosterFormat = document.querySelector('[data-formato-mapa]');
  const seasonPosterType = document.querySelector('[data-tipo-mapa]');
  const seasonPosterButton = document.querySelector('[data-descargar-mapa]');
  const seasonPosterStatus = document.querySelector('[data-estado-mapa]');
  const seasonCarouselButton = document.querySelector('[data-descargar-carrusel-temporada]');
  const seasonFormList = document.querySelector('[data-forma-reciente]');
  const seasonFormStreak = document.querySelector('[data-racha-temporada]');
  const seasonRivalFormList = document.querySelector('[data-forma-rival]');
  const seasonRivalFormTitle = document.querySelector('[data-forma-rival-titulo]');
  const seasonRivalFormStatus = document.querySelector('[data-forma-rival-estado]');
  const seasonShareButton = document.querySelector('[data-compartir-mapa]');
  const seasonShareStatus = document.querySelector('[data-estado-compartir-mapa]');
  const seasonSaveLinkName = document.querySelector('[data-nombre-enlace-mapa]');
  const seasonSaveLinkButton = document.querySelector('[data-guardar-enlace-mapa]');
  const seasonSavedLinksList = document.querySelector('[data-enlaces-guardados]');
  const seasonSavedLinksStatus = document.querySelector('[data-estado-enlaces-guardados]');
  const seasonExportLinksButton = document.querySelector('[data-exportar-enlaces-mapa]');
  const seasonImportLinksButton = document.querySelector('[data-importar-enlaces-mapa]');
  const seasonImportLinksFile = document.querySelector('[data-archivo-enlaces-mapa]');
  const seasonQrButton = document.querySelector('[data-generar-qr-enlace]');
  const seasonQrDownloadButton = document.querySelector('[data-descargar-qr-enlace]');
  const seasonQrA4Button = document.querySelector('[data-descargar-qr-a4]');
  const seasonQrA4Preview = document.querySelector('[data-vista-hoja-qr]');
  const seasonQrA4HorizontalPreview = document.querySelector('[data-vista-hoja-qr-horizontal]');
  const seasonQrScaleConfirm = document.querySelector('[data-confirmar-escala-qr]');
  const seasonQrA4LandscapeButton = document.querySelector('[data-descargar-qr-a4-apaisado]');
  const seasonQrA5Button = document.querySelector('[data-descargar-qr-a5]');
  const seasonQrPaperSelect = document.querySelector('[data-papel-impresion-qr]');
  const seasonQrPreviewDisclosure = document.querySelector('[data-detalles-vista-qr]');
  const seasonQrCopyButton = document.querySelector('[data-copiar-qr-enlace]');
  const seasonQrName = document.querySelector('[data-nombre-qr-enlace]');
  const seasonQrColor = document.querySelector('[data-color-qr-enlace]');
  const seasonQrPrintSize = document.querySelector('[data-tamano-qr-enlace]');
  const seasonQrPreview = document.querySelector('[data-vista-qr-enlace]');
  let seasonQrSvg = '';
  let seasonQrObjectUrl = '';
  const seasonSavedLinksKey = 'lineadepase-mapa-enlaces-v1';
  let seasonOpponentForms = {};
  try { seasonOpponentForms = JSON.parse(document.getElementById('datos-forma-rivales')?.textContent || '{}'); } catch (_) { seasonOpponentForms = {}; }
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
    papel: {background:'#f4efe5',panel:'#fffcf5',header:'#203744',headerText:'#ffffff',brand:'#dce7e2',contextHeader:'#f0f4ed',foreground:'#1e2f38',muted:'#43505a',border:'#aab7b3',accent:'#ad4523',domain:'#43505a'},
    monocromo: {background:'#ffffff',panel:'#ffffff',header:'#1a1a1a',headerText:'#ffffff',brand:'#ffffff',contextHeader:'#f0f0f0',foreground:'#171717',muted:'#414141',border:'#696969',accent:'#1a1a1a',domain:'#414141'}
  };
  const lowInkPrintPalette={background:'#ffffff',panel:'#ffffff',header:'#ffffff',headerText:'#171717',brand:'#414141',contextHeader:'#414141',foreground:'#171717',muted:'#414141',border:'#a3a3a3',accent:'#666666',domain:'#555555'};
  const photocopyPrintPalette={background:'#ffffff',panel:'#ffffff',header:'#ffffff',headerText:'#000000',brand:'#000000',contextHeader:'#000000',foreground:'#000000',muted:'#202020',border:'#000000',accent:'#000000',domain:'#000000'};
  const printSettingsKey='lineadepase-print-settings-v1';
  let inkEstimateSequence=0;
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
    image.src = `../assets/ilustraciones/archivo-jornadas/${row.dataset.assetStem}.svg`;
    image.width = 1200;
    image.height = 630;
    image.loading = 'lazy';
    const homeScore = row.dataset.sede === 'Casa' ? row.dataset.golesZaragoza : row.dataset.golesRival;
    const awayScore = row.dataset.sede === 'Casa' ? row.dataset.golesRival : row.dataset.golesZaragoza;
    const homeTeam = row.dataset.sede === 'Casa' ? 'Real Zaragoza' : row.dataset.rival;
    const awayTeam = row.dataset.sede === 'Casa' ? row.dataset.rival : 'Real Zaragoza';
    image.alt = `Marcador J${round}: ${homeTeam} ${homeScore}–${awayScore} ${awayTeam}, ${row.dataset.fechaPartido}`;
    card.append(image);
    appendText(card, 'figcaption', '', `J${round} · ${row.dataset.rival} · ${row.dataset.fechaPartido} · ${row.dataset.temporada}`);
    if (includeMetrics && row.dataset.posesion) {
      appendText(card, 'p', 'comparacion-estadisticas', `Posesión ${row.dataset.posesion.replace('.', ',')} % · tiros ${row.dataset.tirosZaragoza}–${row.dataset.tirosRival}`);
    } else if (row.dataset.completa !== '1') {
      appendText(card, 'p', 'comparacion-estadisticas', 'Ficha estadística sin validar; se muestra solo el marcador.');
    } else {
      appendText(card, 'p', 'comparacion-estadisticas', 'Ficha estadística validada; no se comparan métricas porque la otra jornada no está validada.');
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
    updateA5PrintPreview();
    scheduleKitEstimates();
  }

  function xml(value) {
    return String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[char]));
  }

  function comparisonSvg(rowA, rowB, format, includeMetrics, includeCaption, includeHeader, showBrand, singleRow = null, contextText = '', density = densitySelect?.value || 'completa', framing = framingSelect?.value || 'equilibrado', altText = altTextInput?.value.trim() || '', paletteOverride = null) {
    const layouts = {
      apaisado: {width:1200,height:630,header:148,panels:[{x:54,y:190,w:528,h:365},{x:618,y:190,w:528,h:365}],titleSize:42,titleY:111,brandY:54,captionY:582,domainY:606},
      cuadrado: {width:1080,height:1080,header:180,panels:[{x:80,y:220,w:920,h:350},{x:80,y:610,w:920,h:350}],titleSize:40,titleY:128,brandY:65,captionY:1010,domainY:1056},
      vertical: {width:1080,height:1350,header:190,panels:[{x:80,y:235,w:920,h:465},{x:80,y:755,w:920,h:465}],titleSize:40,titleY:134,brandY:64,captionY:1258,domainY:1326},
      historias: {width:1080,height:1920,header:520,panels:[{x:80,y:555,w:920,h:420},{x:80,y:1030,w:920,h:420}],titleSize:40,titleY:450,brandY:375,captionY:1520,domainY:1570},
      carrusel: {width:1080,height:1080,header:190,panels:[{x:80,y:260,w:920,h:540}],titleSize:40,titleY:130,brandY:66,captionY:930,domainY:1056,single:true}
    };
    const baseLayout = layouts[format] || layouts.apaisado;
    const palette = paletteOverride || activePalette();
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
    updateContactSheetPrintPreview();
  }

  function seasonPosterRows(season,filtered=true) {
    let result=rows.filter(row=>row.dataset.temporada===season).sort((a,b)=>Number(a.dataset.jornada)-Number(b.dataset.jornada));
    if(filtered&&seasonPosterRival?.value)result=result.filter(row=>row.dataset.rival===seasonPosterRival.value);
    if(filtered&&seasonPosterFrom?.value)result=result.filter(row=>row.dataset.fechaPartido>=seasonPosterFrom.value);
    if(filtered&&seasonPosterTo?.value)result=result.filter(row=>row.dataset.fechaPartido<=seasonPosterTo.value);
    return result;
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
    const seasonRows=seasonPosterRows(season,true), perPage=seasonPosterPageSize(format);
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
    const filterText=[seasonPosterRival?.value?`rival ${seasonPosterRival.value}`:'',seasonPosterFrom?.value?`desde ${seasonPosterFrom.value}`:'',seasonPosterTo?.value?`hasta ${seasonPosterTo.value}`:''].filter(Boolean).join(', ');
    return `Real Zaragoza, temporada ${season}, ${seasonPosterRows(season).length} partidos${filterText?` filtrados por ${filterText}`:''}, lámina ${pageIndex+1} de ${Math.max(1,pages.length)}. ${records.join('; ')}`.slice(0,1000);
  }

  function seasonPosterSvg(season,format,pageIndex=0,customAlt='') {
    const layout=seasonPosterLayout(format), palette=activePalette(), pages=seasonPosterPages(season,format), seasonRows=seasonPosterRows(season,true), pageRows=pages[pageIndex]||[];
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

  function updateSeasonForm() {
    if(!seasonPosterSelect)return;
    const season=seasonPosterSelect.value, matches=seasonPosterRows(season,false).sort((a,b)=>b.dataset.fechaPartido.localeCompare(a.dataset.fechaPartido)||Number(b.dataset.jornada)-Number(a.dataset.jornada));
    const outcome=row=>Number(row.dataset.golesZaragoza)>Number(row.dataset.golesRival)?'V':Number(row.dataset.golesZaragoza)<Number(row.dataset.golesRival)?'D':'E';
    if(seasonFormList)seasonFormList.innerHTML=matches.slice(0,5).map(row=>{const result=outcome(row),word=result==='V'?'victoria':result==='D'?'derrota':'empate';return `<li class="forma-${result.toLowerCase()}" aria-label="Jornada ${row.dataset.jornada}: ${word}" title="J${row.dataset.jornada} · ${word}">${result}</li>`;}).join('')||'<li>Sin resultados</li>';
    if(seasonFormStreak){if(!matches.length){seasonFormStreak.textContent='Aún no hay resultados publicados.';return;}const latest=outcome(matches[0]),count=matches.findIndex(row=>outcome(row)!==latest);const length=count<0?matches.length:count,label=latest==='V'?'victoria':latest==='D'?'derrota':'empate',plural=latest==='V'?'victorias':latest==='D'?'derrotas':'empates';seasonFormStreak.textContent=length===1?`${label[0].toUpperCase()+label.slice(1)} en el último partido.`:`${length} ${plural} consecutivas.`;}
    updateOpponentRecentForm();
  }

  function seasonOutcome(goals,against) { return Number(goals)>Number(against)?'V':Number(goals)<Number(against)?'D':'E'; }

  function updateOpponentRecentForm() {
    if(!seasonRivalFormList||!seasonPosterRival)return;
    const rival=seasonPosterRival.value;
    if(seasonRivalFormTitle)seasonRivalFormTitle.textContent=rival?`${rival} · últimos resultados disponibles`:'Rival seleccionado';
    if(!rival){seasonRivalFormList.innerHTML='';if(seasonRivalFormStatus)seasonRivalFormStatus.textContent='Selecciona un rival para comparar la muestra disponible.';return;}
    const normalize=value=>value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase('es').replace(/[^a-z0-9]+/g,' ').trim();
    const key=Object.keys(seasonOpponentForms).find(team=>{const a=normalize(team),b=normalize(rival);return a===b||a.startsWith(b+' ')||b.startsWith(a+' ');});
    const matches=(key?seasonOpponentForms[key]:[]).slice().sort((a,b)=>b.fecha.localeCompare(a.fecha)||b.jornada-a.jornada).slice(0,5);
    seasonRivalFormList.innerHTML=matches.map(match=>{const result=seasonOutcome(match.goles_favor,match.goles_contra),word=result==='V'?'victoria':result==='D'?'derrota':'empate';return `<li class="forma-${result.toLowerCase()}" aria-label="Jornada ${match.jornada}: ${word} ante ${xml(match.rival)}, ${match.goles_favor} a ${match.goles_contra}" title="J${String(match.jornada).padStart(2,'0')} · ${word} · ${match.goles_favor}–${match.goles_contra}">${result}</li>`;}).join('')||'<li>—</li>';
    if(seasonRivalFormStatus){if(!matches.length){seasonRivalFormStatus.textContent='No hay resultados publicados de este rival en la muestra del grupo.';return;}const rounds=[...new Set(matches.map(match=>match.jornada))].sort((a,b)=>a-b);seasonRivalFormStatus.textContent=`${matches.length} ${matches.length===1?'partido publicado':'partidos publicados'} del rival; jornadas ${rounds.join(', ')}. La muestra disponible puede ser menor que cinco.`;}
  }

  function updateSeasonRivalOptions() {
    if(!seasonPosterRival||!seasonPosterSelect)return;
    const previous=seasonPosterRival.value, rivals=[...new Set(seasonPosterRows(seasonPosterSelect.value,false).map(row=>row.dataset.rival))].sort((a,b)=>a.localeCompare(b,'es'));
    seasonPosterRival.innerHTML='<option value="">Todos los rivales</option>'+rivals.map(rival=>`<option value="${xml(rival)}">${xml(rival)}</option>`).join('');
    if(rivals.includes(previous))seasonPosterRival.value=previous;
  }

  function seasonPosterLinkUrl() {
    const url=new URL(window.location.pathname,window.location.origin), params=url.searchParams;
    const values={'mapa-temporada':seasonPosterSelect?.value||'','mapa-rival':seasonPosterRival?.value||'','mapa-desde':seasonPosterFrom?.value||'','mapa-hasta':seasonPosterTo?.value||'','mapa-formato':seasonPosterFormat?.value||'cuadrado','mapa-archivo':seasonPosterType?.value||'webp'};
    Object.entries(values).forEach(([key,value])=>value?params.set(key,value):params.delete(key));
    return url.href;
  }

  async function copySeasonPosterLink() {
    try { await navigator.clipboard.writeText(seasonPosterLinkUrl());if(seasonShareStatus)seasonShareStatus.textContent='Enlace copiado; conserva la temporada, rival, fechas y formato.'; }
    catch (_) { if(seasonShareStatus)seasonShareStatus.textContent='No se pudo copiar el enlace en este navegador.'; }
  }

  function readSeasonSavedLinks() {
    try {
      const links=JSON.parse(window.localStorage.getItem(seasonSavedLinksKey)||'[]');
      return Array.isArray(links)?links.filter(item=>item&&typeof item.name==='string'&&typeof item.url==='string').slice(0,6).map(item=>({...item,pinned:item.pinned===true})).sort((a,b)=>Number(b.pinned)-Number(a.pinned)):[];
    } catch (_) { return []; }
  }

  function renderSeasonSavedLinks() {
    if(!seasonSavedLinksList)return;
    const links=readSeasonSavedLinks();
    seasonSavedLinksList.innerHTML=links.map((item,index)=>`<li><span>${item.pinned?'★ ':''}${xml(item.name)}</span><div><button type="button" class="boton" data-aplicar-enlace-mapa="${index}">Aplicar</button><button type="button" class="boton" data-copiar-enlace-mapa="${index}">Copiar</button><button type="button" class="boton" data-fijar-enlace-mapa="${index}" aria-pressed="${item.pinned}">${item.pinned?'Desfijar':'Fijar'}</button><button type="button" class="boton" data-subir-enlace-mapa="${index}" aria-label="Subir ${xml(item.name)}">↑</button><button type="button" class="boton" data-bajar-enlace-mapa="${index}" aria-label="Bajar ${xml(item.name)}">↓</button><button type="button" class="boton" data-borrar-enlace-mapa="${index}" aria-label="Borrar ${xml(item.name)}">Borrar</button></div></li>`).join('');
    seasonSavedLinksList.hidden=!links.length;
  }

  function saveNamedSeasonPosterLink() {
    const name=(seasonSaveLinkName?.value||'').trim().slice(0,28);
    if(!name){if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent='Escribe un nombre breve para guardar el enlace.';seasonSaveLinkName?.focus();return;}
    const links=readSeasonSavedLinks(),url=seasonPosterLinkUrl(),existing=links.findIndex(item=>item.name.toLocaleLowerCase('es')===name.toLocaleLowerCase('es'));
    const pinned=existing>=0&&links[existing].pinned===true;
    if(existing>=0)links.splice(existing,1);
    if(links.length>=6)links.pop();
    links.unshift({name,url,pinned});
    try { saveSeasonSavedLinks(links);if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent=`Enlace «${name}» guardado en este navegador.`;if(seasonSaveLinkName)seasonSaveLinkName.value=''; }
    catch (_) { if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent='No se pudo guardar el enlace en este navegador.'; }
  }

  function applySavedSeasonPosterLink(url) {
    try {
      const parsed=new URL(url,window.location.href);
      if(parsed.pathname!==window.location.pathname)throw new Error('enlace no válido');
      clearSeasonLinkQr();
      const params=parsed.searchParams,seasons=[...seasonPosterSelect.options].map(option=>option.value),season=params.get('mapa-temporada');
      if(seasons.includes(season))seasonPosterSelect.value=season;
      updateSeasonRivalOptions();
      const rival=params.get('mapa-rival');if(!rival||[...seasonPosterRival.options].some(option=>option.value===rival))seasonPosterRival.value=rival||'';
      const datePattern=/^\d{4}-\d{2}-\d{2}$/;
      seasonPosterFrom.value=datePattern.test(params.get('mapa-desde')||'')?params.get('mapa-desde'):'';
      seasonPosterTo.value=datePattern.test(params.get('mapa-hasta')||'')?params.get('mapa-hasta'):'';
      if(['cuadrado','vertical','historias'].includes(params.get('mapa-formato')))seasonPosterFormat.value=params.get('mapa-formato');
      if(['png','webp','svg'].includes(params.get('mapa-archivo')))seasonPosterType.value=params.get('mapa-archivo');
      if(seasonPosterSheet)seasonPosterSheet.value='0';
      updateSeasonPosterPreview();
      window.history.replaceState({},'',seasonPosterLinkUrl());
      if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent='Selección aplicada al mapa.';
    } catch (_) { if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent='No se pudo aplicar este enlace guardado.'; }
  }

  function saveSeasonSavedLinks(links) {
    const ordered=links.slice().sort((a,b)=>Number(b.pinned===true)-Number(a.pinned===true)).slice(0,6);
    window.localStorage.setItem(seasonSavedLinksKey,JSON.stringify(ordered));
    renderSeasonSavedLinks();
  }

  function exportSeasonSavedLinks() {
    const payload={format:'lineadepase-mapa-links',version:1,links:readSeasonSavedLinks().map(({name,url,pinned})=>({name,url,pinned}))};
    const encoder=new TextEncoder(),json=encoder.encode(JSON.stringify(payload,null,2));
    const guide=encoder.encode('SELECCIONES GUARDADAS · LÍNEA DE PASE\n\nEste paquete contiene selecciones guardadas del mapa de temporada.\n\nPara recuperarlas:\n1. Abre el archivo visual de Línea de pase.\n2. Pulsa «Importar archivo JSON».\n3. Elige selecciones-mapa-linea-de-pase.json dentro de este ZIP.\n\nSe pueden guardar hasta seis selecciones en cada navegador. La importación combina nombres coincidentes y solo conserva los filtros admitidos por el mapa.\n');
    const blob=zipStored([{name:'selecciones-mapa-linea-de-pase.json',bytes:json},{name:'LEEME.txt',bytes:guide}]);
    saveBlob(blob,'selecciones-mapa-linea-de-pase.zip');
    if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent=`Paquete exportado: ${payload.links.length} ${payload.links.length===1?'selección':'selecciones'} y archivo de instrucciones.`;
  }

  async function seasonImportJsonText(file) {
    if(file.size>1000000)throw new Error('archivo demasiado grande');
    const bytes=new Uint8Array(await file.arrayBuffer());
    const view=new DataView(bytes.buffer,bytes.byteOffset,bytes.byteLength);
    if(bytes.length>=4&&view.getUint32(0,true)===0x04034b50){
      const decoder=new TextDecoder('utf-8'),minEocd=Math.max(0,bytes.length-65557);let eocd=-1;
      for(let offset=bytes.length-22;offset>=minEocd;offset--)if(view.getUint32(offset,true)===0x06054b50){eocd=offset;break;}
      if(eocd<0||eocd+22>bytes.length)throw new Error('ZIP no compatible');
      const entries=view.getUint16(eocd+10,true),centralSize=view.getUint32(eocd+12,true),centralOffset=view.getUint32(eocd+16,true);
      if(entries>32||centralOffset+centralSize>eocd)throw new Error('ZIP no compatible');
      let offset=centralOffset;
      for(let entry=0;entry<entries;entry++){
        if(offset+46>bytes.length||view.getUint32(offset,true)!==0x02014b50)throw new Error('ZIP no compatible');
        const flags=view.getUint16(offset+8,true),method=view.getUint16(offset+10,true),compressedSize=view.getUint32(offset+20,true),uncompressedSize=view.getUint32(offset+24,true),nameLength=view.getUint16(offset+28,true),extraLength=view.getUint16(offset+30,true),commentLength=view.getUint16(offset+32,true),localOffset=view.getUint32(offset+42,true);
        const name=decoder.decode(bytes.subarray(offset+46,offset+46+nameLength));
        offset+=46+nameLength+extraLength+commentLength;
        if(name!=='selecciones-mapa-linea-de-pase.json')continue;
        if((flags&0x0001)||![0,8].includes(method)||uncompressedSize>1000000||compressedSize>1000000)throw new Error('ZIP no compatible');
        if(localOffset+30>bytes.length||view.getUint32(localOffset,true)!==0x04034b50)throw new Error('ZIP no compatible');
        const localNameLength=view.getUint16(localOffset+26,true),localExtraLength=view.getUint16(localOffset+28,true),dataStart=localOffset+30+localNameLength+localExtraLength,dataEnd=dataStart+compressedSize;
        if(dataEnd>bytes.length)throw new Error('ZIP no compatible');
        const compressed=bytes.subarray(dataStart,dataEnd);let payload;
        if(method===0)payload=compressed;
        else {
          if(typeof DecompressionStream!=='function')throw new Error('ZIP comprimido no compatible en este navegador');
          try{payload=new Uint8Array(await new Response(new Blob([compressed]).stream().pipeThrough(new DecompressionStream('deflate-raw'))).arrayBuffer());}
          catch(_){throw new Error('ZIP comprimido no compatible en este navegador');}
        }
        if(payload.length!==uncompressedSize)throw new Error('ZIP no compatible');
        return decoder.decode(payload);
      }
      throw new Error('ZIP sin el archivo JSON de selecciones');
    }
    return new TextDecoder('utf-8').decode(bytes);
  }

  async function importSeasonSavedLinks(file) {
    if(!file)return;
    const isZip=file.name.toLocaleLowerCase('es').endsWith('.zip');
    try {
      let sourceText;
      try{sourceText=await seasonImportJsonText(file);}
      catch(error){
        const message=error instanceof Error?error.message:'';
        if(message==='archivo demasiado grande')throw new Error('El archivo supera el límite de 1 MB. Exporta una selección más pequeña y vuelve a intentarlo.');
        if(message==='ZIP sin el archivo JSON de selecciones')throw new Error('El ZIP no incluye el archivo de selecciones esperado. Comprueba que sea una exportación de Línea de pase.');
        if(message==='ZIP comprimido no compatible en este navegador')throw new Error('Este navegador no puede abrir este ZIP comprimido. Vuelve a exportar las selecciones en JSON desde la web.');
        if(message==='ZIP no compatible')throw new Error('El ZIP está incompleto o usa una compresión que no se puede abrir. Vuelve a exportarlo desde la web.');
        throw new Error('No se pudo leer el archivo seleccionado. Comprueba que sea un JSON o ZIP válido.');
      }
      let payload;
      try{payload=JSON.parse(sourceText);}
      catch(_){throw new Error(isZip?'El ZIP contiene un JSON incompleto o dañado. Vuelve a exportar el paquete.':'El JSON está incompleto o dañado. Guarda una nueva exportación y vuelve a intentarlo.');}
      if(payload?.format!=='lineadepase-mapa-links')throw new Error('El archivo no tiene el formato de selecciones de Línea de pase.');
      if(payload?.version!==1)throw new Error('Esta versión del archivo todavía no se puede importar. Exporta una copia nueva desde la web.');
      if(!Array.isArray(payload.links))throw new Error('El archivo no contiene una lista válida de selecciones.');
      const links=readSeasonSavedLinks();let imported=0,updated=0,skipped=0;
      payload.links.forEach(item=>{
        if(!item||typeof item.name!=='string'||typeof item.url!=='string'){skipped++;return;}
        let parsed;try{parsed=new URL(item.url,window.location.href);}catch(_){skipped++;return;}
        if(parsed.pathname!==window.location.pathname){skipped++;return;}
        const name=item.name.trim().slice(0,28);if(!name){skipped++;return;}
        const localUrl=new URL(window.location.pathname,window.location.origin);
        for(const key of ['mapa-temporada','mapa-rival','mapa-desde','mapa-hasta','mapa-formato','mapa-archivo']){const value=parsed.searchParams.get(key);if(value)localUrl.searchParams.set(key,value);}
        const existing=links.findIndex(link=>link.name.toLocaleLowerCase('es')===name.toLocaleLowerCase('es'));
        const entry={name,url:localUrl.href,pinned:item.pinned===true};
        if(existing>=0){links.splice(existing,1,entry);updated++;}else if(links.length<6){links.push(entry);imported++;}else{skipped++;}
      });
      saveSeasonSavedLinks(links);
      if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent=`Importación terminada: ${imported} nuevas, ${updated} actualizadas, ${skipped} omitidas; límite de seis selecciones.`;
    } catch(error){if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent=error instanceof Error?error.message:'No se pudo leer el archivo. Comprueba el formato y vuelve a intentarlo.';}
    if(seasonImportLinksFile)seasonImportLinksFile.value='';
  }

  function makeSeasonLinkQr() {
    try {
      if(!window.qrcodegen?.QrCode)throw new Error('QR no disponible');
      const qr=window.qrcodegen.QrCode.encodeText(seasonPosterLinkUrl(),window.qrcodegen.QrCode.Ecc.MEDIUM),quiet=4,module=8,size=(qr.size+quiet*2)*module;
      const label=(seasonQrName?.value||'').trim().slice(0,28),labelHeight=label?48:0,height=size+labelHeight;
      const color=seasonQrColor?.value==='marca'?'#2f6b45':'#15221b';
      const printSize=seasonQrPrintSize?.value||'px',svgWidth=printSize==='40mm'?'40mm':printSize==='60mm'?'60mm':`${size}px`,svgHeight=printSize==='40mm'?`${40*height/size}mm`:printSize==='60mm'?`${60*height/size}mm`:`${height}px`;
      let path='';
      for(let y=0;y<qr.size;y++)for(let x=0;x<qr.size;x++)if(qr.getModule(x,y))path+=`M${(x+quiet)*module} ${(y+quiet)*module}h${module}v${module}h-${module}z`;
      seasonQrSvg=`<svg xmlns="http://www.w3.org/2000/svg" width="${svgWidth}" height="${svgHeight}" viewBox="0 0 ${size} ${height}" role="img" aria-label="Código QR para abrir la selección del mapa"><rect width="100%" height="100%" fill="#fff"/><path d="${path}" fill="${color}"/>${label?`<text x="${size/2}" y="${size+32}" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" font-weight="700" fill="#15221b">${xml(label)}</text>`:''}</svg>`;
      if(seasonQrObjectUrl)URL.revokeObjectURL(seasonQrObjectUrl);
      if(seasonQrPreview){seasonQrObjectUrl=URL.createObjectURL(new Blob([seasonQrSvg],{type:'image/svg+xml'}));seasonQrPreview.src=seasonQrObjectUrl;seasonQrPreview.hidden=false;if(seasonQrPreview.parentElement)seasonQrPreview.parentElement.hidden=false;}
      if(seasonQrDownloadButton)seasonQrDownloadButton.disabled=false;
      if(seasonQrCopyButton)seasonQrCopyButton.disabled=false;
      updateSeasonQrQuality();
      if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent='QR listo: contiene solo el enlace de esta selección y se genera en este navegador.';
    } catch(_){if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent='No se pudo generar el QR en este navegador.';}
  }

  function downloadSeasonLinkQr() {
    if(!seasonQrSvg)return;
    saveBlob(new Blob([seasonQrSvg],{type:'image/svg+xml;charset=utf-8'}),'seleccion-mapa-linea-de-pase-qr.svg');
    if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent='QR descargado en SVG.';
  }

  function seasonQrColorHex() { return seasonQrColor?.value==='marca'?'#2f6b45':'#15221b'; }
  function seasonQrPaperIsSoft() { return seasonQrPaperSelect?.value==='suave'; }

  function updateSeasonQrQuality() {
    const status=document.querySelector('[data-calidad-qr]');if(!status)return;
    const hex=seasonQrColorHex(),channels=hex.match(/[0-9a-f]{2}/gi)?.map(value=>parseInt(value,16)/255)||[0,0,0];
    const luminance=channels.map(value=>value<=.04045?value/12.92:((value+.055)/1.055)**2.4).reduce((sum,value,index)=>sum+value*[.2126,.7152,.0722][index],0);
    const ratio=1.05/(luminance+.05),good=ratio>=4.5;
    status.dataset.nivel=good?'correcto':'aviso';
    status.textContent=`Contraste ${ratio.toFixed(2).replace('.',',')}:1 sobre blanco · margen libre de 4 módulos. ${good?'Correcto para compartir e imprimir.':'Elige tinta oscura para mejorar la lectura.'}`;
  }

  function updateSeasonQrPrintPreview() {
    if(!seasonQrA4Preview)return;
    try {
      const qr=seasonQrMatrix(),color=seasonQrColorHex(),view=qr.size+8,path=[],paper=seasonQrPaperIsSoft()?'suave':'blanco';
      for(let y=0;y<qr.size;y++)for(let x=0;x<qr.size;x++)if(qr.getModule(x,y))path.push(`M${x+4} ${y+4}h1v1h-1z`);
      const svg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${view} ${view}" role="img" aria-label="Código QR con margen de cuatro módulos"><rect width="${view}" height="${view}" fill="#fff"/><path d="${path.join('')}" fill="${color}"/></svg>`;
      seasonQrPreviewDisclosure?.querySelectorAll('[data-qr-hoja-codigo]').forEach(node=>{node.innerHTML=svg;});
      const name=(seasonQrName?.value||'').trim();
      const title=seasonQrA4Preview.querySelector('[data-qr-hoja-titulo]');if(title)title.textContent=name||'Selección actual del mapa';
      if(seasonQrA4HorizontalPreview){seasonQrA4HorizontalPreview.dataset.papel=paper;const horizontalTitle=seasonQrA4HorizontalPreview.querySelector('[data-qr-hoja-horizontal-titulo]');if(horizontalTitle)horizontalTitle.textContent=name||'Mapa de temporada';}
      seasonQrA4Preview.dataset.estado='lista';seasonQrA4Preview.dataset.papel=paper;
      ['a','b'].forEach(side=>{
        const row=rounds.get(side==='a'?selectA?.value:selectB?.value),heading=seasonQrA4HorizontalPreview?.querySelector(`[data-qr-hoja-partido-titulo="${side}"]`),score=seasonQrA4HorizontalPreview?.querySelector(`[data-qr-hoja-partido-marcador="${side}"]`),venue=seasonQrA4HorizontalPreview?.querySelector(`[data-qr-hoja-partido-sede="${side}"]`);
        if(!row){if(heading)heading.textContent=side==='a'?'Primera jornada':'Segunda jornada';if(score)score.textContent='Selecciona una jornada disponible';if(venue)venue.textContent='';return;}
        const home=row.dataset.sede==='Casa'?'Real Zaragoza':row.dataset.rival,away=row.dataset.sede==='Casa'?row.dataset.rival:'Real Zaragoza',homeGoals=row.dataset.sede==='Casa'?row.dataset.golesZaragoza:row.dataset.golesRival,awayGoals=row.dataset.sede==='Casa'?row.dataset.golesRival:row.dataset.golesZaragoza;
        if(heading)heading.textContent=`J${row.dataset.jornada.padStart(2,'0')} · ${row.dataset.fechaPartido.split('-').reverse().join('/')}`;
        if(score)score.textContent=`${home} ${homeGoals} – ${awayGoals} ${away}`;
        if(venue)venue.textContent=`${row.dataset.sede==='Casa'?'En casa':'Fuera'} · ${row.dataset.rival}`;
      });
    } catch(_){
      seasonQrA4Preview.dataset.estado='error';
      seasonQrA4Preview.querySelectorAll('[data-qr-hoja-codigo]').forEach(node=>{node.textContent='Vista previa disponible al cargar el código QR.';});
    }
  }

  function seasonQrMatrix() {
    if(!window.qrcodegen?.QrCode)throw new Error('QR no disponible');
    return window.qrcodegen.QrCode.encodeText(seasonPosterLinkUrl(),window.qrcodegen.QrCode.Ecc.MEDIUM);
  }

  function downloadSeasonQrA4() {
    try {
      const qr=seasonQrMatrix(),pageW=595.28,pageH=841.89,ink=seasonQrColorHex(),rgb=ink.match(/[0-9a-f]{2}/gi).map(v=>(parseInt(v,16)/255).toFixed(4)).join(' '),parts=seasonQrPaperIsSoft()?['0.97 0.98 0.96 rg 0 0 595.28 841.89 re f']:[];
      parts.push('0.18 0.42 0.27 rg 42 777 38 3 re f');
      const label=(seasonQrName?.value||'').trim().slice(0,28).normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^\x20-\x7e]/g,'');
      const pdfText=value=>value.replace(/\\/g,'\\\\').replace(/\(/g,'\\(').replace(/\)/g,'\\)');
      parts.push('0.18 0.42 0.27 rg BT /F2 9 Tf 42 754 Td (LINEA DE PASE  /  ARCHIVO VISUAL) Tj ET','0.08 0.13 0.10 rg BT /F2 21 Tf 42 720 Td (Una temporada, dos formas de verla) Tj ET','0.30 0.36 0.32 rg BT /F1 10 Tf 42 699 Td (Escanea el codigo para abrir la seleccion actual del mapa.) Tj ET');
      if(label)parts.push(`0.18 0.42 0.27 rg BT /F2 10 Tf 42 679 Td (${pdfText(label)}) Tj ET`);
      if(seasonQrPaperIsSoft())parts.push('0.92 0.95 0.92 rg 42 403 248 264 re f','0.92 0.95 0.92 rg 305 403 248 264 re f');
      else parts.push('0.72 0.80 0.74 RG 0.8 w 42 403 248 264 re S','0.72 0.80 0.74 RG 0.8 w 305 403 248 264 re S');
      parts.push('0.18 0.42 0.27 rg BT /F2 9 Tf 58 644 Td (GRAN FORMATO) Tj ET','0.18 0.42 0.27 rg BT /F2 9 Tf 321 644 Td (FORMATO COMPACTO) Tj ET');
      const draw=(mm,centerX,topY,caption)=>{
        const points=mm*72/25.4,total=qr.size+8,unit=points/total,x0=centerX-points/2,y0=pageH-topY-points;
        parts.push(`1 1 1 rg ${x0.toFixed(2)} ${y0.toFixed(2)} ${points.toFixed(2)} ${points.toFixed(2)} re f`,`${rgb} rg`);
        for(let y=0;y<qr.size;y++)for(let x=0;x<qr.size;x++)if(qr.getModule(x,y))parts.push(`${(x0+(x+4)*unit).toFixed(3)} ${(y0+(qr.size-y+3)*unit).toFixed(3)} ${unit.toFixed(3)} ${unit.toFixed(3)} re f`);
        parts.push(`0.08 0.13 0.10 rg BT /F2 13 Tf ${(centerX-25).toFixed(2)} ${(y0-27).toFixed(2)} Td (${caption}) Tj ET`);
      };
      draw(60,166,206,'60 mm');draw(40,429,206,'40 mm');
      parts.push('0.30 0.36 0.32 rg BT /F1 10 Tf 42 374 Td (Mismo enlace, dos tamanos para elegir segun el soporte.) Tj ET','0.18 0.42 0.27 rg BT /F2 11 Tf 42 342 Td (IMPORTANTE  /  IMPRIME A TAMANO REAL) Tj ET','0.30 0.36 0.32 rg BT /F1 9 Tf 42 324 Td (En el cuadro de impresion selecciona 100 % o escala real; desactiva "Ajustar a pagina".) Tj ET','0.68 0.74 0.69 RG 0.7 w 42 300 m 553 300 l S','0.30 0.36 0.32 rg BT /F1 9 Tf 42 280 Td (La zona blanca alrededor de cada codigo forma parte del margen de lectura.) Tj ET');
      const content=parts.join('\n'),objects=[
        '<< /Type /Catalog /Pages 2 0 R >>',
        '<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
        `<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${pageW} ${pageH}] /Resources << /Font << /F1 4 0 R /F2 6 0 R >> >> /Contents 5 0 R >>`,
        '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
        `<< /Length ${new TextEncoder().encode(content).length} >>\nstream\n${content}\nendstream`,
        '<< /Type /Font /Subtype /Type1 /BaseFont /Times-Bold >>'
      ];
      let pdf='%PDF-1.4\n',offsets=[0];
      objects.forEach((object,index)=>{offsets.push(new TextEncoder().encode(pdf).length);pdf+=`${index+1} 0 obj\n${object}\nendobj\n`;});
      const xref=new TextEncoder().encode(pdf).length;pdf+=`xref\n0 ${objects.length+1}\n0000000000 65535 f \n`+offsets.slice(1).map(value=>`${String(value).padStart(10,'0')} 00000 n \n`).join('')+`trailer\n<< /Size ${objects.length+1} /Root 1 0 R >>\nstartxref\n${xref}\n%%EOF`;
      saveBlob(new Blob([pdf],{type:'application/pdf'}),'qr-linea-de-pase-a4.pdf');
      if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent=`Hoja A4 descargada en papel ${seasonQrPaperIsSoft()?'verde suave':'blanco'}; imprime al 100 % para conservar las medidas.`;
    } catch(_){if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent='No se pudo preparar la hoja A4 en este navegador.';}
  }

  function downloadSeasonQrA5() {
    try {
      const qr=seasonQrMatrix(),pageW=419.53,pageH=595.28,ink=seasonQrColorHex(),rgb=ink.match(/[0-9a-f]{2}/gi).map(v=>(parseInt(v,16)/255).toFixed(4)).join(' '),parts=seasonQrPaperIsSoft()?['0.97 0.98 0.96 rg 0 0 419.53 595.28 re f']:[];
      const text=value=>value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^\x20-\x7e]/g,'').replace(/\\/g,'\\\\').replace(/\(/g,'\\(').replace(/\)/g,'\\)').slice(0,72);
      const name=(seasonQrName?.value||'').trim();
      parts.push('0.18 0.42 0.27 rg 34 551 32 3 re f','0.18 0.42 0.27 rg BT /F2 9 Tf 34 530 Td (LINEA DE PASE  /  ARCHIVO VISUAL) Tj ET','0.08 0.13 0.10 rg BT /F2 19 Tf 34 497 Td (Una temporada, dos formas de verla) Tj ET',`0.30 0.36 0.32 rg BT /F1 10 Tf 34 475 Td (${text(name||'Mapa de temporada')}) Tj ET`);
      if(seasonQrPaperIsSoft())parts.push('0.92 0.95 0.92 rg 34 182 351 262 re f');else parts.push('0.72 0.80 0.74 RG 0.8 w 34 182 351 262 re S');
      parts.push('0.18 0.42 0.27 rg BT /F2 9 Tf 52 414 Td (QR PARA ABRIR EL MAPA) Tj ET');
      const mm=60,points=mm*72/25.4,total=qr.size+8,unit=points/total,x0=(pageW-points)/2,y0=pageH-207-points;
      parts.push(`1 1 1 rg ${x0.toFixed(2)} ${y0.toFixed(2)} ${points.toFixed(2)} ${points.toFixed(2)} re f`,`${rgb} rg`);
      for(let y=0;y<qr.size;y++)for(let x=0;x<qr.size;x++)if(qr.getModule(x,y))parts.push(`${(x0+(x+4)*unit).toFixed(3)} ${(y0+(qr.size-y+3)*unit).toFixed(3)} ${unit.toFixed(3)} ${unit.toFixed(3)} re f`);
      parts.push('0.08 0.13 0.10 rg BT /F2 12 Tf 182 185 Td (QR de 60 mm) Tj ET','0.30 0.36 0.32 rg BT /F1 9 Tf 34 146 Td (Imprime a tamano real o al 100 % para mantener la medida.) Tj ET','0.68 0.74 0.69 RG 0.7 w 34 126 m 385 126 l S','0.30 0.36 0.32 rg BT /F1 9 Tf 34 105 Td (El margen blanco forma parte del codigo y facilita su lectura.) Tj ET');
      const content=parts.join('\n'),objects=['<< /Type /Catalog /Pages 2 0 R >>','<< /Type /Pages /Kids [3 0 R] /Count 1 >>',`<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${pageW} ${pageH}] /Resources << /Font << /F1 4 0 R /F2 6 0 R >> >> /Contents 5 0 R >>`,'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',`<< /Length ${new TextEncoder().encode(content).length} >>\nstream\n${content}\nendstream`,'<< /Type /Font /Subtype /Type1 /BaseFont /Times-Bold >>'];
      let pdf='%PDF-1.4\n',offsets=[0];objects.forEach((object,index)=>{offsets.push(new TextEncoder().encode(pdf).length);pdf+=`${index+1} 0 obj\n${object}\nendobj\n`;});
      const xref=new TextEncoder().encode(pdf).length;pdf+=`xref\n0 ${objects.length+1}\n0000000000 65535 f \n`+offsets.slice(1).map(value=>`${String(value).padStart(10,'0')} 00000 n \n`).join('')+`trailer\n<< /Size ${objects.length+1} /Root 1 0 R >>\nstartxref\n${xref}\n%%EOF`;
      saveBlob(new Blob([pdf],{type:'application/pdf'}),'qr-linea-de-pase-a5.pdf');
      if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent=`Hoja A5 descargada (${(new Blob([pdf]).size/1024).toFixed(1)} KB) en papel ${seasonQrPaperIsSoft()?'verde suave':'blanco'}; QR de 60 mm.`;
    } catch(_){if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent='No se pudo preparar la hoja A5 en este navegador.';}
  }

  function downloadSeasonQrLandscapeA4() {
    try {
      const qr=seasonQrMatrix(),pageW=841.89,pageH=595.28,ink=seasonQrColorHex(),rgb=ink.match(/[0-9a-f]{2}/gi).map(v=>(parseInt(v,16)/255).toFixed(4)).join(' '),parts=seasonQrPaperIsSoft()?['0.97 0.98 0.96 rg 0 0 841.89 595.28 re f']:[];
      const ascii=value=>value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^\x20-\x7e]/g,'').replace(/\\/g,'\\\\').replace(/\(/g,'\\(').replace(/\)/g,'\\)').slice(0,72);
      const label=(seasonQrName?.value||'').trim().slice(0,28),name=label?ascii(label):'MAPA DE TEMPORADA';
      parts.push('0.18 0.42 0.27 rg 42 555 38 3 re f','BT /F2 9 Tf 42 536 Td (LINEA DE PASE  /  ARCHIVO VISUAL) Tj ET','0.08 0.13 0.10 rg BT /F2 21 Tf 42 504 Td (Dos jornadas, una lectura) Tj ET',`0.30 0.36 0.32 rg BT /F1 10 Tf 42 484 Td (${ascii(name)}) Tj ET`);
      const qrPoints=60*72/25.4,total=qr.size+8,unit=qrPoints/total,x0=157-qrPoints/2,y0=pageH-156-qrPoints;
      parts.push(`0.18 0.42 0.27 rg BT /F2 9 Tf 57 451 Td (CODIGO DEL MAPA) Tj ET`,`1 1 1 rg ${x0.toFixed(2)} ${y0.toFixed(2)} ${qrPoints.toFixed(2)} ${qrPoints.toFixed(2)} re f`,`${rgb} rg`);
      for(let y=0;y<qr.size;y++)for(let x=0;x<qr.size;x++)if(qr.getModule(x,y))parts.push(`${(x0+(x+4)*unit).toFixed(3)} ${(y0+(qr.size-y+3)*unit).toFixed(3)} ${unit.toFixed(3)} ${unit.toFixed(3)} re f`);
      parts.push('0.30 0.36 0.32 rg BT /F1 9 Tf 85 223 Td (Escanea para abrir el mapa actual.) Tj ET','0.18 0.42 0.27 rg BT /F2 9 Tf 302 451 Td (MARCADORES DE LA COMPARACION) Tj ET');
      ['a','b'].forEach((side,index)=>{
        const row=rounds.get(side==='a'?selectA?.value:selectB?.value),cardY=index===0?276:112,headingY=cardY+91,scoreY=cardY+53,venueY=cardY+28;
        if(seasonQrPaperIsSoft())parts.push(`0.92 0.95 0.92 rg 298 ${cardY} 502 142 re f`);else parts.push(`0.72 0.80 0.74 RG 0.8 w 298 ${cardY} 502 142 re S`);
        if(!row){parts.push(`0.08 0.13 0.10 rg BT /F2 12 Tf 316 ${scoreY} Td (Selecciona dos jornadas para ver los marcadores.) Tj ET`);return;}
        const date=row.dataset.fechaPartido.split('-').reverse().join('/'),home=row.dataset.sede==='Casa'?'Real Zaragoza':row.dataset.rival,away=row.dataset.sede==='Casa'?row.dataset.rival:'Real Zaragoza',homeGoals=row.dataset.sede==='Casa'?row.dataset.golesZaragoza:row.dataset.golesRival,awayGoals=row.dataset.sede==='Casa'?row.dataset.golesRival:row.dataset.golesZaragoza;
        parts.push(`0.18 0.42 0.27 rg BT /F2 9 Tf 316 ${headingY} Td (${ascii(`J${row.dataset.jornada.padStart(2,'0')}  /  ${row.dataset.rival}  /  ${date}`)}) Tj ET`,`0.08 0.13 0.10 rg BT /F2 16 Tf 316 ${scoreY} Td (${ascii(`${home}   ${homeGoals} - ${awayGoals}   ${away}`)}) Tj ET`,`0.30 0.36 0.32 rg BT /F1 9 Tf 316 ${venueY} Td (${row.dataset.sede==='Casa'?'En casa':'Fuera'}  /  ${ascii(row.dataset.rival)}) Tj ET`);
      });
      parts.push('0.30 0.36 0.32 rg BT /F1 9 Tf 42 62 Td (QR de 60 mm con margen de lectura. Imprime a tamano real o al 100 %.) Tj ET','0.18 0.42 0.27 rg BT /F2 9 Tf 614 62 Td (PAPEL A4  /  297 x 210 mm) Tj ET');
      const content=parts.join('\n'),objects=['<< /Type /Catalog /Pages 2 0 R >>','<< /Type /Pages /Kids [3 0 R] /Count 1 >>',`<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${pageW} ${pageH}] /Resources << /Font << /F1 4 0 R /F2 6 0 R >> >> /Contents 5 0 R >>`,'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',`<< /Length ${new TextEncoder().encode(content).length} >>\nstream\n${content}\nendstream`,'<< /Type /Font /Subtype /Type1 /BaseFont /Times-Bold >>'];
      let pdf='%PDF-1.4\n',offsets=[0];objects.forEach((object,index)=>{offsets.push(new TextEncoder().encode(pdf).length);pdf+=`${index+1} 0 obj\n${object}\nendobj\n`;});
      const xref=new TextEncoder().encode(pdf).length;pdf+=`xref\n0 ${objects.length+1}\n0000000000 65535 f \n`+offsets.slice(1).map(value=>`${String(value).padStart(10,'0')} 00000 n \n`).join('')+`trailer\n<< /Size ${objects.length+1} /Root 1 0 R >>\nstartxref\n${xref}\n%%EOF`;
      saveBlob(new Blob([pdf],{type:'application/pdf'}),'qr-y-comparacion-linea-de-pase-a4-apaisado.pdf');
      if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent=`Hoja A4 apaisada descargada en papel ${seasonQrPaperIsSoft()?'verde suave':'blanco'}; los resultados corresponden a las dos jornadas elegidas.`;
    } catch(_){if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent='No se pudo preparar la hoja apaisada en este navegador.';}
  }

  async function copySeasonLinkQr() {
    if(!seasonQrSvg)return;
    try {
      if(!navigator.clipboard?.write||!window.ClipboardItem)throw new Error('portapapeles no disponible');
      const png=await svgToRaster(seasonQrSvg,'image/png');
      await navigator.clipboard.write([new ClipboardItem({'image/png':png})]);
      if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent='Imagen QR copiada al portapapeles.';
    } catch(_){if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent='Este navegador no permite copiar la imagen QR; puedes descargar el SVG.';}
  }

  function clearSeasonLinkQr() {
    seasonQrSvg='';
    if(seasonQrObjectUrl){URL.revokeObjectURL(seasonQrObjectUrl);seasonQrObjectUrl='';}
    if(seasonQrPreview){seasonQrPreview.removeAttribute('src');seasonQrPreview.hidden=true;if(seasonQrPreview.parentElement)seasonQrPreview.parentElement.hidden=true;}
    if(seasonQrDownloadButton)seasonQrDownloadButton.disabled=true;
    if(seasonQrCopyButton)seasonQrCopyButton.disabled=true;
    updateSeasonQrPrintPreview();
  }

  function restoreSeasonPosterFromUrl() {
    if(!seasonPosterSelect)return;
    const params=new URLSearchParams(window.location.search), seasons=[...seasonPosterSelect.options].map(option=>option.value);
    const season=params.get('mapa-temporada');if(seasons.includes(season))seasonPosterSelect.value=season;
    updateSeasonRivalOptions();
    const rival=params.get('mapa-rival');if(rival&&[...seasonPosterRival.options].some(option=>option.value===rival))seasonPosterRival.value=rival;
    const datePattern=/^\d{4}-\d{2}-\d{2}$/;
    if(datePattern.test(params.get('mapa-desde')||''))seasonPosterFrom.value=params.get('mapa-desde');
    if(datePattern.test(params.get('mapa-hasta')||''))seasonPosterTo.value=params.get('mapa-hasta');
    if(['cuadrado','vertical','historias'].includes(params.get('mapa-formato')))seasonPosterFormat.value=params.get('mapa-formato');
    if(['png','webp','svg'].includes(params.get('mapa-archivo')))seasonPosterType.value=params.get('mapa-archivo');
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
    seasonPosterPreview.src=`data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg||`<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080"><rect width="100%" height="100%" fill="#f4f1e8"/><text x="540" y="540" text-anchor="middle" font-family="Arial" font-size="32">No hay partidos para estos filtros</text></svg>`)}`;
    seasonPosterPreview.alt=alt;
    if(seasonPosterPreviewCaption)seasonPosterPreviewCaption.textContent=pages.length?`Vista previa · lámina ${pageIndex+1} de ${pages.length} · ${format==='cuadrado'?'1080 × 1080':format==='vertical'?'1080 × 1350':'1080 × 1920'}`:'Vista previa · sin partidos para los filtros elegidos';
    updateSeasonForm();
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

  function seasonCarouselSvg(season,kind,format='cuadrado') {
    const all=seasonPosterRows(season,false), subset=kind==='global'?all:all.filter(row=>row.dataset.sede===(kind==='casa'?'Casa':'Fuera'));
    const palette=activePalette(), counts=subset.reduce((c,row)=>{c[posterOutcome(row).label]++;return c;},{VICTORIA:0,EMPATE:0,DERROTA:0});
    const totals=all.reduce((c,row)=>{const key=row.dataset.sede==='Casa'?'casa':'fuera';c[key][posterOutcome(row).label]++;return c;},{casa:{VICTORIA:0,EMPATE:0,DERROTA:0},fuera:{VICTORIA:0,EMPATE:0,DERROTA:0}});
    const specs={
      cuadrado:{width:1080,height:1080,safeTop:0,safeBottom:0,bandTop:0,bandHeight:390,brandY:76,titleY:158,seasonY:212,summaryY:296,noteY:350,startY:510,gap:54,footerY:1035,font:22},
      vertical:{width:1080,height:1350,safeTop:0,safeBottom:0,bandTop:0,bandHeight:450,brandY:76,titleY:166,seasonY:222,summaryY:320,noteY:378,startY:545,gap:62,footerY:1305,font:22},
      historias:{width:1080,height:1920,safeTop:260,safeBottom:260,bandTop:260,bandHeight:520,brandY:338,titleY:422,seasonY:480,summaryY:585,noteY:640,startY:770,gap:82,footerY:1600,font:26}
    };
    const spec=specs[format]||specs.cuadrado, {width,height,safeTop,safeBottom,bandTop,bandHeight,brandY,titleY,seasonY,summaryY,noteY,startY,gap,footerY,font}=spec;
    const title=kind==='global'?'Balance de temporada':kind==='casa'?'El Zaragoza en casa':'El Zaragoza fuera';
    const maxRows=Math.max(0,Math.floor((footerY-startY-28)/gap)), rowsToShow=kind==='global'?[]:subset.slice().reverse().slice(-maxRows).reverse();
    const cards=rowsToShow.map((row,index)=>{const y=startY+index*gap,out=posterOutcome(row),description=row.dataset.sede==='Casa'?row.dataset.rival:`${row.dataset.rival} · fuera`;return `<text x="78" y="${y}" fill="${palette.foreground}" font-family="Arial,sans-serif" font-size="${font}" font-weight="700">J${row.dataset.jornada.padStart(2,'0')}</text><text x="205" y="${y}" fill="${palette.foreground}" font-family="Arial,sans-serif" font-size="${font}">${xml(description)}</text><text x="1002" y="${y}" text-anchor="end" fill="${out.color}" font-family="Arial,sans-serif" font-size="${font+1}" font-weight="800">${row.dataset.golesZaragoza}–${row.dataset.golesRival}</text>`;}).join('');
    const summary=`${counts.VICTORIA} victorias · ${counts.EMPATE} empates · ${counts.DERROTA} derrotas`;
    const homeAwaySummary=`Casa ${totals.casa.VICTORIA}V–${totals.casa.EMPATE}E–${totals.casa.DERROTA}D · Fuera ${totals.fuera.VICTORIA}V–${totals.fuera.EMPATE}E–${totals.fuera.DERROTA}D`;
    const note=kind==='global'?homeAwaySummary:`Balance sobre ${subset.length} partidos: ${summary}${subset.length>rowsToShow.length?` · últimos ${rowsToShow.length} de ${subset.length}`:''}`;
    const rowAlt=rowsToShow.map(row=>`J${row.dataset.jornada} ${row.dataset.sede.toLowerCase()} ante ${row.dataset.rival} ${row.dataset.golesZaragoza}–${row.dataset.golesRival}`).join('; ');
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="t d"><title id="t">${xml(title)} · ${xml(season)}</title><desc id="d">${xml(title)}. ${xml(summary)}. ${xml(note)}. ${xml(rowAlt)}. Zona segura de historias: ${safeTop} píxeles arriba y ${safeBottom} abajo.</desc><rect width="${width}" height="${height}" fill="${palette.background}"/><path d="M0 ${bandTop}h${width}v${bandHeight}H0z" fill="${palette.header}"/><text x="64" y="${brandY}" fill="${palette.brand}" font-family="Arial,sans-serif" font-size="18" font-weight="700" letter-spacing="3">LÍNEA DE PASE · REAL ZARAGOZA</text><text x="64" y="${titleY}" fill="${palette.headerText}" font-family="Arial,sans-serif" font-size="44" font-weight="800">${xml(title)}</text><text x="64" y="${seasonY}" fill="${palette.contextHeader}" font-family="Arial,sans-serif" font-size="28">${xml(season)} · ${subset.length} partidos</text><text x="64" y="${summaryY}" fill="${palette.headerText}" font-family="Arial,sans-serif" font-size="27" font-weight="700">${xml(summary)}</text><text x="64" y="${noteY}" fill="${palette.contextHeader}" font-family="Arial,sans-serif" font-size="21">${xml(note)}</text>${cards||`<text x="64" y="${startY}" fill="${palette.muted}" font-family="Arial,sans-serif" font-size="24">${all.length} resultados publicados en la temporada.</text>`}<text x="64" y="${footerY}" fill="${palette.muted}" font-family="Arial,sans-serif" font-size="18">Resultados publicados · lineadepase.com</text></svg>`;
  }

  async function downloadSeasonCarousel() {
    const season=seasonPosterSelect?.value, type=seasonPosterType?.value||'webp', format=seasonPosterFormat?.value||'cuadrado', safeSeason=season.replace(/[^0-9a-z]+/gi,'-').replace(/^-|-$/g,''), files=[];
    for(const kind of ['global','casa','fuera']){const svg=seasonCarouselSvg(season,kind,format),blob=type==='svg'?new Blob([svg],{type:'image/svg+xml;charset=utf-8'}):await svgToRaster(svg,type==='webp'?'image/webp':'image/png');if(type==='webp'&&blob.type!=='image/webp')throw new Error('Este navegador no ofrece exportación WebP.');files.push({name:`${kind==='global'?'balance-global':kind==='casa'?'en-casa':'fuera'}-${format}.${type}`,bytes:new Uint8Array(await blob.arrayBuffer())});}
    const zip=zipStored(files);saveBlob(zip,`carrusel-temporada-${safeSeason}-${format}-${type}.zip`);if(seasonPosterStatus)seasonPosterStatus.textContent=`Carrusel de 3 láminas ${format} descargado · ${(zip.size/1024).toFixed(1)} KB.`;
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

  function printPageSettings() {
    const landscape=printOrientationSelect?.value==='apaisado',photo=printPaperSelect?.value==='fotografico';
    return {landscape,photo,width:landscape?297:210,height:landscape?210:297,margin:photo?6:10};
  }

  function savePrintSettings() {
    try {
      localStorage.setItem(printSettingsKey,JSON.stringify({
        orientation:printOrientationSelect?.value==='apaisado'?'apaisado':'vertical',
        paper:printPaperSelect?.value==='fotografico'?'fotografico':'normal',
        variant:['cuadrado','vertical','historias'].includes(contactSheetVariantSelect?.value)?contactSheetVariantSelect.value:'todos',
        a5Mode:['monocromo','fotocopia'].includes(comparisonA5InkSelect?.value)?comparisonA5InkSelect.value:'color'
      }));
    } catch (_) {}
  }

  function restorePrintSettings() {
    try {
      const saved=JSON.parse(localStorage.getItem(printSettingsKey)||'null');
      if(!saved)return;
      if(printOrientationSelect&&['vertical','apaisado'].includes(saved.orientation))printOrientationSelect.value=saved.orientation;
      if(printPaperSelect&&['normal','fotografico'].includes(saved.paper))printPaperSelect.value=saved.paper;
      if(contactSheetVariantSelect&&['todos','cuadrado','vertical','historias'].includes(saved.variant))contactSheetVariantSelect.value=saved.variant;
      if(comparisonA5InkSelect&&['color','monocromo','fotocopia'].includes(saved.a5Mode))comparisonA5InkSelect.value=saved.a5Mode;
    } catch (_) {}
  }

  function clearPrintSettings() {
    if(printOrientationSelect)printOrientationSelect.value='vertical';
    if(printPaperSelect)printPaperSelect.value='normal';
    if(contactSheetVariantSelect)contactSheetVariantSelect.value='todos';
    if(comparisonA5InkSelect)comparisonA5InkSelect.value='color';
    try { localStorage.removeItem(printSettingsKey); } catch (_) {}
    updateContactSheetPrintPreview();
    updateA5PrintPreview();
    if(printSettingsStatus)printSettingsStatus.textContent='Preferencias de impresión restauradas.';
  }

  function printablePage(svg,width,height) {
    const source=new DOMParser().parseFromString(svg,'image/svg+xml'),inner=source.querySelector('svg'),title=inner?.querySelector(':scope > title')?.textContent?.trim()||'Documento visual imprimible · Línea de pase',description=inner?.querySelector(':scope > desc')?.textContent?.trim()||'Composición gráfica en formato '+width+' × '+height+' mm.',escape=value=>value.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}mm" height="${height}mm" viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="pagina-imprimible-titulo pagina-imprimible-descripcion"><title id="pagina-imprimible-titulo">${escape(title)}</title><desc id="pagina-imprimible-descripcion">${escape(description)}</desc><rect width="${width}" height="${height}" fill="#fff"/>${svg}</svg>`;
  }

  function updateContactSheetPrintPreview() {
    if(!contactSheetPrintPreview)return;
    try {
      const svg=buildPrintableContactSheet(true);
      contactSheetPrintPreview.src=`data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
      const {landscape,photo}=printPageSettings(),variant=contactSheetVariantSelect?.value||'todos',variantLabel=variant==='todos'?'tres formatos':variant==='historias'?'historias':variant;
      contactSheetPrintPreview.alt=`Vista previa de hoja A4 ${landscape?'apaisada':'vertical'} para papel ${photo?'fotográfico':'normal'}, con ${variantLabel} y marcas de corte.`;
      if(contactSheetPrintPreviewCaption)contactSheetPrintPreviewCaption.textContent=`A4 ${landscape?'apaisada':'vertical'} · ${variantLabel} · ${photo?'fotográfico, margen de 6 mm':'normal, margen de 10 mm'}`;
    } catch (_) {
      contactSheetPrintPreview.removeAttribute('src');
      if(contactSheetPrintPreviewCaption)contactSheetPrintPreviewCaption.textContent='Selecciona dos jornadas para ver la maqueta de impresión.';
    }
  }

  function updateA5PrintPreview() {
    if(!comparisonA5PrintPreview)return;
    try {
      const svg=buildPrintableComparisonA5(),mode=comparisonA5InkSelect?.value||'color';
      comparisonA5PrintPreview.src=`data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
      const label=mode==='monocromo'?'monocromo de bajo consumo':mode==='fotocopia'?'alto contraste para fotocopias':'color';
      comparisonA5PrintPreview.alt=`Vista previa de comparación A5 en ${label}, con escala de 10 mm.`;
      if(comparisonA5PrintPreviewCaption)comparisonA5PrintPreviewCaption.textContent=`A5 · ${label} · escala real`;
    } catch (_) {
      comparisonA5PrintPreview.removeAttribute('src');
      if(comparisonA5PrintPreviewCaption)comparisonA5PrintPreviewCaption.textContent='Selecciona dos jornadas para ver la ficha A5.';
    }
    updateInkCoverageEstimate();
  }

  function estimateInkCoverage(svg) {
    return new Promise(resolve=>{
      const image=new Image();
      image.onload=()=>{
        try {
          const canvas=document.createElement('canvas'),width=148,height=210;canvas.width=width;canvas.height=height;
          const context=canvas.getContext('2d',{willReadFrequently:true});if(!context){resolve(null);return;}
          context.fillStyle='#fff';context.fillRect(0,0,width,height);context.drawImage(image,0,0,width,height);
          const pixels=context.getImageData(0,0,width,height).data;let ink=0,total=0;
          for(let y=0;y<height;y+=2){for(let x=0;x<width;x+=2){const offset=(y*width+x)*4,luminance=.2126*pixels[offset]+.7152*pixels[offset+1]+.0722*pixels[offset+2];if(luminance<230)ink++;total++;}}
          resolve(ink/total*100);
        } catch (_) { resolve(null); }
      };
      image.onerror=()=>resolve(null);
      image.src=`data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
    });
  }

  async function updateInkCoverageEstimate() {
    const sequence=++inkEstimateSequence;
    if(!Object.values(inkCoverageOutputs).some(Boolean))return;
    const currentMode=comparisonA5InkSelect?.value||'color',measurements=[];
    try {
      for(const mode of ['color','monocromo','fotocopia']){
        if(comparisonA5InkSelect)comparisonA5InkSelect.value=mode;
        measurements.push([mode,buildPrintableComparisonA5()]);
      }
    } catch (_) {
      Object.values(inkCoverageOutputs).forEach(output=>{if(output)output.textContent='Disponible al elegir dos jornadas.';});
      if(comparisonA5InkSelect)comparisonA5InkSelect.value=currentMode;
      return;
    }
    if(comparisonA5InkSelect)comparisonA5InkSelect.value=currentMode;
    const values=await Promise.all(measurements.map(([,svg])=>estimateInkCoverage(svg)));
    if(sequence!==inkEstimateSequence)return;
    const colorCoverage=values[0];
    measurements.forEach(([mode],index)=>{
      const output=inkCoverageOutputs[mode],percentage=values[index];if(!output)return;
      if(percentage===null){output.textContent='No disponible';return;}
      const value=percentage.toFixed(1).replace('.',',');
      if(mode==='color'||colorCoverage===null){output.textContent=`${value} % de superficie oscura · referencia`;return;}
      const difference=colorCoverage-percentage,amount=Math.abs(difference).toFixed(1).replace('.',',');
      output.textContent=`${value} % de superficie oscura · ${difference>=0?'ahorro estimado':'más cobertura'} de ${amount} puntos porcentuales frente al color`;
    });
  }

  function openA5PrintPreview() {
    if(!comparisonA5PrintPreview?.src||!comparisonA5Dialog||!comparisonA5DialogImage)return;
    comparisonA5DialogImage.src=comparisonA5PrintPreview.src;
    comparisonA5DialogImage.alt=comparisonA5PrintPreview.alt;
    if(typeof comparisonA5Dialog.showModal==='function')comparisonA5Dialog.showModal();
    else comparisonA5Dialog.setAttribute('open','');
  }

  function downloadPrintableSocialSvg() {
    const rowA=rounds.get(selectA?.value),rowB=rounds.get(selectB?.value);
    if(!rowA||!rowB)throw new Error('Selecciona dos jornadas antes de preparar la plantilla.');
    const requested=formatSelect?.value||'apaisado',format=requested==='carrusel'?'cuadrado':requested;
    const metrics=rowA.dataset.completa==='1'&&rowB.dataset.completa==='1'&&Boolean(metricsToggle?.checked),
      svg=comparisonSvg(rowA,rowB,format,metrics,Boolean(captionToggle?.checked),!Boolean(noHeaderToggle?.checked),Boolean(brandToggle?.checked),null,'',densitySelect?.value,framingSelect?.value,altTextCustomized?altTextInput?.value.trim()||'':describeRows([rowA,rowB],densitySelect?.value||'completa',metrics));
    const match=svg.match(/viewBox="([^"]+)"/),body=svg.slice(svg.indexOf('>')+1,svg.lastIndexOf('</svg>'));
    if(!match||!body)throw new Error('No se pudo preparar la plantilla seleccionada.');
    const settings=printPageSettings(),safeMargin=settings.margin+5.5,widthLimit=settings.width-safeMargin*2,heightLimit=settings.height-safeMargin*2,
      [sourceW,sourceH]=match[1].split(/\s+/).slice(2).map(Number),cardW=Math.min(widthLimit,heightLimit*sourceW/sourceH),cardH=cardW*sourceH/sourceW,
      x=(settings.width-cardW)/2,y=(settings.height-cardH)/2,crop=printCropMarks(x,y,cardW,cardH),center=settings.width/2,
      footerY=settings.height-4.5,scaleY=settings.height-11;
    const footer=`<text x="${center}" y="${footerY}" text-anchor="middle" fill="#536257" font-family="Arial,sans-serif" font-size="2.5">A4 ${settings.landscape?'apaisado':'vertical'} · escala real · margen ${settings.margin} mm</text>`;
    const art=`${crop}<svg x="${x}" y="${y}" width="${cardW}" height="${cardH}" viewBox="${match[1]}" preserveAspectRatio="none">${body}</svg>${printCalibrationScale(scaleY)}${footer}`;
    const printable=printablePage(art,settings.width,settings.height),blob=new Blob([printable],{type:'image/svg+xml;charset=utf-8'}),limit=300*1024;
    if(blob.size>limit)throw new Error('La plantilla supera 300 KB; reduce la densidad del diseño y vuelve a intentarlo.');
    const safe=value=>value.replace(/[^0-9a-z]+/gi,'-').replace(/^-|-$/g,'');
    saveBlob(blob,`plantilla-social-${safe(rowA.dataset.comparisonId)}-${safe(rowB.dataset.comparisonId)}-${settings.landscape?'apaisado':'vertical'}-a4.svg`);
    if(socialPrintStatus)socialPrintStatus.textContent=`SVG A4 listo · ${(blob.size/1024).toFixed(1)} KB de 300 KB · ${Math.round(cardW)} × ${Math.round(cardH)} mm · papel ${settings.photo?'fotográfico (margen de 6 mm)':'normal (margen de 10 mm)'}.${requested==='carrusel'?' Se ha preparado en formato cuadrado.':''}`;
  }

  function printCropMarks(x,y,width,height) {
    const gap=1.5,mark=4;
    return `<g fill="none" stroke="#171717" stroke-width=".22"><path d="M${x-gap-mark} ${y}h${mark} M${x} ${y-gap-mark}v${mark} M${x+width+gap} ${y}h${mark} M${x+width} ${y-gap-mark}v${mark} M${x-gap-mark} ${y+height}h${mark} M${x} ${y+height+gap}v${mark} M${x+width+gap} ${y+height}h${mark} M${x+width} ${y+height+gap}v${mark}"/></g>`;
  }

  function printCalibrationScale(y=286) {
    return `<g fill="none" stroke="#171717" stroke-width=".25"><path d="M10 ${y}h10 M10 ${y-.8}v1.6 M20 ${y-.8}v1.6"/></g><text x="23" y="${y+1}" fill="#171717" font-family="Arial,sans-serif" font-size="2.5">10 mm</text>`;
  }

  function buildPrintableContactSheet(showGuides=false) {
    const rowA=rounds.get(selectA?.value),rowB=rounds.get(selectB?.value);
    if(!rowA||!rowB)throw new Error('Selecciona dos jornadas antes de preparar la hoja de contacto.');
    const settings=printPageSettings(),metrics=rowA.dataset.completa==='1'&&rowB.dataset.completa==='1'&&Boolean(metricsToggle?.checked),
      caption=Boolean(captionToggle?.checked),header=!Boolean(noHeaderToggle?.checked),brand=Boolean(brandToggle?.checked),
      density=densitySelect?.value||'completa',framing=framingSelect?.value||'equilibrado',alt=altTextCustomized?altTextInput?.value.trim()||'':describeRows([rowA,rowB],density,metrics),
      safeStart=settings.margin+5.5,usableSpan=settings.width-2*safeStart,selected=contactSheetVariantSelect?.value||'todos',
      allVariants=[['cuadrado','CUADRADA','1080 × 1080'],['vertical','VERTICAL','1080 × 1350'],['historias','HISTORIAS','1080 × 1920']],
      variants=selected==='todos'?allVariants:allVariants.filter(([format])=>format===selected);
    if(!variants.length)throw new Error('Elige un formato válido para la hoja de contacto.');
    const center=settings.width/2,titleY=settings.landscape?15:22,subtitleY=settings.landscape?23:30,scaleY=settings.height-11,footerY=settings.height-4.5;
    const pieces=variants.map(([format,label,sizeLabel],index)=>{
      const source=comparisonSvg(rowA,rowB,format,metrics,caption,header,brand,null,'',density,framing,alt),match=source.match(/viewBox="([^"]+)"/),body=source.slice(source.indexOf('>')+1,source.lastIndexOf('</svg>'));
      if(!match||!body)throw new Error('No se pudo preparar una de las variantes sociales.');
      const [sourceW,sourceH]=match[1].split(/\s+/).slice(2).map(Number);
      let x,y,width,height;
      if(selected==='todos'){
        width=settings.photo?(settings.landscape?75:55):(settings.landscape?70:50);
        const gap=Math.max(11,(usableSpan-width*3)/2),xs=[safeStart,safeStart+width+gap,safeStart+2*(width+gap)];
        height=width*sourceH/sourceW;x=xs[index];y=settings.landscape?(settings.photo?60:62):(settings.photo?74:78);
      }else{
        const top=titleY+20,bottom=settings.height-28,availableHeight=bottom-top;
        width=Math.min(usableSpan,availableHeight*sourceW/sourceH);height=width*sourceH/sourceW;
        x=(settings.width-width)/2;y=top+(availableHeight-height)/2;
      }
      const labelY=selected==='todos'?y-28:y-7,sizeY=selected==='todos'?y-21:y-2.5,labelSize=selected==='todos'?3.4:4.2,dimensionSize=selected==='todos'?2.8:3.2;
      return `<text x="${x+width/2}" y="${labelY}" text-anchor="middle" fill="#171717" font-family="Arial,sans-serif" font-size="${labelSize}" font-weight="700">${label}</text><text x="${x+width/2}" y="${sizeY}" text-anchor="middle" fill="#414141" font-family="Arial,sans-serif" font-size="${dimensionSize}">${sizeLabel}</text>${printCropMarks(x,y,width,height)}<svg x="${x}" y="${y}" width="${width}" height="${height}" viewBox="${match[1]}" preserveAspectRatio="none">${body}</svg>`;
    }).join('');
    const title=`<text x="${center}" y="${titleY}" text-anchor="middle" fill="#171717" font-family="Georgia,serif" font-size="5.2" font-weight="700">${selected==='todos'?'Una comparación, tres formatos':'Una comparación, un formato'}</text><text x="${center}" y="${subtitleY}" text-anchor="middle" fill="#414141" font-family="Arial,sans-serif" font-size="3">Misma pareja · ${settings.photo?'papel fotográfico, margen 6 mm':'papel normal, margen 10 mm'}</text>`;
    const footer=`<text x="${center}" y="${footerY}" text-anchor="middle" fill="#414141" font-family="Arial,sans-serif" font-size="2.5">A4 ${settings.landscape?'apaisado':'vertical'} · escala real · recorta por las marcas</text>`;
    const guide=showGuides?`<rect x="${safeStart}" y="${safeStart}" width="${usableSpan}" height="${settings.height-2*safeStart}" fill="none" stroke="#c65a2b" stroke-width=".45" stroke-dasharray="2 1.2"/><text x="${safeStart+2}" y="${safeStart+4}" fill="#9b3d1c" font-family="Arial,sans-serif" font-size="2.5" font-weight="700">LÍMITE DE SEGURIDAD</text>`:'';
    return printablePage(`${title}${pieces}${guide}${printCalibrationScale(scaleY)}${footer}`,settings.width,settings.height);
  }

  function pdfEscape(value) {
    const normalized=value.replace(/×/g,'x').replace(/·/g,' / ').replace(/→/g,'>');
    const winAnsiSpecial=new Map([[0x20ac,0x80],[0x201a,0x82],[0x192,0x83],[0x201e,0x84],[0x2026,0x85],[0x2020,0x86],[0x2021,0x87],[0x2c6,0x88],[0x2030,0x89],[0x160,0x8a],[0x2039,0x8b],[0x152,0x8c],[0x17d,0x8e],[0x2018,0x91],[0x2019,0x92],[0x201c,0x93],[0x201d,0x94],[0x2022,0x95],[0x2013,0x96],[0x2014,0x97],[0x2dc,0x98],[0x2122,0x99],[0x161,0x9a],[0x203a,0x9b],[0x153,0x9c],[0x17e,0x9e],[0x178,0x9f]]);
    return [...normalized].map(character=>{
      const point=character.codePointAt(0),code=winAnsiSpecial.get(point)??(point<=0xff?point:null);
      if(code===null||code<0x20)return '';
      if(code===0x5c||code===0x28||code===0x29)return `\\${String.fromCharCode(code)}`;
      if(code>=0x20&&code<=0x7e)return String.fromCharCode(code);
      return `\\${code.toString(8).padStart(3,'0')}`;
    }).join('');
  }

  async function loadPdfFonts() {
    if(!loadPdfFonts.promise)loadPdfFonts.promise=Promise.all([
      fetch('../analisis/comun/fuentes/Archivo-Regular.ttf').then(response=>{if(!response.ok)throw new Error('No se pudo cargar la fuente Archivo Regular.');return response.arrayBuffer();}),
      fetch('../analisis/comun/fuentes/Archivo-Bold.ttf').then(response=>{if(!response.ok)throw new Error('No se pudo cargar la fuente Archivo Bold.');return response.arrayBuffer();}),
      fetch('../assets/archivo-visual-font-metrics.json').then(response=>{if(!response.ok)throw new Error('No se pudieron cargar las métricas tipográficas del PDF.');return response.json();})
    ]).then(async([regular,bold,metrics])=>{
      if(typeof CompressionStream==='undefined')throw new Error('Este navegador no permite comprimir las fuentes del PDF. Descarga la versión HTML imprimible.');
      const compress=async(buffer)=>new Uint8Array(await new Response(new Blob([buffer]).stream().pipeThrough(new CompressionStream('deflate'))).arrayBuffer());
      return {regular:{bytes:await compress(regular),length:regular.byteLength,metrics:metrics.regular},bold:{bytes:await compress(bold),length:bold.byteLength,metrics:metrics.bold}};
    });
    return loadPdfFonts.promise;
  }

  async function svgToVectorPdf(svg,title='Material visual imprimible · Línea de pase') {
    const documentSvg=new DOMParser().parseFromString(svg,'image/svg+xml');
    if(documentSvg.querySelector('parsererror'))throw new Error('No se pudo leer la plantilla SVG.');
    const root=documentSvg.documentElement,pageMmW=parseFloat(root.getAttribute('width')),pageMmH=parseFloat(root.getAttribute('height')),
      view=(root.getAttribute('viewBox')||`0 0 ${pageMmW} ${pageMmH}`).trim().split(/\s+/).map(Number),factor=72/25.4,pageW=pageMmW*factor,pageH=pageMmH*factor,parts=[],taggedText=[];
    if(!(pageMmW>0&&pageMmH>0&&view.length===4&&view[2]>0&&view[3]>0))throw new Error('El documento no tiene medidas de impresión válidas.');
    const color=value=>{let token=value||'#000000';const short=token.match(/^#([0-9a-f]{3})$/i);if(short)token='#'+[...short[1]].map(char=>char+char).join('');const match=token.match(/^#([0-9a-f]{6})$/i);if(!match)return [0,0,0];return [0,2,4].map(i=>parseInt(match[1].slice(i,i+2),16)/255);};
    const rgb=value=>color(value).map(v=>v.toFixed(4)).join(' ');
    const number=(node,name,fallback=0)=>{const raw=node.getAttribute(name);if(!raw)return fallback;if(raw.endsWith('%'))return Number(raw.slice(0,-1))/100*(name==='width'?node.__viewW||0:node.__viewH||0);return parseFloat(raw)||0;};
    const point=(x,y,ctx)=>[(ctx.x+x*ctx.sx)*factor,pageH-(ctx.y+y*ctx.sy)*factor];
    const drawPath=(d,ctx)=>{
      const tokens=d.match(/[a-zA-Z]|[-+]?(?:\d*\.)?\d+(?:[eE][-+]?\d+)?/g)||[];let i=0,cmd='',x=0,y=0,startX=0,startY=0,out=[];
      const take=()=>Number(tokens[i++]);
      while(i<tokens.length){if(/[a-z]/i.test(tokens[i]))cmd=tokens[i++];if(!cmd)break;const rel=cmd===cmd.toLowerCase(),op=cmd.toUpperCase();
        if(op==='Z'){out.push('h');x=startX;y=startY;cmd='';continue;}
        if(op==='M'||op==='L'){if(i+1>=tokens.length)break;let nx=take(),ny=take();if(rel){nx+=x;ny+=y;}const q=point(nx,ny,ctx);out.push(`${q[0].toFixed(3)} ${q[1].toFixed(3)} ${op==='M'?'m':'l'}`);x=nx;y=ny;if(op==='M'){startX=x;startY=y;cmd=rel?'l':'L';}}
        else if(op==='H'){const nx=take()+(rel?x:0),q=point(nx,y,ctx);out.push(`${q[0].toFixed(3)} ${q[1].toFixed(3)} l`);x=nx;}
        else if(op==='V'){const ny=take()+(rel?y:0),q=point(x,ny,ctx);out.push(`${q[0].toFixed(3)} ${q[1].toFixed(3)} l`);y=ny;}
        else if(op==='C'){if(i+5>=tokens.length)break;let x1=take(),y1=take(),x2=take(),y2=take(),nx=take(),ny=take();if(rel){x1+=x;y1+=y;x2+=x;y2+=y;nx+=x;ny+=y;}const a=point(x1,y1,ctx),b=point(x2,y2,ctx),c=point(nx,ny,ctx);out.push(`${a[0].toFixed(3)} ${a[1].toFixed(3)} ${b[0].toFixed(3)} ${b[1].toFixed(3)} ${c[0].toFixed(3)} ${c[1].toFixed(3)} c`);x=nx;y=ny;}
        else {cmd='';}
      }
      return out.join(' ');
    };
    const drawText=(node,ctx)=>{
      const raw=node.textContent||'',text=pdfEscape(raw);if(!text)return;
      const x=number(node,'x'),y=number(node,'y'),size=number(node,'font-size',16),weight=Number(node.getAttribute('font-weight')||400),family=node.getAttribute('font-family')||'Arial',anchor=node.getAttribute('text-anchor')||'start',
        [px,py]=point(x,y,ctx),fontSize=size*ctx.sy*factor,firstFamily=family.split(',')[0].trim().toLowerCase(),serif=/^(times|georgia|serif)(\b|$)/.test(firstFamily),font=serif?'/F3':weight>=600?'/F2':'/F1',textLength=node.hasAttribute('textLength')?number(node,'textLength')*ctx.sx*factor:null,
        naturalWidth=text.length*size*(serif?.52:.54)*ctx.sx*factor,letterSpacing=number(node,'letter-spacing')*ctx.sx*factor,measuredWidth=naturalWidth+Math.max(0,text.length-1)*letterSpacing,width=textLength===null?measuredWidth:Math.min(textLength,naturalWidth),horizontalScale=textLength!==null&&naturalWidth>textLength?textLength/naturalWidth*100:100,startX=px-(anchor==='middle'?width/2:anchor==='end'?width:0);
      const mcid=taggedText.length;taggedText.push(raw);
      parts.push(`/P <</MCID ${mcid}>> BDC`,`${rgb(node.getAttribute('fill')||'#000000')} rg BT ${font} ${fontSize.toFixed(3)} Tf ${horizontalScale.toFixed(2)} Tz ${letterSpacing.toFixed(3)} Tc 1 0 0 1 ${startX.toFixed(3)} ${py.toFixed(3)} Tm (${text}) Tj ET`,'EMC');
    };
    const walk=(node,ctx)=>{
      const tag=node.localName;
      if(tag==='title'||tag==='desc'||tag==='defs'||tag==='metadata')return;
      if(tag==='svg'){
        let childCtx=ctx;
        if(node!==root){const x=number(node,'x'),y=number(node,'y'),w=number(node,'width'),h=number(node,'height'),vb=(node.getAttribute('viewBox')||`0 0 ${w} ${h}`).trim().split(/\s+/).map(Number);if(vb.length!==4||!vb[2]||!vb[3])return;const sx=w/vb[2],sy=h/vb[3];childCtx={x:ctx.x+x*ctx.sx-vb[0]*sx*ctx.sx,y:ctx.y+y*ctx.sy-vb[1]*sy*ctx.sy,sx:ctx.sx*sx,sy:ctx.sy*sy};}
        node.childNodes.forEach(child=>{if(child.nodeType===1)walk(child,childCtx);});return;
      }
      if(tag==='g'){node.childNodes.forEach(child=>{if(child.nodeType===1)walk(child,ctx);});return;}
      if(tag==='rect'){
        const x=number(node,'x'),y=number(node,'y'),w=number(node,'width'),h=number(node,'height'),left=(ctx.x+x*ctx.sx)*factor,bottom=pageH-(ctx.y+(y+h)*ctx.sy)*factor,width=w*ctx.sx*factor,height=h*ctx.sy*factor,fill=node.getAttribute('fill'),stroke=node.getAttribute('stroke'),sw=number(node,'stroke-width',1)*Math.min(ctx.sx,ctx.sy)*factor;
        parts.push('/Artifact BMC','q');if(fill&&fill!=='none')parts.push(`${rgb(fill)} rg`);if(stroke&&stroke!=='none')parts.push(`${rgb(stroke)} RG ${sw.toFixed(3)} w`);parts.push(`${left.toFixed(3)} ${bottom.toFixed(3)} ${width.toFixed(3)} ${height.toFixed(3)} re`,fill&&fill!=='none'&&stroke&&stroke!=='none'?'B':fill&&fill!=='none'?'f':stroke&&stroke!=='none'?'S':'n','Q','EMC');return;
      }
      if(tag==='path'){
        const path=drawPath(node.getAttribute('d')||'',ctx),fill=node.getAttribute('fill'),stroke=node.getAttribute('stroke'),sw=number(node,'stroke-width',1)*Math.min(ctx.sx,ctx.sy)*factor;
        if(!path)return;parts.push('/Artifact BMC','q');if(fill&&fill!=='none')parts.push(`${rgb(fill)} rg`);if(stroke&&stroke!=='none')parts.push(`${rgb(stroke)} RG ${sw.toFixed(3)} w`);const dash=node.getAttribute('stroke-dasharray');if(dash)parts.push(`[${dash.split(/[ ,]+/).map(v=>(Number(v)*Math.min(ctx.sx,ctx.sy)*factor).toFixed(3)).join(' ')}] 0 d`);parts.push(path,fill&&fill!=='none'&&stroke&&stroke!=='none'?'B':fill&&fill!=='none'?'f':stroke&&stroke!=='none'?'S':'n','Q','EMC');return;
      }
      if(tag==='text'){drawText(node,ctx);return;}
    };
    const ctx={x:0,y:0,sx:pageMmW/view[2],sy:pageMmH/view[3]};root.childNodes.forEach(child=>{if(child.nodeType===1)walk(child,ctx);});
    const content=parts.join('\n'),fonts=await loadPdfFonts(),documentStructId=13,tagRefs=taggedText.map((_,index)=>`${14+index} 0 R`),metadataId=14+taggedText.length,infoId=metadataId+1,
      xmlEscape=value=>value.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&apos;'),
      xmp=`<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>\n<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Línea de pase"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"><rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xmp="http://ns.adobe.com/xap/1.0/"><dc:title><rdf:Alt><rdf:li xml:lang="x-default">${xmlEscape(title)}</rdf:li></rdf:Alt></dc:title><dc:creator><rdf:Seq><rdf:li>Ángel Marqueta Alonso</rdf:li></rdf:Seq></dc:creator><dc:language><rdf:Bag><rdf:li>es-ES</rdf:li></rdf:Bag></dc:language><dc:format>application/pdf</dc:format><xmp:CreatorTool>Línea de pase</xmp:CreatorTool></rdf:Description></rdf:RDF></x:xmpmeta>\n<?xpacket end="w"?>`,
      fontObject=(font,name,descriptorId)=>`<< /Type /Font /Subtype /TrueType /BaseFont /${name} /FirstChar ${font.metrics.firstChar} /LastChar ${font.metrics.lastChar} /Widths [${font.metrics.widths.join(' ')}] /Encoding /WinAnsiEncoding /FontDescriptor ${descriptorId} 0 R >>`,
      fontDescriptor=(font,name,fileId)=>`<< /Type /FontDescriptor /FontName /${name} /Flags 32 /FontBBox [${font.metrics.bbox.join(' ')}] /ItalicAngle 0 /Ascent ${font.metrics.ascent} /Descent ${font.metrics.descent} /CapHeight ${font.metrics.capHeight} /StemV ${font.metrics.stemV} /FontFile2 ${fileId} 0 R >>`,
      objects=[
      `<< /Type /Catalog /Pages 2 0 R /Lang (es-ES) /Metadata ${metadataId} 0 R /MarkInfo << /Marked true >> /StructTreeRoot 11 0 R /ViewerPreferences << /DisplayDocTitle true >> >>`,
      '<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
      `<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${pageW.toFixed(2)} ${pageH.toFixed(2)}] /Resources << /Font << /F1 4 0 R /F2 5 0 R /F3 4 0 R >> >> /StructParents 0 /Tabs /S /Contents 10 0 R >>`,
      fontObject(fonts.regular,'LdpArchivoRegular',6),fontObject(fonts.bold,'LdpArchivoBold',7),fontDescriptor(fonts.regular,'LdpArchivoRegular',8),fontDescriptor(fonts.bold,'LdpArchivoBold',9),
      null,null,
      `<< /Length ${new TextEncoder().encode(content).length} >>\nstream\n${content}\nendstream`,
      `<< /Type /StructTreeRoot /K ${documentStructId} 0 R /ParentTree 12 0 R /ParentTreeNextKey 1 >>`,
      `<< /Nums [0 [${tagRefs.join(' ')}]] >>`,
      `<< /Type /StructElem /S /Document /P 11 0 R /K [${tagRefs.join(' ')}] >>`,
      ...taggedText.map((_,index)=>`<< /Type /StructElem /S /P /P ${documentStructId} 0 R /Pg 3 0 R /K ${index} >>`),
      `<< /Type /Metadata /Subtype /XML /Length ${new TextEncoder().encode(xmp).length} >>\nstream\n${xmp}\nendstream`,
      `<< /Title (${pdfEscape(title)}) /Author (Linea de pase) /Subject (Documento en espanol; lectura marcada en es-ES) >>`
    ];
    const streamObject=(bytes,length)=>[`<< /Length ${bytes.length} /Length1 ${length} /Filter /FlateDecode >>\nstream\n`,bytes,'\nendstream'];
    objects[7]=streamObject(fonts.regular.bytes,fonts.regular.length);objects[8]=streamObject(fonts.bold.bytes,fonts.bold.length);
    const encoder=new TextEncoder(),toBytes=value=>typeof value==='string'?encoder.encode(value):value,
      joinBytes=chunks=>{const converted=chunks.map(toBytes),result=new Uint8Array(converted.reduce((sum,item)=>sum+item.length,0));let cursor=0;for(const item of converted){result.set(item,cursor);cursor+=item.length;}return result;};
    const header=encoder.encode('%PDF-1.4\n'),objectBytes=objects.map((object,index)=>joinBytes([`${index+1} 0 obj\n`,...(Array.isArray(object)?object:[object]),'\nendobj\n']));
    let byteLength=header.length,offsets=[0];objectBytes.forEach(bytes=>{offsets.push(byteLength);byteLength+=bytes.length;});
    const xref=byteLength,trailer=encoder.encode(`xref\n0 ${objects.length+1}\n0000000000 65535 f \n`+offsets.slice(1).map(value=>`${String(value).padStart(10,'0')} 00000 n \n`).join('')+`trailer\n<< /Size ${objects.length+1} /Root 1 0 R /Info ${infoId} 0 R >>\nstartxref\n${xref}\n%%EOF`),
      pdf=joinBytes([header,...objectBytes,trailer]);
    return {blob:new Blob([pdf],{type:'application/pdf'}),pageMmW,pageMmH};
  }

  async function downloadPrintableContactSheetPdf() {
    const rowA=rounds.get(selectA?.value),rowB=rounds.get(selectB?.value),settings=printPageSettings();
    const {blob,pageMmW,pageMmH}=await svgToVectorPdf(buildPrintableContactSheet(false),`Hoja de contacto A4 · ${rowA.dataset.rival} y ${rowB.dataset.rival}`);if(blob.size>300*1024)throw new Error('El PDF supera 300 KB; reduce la densidad del diseño y vuelve a intentarlo.');
    const safe=value=>value.replace(/[^0-9a-z]+/gi,'-').replace(/^-|-$/g,'');
    saveBlob(blob,`hoja-contacto-${safe(rowA.dataset.comparisonId)}-${safe(rowB.dataset.comparisonId)}-${settings.landscape?'apaisado':'vertical'}-a4.pdf`);
    if(socialPrintStatus)socialPrintStatus.textContent=`PDF vectorial listo · ${(blob.size/1024).toFixed(1)} KB · A4 ${pageMmW} × ${pageMmH} mm · tres formatos, marcas de corte y escala de 10 mm.`;
  }

  function buildPrintableComparisonA5() {
    const rowA=rounds.get(selectA?.value),rowB=rounds.get(selectB?.value);if(!rowA||!rowB)throw new Error('Selecciona dos jornadas antes de preparar la hoja A5.');
    const format='vertical',mode=comparisonA5InkSelect?.value||'color',lowInk=mode==='monocromo',photocopy=mode==='fotocopia',metrics=rowA.dataset.completa==='1'&&rowB.dataset.completa==='1'&&Boolean(metricsToggle?.checked),
      card=comparisonSvg(rowA,rowB,format,metrics,Boolean(captionToggle?.checked),!Boolean(noHeaderToggle?.checked),Boolean(brandToggle?.checked),null,'',densitySelect?.value,framingSelect?.value,altTextCustomized?altTextInput?.value.trim()||'':describeRows([rowA,rowB],densitySelect?.value||'completa',metrics),photocopy?photocopyPrintPalette:lowInk?lowInkPrintPalette:null),match=card.match(/viewBox="([^"]+)"/),body=card.slice(card.indexOf('>')+1,card.lastIndexOf('</svg>'));
    if(!match||!body)throw new Error('No se pudo preparar la comparación para A5.');
    const settings=printPageSettings(),pageW=148,pageH=210,margin=settings.margin,maxW=pageW-margin*2,maxH=settings.photo?152:142,[sourceW,sourceH]=match[1].split(/\s+/).slice(2).map(Number),cardW=Math.min(maxW,maxH*sourceW/sourceH),cardH=cardW*sourceH/sourceW,x=(pageW-cardW)/2,y=100-cardH/2,scaleY=191;
    const art=`<text x="74" y="13" text-anchor="middle" fill="#171717" font-family="Arial,sans-serif" font-size="3.5" font-weight="700">COMPARACIÓN · A5${lowInk?' · BAJA TINTA':photocopy?' · ALTO CONTRASTE':''}</text><text x="74" y="20" text-anchor="middle" fill="#414141" font-family="Arial,sans-serif" font-size="2.5">${settings.photo?'PAPEL FOTOGRÁFICO · MARGEN 6 mm':'PAPEL NORMAL · MARGEN 10 mm'}</text><svg x="${x}" y="${y}" width="${cardW}" height="${cardH}" viewBox="${match[1]}" preserveAspectRatio="none">${body}</svg>${printCalibrationScale(scaleY)}<text x="74" y="205" text-anchor="middle" fill="#414141" font-family="Arial,sans-serif" font-size="2.3">A5 · IMPRIMIR AL 100 % · ESCALA REAL</text>`;
    return printablePage(art,pageW,pageH);
  }

  async function downloadPrintableComparisonA5() {
    const rowA=rounds.get(selectA?.value),rowB=rounds.get(selectB?.value),{blob,pageMmW,pageMmH}=await svgToVectorPdf(buildPrintableComparisonA5(),`Comparación A5 · ${rowA.dataset.rival} y ${rowB.dataset.rival}`);
    if(blob.size>300*1024)throw new Error('El PDF A5 supera 300 KB; reduce la densidad del diseño y vuelve a intentarlo.');
    const safe=value=>value.replace(/[^0-9a-z]+/gi,'-').replace(/^-|-$/g,'');
    saveBlob(blob,`comparacion-${safe(rowA.dataset.comparisonId)}-${safe(rowB.dataset.comparisonId)}-a5.pdf`);
    const mode=comparisonA5InkSelect?.value||'color',modeLabel=mode==='monocromo'?' · monocromo de bajo consumo':mode==='fotocopia'?' · alto contraste para fotocopias':'';
    if(socialPrintStatus)socialPrintStatus.textContent=`PDF A5 listo · ${(blob.size/1024).toFixed(1)} KB · comparación ${pageMmW} × ${pageMmH} mm con escala de 10 mm${modeLabel}.`;
  }

  function downloadComparisonText() {
    const selected=[rounds.get(selectA?.value),rounds.get(selectB?.value)];
    if(selected.some(row=>!row))throw new Error('Selecciona dos jornadas antes de preparar el texto.');
    const dateLabel=value=>{const [year,month,day]=value.split('-');return `${day}/${month}/${year}`;};
    const lines=['Línea de pase · Comparación de jornadas',`Temporada: ${selected[0].dataset.temporada}`, ''];
    selected.forEach(row=>{
      const round=String(row.dataset.jornada).padStart(2,'0');
      lines.push(`J${round} · ${dateLabel(row.dataset.fechaPartido)}`);
      lines.push(`Real Zaragoza ${row.dataset.golesZaragoza}–${row.dataset.golesRival} ${row.dataset.rival} · ${row.dataset.sede==='Fuera'?'fuera':'en casa'}.`);
      if(row.dataset.completa==='1'){
        lines.push(`Posesión: ${row.dataset.posesion} %. Tiros: ${row.dataset.tirosZaragoza}–${row.dataset.tirosRival}.`);
        if(/^\d+$/.test(row.dataset.aPuertaZaragoza)&&/^\d+$/.test(row.dataset.aPuertaRival))lines.push(`Tiros a puerta: ${row.dataset.aPuertaZaragoza}–${row.dataset.aPuertaRival}.`);
      }else lines.push('Ficha estadística sin validar; solo se incluye el marcador.');
      lines.push('');
    });
    lines.push('Los datos corresponden a la ficha publicada en el archivo visual.');
    const blob=new Blob([lines.join('\n')+'\n'],{type:'text/plain;charset=utf-8'});
    const safe=value=>value.replace(/[^0-9a-z]+/gi,'-').replace(/^-|-$/g,'');
    saveBlob(blob,`comparacion-${safe(selected[0].dataset.comparisonId)}-${safe(selected[1].dataset.comparisonId)}.txt`);
    if(socialPrintStatus)socialPrintStatus.textContent=`Texto accesible listo · ${(blob.size/1024).toFixed(1)} KB · dos jornadas.`;
  }

  function openPrintableComparisonHtml() {
    const selected=[rounds.get(selectA?.value),rounds.get(selectB?.value)];
    if(selected.some(row=>!row))throw new Error('Selecciona dos jornadas antes de preparar la versión HTML.');
    const escapeHtml=value=>String(value).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;'),
      dateLabel=value=>{const [year,month,day]=value.split('-');return `${day}/${month}/${year}`;},
      matchSection=row=>{
        const season=escapeHtml(row.dataset.temporada),round=String(row.dataset.jornada).padStart(2,'0'),opponent=escapeHtml(row.dataset.rival),zGoals=escapeHtml(row.dataset.golesZaragoza),rGoals=escapeHtml(row.dataset.golesRival),venue=row.dataset.sede==='Fuera'?'Fuera':'En casa';
        const stats=row.dataset.completa==='1'?`<dl><div><dt>Posesión del Zaragoza</dt><dd>${escapeHtml(row.dataset.posesion)} %</dd></div><div><dt>Tiros · Zaragoza–rival</dt><dd>${escapeHtml(row.dataset.tirosZaragoza)}–${escapeHtml(row.dataset.tirosRival)}</dd></div>${/^\d+$/.test(row.dataset.aPuertaZaragoza)&&/^\d+$/.test(row.dataset.aPuertaRival)?`<div><dt>Tiros a puerta · Zaragoza–rival</dt><dd>${escapeHtml(row.dataset.aPuertaZaragoza)}–${escapeHtml(row.dataset.aPuertaRival)}</dd></div>`:''}</dl><p class="estado validado">Ficha completa; estadísticas incluidas.</p>`:'<p class="estado pendiente">Ficha estadística sin validar. Se muestra solo el marcador.</p>';
        return `<section aria-labelledby="jornada-${round}-${season.replace(/[^a-z0-9]+/gi,'-')}"><h2 id="jornada-${round}-${season.replace(/[^a-z0-9]+/gi,'-')}">Jornada ${round} · ${dateLabel(row.dataset.fechaPartido)} · ${season}</h2><p class="resultado"><strong>Real Zaragoza ${zGoals}–${rGoals} ${opponent}</strong> · ${venue}.</p>${stats}</section>`;
      },
      documentTitle=`Comparación J${String(selected[0].dataset.jornada).padStart(2,'0')} y J${String(selected[1].dataset.jornada).padStart(2,'0')} · Zaragoza ante ${selected[0].dataset.rival} y ${selected[1].dataset.rival} · Línea de pase`,
      html=`<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escapeHtml(documentTitle)}</title><style>:root{font-family:Arial,Helvetica,sans-serif;color:#17251c;background:#fff}body{max-width:44rem;margin:2rem auto;padding:0 1.25rem;line-height:1.55}header{border-bottom:2px solid #174a30;padding-bottom:1rem}h1{font-size:1.7rem;line-height:1.2}h2{font-size:1.15rem;margin-bottom:.45rem}section{padding:1rem 0;border-bottom:1px solid #cfd9d1;break-inside:avoid}dl{display:grid;grid-template-columns:repeat(auto-fit,minmax(9rem,1fr));gap:.5rem 1rem}dt{font-size:.9rem;color:#46574b}dd{margin:.15rem 0;font-weight:700}.estado{padding:.6rem .75rem;border-radius:.35rem}.validado{background:#e5f1e8;color:#174a30}.pendiente{background:#f4efe2;color:#654d17}.resultado{font-size:1.2rem}footer{font-size:.85rem;color:#536257;padding-top:1rem}.imprimir{font:inherit;padding:.6rem 1rem;margin:1rem 0;background:#174a30;color:#fff;border:0;border-radius:.35rem;cursor:pointer}@media print{@page{size:A5 portrait;margin:12mm}body{max-width:none;margin:0;padding:0}.imprimir{display:none}section{break-inside:avoid}header{border-color:#333}.estado{border:1px solid #777;background:#fff!important;color:#111!important}}</style></head><body><header><p>Línea de pase · Comparación de jornadas</p><h1>Real Zaragoza · temporada ${escapeHtml(selected[0].dataset.temporada)}</h1><p>Marcadores y estadísticas verificadas disponibles para las dos jornadas seleccionadas.</p></header><button class="imprimir" type="button" onclick="window.print()">Imprimir o guardar como PDF</button><main>${selected.map(matchSection).join('')}</main><footer>Las estadísticas solo se incluyen cuando la ficha está completa y validada.</footer></body></html>`,
      printWindow=window.open('','_blank');
    if(printWindow){printWindow.document.open();printWindow.document.write(html);printWindow.document.close();printWindow.focus();if(socialPrintStatus)socialPrintStatus.textContent='Versión HTML accesible abierta · puedes imprimirla o guardarla como PDF desde el navegador.';return;}
    const blob=new Blob([html],{type:'text/html;charset=utf-8'}),safe=value=>value.replace(/[^0-9a-z]+/gi,'-').replace(/^-|-$/g,'');
    saveBlob(blob,`comparacion-${safe(selected[0].dataset.comparisonId)}-${safe(selected[1].dataset.comparisonId)}-imprimible.html`);
    if(socialPrintStatus)socialPrintStatus.textContent='El navegador bloqueó la pestaña nueva; se descargó la versión HTML accesible para abrirla e imprimirla.';
  }

  function downloadPrintableContactSheet() {
    const rowA=rounds.get(selectA?.value),rowB=rounds.get(selectB?.value),settings=printPageSettings();
    const printable=buildPrintableContactSheet(),blob=new Blob([printable],{type:'image/svg+xml;charset=utf-8'}),limit=300*1024;
    if(blob.size>limit)throw new Error('La hoja supera 300 KB; reduce la densidad del diseño y vuelve a intentarlo.');
    const safe=value=>value.replace(/[^0-9a-z]+/gi,'-').replace(/^-|-$/g,'');
    saveBlob(blob,`hoja-contacto-${safe(rowA.dataset.comparisonId)}-${safe(rowB.dataset.comparisonId)}-${settings.landscape?'apaisado':'vertical'}-a4.svg`);
    const variant=contactSheetVariantSelect?.value||'todos',variantLabel=variant==='todos'?'tres formatos':variant==='historias'?'historias':variant;
    if(socialPrintStatus)socialPrintStatus.textContent=`Hoja de contacto lista · ${(blob.size/1024).toFixed(1)} KB de 300 KB · ${variantLabel} con marcas de corte y escala de 10 mm · A4 ${settings.landscape?'apaisada':'vertical'} · papel ${settings.photo?'fotográfico, margen de 6 mm':'normal, margen de 10 mm'}.${paletteSelect?.value==='monocromo'?' Paleta monocroma aplicada.':' Elige «Blanco y negro» para imprimir sin color.'}`;
  }

  function printSvgPage(svg,width,height,title) {
    const printWindow=window.open('','_blank','popup,width=980,height=760');
    if(!printWindow){if(socialPrintStatus)socialPrintStatus.textContent='El navegador bloqueó la ventana de impresión. Permite ventanas emergentes para imprimir o descarga el PDF.';return false;}
    printWindow.document.open();
    printWindow.document.write(`<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title><style>@page{size:${width}mm ${height}mm;margin:0}html,body{margin:0;padding:0;width:${width}mm;height:${height}mm;background:#fff}svg{display:block;width:${width}mm;height:${height}mm}*{-webkit-print-color-adjust:exact;print-color-adjust:exact}@media screen{body{display:grid;place-items:center;width:100vw;height:100vh;background:#e8ece9}svg{width:min(96vw,${width}mm);height:auto;max-height:96vh;object-fit:contain;box-shadow:0 3px 22px #0003}}</style></head><body>${svg}</body></html>`);
    printWindow.document.close();
    if(socialPrintStatus)socialPrintStatus.textContent=`Vista de impresión abierta · papel ${width===148?'A5':`A4 ${width>height?'apaisado':'vertical'}`} · selecciona escala 100 % para conservar la regla de 10 mm.`;
    try{printWindow.focus();printWindow.print();}catch(_){if(socialPrintStatus)socialPrintStatus.textContent='No se pudo abrir el diálogo de impresión. Descarga el PDF para continuar.';}
    return true;
  }

  function printContactSheetDirectly() {
    const settings=printPageSettings();
    printSvgPage(buildPrintableContactSheet(false),settings.width,settings.height,'Hoja de contacto · Línea de pase');
  }

  function printComparisonA5Directly() {
    printSvgPage(buildPrintableComparisonA5(),148,210,'Comparación A5 · Línea de pase');
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
    restorePrintSettings();
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
    seasonCarouselButton?.addEventListener('click',async()=>{if(seasonPosterStatus)seasonPosterStatus.textContent='Preparando el carrusel…';try{await downloadSeasonCarousel();}catch(error){if(seasonPosterStatus)seasonPosterStatus.textContent=error instanceof Error?error.message:'No se pudo preparar el carrusel.';}});
    seasonShareButton?.addEventListener('click',copySeasonPosterLink);
    seasonSaveLinkButton?.addEventListener('click',saveNamedSeasonPosterLink);
    seasonExportLinksButton?.addEventListener('click',exportSeasonSavedLinks);
    seasonImportLinksButton?.addEventListener('click',()=>seasonImportLinksFile?.click());
    seasonImportLinksFile?.addEventListener('change',()=>importSeasonSavedLinks(seasonImportLinksFile.files?.[0]));
    seasonQrButton?.addEventListener('click',makeSeasonLinkQr);
    seasonQrDownloadButton?.addEventListener('click',downloadSeasonLinkQr);
    seasonQrA4Button?.addEventListener('click',downloadSeasonQrA4);
    seasonQrA4LandscapeButton?.addEventListener('click',downloadSeasonQrLandscapeA4);
    seasonQrCopyButton?.addEventListener('click',copySeasonLinkQr);
    seasonQrName?.addEventListener('input',()=>{if(seasonQrSvg)clearSeasonLinkQr();else updateSeasonQrPrintPreview();});
    [seasonQrColor,seasonQrPrintSize].forEach(control=>control?.addEventListener('change',()=>{updateSeasonQrQuality();if(seasonQrSvg)clearSeasonLinkQr();else updateSeasonQrPrintPreview();}));
    if(seasonQrA4Button)seasonQrA4Button.disabled=!seasonQrScaleConfirm?.checked;
    if(seasonQrA4LandscapeButton)seasonQrA4LandscapeButton.disabled=!seasonQrScaleConfirm?.checked;
    if(seasonQrA5Button)seasonQrA5Button.disabled=!seasonQrScaleConfirm?.checked;
    seasonQrScaleConfirm?.addEventListener('change',()=>{if(seasonQrA4Button)seasonQrA4Button.disabled=!seasonQrScaleConfirm.checked;if(seasonQrA4LandscapeButton)seasonQrA4LandscapeButton.disabled=!seasonQrScaleConfirm.checked;if(seasonQrA5Button)seasonQrA5Button.disabled=!seasonQrScaleConfirm.checked;});
    seasonQrPaperSelect?.addEventListener('change',updateSeasonQrPrintPreview);
    [selectA,selectB].forEach(control=>control?.addEventListener('change',updateSeasonQrPrintPreview));
    const updateQrDisclosureLabel=()=>{const summary=seasonQrPreviewDisclosure?.querySelector('summary');if(summary)summary.textContent=seasonQrPreviewDisclosure.open?'Ocultar las maquetas A4':'Mostrar las maquetas A4';};
    seasonQrPreviewDisclosure?.addEventListener('toggle',updateQrDisclosureLabel);
    const qrMobileQuery=window.matchMedia?.('(max-width: 600px)');
    if(qrMobileQuery?.matches&&seasonQrPreviewDisclosure)seasonQrPreviewDisclosure.open=false;
    qrMobileQuery?.addEventListener?.('change',event=>{if(event.matches&&seasonQrPreviewDisclosure)seasonQrPreviewDisclosure.open=false;});
    updateQrDisclosureLabel();
    updateSeasonQrQuality();
    updateSeasonQrPrintPreview();
    seasonSaveLinkName?.addEventListener('keydown',event=>{if(event.key==='Enter'){event.preventDefault();saveNamedSeasonPosterLink();}});
    seasonSavedLinksList?.addEventListener('click',async event=>{
      const button=event.target.closest('button[data-aplicar-enlace-mapa],button[data-copiar-enlace-mapa],button[data-borrar-enlace-mapa],button[data-fijar-enlace-mapa],button[data-subir-enlace-mapa],button[data-bajar-enlace-mapa]');
      if(!button)return;
      const index=Number(button.dataset.aplicarEnlaceMapa??button.dataset.copiarEnlaceMapa??button.dataset.borrarEnlaceMapa??button.dataset.fijarEnlaceMapa??button.dataset.subirEnlaceMapa??button.dataset.bajarEnlaceMapa),links=readSeasonSavedLinks(),item=links[index];
      if(!item)return;
      if(button.hasAttribute('data-aplicar-enlace-mapa'))applySavedSeasonPosterLink(item.url);
      else if(button.hasAttribute('data-copiar-enlace-mapa')){try{await navigator.clipboard.writeText(item.url);if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent=`Enlace «${item.name}» copiado.`;}catch(_){if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent='No se pudo copiar este enlace en el navegador.';}}
      else if(button.hasAttribute('data-borrar-enlace-mapa')){links.splice(index,1);try{saveSeasonSavedLinks(links);if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent=`Enlace «${item.name}» borrado.`;}catch(_){if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent='No se pudo borrar este enlace guardado.';}}
      else if(button.hasAttribute('data-fijar-enlace-mapa')){item.pinned=!item.pinned;try{saveSeasonSavedLinks(links);if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent=`Enlace «${item.name}» ${item.pinned?'fijado arriba':'desfijado'}.`;}catch(_){if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent='No se pudo actualizar el enlace.';}}
      else {const delta=button.hasAttribute('data-subir-enlace-mapa')?-1:1,target=index+delta;if(target>=0&&target<links.length&&links[target].pinned===item.pinned){[links[index],links[target]]=[links[target],links[index]];try{saveSeasonSavedLinks(links);if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent='Orden de enlaces actualizado.';}catch(_){if(seasonSavedLinksStatus)seasonSavedLinksStatus.textContent='No se pudo ordenar los enlaces.';}}}
    });
    [seasonPosterFormat,seasonPosterType,seasonPosterRival,seasonPosterFrom,seasonPosterTo].forEach(control=>control?.addEventListener('change',()=>{clearSeasonLinkQr();updateSeasonPosterPreview();if(seasonPosterStatus)seasonPosterStatus.textContent='El mapa está listo para descargar.';}));
    seasonPosterSelect?.addEventListener('change',()=>{clearSeasonLinkQr();updateSeasonRivalOptions();if(seasonPosterSheet)seasonPosterSheet.value='0';updateSeasonPosterPreview();if(seasonPosterStatus)seasonPosterStatus.textContent='Temporada actualizada.';});
    seasonPosterSheet?.addEventListener('change',updateSeasonPosterPreview);
    seasonPosterAlt?.addEventListener('input',()=>{seasonPosterAltCustomized=true;updateSeasonPosterPreview();});
    resetSeasonPosterAlt?.addEventListener('click',()=>{seasonPosterAltCustomized=false;updateSeasonPosterPreview();if(seasonPosterStatus)seasonPosterStatus.textContent='Texto alternativo actualizado con los resultados.';});
    restoreSeasonPosterFromUrl();
    updateSeasonPosterPreview();
    renderSeasonSavedLinks();
    socialKitFormat?.addEventListener('change',scheduleKitEstimates);
    socialKitButton?.addEventListener('click',async () => {
      if (socialKitStatus) socialKitStatus.textContent = 'Preparando tres formatos…';
      try { await downloadSocialKit(); }
      catch (error) {
        if (socialKitStatus) socialKitStatus.textContent = error instanceof Error ? error.message : 'No se pudo preparar el kit social.';
      }
    });
    seasonQrA5Button?.addEventListener('click',downloadSeasonQrA5);
    socialPrintButton?.addEventListener('click',()=>{try{downloadPrintableSocialSvg();}catch(error){if(socialPrintStatus)socialPrintStatus.textContent=error instanceof Error?error.message:'No se pudo preparar la plantilla imprimible.';}});
    contactSheetPrintButton?.addEventListener('click',()=>{try{downloadPrintableContactSheet();}catch(error){if(socialPrintStatus)socialPrintStatus.textContent=error instanceof Error?error.message:'No se pudo preparar la hoja de contacto.';}});
    contactSheetPdfButton?.addEventListener('click',async()=>{try{await downloadPrintableContactSheetPdf();}catch(error){if(socialPrintStatus)socialPrintStatus.textContent=error instanceof Error?error.message:'No se pudo preparar el PDF vectorial.';}});
    contactSheetDirectPrintButton?.addEventListener('click',()=>{try{printContactSheetDirectly();}catch(error){if(socialPrintStatus)socialPrintStatus.textContent=error instanceof Error?error.message:'No se pudo abrir la impresión A4.';}});
    comparisonA5PdfButton?.addEventListener('click',async()=>{try{await downloadPrintableComparisonA5();}catch(error){if(socialPrintStatus)socialPrintStatus.textContent=error instanceof Error?error.message:'No se pudo preparar el PDF A5.';}});
    comparisonTextButton?.addEventListener('click',()=>{try{downloadComparisonText();}catch(error){if(socialPrintStatus)socialPrintStatus.textContent=error instanceof Error?error.message:'No se pudo preparar el texto de la comparación.';}});
    comparisonHtmlButton?.addEventListener('click',()=>{try{openPrintableComparisonHtml();}catch(error){if(socialPrintStatus)socialPrintStatus.textContent=error instanceof Error?error.message:'No se pudo preparar la versión HTML accesible.';}});
    comparisonA5DirectPrintButton?.addEventListener('click',()=>{try{printComparisonA5Directly();}catch(error){if(socialPrintStatus)socialPrintStatus.textContent=error instanceof Error?error.message:'No se pudo abrir la impresión A5.';}});
    [printPaperSelect,printOrientationSelect,contactSheetVariantSelect].forEach(control=>control?.addEventListener('change',()=>{savePrintSettings();updateContactSheetPrintPreview();updateA5PrintPreview();if(printSettingsStatus)printSettingsStatus.textContent='Preferencias guardadas en este navegador.';}));
    comparisonA5InkSelect?.addEventListener('change',()=>{savePrintSettings();updateA5PrintPreview();if(printSettingsStatus)printSettingsStatus.textContent='Preferencias guardadas en este navegador.';});
    resetPrintSettingsButton?.addEventListener('click',clearPrintSettings);
    comparisonA5PreviewButton?.addEventListener('click',openA5PrintPreview);
    comparisonA5DialogClose?.addEventListener('click',()=>{if(typeof comparisonA5Dialog?.close==='function')comparisonA5Dialog.close();else comparisonA5Dialog?.removeAttribute('open');});
    comparisonA5Dialog?.addEventListener('click',event=>{if(event.target===comparisonA5Dialog&&typeof comparisonA5Dialog.close==='function')comparisonA5Dialog.close();});
    document.addEventListener('keydown',event=>{
      if(event.altKey||event.ctrlKey||event.metaKey)return;
      const target=event.target,tag=target instanceof HTMLElement?target.tagName:'';
      if(['INPUT','TEXTAREA','SELECT'].includes(tag)||(target instanceof HTMLElement&&target.isContentEditable))return;
      if(event.key.toLowerCase()==='p'){
        event.preventDefault();
        if(comparisonA5Dialog?.open){if(typeof comparisonA5Dialog.close==='function')comparisonA5Dialog.close();else comparisonA5Dialog.removeAttribute('open');}
        else openA5PrintPreview();
      }else if(event.key==='Escape'&&comparisonA5Dialog?.open){
        if(typeof comparisonA5Dialog.close==='function')comparisonA5Dialog.close();else comparisonA5Dialog.removeAttribute('open');
      }
    });
    printQuickButtons.forEach(button=>button.addEventListener('click',()=>{
      const target=document.querySelector(button.dataset.saltoImpresion==='a4'?'[data-imprimir-hoja-directa]':'[data-imprimir-a5-directa]');
      if(!target)return;
      target.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'center'});
      target.focus({preventScroll:true});
    }));
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
