(() => {
  const controls = document.getElementById('controles-archivo');
  if (!controls) return;
  const search = document.getElementById('buscar-archivo');
  const keys = ['temporada', 'rival', 'tema', 'tipo'];
  const filters = keys.map(key => document.getElementById(`filtro-${key}`));
  const cards = [...document.querySelectorAll('.archivo-lista > li')];
  const folders = [...document.querySelectorAll('.archivo-carpeta')];
  const shareButton = document.getElementById('compartir-filtros');
  const shareStatus = document.getElementById('estado-compartir-archivo');
  let wasFiltering = false;
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();

  const incoming = new URLSearchParams(window.location.search);
  search.value = incoming.get('q') || '';
  filters.forEach((filter, index) => {
    const value = incoming.get(keys[index]);
    if (value && [...filter.options].some(option => option.value === value)) filter.value = value;
  });

  function syncUrl() {
    const url = new URL(window.location.href);
    const params = new URLSearchParams();
    if (search.value.trim()) params.set('q', search.value.trim());
    filters.forEach((filter, index) => {
      if (filter.value) params.set(keys[index], filter.value);
    });
    url.search = params.toString();
    window.history.replaceState(window.history.state, '', url);
  }

  function update() {
    const query = normalize(search.value);
    let count = 0;
    cards.forEach(card => {
      const matches = normalize(card.textContent).includes(query) && filters.every((filter, i) => !filter.value || card.dataset[keys[i]] === filter.value);
      card.hidden = !matches;
      if (matches) count += 1;
    });
    const filtering = !!query || filters.some(filter => !!filter.value);
    folders.forEach(folder => {
      const visible = [...folder.querySelectorAll('.archivo-lista > li')].filter(card => !card.hidden).length;
      folder.hidden = visible === 0;
      folder.querySelector('.carpeta-cantidad').textContent = `${visible} ${visible === 1 ? 'recurso' : 'recursos'}`;
      if (filtering) folder.open = visible > 0;
      else if (wasFiltering) folder.open = false;
    });
    wasFiltering = filtering;
    document.getElementById('recuento-archivo').textContent = `${count} ${count === 1 ? 'resultado encontrado' : 'resultados encontrados'}`;
    document.getElementById('archivo-vacio').hidden = count !== 0;
    syncUrl();
  }

  controls.hidden = false;
  search.addEventListener('input', update);
  filters.forEach(filter => filter.addEventListener('change', update));
  document.getElementById('limpiar-archivo').addEventListener('click', () => {
    search.value = '';
    filters.forEach(filter => { filter.value = ''; });
    if (shareStatus) shareStatus.textContent = '';
    update();
    search.focus();
  });
  if (shareButton) {
    shareButton.addEventListener('click', async () => {
      syncUrl();
      try {
        await navigator.clipboard.writeText(window.location.href);
        shareStatus.textContent = 'Enlace de búsqueda copiado.';
      } catch {
        shareStatus.textContent = 'La búsqueda ya está en la dirección de esta página; se puede copiar desde el navegador.';
      }
    });
  }
  update();
})();
