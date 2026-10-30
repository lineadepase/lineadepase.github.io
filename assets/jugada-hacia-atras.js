(() => {
  const control = document.querySelector('[data-jugada-inversa]');
  if (!control) return;
  const nodes = [...document.querySelectorAll('.pizarron-secuencia [data-paso]')];
  const steps = [...document.querySelectorAll('.pizarron-pasos li')];
  const status = control.querySelector('[data-estado-jugada]');
  const back = control.querySelector('[data-retroceder]');
  const forward = control.querySelector('[data-avanzar]');
  if (!nodes.length || !steps.length || !status || !back || !forward) return;
  let current = steps.length - 1;
  const render = () => {
    nodes.forEach((node, index) => node.classList.toggle('paso-activo', index === current));
    steps.forEach((step, index) => step.toggleAttribute('data-paso-actual', index === current));
    status.textContent = `Paso ${current + 1} de ${steps.length}: ${steps[current].textContent.trim()}`;
    back.disabled = current === 0;
    forward.disabled = current === steps.length - 1;
  };
  back.addEventListener('click', () => { current = Math.max(0, current - 1); render(); });
  forward.addEventListener('click', () => { current = Math.min(steps.length - 1, current + 1); render(); });
  render();
})();
