(() => {
  'use strict';
  const collectionControls=document.querySelector('[data-filtros-galeria="coleccion"]');
  const formatControls=document.querySelector('[data-filtros-galeria="formato"]');
  const grid=document.querySelector('[data-galeria-visual]');
  if(!collectionControls||!formatControls||!grid)return;
  const cards=[...grid.querySelectorAll('[data-coleccion-visual]')];
  const status=document.querySelector('[data-recuento-galeria]');
  const state={collection:'todos',format:'todos'};
  function update(){
    let visible=0;
    cards.forEach(card=>{
      const collectionMatch=state.collection==='todos'||card.dataset.coleccionVisual===state.collection;
      const formatMatch=state.format==='todos'||card.dataset.formatosVisual.split(' ').includes(state.format);
      const show=collectionMatch&&formatMatch;
      card.hidden=!show;
      if(show)visible++;
    });
    collectionControls.querySelectorAll('[data-filtro-coleccion]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.filtroColeccion===state.collection)));
    formatControls.querySelectorAll('[data-filtro-formato]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.filtroFormato===state.format)));
    status.textContent=`${visible} ${visible===1?'pieza':'piezas'}`;
  }
  collectionControls.querySelectorAll('[data-filtro-coleccion]').forEach(button=>button.addEventListener('click',()=>{state.collection=button.dataset.filtroColeccion;update();}));
  formatControls.querySelectorAll('[data-filtro-formato]').forEach(button=>button.addEventListener('click',()=>{state.format=button.dataset.filtroFormato;update();}));
  collectionControls.hidden=false;
  formatControls.hidden=false;
  update();
})();
