(() => {
  'use strict';
  const chart=document.getElementById('mapa-plot');if(!chart)return;
  const team=document.getElementById('mapa-equipo'),xMetric=document.getElementById('mapa-x'),yMetric=document.getElementById('mapa-y'),venue=document.getElementById('mapa-sede'),period=document.getElementById('mapa-periodo'),source=document.getElementById('mapa-fuente');
  const fmt=n=>n.toLocaleString('es-ES',{maximumFractionDigits:2});
  const node=(tag,text)=>{const el=document.createElement(tag);if(text!==undefined)el.textContent=text;return el;};
  const params=new URL(location.href).searchParams;[['equipo',team],['x',xMetric],['y',yMetric],['sede',venue],['periodo',period],['fuente',source]].forEach(([k,s])=>{if([...s.options].some(o=>o.value===params.get(k)))s.value=params.get(k);});
  fetch('../datos/comparador-grupo2.json').then(r=>{if(!r.ok)throw Error();return r.json();}).then(data=>{
    function update(){
      const options={sede:venue.value,periodo:period.value,fuente:source.value,jornada:data.jornada,modo:'promedio'};
      const sample=LPGrupo.filter(data.partidos,options),names=[...new Set(sample.map(r=>r.equipo))].sort();
      const points=names.map(name=>{const rows=sample.filter(r=>r.equipo===name);return {name,x:LPGrupo.calc(rows,xMetric.value,options),y:LPGrupo.calc(rows,yMetric.value,options)};}).filter(p=>p.x.value!==null&&p.y.value!==null);
      chart.replaceChildren();
      const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('viewBox','0 0 850 540');svg.setAttribute('role','group');svg.setAttribute('aria-label','Mapa de los equipos: '+LPGrupo.label(xMetric.value)+' y '+LPGrupo.label(yMetric.value));
      const el=(tag,attributes,text)=>{const n=document.createElementNS(svg.namespaceURI,tag);Object.entries(attributes).forEach(([k,v])=>n.setAttribute(k,v));if(text!==undefined)n.textContent=text;svg.append(n);return n;};
      const maxX=Math.max(1,...points.map(p=>p.x.value))*1.12,maxY=Math.max(1,...points.map(p=>p.y.value))*1.12;
      const x=v=>85+v/maxX*700,y=v=>435-v/maxY*365;
      for(let i=0;i<=4;i++){const vx=maxX*i/4,vy=maxY*i/4;el('line',{x1:x(vx),x2:x(vx),y1:70,y2:435,stroke:'#dce5df'});el('line',{x1:85,x2:785,y1:y(vy),y2:y(vy),stroke:'#dce5df'});el('text',{x:x(vx),y:461,'text-anchor':'middle',fill:'currentColor','font-size':14},fmt(vx));el('text',{x:72,y:y(vy)+5,'text-anchor':'end',fill:'currentColor','font-size':14},fmt(vy));}
      const mx=LPGrupo.reference(sample,xMetric.value,options).value,my=LPGrupo.reference(sample,yMetric.value,options).value;
      if(mx!==null)el('line',{x1:x(mx),x2:x(mx),y1:70,y2:435,stroke:'#647869','stroke-dasharray':'6 5'});
      if(my!==null)el('line',{x1:85,x2:785,y1:y(my),y2:y(my),stroke:'#647869','stroke-dasharray':'6 5'});
      el('text',{x:435,y:506,'text-anchor':'middle',fill:'currentColor','font-size':17},LPGrupo.label(xMetric.value));
      el('text',{x:85,y:35,fill:'currentColor','font-size':17},'Eje vertical: '+LPGrupo.label(yMetric.value));
      points.forEach(p=>{const chosen=p.name===team.value,circle=el('circle',{cx:x(p.x.value),cy:y(p.y.value),r:chosen?10:6.5,fill:chosen?'#ff6a2b':'#427951',stroke:chosen?'#1f3528':'#ffffff','stroke-width':2,tabindex:0,role:'button','aria-label':p.name+': '+fmt(p.x.value)+'; '+fmt(p.y.value)});const title=document.createElementNS(svg.namespaceURI,'title');title.textContent=p.name+' · '+fmt(p.x.value)+' / '+fmt(p.y.value);circle.append(title);const choose=()=>{team.value=p.name;update();};circle.addEventListener('click',choose);circle.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();choose();}});if(chosen)el('text',{x:x(p.x.value)+(x(p.x.value)>600?-14:14),y:y(p.y.value)-15,'text-anchor':x(p.x.value)>600?'end':'start',fill:'currentColor','font-size':16,'font-weight':700},p.name);});
      chart.append(svg);
      const chosen=points.find(p=>p.name===team.value);document.getElementById('mapa-detalle').textContent=chosen?chosen.name+': '+fmt(chosen.x.value)+' en '+LPGrupo.label(xMetric.value)+' ('+chosen.x.count+' partidos) y '+fmt(chosen.y.value)+' en '+LPGrupo.label(yMetric.value)+' ('+chosen.y.count+' partidos).':'El equipo seleccionado no tiene datos suficientes para estos ejes.';
      document.getElementById('mapa-nota').textContent='Corte J'+data.jornada+' · '+(period.value==='ultimas5'?'Últimas cinco jornadas':'Toda la temporada')+' · '+(venue.value||'Casa y fuera')+' · xG: '+(source.value==='sofascore'?'Sofascore':'Sofascore y fuentes complementarias')+'. Las líneas discontinuas representan la media del grupo.';
      const tbody=document.getElementById('mapa-tabla');tbody.replaceChildren();[...points].sort((a,b)=>b.x.value-a.x.value).forEach(p=>{const tr=node('tr');[p.name,fmt(p.x.value)+' (n='+p.x.count+')',fmt(p.y.value)+' (n='+p.y.count+')'].forEach(t=>tr.append(node('td',t)));tbody.append(tr);});
      document.getElementById('mapa-th-x').textContent=LPGrupo.label(xMetric.value);document.getElementById('mapa-th-y').textContent=LPGrupo.label(yMetric.value);
      const rival=team.value==='Real Zaragoza'?'Villarreal B':team.value;
      const query=new URLSearchParams({a:'Real Zaragoza',b:rival,sede:venue.value,fuente:source.value,periodo:period.value,modo:'promedio'});const compareLink=document.getElementById('mapa-comparar');compareLink.href='../comparador/index.html?'+query;compareLink.textContent=team.value==='Real Zaragoza'?'Comparar Zaragoza y Villarreal B':'Comparar el equipo con el Zaragoza';
      const url=new URL(location.href);Object.entries({equipo:team.value,x:xMetric.value,y:yMetric.value,sede:venue.value,fuente:source.value,periodo:period.value}).forEach(([k,v])=>url.searchParams.set(k,v));history.replaceState(null,'',url);
    }
    document.getElementById('controles-mapa').hidden=false;[team,xMetric,yMetric,venue,period,source].forEach(s=>s.addEventListener('change',update));update();
  }).catch(()=>{document.getElementById('mapa-detalle').textContent='No se han podido cargar los datos del mapa. La tabla del análisis del grupo sigue disponible.';});
})();
