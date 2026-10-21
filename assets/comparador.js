(() => {
  'use strict';
  const state=document.getElementById('estado-comparador'),controls=document.getElementById('controles-comparador');
  if(!state||!controls)return;
  const result=document.getElementById('resultado-comparador'),provenance=document.getElementById('fuentes-comparadas');
  const a=document.getElementById('equipo-a'),b=document.getElementById('equipo-b'),venue=document.getElementById('sede-comparador'),source=document.getElementById('fuentes-comparador'),mode=document.getElementById('modo-comparador'),period=document.getElementById('periodo-comparador');
  const format=n=>n.toLocaleString('es-ES',{maximumFractionDigits:2});
  const node=(tag,text,cls)=>{const el=document.createElement(tag);if(text!==undefined)el.textContent=text;if(cls)el.className=cls;return el;};
  const metrics=['pj','puntos','gf','gc','xg','xgc','claras','clarasContra','tiros','posesion'];
  let exported=[];
  function restore(){const params=new URL(location.href).searchParams;[['a',a],['b',b],['sede',venue],['fuente',source],['modo',mode],['periodo',period]].forEach(([key,select])=>{const value=params.get(key);if([...select.options].some(o=>o.value===value))select.value=value;});}
  restore();
  fetch('../datos/comparador-grupo2.json').then(r=>{if(!r.ok)throw Error();return r.json();}).then(data=>{
    function update(save=true){
      const options={sede:venue.value,fuente:source.value,modo:mode.value,periodo:period.value,jornada:data.jornada};
      const sample=LPGrupo.filter(data.partidos,options),names=[a.value,b.value],rows=names.map(team=>sample.filter(r=>r.equipo===team));
      if(save){const url=new URL(location.href);Object.entries({a:a.value,b:b.value,sede:venue.value,fuente:source.value,modo:mode.value,periodo:period.value}).forEach(([k,v])=>url.searchParams.set(k,v));history.replaceState(null,'',url);}
      result.replaceChildren();provenance.replaceChildren();exported=[];
      const wrap=node('div',undefined,'tabla-comparador'),table=node('table');
      table.append(node('caption',names.join(' frente a ')+' · '+(venue.value||'Casa y fuera')+' · '+(period.value==='ultimas5'?'Últimas cinco jornadas':'Toda la temporada')));
      const head=node('thead'),hr=node('tr');['Indicador',...names,'Media del grupo'].forEach(t=>{const th=node('th',t);th.scope='col';hr.append(th);});head.append(hr);table.append(head);
      const body=node('tbody');
      metrics.forEach(id=>{
        const title=LPGrupo.label(id,mode.value),tr=node('tr'),th=node('th',title);th.scope='row';
        if(id!=='pj'){th.append(node('small',LPGrupo.definitions[id].direction));const details=node('details',undefined,'ayuda-metrica');details.append(node('summary','Qué mide'),node('p',LPGrupo.definitions[id].description));th.append(details);}
        tr.append(th);
        const values=rows.map(r=>LPGrupo.calc(r,id,options)),reference=LPGrupo.reference(sample,id,options);
        values.forEach(value=>{
          const td=node('td');td.append(node('strong',value.value===null?'Sin dato':format(value.value)));
          if(id!=='pj')td.append(node('small',value.count+' partidos con dato'));
          if(value.value!==null&&id!=='pj'){
            const track=node('span',undefined,'pista-comparador'),bar=node('span',undefined,'barra-comparador'),mark=node('span',undefined,'marca-media');track.setAttribute('aria-hidden','true');
            bar.style.width=(reference.max?value.value/reference.max*100:0)+'%';mark.style.left=(reference.max?reference.value/reference.max*100:0)+'%';track.append(bar,mark);td.append(track);
          }
          tr.append(td);
        });
        const referenceCell=node('td');referenceCell.append(node('strong',reference.value===null?'Sin dato':format(reference.value)),node('small',mode.value==='totales'||id==='pj'?'Media por equipo':'Media por partido'));tr.append(referenceCell);body.append(tr);
        exported.push({label:title,values:values.map(v=>v.value===null?'Sin dato':format(v.value)+' (n='+v.count+')'),reference:reference.value===null?'Sin dato':format(reference.value)});
      });
      table.append(body);wrap.append(table);result.append(wrap);
      rows.forEach((matches,i)=>{provenance.append(node('h3',names[i]));const list=node('ul');matches.forEach(row=>{const li=node('li','J'+row.jornada+' · '+row.rival+' · ');if(!Number.isFinite(row.xg))li.append(document.createTextNode('xG sin dato'));else{const link=node('a',LPGrupo.official(row)?'Sofascore':'Fuente complementaria');try{const url=new URL(row.fuente_xg);if(url.protocol==='https:')link.href=url.href;}catch{}li.append(link);if(source.value==='sofascore'&&!LPGrupo.official(row))li.append(document.createTextNode(' · excluida del cálculo de xG'));}list.append(li);});provenance.append(list);});
      state.textContent=names[0]+' ('+rows[0].length+' partidos) frente a '+names[1]+' ('+rows[1].length+' partidos). '+(mode.value==='promedio'?'Valores por partido.':'Totales del filtro.')+' Corte: J'+data.jornada+'.';
      document.getElementById('ir-mapa').href='../mapa-grupo/index.html?equipo='+encodeURIComponent(a.value)+'&sede='+encodeURIComponent(venue.value)+'&fuente='+source.value+'&periodo='+period.value;
    }
    controls.hidden=false;[a,b,venue,source,mode,period].forEach(s=>s.addEventListener('change',()=>update()));
    document.getElementById('intercambiar-equipos').addEventListener('click',()=>{[a.value,b.value]=[b.value,a.value];update();});
    document.getElementById('copiar-comparacion').addEventListener('click',async()=>{update();const url=location.href;try{await navigator.clipboard.writeText(url);document.getElementById('estado-compartir').textContent='Enlace copiado con todos los filtros.';}catch{const fallback=document.getElementById('enlace-comparacion');fallback.hidden=false;fallback.value=url;fallback.focus();fallback.select();document.getElementById('estado-compartir').textContent='El enlace está seleccionado y se puede copiar.';}});
    document.getElementById('descargar-comparacion').addEventListener('click',()=>{
      const canvas=document.createElement('canvas');canvas.width=1500;canvas.height=1130;const ctx=canvas.getContext('2d');ctx.fillStyle='#ffffff';ctx.fillRect(0,0,1500,1130);ctx.fillStyle='#123923';ctx.font='bold 32px Arial';ctx.fillText('Primera Federación · Grupo 2',50,55);ctx.font='bold 25px Arial';ctx.fillText(a.value+' frente a '+b.value,50,99);ctx.font='19px Arial';ctx.fillText((venue.value||'Casa y fuera')+' · '+(period.value==='ultimas5'?'Últimas cinco jornadas':'Toda la temporada')+' · '+(mode.value==='promedio'?'Por partido':'Totales')+' · Corte J'+data.jornada,50,136);
      ctx.fillStyle='#eaf1ec';ctx.fillRect(40,170,1420,52);ctx.fillStyle='#152a1e';ctx.font='bold 20px Arial';[['Indicador',55],[a.value,630],[b.value,920],['Media del grupo',1210]].forEach(([t,x])=>ctx.fillText(t,x,203));
      exported.forEach((row,i)=>{const y=255+i*66;if(i%2===0){ctx.fillStyle='#f6f8f5';ctx.fillRect(40,y-25,1420,60);}ctx.fillStyle='#152a1e';ctx.font='19px Arial';ctx.fillText(row.label,55,y);ctx.fillText(row.values[0],630,y);ctx.fillText(row.values[1],920,y);ctx.fillText(row.reference,1210,y);});
      ctx.font='18px Arial';ctx.fillStyle='#506657';ctx.fillText('xG: '+(source.value==='sofascore'?'solo Sofascore':'Sofascore y fuentes complementarias documentadas')+'. n = partidos con dato.',50,978);ctx.fillText('La posesión mantiene su media porcentual. Cobertura y fuentes en el análisis original.',50,1008);ctx.fillStyle='#1f6b3e';ctx.font='bold 24px Arial';ctx.fillText('Línea de pase · lineadepase.com',50,1070);
      canvas.toBlob(blob=>{if(!blob)return;const url=URL.createObjectURL(blob),link=document.createElement('a');link.href=url;link.download='linea-de-pase-comparacion-grupo2.png';link.click();setTimeout(()=>URL.revokeObjectURL(url),30000);},'image/png');
    });
    window.addEventListener('popstate',()=>{restore();update(false);});update(false);
  }).catch(()=>{state.textContent='No se han podido cargar los datos. La tabla del análisis del grupo sigue disponible.';});
})();
