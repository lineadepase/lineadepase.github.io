(() => {
  const raiz = document.documentElement;
  raiz.classList.add('js-inicializando');
  window.addEventListener('load', () => raiz.classList.remove('js-inicializando'), {once:true});
  try {
    const guardado = localStorage.getItem('lineadepase-tema');
    if (guardado === 'light' || guardado === 'dark') document.documentElement.dataset.theme = guardado;
  } catch (_) { /* Las preferencias siguen funcionando sin almacenamiento. */ }
})();
