(() => {
  const selector = document.getElementById('selector-espejo');
  const button = document.getElementById('comparar-espejo');
  const result = document.getElementById('resultado-espejo');
  const status = document.getElementById('estado-espejo');
  if (!selector || !button || !result || !status) return;

  const matches = [...document.querySelectorAll('.espejo-partido')].map(card => ({
    jornada: Number(card.dataset.jornada), rival: card.dataset.rival,
    posesion: Number(card.dataset.posesion), diferenciaTiros: Number(card.dataset.diferenciaTiros),
    gf: Number(card.dataset.gf), gc: Number(card.dataset.gc),
    tirosZ: Number(card.dataset.tirosZ), tirosR: Number(card.dataset.tirosR)
  }));

  function card(match, heading) {
    const article = document.createElement('article');
    article.className = 'espejo-resultado';
    const title = document.createElement('h3');
    title.textContent = heading;
    const name = document.createElement('p');
    name.textContent = `J${match.jornada} · Real Zaragoza – ${match.rival}`;
    const stats = document.createElement('p');
    stats.textContent = `Posesión: ${match.posesion}% · Tiros: ${match.tirosZ}–${match.tirosR}`;
    const score = document.createElement('p');
    score.innerHTML = '<strong>Resultado:</strong> ';
    score.append(document.createTextNode(`${match.gf}–${match.gc} para el Zaragoza`));
    const link = document.createElement('a');
    link.href = `../proyectos/real-zaragoza/jornada-${match.jornada}.html#titulo-claves`;
    link.textContent = 'Consultar el análisis →';
    article.append(title, name, stats, score, link);
    return article;
  }

  button.addEventListener('click', () => {
    const selected = matches.find(match => match.jornada === Number(selector.value));
    if (!selected) return;
    const candidates = matches.filter(match => match.jornada !== selected.jornada &&
      (match.gf !== selected.gf || match.gc !== selected.gc));
    if (!candidates.length) {
      result.replaceChildren();
      status.textContent = 'No hay otro partido comparable con un resultado distinto en la muestra actual.';
      return;
    }
    candidates.sort((a, b) => {
      const distance = match => Math.abs(match.posesion - selected.posesion) / 5 +
        Math.abs(match.diferenciaTiros - selected.diferenciaTiros) / 5;
      return distance(a) - distance(b) || a.jornada - b.jornada;
    });
    const nearest = candidates[0];
    result.replaceChildren(card(selected, 'Partido elegido'), card(nearest, 'Perfil más cercano con otro resultado'));
    const possessionGap = Math.abs(nearest.posesion - selected.posesion);
    const shotGap = Math.abs(nearest.diferenciaTiros - selected.diferenciaTiros);
    status.textContent = `Diferencia entre perfiles: ${possessionGap} puntos de posesión y ${shotGap} tiros en el balance relativo.`;
  });
})();
