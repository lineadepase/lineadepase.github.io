(function(){
'use strict';
const $=id=>document.getElementById(id),fmt=new Intl.NumberFormat('es-ES',{maximumFractionDigits:1});
const key='ldp-pasaporte-v2',areas=['DataLab','Museo','Play','Zaragoza','Pro','Studio','Media'];let state={areas:[],nota:''},storage=true;
try{const s=JSON.parse(localStorage.getItem(key));if(s&&Array.isArray(s.areas)&&typeof s.nota==='string')state={areas:[...new Set(s.areas.filter(x=>areas.includes(x)))],nota:s.nota.slice(0,2000)};}catch(e){storage=false;}
const stamps=areas.map(name=>({name,button:$('sello-'+name.toLowerCase())})).filter(item=>item.button);
const areaLabel=name=>name==='Play'?'Juegos':name;
function render(){
 if($('progreso'))$('progreso').textContent=new Set(state.areas).size+' de '+areas.length+' áreas exploradas';
 if($('sellos'))$('sellos').querySelectorAll('input').forEach((input,i)=>input.checked=state.areas.includes(areas[i]));
 stamps.forEach(({name,button})=>{const marked=state.areas.includes(name);button.textContent=marked?areaLabel(name)+' guardado · Quitar del pasaporte':'Guardar '+areaLabel(name)+' en mi pasaporte';button.setAttribute('aria-pressed',String(marked));});
 if($('pasaporte-barra'))$('pasaporte-barra').value=state.areas.length;
 if($('pasaporte-retomar')){const next=areas.find(name=>!state.areas.includes(name));$('pasaporte-retomar').href=globalThis.LDP2.areaLink(next?next.toLowerCase():'datalab',document.body?.dataset.areaRoot);$('pasaporte-retomar').textContent=next?'Continuar por '+areaLabel(next)+' →':'Has explorado todas las áreas · Volver a DataLab →';}
}
stamps.forEach(({name,button})=>{button.hidden=false;button.addEventListener('click',()=>{state.areas=state.areas.includes(name)?state.areas.filter(item=>item!==name):[...state.areas,name];save();});});
function save(){try{localStorage.setItem(key,JSON.stringify(state));if($('guardado'))$('guardado').textContent='Guardado en este navegador.';}catch(e){storage=false;if($('guardado'))$('guardado').textContent='No se puede guardar en este navegador. Descarga tu pasaporte para conservarlo.';}render();}
if($('sellos'))areas.forEach(name=>{const label=document.createElement('label'),input=document.createElement('input');input.type='checkbox';input.checked=state.areas.includes(name);input.addEventListener('change',()=>{state.areas=state.areas.filter(x=>x!==name);if(input.checked)state.areas.push(name);save();});label.append(input,document.createTextNode(areaLabel(name)));$('sellos').append(label);});
if($('nota')){$('nota').value=state.nota;$('nota').addEventListener('input',()=>{state.nota=$('nota').value;save();});}
if($('exportar'))$('exportar').addEventListener('click',()=>{const blob=new Blob(['LÍNEA DE PASE · PASAPORTE\n\nÁreas exploradas: '+state.areas.map(areaLabel).join(', ')+'\n\nMi aprendizaje:\n'+state.nota],{type:'text/plain;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='linea-de-pase-pasaporte.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
if($('borrar'))$('borrar').addEventListener('click',()=>{state={areas:[],nota:''};let removed=true;try{localStorage.removeItem(key);}catch(e){removed=false;}$('nota').value='';$('sellos').querySelectorAll('input').forEach(i=>i.checked=false);if($('guardado'))$('guardado').textContent=removed?'Recorrido borrado.':'Recorrido vaciado en pantalla. El navegador no permitió borrar la copia guardada; elimínala desde los datos del sitio.';render();});render();if(!storage)if($('guardado'))$('guardado').textContent='Almacenamiento no disponible. Puedes descargar tu recorrido.';
if($('pasaporte-json')){
 let pending=null;
 $('pasaporte-json').addEventListener('click',()=>{const content=JSON.stringify({version:1,areas:state.areas,nota:state.nota},null,2),blob=new Blob([content],{type:'application/json;charset=utf-8'}),url=URL.createObjectURL(blob),link=document.createElement('a');link.href=url;link.download='linea-de-pase-pasaporte.json';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
 let importRequest=0;
 $('pasaporte-archivo').addEventListener('change',async()=>{const request=++importRequest;pending=null;$('pasaporte-aplicar').disabled=true;const file=$('pasaporte-archivo').files[0];if(!file){$('pasaporte-importacion').textContent='No se ha elegido un archivo.';return;}try{if(file.size>25000)throw new Error('Archivo demasiado grande');const parsed=globalThis.LDP2.passport(JSON.parse(await file.text()),areas);if(request!==importRequest)return;pending=parsed;$('pasaporte-importacion').textContent='Copia válida: '+parsed.areas.length+' áreas y '+parsed.nota.length+' caracteres de nota. Confirma para sustituir tu recorrido.';$('pasaporte-aplicar').disabled=false;}catch(e){if(request===importRequest)$('pasaporte-importacion').textContent='No se pudo leer la copia. Elige un JSON de pasaporte válido, de hasta 25 KB y con una nota de hasta 2000 caracteres.';}});
 $('pasaporte-aplicar').addEventListener('click',()=>{if(!pending)return;state=pending;pending=null;$('nota').value=state.nota;if($('sellos'))$('sellos').querySelectorAll('input').forEach((input,i)=>input.checked=state.areas.includes(areas[i]));save();$('pasaporte-importacion').textContent='Copia aplicada al recorrido.';$('pasaporte-aplicar').disabled=true;});
}

})();
