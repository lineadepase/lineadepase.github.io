(() => {
  'use strict';
  const state = document.getElementById('estado-comparador');
  const controls = document.getElementById('controles-comparador');
  if (!state || !controls) return;
  const result = document.getElementById('resultado-comparador');
  const provenance = document.getElementById('fuentes-comparadas');
  const a = document.getElementById('equipo-a'), b = document.getElementById('equipo-b');
  const venue = document.getElementById('sede-comparador'), source = document.getElementById('fuentes-comparador');
  const format = n => n.toLocaleString('es-ES', {maximumFractionDigits: 2});
  const metrics = [
    ['Partidos', null, 'count'], ['Puntos', null, 'points'],
    ['Goles a favor', 'goles_favor', 'sum'], ['Goles en contra', 'goles_contra', 'sum'],
    ['xG a favor por partido', 'xg', 'mean'], ['xG en contra por partido', 'xg_rival', 'mean'],
    ['Ocasiones claras a favor por partido', 'ocasiones_claras', 'mean'],
    ['Ocasiones claras en contra por partido', 'ocasiones_claras_rival', 'mean'],
    ['Tiros por partido', 'tiros', 'mean'], ['Posesión media (%)', 'posesion_pct', 'mean']
  ];
  const node = (tag, text, className) => { const el = document.createElement(tag); if (text !== undefined) el.textContent = text; if (className) el.className = className; return el; };
  const official = row => { try { return new URL(row.fuente_xg).hostname.endsWith('sofascore.com'); } catch { return false; } };
  function calculate(rows, key, mode) {
    if (mode === 'count') return {value: rows.length, count: rows.length};
    if (mode === 'points') return {value: rows.reduce((sum, row) => sum + (row.goles_favor > row.goles_contra ? 3 : row.goles_favor === row.goles_contra ? 1 : 0), 0), count: rows.length};
    const usable = rows.filter(row => Number.isFinite(row[key]) && (!key.startsWith('xg') || source.value === 'todas' || official(row)));
    if (!usable.length) return {value: null, count: 0};
    const sum = usable.reduce((total, row) => total + row[key], 0);
    return {value: mode === 'sum' ? sum : sum / usable.length, count: usable.length};
  }
  fetch('../datos/comparador-grupo2.json').then(response => { if (!response.ok) throw Error(); return response.json(); }).then(data => {
    function update() {
      const names = [a.value, b.value];
      const rows = names.map(team => data.partidos.filter(row => row.equipo === team && (!venue.value || row.sede === venue.value)));
      result.replaceChildren(); provenance.replaceChildren();
      const wrap = node('div', undefined, 'tabla-comparador');
      const table = node('table'); table.append(node('caption', 'Comparación de ' + names.join(' y ') + ' · ' + (venue.value || 'Casa y fuera')));
      const head = node('thead'), hr = node('tr');
      ['Indicador', ...names].forEach(name => { const th=node('th', name); th.scope='col'; hr.append(th); });
      head.append(hr); table.append(head);
      const body = node('tbody');
      metrics.forEach(([label, key, mode]) => {
        const tr=node('tr'), th=node('th', label); th.scope='row'; tr.append(th);
        const values=rows.map(matches=>calculate(matches,key,mode));
        values.forEach(value => {
          const td=node('td'); td.append(node('strong', value.value === null ? 'Sin dato' : format(value.value)));
          if (key) td.append(node('small', value.count + ' partidos con dato'));
          if (value.value !== null && key) {
            const max=Math.max(...values.map(v=>v.value || 0));
            const bar=node('span', undefined, 'barra-comparador'); bar.setAttribute('aria-hidden','true');
            bar.style.width=(max ? value.value / max * 100 : 0)+'%'; td.append(bar);
          }
          tr.append(td);
        });
        body.append(tr);
      });
      table.append(body); wrap.append(table); result.append(wrap);
      rows.forEach((matches,i)=>{
        provenance.append(node('h3',names[i]));
        const list=node('ul');
        matches.forEach(row=>{
          const li=node('li', 'J'+row.jornada+' · '+row.rival+' · ');
          if (!Number.isFinite(row.xg)) li.append(document.createTextNode('xG sin dato'));
          else {
            const link=node('a',official(row)?'Sofascore':'Fuente complementaria');
            try { const url=new URL(row.fuente_xg); if(url.protocol==='https:') link.href=url.href; } catch {}
            li.append(link); if(source.value==='sofascore'&&!official(row)) li.append(document.createTextNode(' · excluida de los promedios de xG'));
          }
          list.append(li);
        });
        provenance.append(list);
      });
      state.textContent = names[0]+' ('+rows[0].length+' partidos) frente a '+names[1]+' ('+rows[1].length+' partidos). Datos hasta la jornada '+data.jornada+'.';
    }
    controls.hidden=false;
    [a,b,venue,source].forEach(select=>select.addEventListener('change',update));
    update();
  }).catch(()=>{ state.textContent='No se han podido cargar los datos. Recarga la página o consulta las tablas del análisis del grupo.'; });
})();
