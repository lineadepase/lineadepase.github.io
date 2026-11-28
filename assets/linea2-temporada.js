(function(){
'use strict';
const $=id=>document.getElementById(id),core=globalThis.LDP2;
if(!$('temporada-datos'))return;
const shared=core.readView(globalThis.location?.search||'');
function invalidateShare(kind){if($(kind+'-compartir'))$(kind+'-compartir').hidden=true;}
const number=new Intl.NumberFormat('es-ES',{maximumFractionDigits:1});
function download(content,type,name){const url=URL.createObjectURL(new Blob([content],{type})),link=document.createElement('a');link.href=url;link.download=name;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
const payload=JSON.parse($('temporada-datos').textContent);let selection=[];
const rows=[...document.querySelectorAll('[data-season-row]')];
const compareBoxes=[...document.querySelectorAll('[data-compare-id]')];
let compareIds=[];
function updateComparison(message=''){
 const status=$('temporada-seleccion'),link=$('temporada-studio');if(!status||!link)return;
 compareBoxes.forEach(box=>box.checked=compareIds.includes(box.dataset.compareId));
 link.hidden=compareIds.length!==2;
 if($('temporada-redaccion')){$('temporada-redaccion').hidden=compareIds.length!==2;if(compareIds.length===2&&document.body?.dataset.areaRoot)$('temporada-redaccion').href=core.editorialUrl(globalThis.location.href,compareIds);}
 if(compareIds.length===2)link.href=core.comparisonUrl(globalThis.location?.href||'https://lineadepase.com/datalab-prototipo/',compareIds,document.body?.dataset.siteRoot);
 const names=compareIds.map(id=>{const match=payload.partidos.find(m=>m.archivo_id===id);return match?'J'+match.jornada+' · '+match.rival:id;});
 status.textContent=message||(names.length?'Selección ('+names.length+'/2): '+names.join(' / '):'Elige dos jornadas de la tabla para compararlas en Studio.');
}
compareBoxes.forEach(box=>{box.hidden=false;if(box.parentElement)box.parentElement.hidden=false;box.addEventListener('change',()=>{const id=box.dataset.compareId;if(box.checked&&!compareIds.includes(id)){if(compareIds.length===2){box.checked=false;updateComparison('Ya has elegido dos jornadas. Quita una antes de añadir otra.');return;}compareIds.push(id);}else if(!box.checked)compareIds=compareIds.filter(value=>value!==id);updateComparison();});});
if($('temporada-comparar'))$('temporada-comparar').hidden=compareBoxes.length===0;
function season(){
 invalidateShare('temporada');
 selection=core.filterMatches(payload.partidos,$('temporada-sede').value,$('temporada-resultado').value,$('temporada-cobertura').value);
 const previousCount=compareIds.length;compareIds=compareIds.filter(id=>selection.some(m=>m.archivo_id===id));updateComparison(compareIds.length<previousCount?'Se han quitado de la comparación las jornadas ocultas por los filtros.':'');
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
[['venue','temporada-sede'],['result','temporada-resultado'],['coverage','temporada-cobertura']].forEach(([key,id])=>{if(shared[key]!==undefined)$(id).value=shared[key];});
$('temporada-controles').hidden=false;$('temporada-acciones').hidden=false;season();
function share(kind){
 const button=$(kind+'-enlace');if(!button)return;button.hidden=false;
 button.addEventListener('click',()=>{const state={shots:$('tiros')?Number($('tiros').value):undefined,probability:$('prob')?Number($('prob').value):undefined,sampleShots:$('muestra-tiros')?Number($('muestra-tiros').value):undefined,sampleGoals:$('muestra-goles')?Number($('muestra-goles').value):undefined,venue:$('temporada-sede')?.value,result:$('temporada-resultado')?.value,coverage:$('temporada-cobertura')?.value};
 const field=$(kind+'-url');field.value=core.viewUrl(globalThis.location?.href||'https://lineadepase.com/datalab-prototipo/',state,kind==='temporada'?'season':'labs');$(kind+'-compartir').hidden=false;field.focus();field.select();});
}
share('temporada');
})();
