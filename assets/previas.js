/* Las fechas se interpretan en Madrid; una hora programada no acredita el estado del partido. */
(() => {
  function actualizar() {
    const grid = document.querySelector('.previas-rejilla');
    if (!grid) return;
    const parts = new Intl.DateTimeFormat('en-CA', {timeZone:'Europe/Madrid',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(new Date());
    const value = key => parts.find(x => x.type === key).value;
    const today = `${value('year')}-${value('month')}-${value('day')}`;
    const cards = Array.from(grid.children);
    cards.sort((a,b) => {
      const ad=a.dataset.fecha, bd=b.dataset.fecha;
      if ((ad>=today)!==(bd>=today)) return ad>=today?-1:1;
      return ad>=today?ad.localeCompare(bd):bd.localeCompare(ad);
    });
    for (const card of cards) {
      const date=card.dataset.fecha, short=date.slice(8,10)+'/'+date.slice(5,7);
      card.querySelector('.estado-previa').textContent = date===today ? 'Hoy'+(card.dataset.hora?' · '+card.dataset.hora:'') : (date<today?'Previa del ':'Próxima cita · ')+short;
      grid.appendChild(card);
    }
  }
  actualizar();
  setInterval(actualizar,60000);
  document.addEventListener('visibilitychange',()=>{if(!document.hidden)actualizar();});
})();
