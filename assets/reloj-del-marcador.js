(() => {
  const raw = document.getElementById('datos-reloj')?.textContent;
  const selector = document.getElementById('selector-reloj');
  const output = document.getElementById('reloj-resultado');
  if (!raw || !selector || !output) return;
  let matches;
  try { matches = JSON.parse(raw); } catch { return; }
  if (!matches.length) return;

  const names = match => match.sede === 'Casa'
    ? `Real Zaragoza – ${match.rival}` : `${match.rival} – Real Zaragoza`;
  matches.forEach((match, index) => {
    const option = document.createElement('option');
    option.value = String(index);
    option.textContent = `J${match.jornada} · ${names(match)}`;
    selector.append(option);
  });

  const buildTimeline = match => {
    const events = [];
    const stoppage = [];
    match.goles.forEach((goal, order) => {
      const [baseText, addedText] = String(goal.minuto).split('+');
      const base = Number(baseText);
      const added = Number(addedText || 0);
      const label = `${base}${added ? `+${added}` : ''}`;
      if (added) stoppage.push({...goal, label, period: base >= 90 ? 'descuento final' : 'descuento de la primera parte', order});
      if (base >= 90 && added) {
        return;
      }
      const minute = base === 45 && added ? 45 : Math.min(90, base);
      if (minute < 0 || minute > 90) return;
      events.push({...goal, minute, label, order});
    });
    events.sort((a, b) => a.minute - b.minute || a.order - b.order);
    const totals = { empate: 0, ventaja: 0, desventaja: 0 };
    const segments = [];
    let z = 0, r = 0, cursor = 0;
    const state = () => z === r ? 'empate' : z > r ? 'ventaja' : 'desventaja';
    for (const event of events) {
      if (event.minute > cursor) {
        const kind = state();
        const duration = event.minute - cursor;
        segments.push({kind, start: cursor, end: event.minute, duration});
        totals[kind] += duration;
        cursor = event.minute;
      }
      if (event.sentido === 'Favor') z += 1; else r += 1;
    }
    if (cursor < 90) {
      const kind = state();
      const duration = 90 - cursor;
      segments.push({kind, start: cursor, end: 90, duration});
      totals[kind] += duration;
    }
    return {segments, totals, stoppage};
  };

  function render() {
    const match = matches[Number(selector.value)];
    if (!match) return;
    const {segments, totals, stoppage} = buildTimeline(match);
    const bar = document.createElement('div');
    bar.className = 'reloj-barra';
    bar.setAttribute('role', 'img');
    bar.setAttribute('aria-label', `En los 90 minutos reglamentarios: ${totals.ventaja} minutos en ventaja, ${totals.empate} en empate y ${totals.desventaja} en desventaja para el Zaragoza.`);
    for (const segment of segments) {
      if (!segment.duration) continue;
      const piece = document.createElement('div');
      piece.className = `reloj-tramo ${segment.kind}`;
      piece.style.width = `${segment.duration / 90 * 100}%`;
      piece.title = `${segment.duration} min · ${segment.kind}`;
      if (segment.duration >= 10) piece.textContent = `${segment.start}′–${segment.end}′`;
      bar.append(piece);
    }
    const summary = document.createElement('dl');
    summary.className = 'reloj-resumen';
    for (const [kind, label] of [['ventaja', 'En ventaja'], ['empate', 'En empate'], ['desventaja', 'En desventaja']]) {
      const item = document.createElement('div');
      const term = document.createElement('dt'); term.textContent = label;
      const value = document.createElement('dd'); value.textContent = `${totals[kind]} min`;
      item.append(term, value); summary.append(item);
    }
    const heading = document.createElement('p');
    heading.className = 'reloj-final';
    const finalScore = match.sede === 'Casa'
      ? `Real Zaragoza ${match.golesFavor}–${match.golesContra} ${match.rival}`
      : `${match.rival} ${match.golesContra}–${match.golesFavor} Real Zaragoza`;
    heading.textContent = `Resultado final: ${finalScore}`;
    const range = document.createElement('p'); range.textContent = 'Minutos reglamentarios';
    const legend = document.createElement('div'); legend.className = 'reloj-leyenda';
    for (const [kind, label] of [['ventaja', 'Zaragoza en ventaja'], ['empate', 'Marcador empatado'], ['desventaja', 'Zaragoza en desventaja']]) {
      const span = document.createElement('span');
      const swatch = document.createElement('i'); swatch.className = `reloj-muestra ${kind}`;
      span.append(swatch, document.createTextNode(label)); legend.append(span);
    }
    const source = document.createElement('a'); source.href = match.href;
    source.textContent = 'Consultar ficha y cronología →';
    output.replaceChildren(heading, range, bar, legend, summary, source);
    if (stoppage.length) {
      const note = document.createElement('p'); note.className = 'reloj-descuento';
      const descriptions = stoppage.map(event => `${event.period}, ${event.label}′: ${event.sentido === 'Favor' ? 'gol del Zaragoza' : 'gol del rival'}${event.jugador ? ` (${event.jugador})` : ''}`).join('; ');
      note.textContent = `Goles de descuento, fuera de la barra: ${descriptions}.`;
      output.append(note);
    }
  }

  selector.addEventListener('change', render);
  render();
})();
