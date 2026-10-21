(() => {
  const controls = document.getElementById('controles-archivo');
  if (!controls) return;
  const search = document.getElementById('buscar-archivo');
  const keys = ['temporada', 'rival', 'tema'];
  const filters = keys.map(key => document.getElementById(`filtro-${key}`));
  const cards = [...document.querySelectorAll('.archivo-lista > li')];
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  function update() {
    const query = normalize(search.value);
    let count = 0;
    cards.forEach(card => {
      const matches = normalize(card.textContent).includes(query) && filters.every((filter, i) => !filter.value || card.dataset[keys[i]] === filter.value);
      card.hidden = !matches;
      if (matches) count += 1;
    });
    document.getElementById('recuento-archivo').textContent = `${count} ${count === 1 ? 'análisis encontrado' : 'análisis encontrados'}`;
    document.getElementById('archivo-vacio').hidden = count !== 0;
  }
  controls.hidden = false;
  search.addEventListener('input', update);
  filters.forEach(filter => filter.addEventListener('change', update));
  document.getElementById('limpiar-archivo').addEventListener('click', () => {
    search.value = '';
    filters.forEach(filter => { filter.value = ''; });
    update();
    search.focus();
  });
  update();
})();
