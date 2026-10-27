(() => {
  'use strict';
  document.querySelectorAll('.reto-marcador').forEach(card => {
    const form = card.querySelector('.marcador-ciego-form');
    const reveal = card.querySelector('.marcador-ciego-revelar');
    const feedback = card.querySelector('.marcador-ciego-feedback');
    if (!form || !reveal || !feedback) return;
    form.addEventListener('submit', event => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const guessHome = Number(form.elements.local.value);
      const guessAway = Number(form.elements.visitante.value);
      const scoreHome = Number(card.dataset.golesLocal);
      const scoreAway = Number(card.dataset.golesVisitante);
      const exact = guessHome === scoreHome && guessAway === scoreAway;
      const outcome = Math.sign(guessHome - guessAway) === Math.sign(scoreHome - scoreAway);
      feedback.textContent = exact ? 'Marcador exacto.' : outcome ? 'Has acertado quién ganó, aunque no el marcador.' : 'El marcador contaba otra historia.';
      reveal.open = true;
      form.querySelectorAll('input,button').forEach(control => { control.disabled = true; });
    });
  });
})();
