(() => {
  'use strict';
  const controls=document.querySelector('[data-filtros-galeria]');
  const grid=document.querySelector('[data-galeria-visual]');
  if(!controls||!grid)return;
  const buttons=[...controls.querySelectorAll('[data-filtro-visual]')];
  const cards=[...grid.querySelectorAll('[data-coleccion-visual]')];
  const status=document.querySelector('[data-recuento-galeria]');
  function filter(category){
    let visible=0;
    cards.forEach(card=>{const show=category==='todos'||card.dataset.coleccionVisual===category;card.hidden=!show;if(show)visible++;});
    buttons.forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.filtroVisual===category)));
    status.textContent=`${visible} ${visible===1?'pieza':'piezas'}`;
  }
  buttons.forEach(button=>button.addEventListener('click',()=>filter(button.dataset.filtroVisual)));
  controls.hidden=false;
})();
