(function(){
'use strict';
const $=id=>document.getElementById(id),core=globalThis.LDP2;
const number=new Intl.NumberFormat('es-ES',{maximumFractionDigits:1});
const percent=value=>number.format(value*100)+' %';
function download(content,type,name){const url=URL.createObjectURL(new Blob([content],{type})),link=document.createElement('a');link.href=url;link.download=name;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
function distribution(){
 const n=Number($('tiros').value),p=Number($('prob').value)/100,values=core.distribution(n,p),max=Math.max(...values),mode=values.indexOf(max);
 const rows=values.map((probability,goals)=>{const row=document.createElement('tr'),label=document.createElement('th'),value=document.createElement('td'),chart=document.createElement('td'),bar=document.createElement('span');label.scope='row';label.textContent=String(goals);value.textContent=probability>0&&probability<.0005?'< 0,1 %':percent(probability);bar.className='probability-bar';bar.style.width=(probability/max*100)+'%';bar.setAttribute('aria-hidden','true');chart.append(bar);row.append(label,value,chart);return row;});
 $('distribucion-cuerpo').replaceChildren(...rows);
 $('distribucion-resumen').textContent='Promedio: '+number.format(n*p)+' goles. Un resultado más probable: '+mode+' goles ('+percent(max)+'). Puede haber empates en la probabilidad máxima.';
}
$('tiros').addEventListener('input',distribution);$('prob').addEventListener('input',distribution);distribution();
function uncertainty(){
 const n=Number($('muestra-tiros').value),input=$('muestra-goles');input.max=String(n);input.value=String(Math.min(Number(input.value),n));const k=Number(input.value),interval=core.wilson(k,n);
 $('muestra-n').value=n;$('muestra-k').value=k;$('muestra-resultado').textContent=percent(interval.rate);
 $('muestra-intervalo').style.left=(interval.low*100)+'%';$('muestra-intervalo').style.width=((interval.high-interval.low)*100)+'%';
 $('muestra-lectura').textContent=k+' goles en '+n+' disparos. Intervalo: '+percent(interval.low)+' a '+percent(interval.high)+'. Amplitud: '+number.format((interval.high-interval.low)*100)+' puntos porcentuales.';
}
$('muestra-tiros').addEventListener('input',uncertainty);$('muestra-goles').addEventListener('input',uncertainty);uncertainty();
const payload=JSON.parse($('temporada-datos').textContent);let selection=[];
const rows=[...document.querySelectorAll('[data-season-row]')];
function season(){
 selection=core.filterMatches(payload.partidos,$('temporada-sede').value,$('temporada-resultado').value,$('temporada-cobertura').value);
 const summary=core.summarize(selection),shown=new Set(selection.map(m=>String(m.jornada)));
 rows.forEach(row=>row.hidden=!shown.has(row.dataset.seasonRow));
 const values=[['Partidos',summary.games],['Puntos',summary.points],['Goles a favor',summary.gf],['Goles en contra',summary.gc]];
 $('temporada-resumen').replaceChildren(...values.map(([name,value])=>{const item=document.createElement('p'),strong=document.createElement('strong');strong.textContent=String(value);item.append(strong,document.createTextNode(name));return item;}));
 const shots=summary.shots===null?'Sin tiros validados para esta selección.':'Tiros por partido: '+number.format(summary.shots)+'–'+number.format(summary.against)+' (Zaragoza–rival; n = '+summary.shotsCount+').';
 const possession=summary.possession===null?'Sin posesión validada.':'Posesión media: '+number.format(summary.possession)+' % (n = '+summary.possessionCount+').';
 $('temporada-metricas').textContent=summary.complete+' fichas completas de '+summary.games+' partidos. '+shots+' '+possession;
 $('temporada-vacia').hidden=selection.length>0;$('temporada-csv').disabled=selection.length===0;
}
['temporada-sede','temporada-resultado','temporada-cobertura'].forEach(id=>$(id).addEventListener('change',season));
$('temporada-restablecer').addEventListener('click',()=>{$('temporada-sede').value='Todas';$('temporada-resultado').value='Todos';$('temporada-cobertura').value='Todas';season();});
$('temporada-csv').addEventListener('click',()=>{if(selection.length)download(core.csv(selection,payload.corte),'text/csv;charset=utf-8','zaragoza-seleccion-'+payload.corte+'.csv');});
$('temporada-controles').hidden=false;$('temporada-acciones').hidden=false;season();
})();
