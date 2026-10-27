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

  const labelFor = (date, time, now) => {
    if (date < now.date) return 'Partido disputado';
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
      const label = card.querySelector('.estado-previa');
      if (label) {
        label.textContent = labelFor(date, time, now);
      }
      const previewLink = card.querySelector('.enlace-editorial');
      if (previewLink && date < now.date) previewLink.textContent = 'Consultar la previa publicada antes del partido';
    });

    document.querySelectorAll('.estado-partido-detalle[data-fecha]').forEach(label => {
      const date = label.dataset.fecha;
      const time = label.dataset.hora || '';
      label.textContent = labelFor(date, time, now);
    });

    document.querySelectorAll('.calendario-partido[data-fecha]').forEach(link => {
      const date = link.dataset.fecha;
      const time = link.dataset.hora || '00:00';
      const started = date < now.date || (date === now.date && now.time >= time);
      link.hidden = started;
    });

    document.querySelectorAll('.postpartido-disponible[data-fecha]').forEach(note => {
      note.hidden = note.dataset.fecha >= now.date;
    });
  }

  update();
  window.setInterval(update, 60_000);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) update(); });
})();
