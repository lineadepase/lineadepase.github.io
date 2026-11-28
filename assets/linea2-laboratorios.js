(function(){
'use strict';
const $=id=>document.getElementById(id),core=globalThis.LDP2;
if(!$('tiros'))return;
const shared=core.readView(globalThis.location?.search||'');
if(shared.shots!==undefined)$('tiros').value=String(shared.shots);
if(shared.probability!==undefined)$('prob').value=String(shared.probability);
if(shared.sampleShots!==undefined)$('muestra-tiros').value=String(shared.sampleShots);
$('muestra-goles').max=String($('muestra-tiros').value);
if(shared.sampleGoals!==undefined)$('muestra-goles').value=String(Math.min(shared.sampleGoals,Number($('muestra-tiros').value)));
function invalidateShare(kind){if($(kind+'-compartir'))$(kind+'-compartir').hidden=true;}
const number=new Intl.NumberFormat('es-ES',{maximumFractionDigits:1});
const percent=value=>number.format(value*100)+' %';
function download(content,type,name){const url=URL.createObjectURL(new Blob([content],{type})),link=document.createElement('a');link.href=url;link.download=name;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
function distribution(){
 invalidateShare('laboratorios');
 const n=Number($('tiros').value),p=Number($('prob').value)/100,values=core.distribution(n,p),max=Math.max(...values),mode=values.indexOf(max);
 const rows=values.map((probability,goals)=>{const row=document.createElement('tr'),label=document.createElement('th'),value=document.createElement('td'),chart=document.createElement('td'),bar=document.createElement('span');label.scope='row';label.textContent=String(goals);value.textContent=probability>0&&probability<.0005?'< 0,1 %':percent(probability);bar.className='probability-bar';bar.style.width=(probability/max*100)+'%';bar.setAttribute('aria-hidden','true');chart.append(bar);row.append(label,value,chart);return row;});
 $('distribucion-cuerpo').replaceChildren(...rows);
 $('distribucion-resumen').textContent='Promedio: '+number.format(n*p)+' goles. Un resultado más probable: '+mode+' goles ('+percent(max)+'). Puede haber empates en la probabilidad máxima.';
}
$('tiros').addEventListener('input',distribution);$('prob').addEventListener('input',distribution);distribution();
function uncertainty(){
 invalidateShare('laboratorios');
 const n=Number($('muestra-tiros').value),input=$('muestra-goles');input.max=String(n);input.value=String(Math.min(Number(input.value),n));const k=Number(input.value),interval=core.wilson(k,n);
 $('muestra-n').value=n;$('muestra-k').value=k;$('muestra-resultado').textContent=percent(interval.rate);
 $('muestra-intervalo').style.left=(interval.low*100)+'%';$('muestra-intervalo').style.width=((interval.high-interval.low)*100)+'%';
 $('muestra-lectura').textContent=k+' goles en '+n+' disparos. Intervalo: '+percent(interval.low)+' a '+percent(interval.high)+'. Amplitud: '+number.format((interval.high-interval.low)*100)+' puntos porcentuales.';
}
$('muestra-tiros').addEventListener('input',uncertainty);$('muestra-goles').addEventListener('input',uncertainty);uncertainty();
function share(kind){
 const button=$(kind+'-enlace');if(!button)return;button.hidden=false;
 button.addEventListener('click',()=>{const state={shots:$('tiros')?Number($('tiros').value):undefined,probability:$('prob')?Number($('prob').value):undefined,sampleShots:$('muestra-tiros')?Number($('muestra-tiros').value):undefined,sampleGoals:$('muestra-goles')?Number($('muestra-goles').value):undefined,venue:$('temporada-sede')?.value,result:$('temporada-resultado')?.value,coverage:$('temporada-cobertura')?.value};
 const field=$(kind+'-url');field.value=core.viewUrl(globalThis.location?.href||'https://lineadepase.com/datalab-prototipo/',state,kind==='temporada'?'season':'labs');$(kind+'-compartir').hidden=false;field.focus();field.select();});
}
share('laboratorios');
})();
