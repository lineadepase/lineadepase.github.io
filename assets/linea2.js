(function(){
'use strict';
const $=id=>document.getElementById(id),fmt=new Intl.NumberFormat('es-ES',{maximumFractionDigits:1});
const tiros=$('tiros'),prob=$('prob');
if(globalThis.location&&globalThis.LDP2){const view=globalThis.LDP2.readView(globalThis.location.search);if(view.shots!==undefined)tiros.value=String(view.shots);if(view.probability!==undefined)prob.value=String(view.probability);}
function actualizar(){const n=Number(tiros.value),p=Number(prob.value)/100,q=1-Math.pow(1-p,n);$('n').value=n;$('p').value=fmt.format(p*100)+' %';$('resultado').textContent=fmt.format(q*100)+' %';$('barra').style.width=q*100+'%';$('esperados').textContent='Goles esperados: '+fmt.format(n*p);$('simulacion').textContent='';}
tiros.addEventListener('input',actualizar);prob.addEventListener('input',actualizar);actualizar();
$('simular').addEventListener('click',()=>{let goles=0;for(let i=0;i<Number(tiros.value);i++)if(Math.random()<Number(prob.value)/100)goles++;$('simulacion').textContent=goles+' goles en esta serie. Repite: el azar produce resultados distintos incluso con la misma probabilidad.';});
const questions=[
 {text:'Con dos disparos independientes al 50 %, ¿cuál es la probabilidad de marcar al menos una vez?',options:['50 %','75 %','100 %'],correct:1,why:'Solo no marcas si fallas ambos: 0,5 × 0,5 = 0,25. Por tanto, marcas al menos una vez en el 75 % de las series.'},
 {text:'Un equipo acumula 2 xG. ¿Qué significa?',options:['Marcará exactamente 2 goles','Sus ocasiones suman 2 goles esperados','Tiene un 200 % de probabilidad de ganar'],correct:1,why:'El xG suma probabilidades de los remates. No garantiza un marcador ni mide directamente la probabilidad de victoria.'},
 {text:'Un jugador marca 3 goles con 1 xG en un partido. ¿Demuestra que siempre define mejor que la media?',options:['Sí, ya está demostrado','No, un solo partido no basta','Sí, si su equipo gana'],correct:1,why:'Una muestra pequeña mezcla habilidad y variación aleatoria. Necesitamos más remates, contexto y una evaluación de la incertidumbre.'}
];
const answerButtons=[...document.querySelectorAll('[data-answer]')];let round=0,score=0,answered=false,history=[];
function showQuestion(){const q=questions[round];$('reto-pregunta').textContent=q.text;$('reto-progreso').textContent='Pregunta '+(round+1)+' de '+questions.length+' · Aciertos: '+score;answerButtons.forEach((b,i)=>{b.textContent=q.options[i];b.disabled=false;b.dataset.state=''});$('respuesta').textContent='';$('reto-siguiente').disabled=true;$('reto-siguiente').textContent=round===questions.length-1?'Ver resultado':'Siguiente pregunta';answered=false;if($('reto-resumen'))$('reto-resumen').hidden=true;}
function review(){
 if($('reto-historial'))$('reto-historial').replaceChildren(...history.map((correct,i)=>{const item=document.createElement('li');item.textContent='Pregunta '+(i+1)+' · '+(correct?'Acierto':'Para repasar');return item;}));
}
function summary(){
 const panel=$('reto-resumen');if(!panel)return;panel.replaceChildren();panel.hidden=false;const title=document.createElement('h3');title.textContent=score===questions.length?'Has completado el reto':'Ahora, a revisar la jugada';const text=document.createElement('p');text.textContent='Has acertado '+score+' de '+questions.length+'. Puedes repetir o profundizar en los conceptos.';panel.append(title,text);const sources=[['Experimentar con la probabilidad','#datalab'],['Comprender los goles esperados','../proyectos/xg/'],['Leer los conceptos y sus límites','../conceptos/']];sources.forEach(([label,href])=>{const p=document.createElement('p'),link=document.createElement('a');link.textContent=label;link.href=href;p.append(link);panel.append(p);});
}
answerButtons.forEach((b,i)=>b.addEventListener('click',()=>{if(answered)return;answered=true;const q=questions[round],correct=i===q.correct;if(correct)score++;history.push(correct);answerButtons.forEach((button,index)=>{button.dataset.state=index===q.correct?'correct':index===i?'incorrect':'neutral';if(index===q.correct)button.textContent='✓ '+q.options[index];else if(index===i)button.textContent='× '+q.options[index];});review();$('respuesta').textContent=(correct?'Correcto. ':'La respuesta es «'+q.options[q.correct]+'». ')+q.why;answerButtons.forEach(button=>button.disabled=true);$('reto-siguiente').disabled=false;$('reto-progreso').textContent='Pregunta '+(round+1)+' de '+questions.length+' · Aciertos: '+score;}));
$('reto-siguiente').addEventListener('click',()=>{if(!answered)return;if(round<questions.length-1){round++;showQuestion();$('reto-pregunta').focus();}else{$('reto-progreso').textContent='Recorrido completado: '+score+' de '+questions.length+' aciertos.';$('reto-siguiente').disabled=true;summary();$('reto-progreso').focus();}});
$('reto-reiniciar').addEventListener('click',()=>{round=0;score=0;history=[];review();showQuestion();$('reto-pregunta').focus();});showQuestion();
const studioForm=$('studio-form');
if(studioForm)studioForm.addEventListener('submit',event=>{if($('studio-jornada_a').value===$('studio-jornada_b').value){event.preventDefault();$('studio-estado').textContent='Elige dos jornadas distintas para comparar.';$('studio-jornada_b').focus();}});
const key='ldp-pasaporte-v2',areas=['DataLab','Museo','Play','Zaragoza','Pro','Studio','Media'];let state={areas:[],nota:''},storage=true;
try{const s=JSON.parse(localStorage.getItem(key));if(s&&Array.isArray(s.areas)&&typeof s.nota==='string')state={areas:[...new Set(s.areas.filter(x=>areas.includes(x)))],nota:s.nota.slice(0,2000)};}catch(e){storage=false;}
const stamps=areas.map(name=>({name,button:$('sello-'+name.toLowerCase())})).filter(item=>item.button);
function render(){
 $('progreso').textContent=new Set(state.areas).size+' de '+areas.length+' áreas exploradas';
 $('sellos').querySelectorAll('input').forEach((input,i)=>input.checked=state.areas.includes(areas[i]));
 stamps.forEach(({name,button})=>{const marked=state.areas.includes(name);button.textContent=marked?name+' guardado · Quitar del pasaporte':'Guardar '+name+' en mi pasaporte';button.setAttribute('aria-pressed',String(marked));});
 if($('pasaporte-barra'))$('pasaporte-barra').value=state.areas.length;
 if($('pasaporte-retomar')){const next=areas.find(name=>!state.areas.includes(name));$('pasaporte-retomar').href='#'+(next?next.toLowerCase():'datalab');$('pasaporte-retomar').textContent=next?'Continuar por '+next+' →':'Has explorado todas las áreas · Volver a DataLab →';}
}
stamps.forEach(({name,button})=>{button.hidden=false;button.addEventListener('click',()=>{state.areas=state.areas.includes(name)?state.areas.filter(item=>item!==name):[...state.areas,name];save();});});
function save(){try{localStorage.setItem(key,JSON.stringify(state));$('guardado').textContent='Guardado en este navegador.';}catch(e){storage=false;$('guardado').textContent='No se puede guardar en este navegador. Descarga tu pasaporte para conservarlo.';}render();}
areas.forEach(name=>{const label=document.createElement('label'),input=document.createElement('input');input.type='checkbox';input.checked=state.areas.includes(name);input.addEventListener('change',()=>{state.areas=state.areas.filter(x=>x!==name);if(input.checked)state.areas.push(name);save();});label.append(input,document.createTextNode(name));$('sellos').append(label);});
$('nota').value=state.nota;$('nota').addEventListener('input',()=>{state.nota=$('nota').value;save();});
$('exportar').addEventListener('click',()=>{const blob=new Blob(['LÍNEA DE PASE · PASAPORTE\n\nÁreas exploradas: '+state.areas.join(', ')+'\n\nMi aprendizaje:\n'+state.nota],{type:'text/plain;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='linea-de-pase-pasaporte.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
$('borrar').addEventListener('click',()=>{state={areas:[],nota:''};let removed=true;try{localStorage.removeItem(key);}catch(e){removed=false;}$('nota').value='';$('sellos').querySelectorAll('input').forEach(i=>i.checked=false);$('guardado').textContent=removed?'Recorrido borrado.':'Recorrido vaciado en pantalla. El navegador no permitió borrar la copia guardada; elimínala desde los datos del sitio.';render();});render();if(!storage)$('guardado').textContent='Almacenamiento no disponible. Puedes descargar tu recorrido.';
if($('pasaporte-json')){
 let pending=null;
 $('pasaporte-json').addEventListener('click',()=>{const content=JSON.stringify({version:1,areas:state.areas,nota:state.nota},null,2),blob=new Blob([content],{type:'application/json;charset=utf-8'}),url=URL.createObjectURL(blob),link=document.createElement('a');link.href=url;link.download='linea-de-pase-pasaporte.json';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
 let importRequest=0;
 $('pasaporte-archivo').addEventListener('change',async()=>{const request=++importRequest;pending=null;$('pasaporte-aplicar').disabled=true;const file=$('pasaporte-archivo').files[0];if(!file){$('pasaporte-importacion').textContent='No se ha elegido un archivo.';return;}try{if(file.size>25000)throw new Error('Archivo demasiado grande');const parsed=globalThis.LDP2.passport(JSON.parse(await file.text()),areas);if(request!==importRequest)return;pending=parsed;$('pasaporte-importacion').textContent='Copia válida: '+parsed.areas.length+' áreas y '+parsed.nota.length+' caracteres de nota. Confirma para sustituir tu recorrido.';$('pasaporte-aplicar').disabled=false;}catch(e){if(request===importRequest)$('pasaporte-importacion').textContent='No se pudo leer la copia. Elige un JSON de pasaporte válido, de hasta 25 KB y con una nota de hasta 2000 caracteres.';}});
 $('pasaporte-aplicar').addEventListener('click',()=>{if(!pending)return;state=pending;pending=null;$('nota').value=state.nota;$('sellos').querySelectorAll('input').forEach((input,i)=>input.checked=state.areas.includes(areas[i]));save();$('pasaporte-importacion').textContent='Copia aplicada al recorrido.';$('pasaporte-aplicar').disabled=true;});
}
})();
