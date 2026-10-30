/* Mantiene las previas útiles después del pitido final según la hora de Madrid. */
(() => {
  const nowInMadrid = () => {
    const parts = new Intl.DateTimeFormat('en-CA', {
      timeZone: 'Europe/Madrid', year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit', hourCycle: 'h23'
    }).formatToParts(new Date());
    const get = type => parts.find(part => part.type === type)?.value || '';
    return { date: `${get('year')}-${get('month')}-${get('day')}`, time: `${get('hour')}:${get('minute')}` };
  };

  const labelFor = (date, time, now, confirmed, score) => {
    const passed = date < now.date || (date === now.date && time && now.time >= time);
    if (passed) return confirmed ? `Resultado confirmado · ${score}` : 'Pendiente de confirmación editorial';
    if (date === now.date) {
      if (time && now.time >= time) return `Inicio previsto superado · sin marcador en directo`;
      return `Hoy${time ? ` · ${time}` : ''}`;
    }
    return `Próxima cita · ${date.slice(8, 10)}/${date.slice(5, 7)}`;
  };

  function update() {
    const now = nowInMadrid();
    document.querySelectorAll('.tarjeta-previa[data-fecha]').forEach(card => {
      const date = card.dataset.fecha;
      const time = card.dataset.hora || '';
      const confirmed = card.dataset.resultadoConfirmado === 'true';
      const score = card.dataset.marcador || '';
      const label = card.querySelector('.estado-previa');
      if (label) label.textContent = labelFor(date, time, now, confirmed, score);
      const previewLink = card.querySelector('.enlace-editorial');
      const passed = date < now.date || (date === now.date && time && now.time >= time);
      if (previewLink && passed) previewLink.textContent = confirmed ? 'Releer la previa' : 'Consultar la previa';
    });

    document.querySelectorAll('.estado-partido-detalle[data-fecha]').forEach(label => {
      const date = label.dataset.fecha;
      const time = label.dataset.hora || '';
      label.textContent = labelFor(date, time, now, label.dataset.resultadoConfirmado === 'true', label.dataset.marcador || '');
    });

    document.querySelectorAll('.calendario-partido[data-fecha]').forEach(link => {
      const date = link.dataset.fecha;
      const time = link.dataset.hora || '00:00';
      const started = date < now.date || (date === now.date && now.time >= time);
      link.hidden = started;
    });

    document.querySelectorAll('.postpartido-disponible[data-fecha]').forEach(note => {
      note.hidden = note.dataset.resultadoConfirmado !== 'true';
    });
  }

  update();
  window.setInterval(update, 60_000);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) update(); });
})();
