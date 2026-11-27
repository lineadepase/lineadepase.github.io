(function(){
'use strict';
const $=id=>document.getElementById(id),fmt=new Intl.NumberFormat('es-ES',{maximumFractionDigits:1});
const tiros=$('tiros'),prob=$('prob');
function actualizar(){const n=Number(tiros.value),p=Number(prob.value)/100,q=1-Math.pow(1-p,n);$('n').value=n;$('p').value=fmt.format(p*100)+' %';$('resultado').textContent=fmt.format(q*100)+' %';$('barra').style.width=q*100+'%';$('esperados').textContent='Goles esperados: '+fmt.format(n*p);$('simulacion').textContent='';}
tiros.addEventListener('input',actualizar);prob.addEventListener('input',actualizar);actualizar();
$('simular').addEventListener('click',()=>{let goles=0;for(let i=0;i<Number(tiros.value);i++)if(Math.random()<Number(prob.value)/100)goles++;$('simulacion').textContent=goles+' goles en esta serie. Repite: el azar produce resultados distintos incluso con la misma probabilidad.';});
document.querySelectorAll('[data-answer]').forEach(b=>b.addEventListener('click',()=>{$('respuesta').textContent=b.dataset.answer==='75'?'Correcto: 75 %. Solo no marcas si fallas ambos: 0,5 × 0,5 = 0,25.':'Prueba de nuevo. Calcula primero la probabilidad de fallar ambos disparos.';}));
const key='ldp-pasaporte-v2',areas=['DataLab','Museo','Play','Zaragoza','Pro','Studio','Media'];let state={areas:[],nota:''},storage=true;
try{const s=JSON.parse(localStorage.getItem(key));if(s&&Array.isArray(s.areas)&&typeof s.nota==='string')state={areas:s.areas.filter(x=>areas.includes(x)),nota:s.nota.slice(0,2000)};}catch(e){storage=false;}
function render(){ $('progreso').textContent=new Set(state.areas).size+' de '+areas.length+' áreas exploradas'; }
function save(){try{localStorage.setItem(key,JSON.stringify(state));$('guardado').textContent='Guardado en este navegador.';}catch(e){storage=false;$('guardado').textContent='No se puede guardar en este navegador. Descarga tu pasaporte para conservarlo.';}render();}
areas.forEach(name=>{const label=document.createElement('label'),input=document.createElement('input');input.type='checkbox';input.checked=state.areas.includes(name);input.addEventListener('change',()=>{state.areas=state.areas.filter(x=>x!==name);if(input.checked)state.areas.push(name);save();});label.append(input,document.createTextNode(name));$('sellos').append(label);});
$('nota').value=state.nota;$('nota').addEventListener('input',()=>{state.nota=$('nota').value;save();});
$('exportar').addEventListener('click',()=>{const blob=new Blob(['LÍNEA DE PASE · PASAPORTE\n\nÁreas exploradas: '+state.areas.join(', ')+'\n\nMi aprendizaje:\n'+state.nota],{type:'text/plain;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='linea-de-pase-pasaporte.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
$('borrar').addEventListener('click',()=>{state={areas:[],nota:''};try{localStorage.removeItem(key);}catch(e){}$('nota').value='';$('sellos').querySelectorAll('input').forEach(i=>i.checked=false);$('guardado').textContent='Recorrido borrado.';render();});render();if(!storage)$('guardado').textContent='Almacenamiento no disponible. Puedes descargar tu recorrido.';
})();
