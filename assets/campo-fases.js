(() => {
  'use strict';
  const root=document.querySelector('[data-campo-lecturas]');
  if(!root)return;
  const buttons=[...root.querySelectorAll('[data-elegir-fase]')];
  const layers=[...root.querySelectorAll('[data-fase-campo]')];
  const name=root.querySelector('[data-campo-nombre]');
  const description=root.querySelector('[data-campo-descripcion]');
  const title=root.querySelector('#titulo-vista-campo');
  const desc=root.querySelector('#descripcion-vista-campo');
  const phases={
    amplitud:{name:'Amplitud · Abrir el campo',text:'Los jugadores de banda ofrecen líneas exteriores para ensanchar la defensa. El dibujo muestra una idea de ocupación, no una estructura observada en un equipo.'},
    presion:{name:'Presión · Orientar la salida',text:'Un grupo reduce líneas de pase y guía la salida rival hacia una zona. Las flechas indican una intención colectiva, no la presión exacta de un partido.'},
    transicion:{name:'Transición · Avanzar tras recuperar',text:'Después de recuperar el balón, una salida vertical y apoyos por delante pueden aprovechar el espacio. Es una secuencia didáctica, no una jugada reconstruida.'}
  };
  function select(key){
    const phase=phases[key];if(!phase)return;
    buttons.forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.elegirFase===key)));
    layers.forEach(layer=>{layer.style.display=layer.dataset.faseCampo===key?'':'none';});
    name.textContent=phase.name;description.textContent=phase.text;
    title.textContent='Vista de '+phase.name.split(' · ')[0].toLowerCase();desc.textContent=phase.text;
  }
  buttons.forEach(button=>button.addEventListener('click',()=>select(button.dataset.elegirFase)));
  root.querySelector('[data-campo-controles]').hidden=false;
})();
