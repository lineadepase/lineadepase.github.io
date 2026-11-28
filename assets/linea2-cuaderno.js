// Generado por herramientas/linea2_runtime.py; editar los módulos de área.
(function(){
'use strict';
const $=id=>document.getElementById(id),core=globalThis.LDP2;
const fmt=new Intl.NumberFormat('es-ES',{maximumFractionDigits:1}),precise=new Intl.NumberFormat('es-ES',{maximumFractionDigits:2});
if($('escenario-a-n')){
 function render(){
  const results={};
  for(const code of ['a','b']){
   const n=Number($('escenario-'+code+'-n').value),p=Number($('escenario-'+code+'-p').value);
   const result=core.scenario(n,p/100);results[code]=result;
   $('escenario-'+code+'-n-valor').value=n;$('escenario-'+code+'-p-valor').value=fmt.format(p)+' %';
   $('escenario-'+code+'-xg').textContent=precise.format(result.expected);$('escenario-'+code+'-gol').textContent=fmt.format(result.atLeastOne*100)+' %';
  }
  const same=Math.abs(results.a.expected-results.b.expected)<1e-10,difference=results.b.atLeastOne-results.a.atLeastOne;
  const start=same?'Ambos escenarios suman '+precise.format(results.a.expected)+' goles esperados. ':'A suma '+precise.format(results.a.expected)+' goles esperados y B suma '+precise.format(results.b.expected)+'. ';
  $('escenarios-lectura').textContent=start+(Math.abs(difference)<1e-12?'La probabilidad de al menos un gol también es igual.':'En este modelo, '+(difference>0?'B':'A')+' tiene '+fmt.format(Math.abs(difference)*100)+' puntos porcentuales más de probabilidad de marcar al menos una vez.');
 }
 for(const code of ['a','b'])for(const field of ['n','p'])$('escenario-'+code+'-'+field).addEventListener('input',render);
 $('escenarios-restablecer').addEventListener('click',()=>{$('escenario-a-n').value='10';$('escenario-a-p').value='10';$('escenario-b-n').value='2';$('escenario-b-p').value='50';render();});render();
}
})();

(function(){
'use strict';
const $=id=>document.getElementById(id),core=globalThis.LDP2;
const fmt=new Intl.NumberFormat('es-ES',{maximumFractionDigits:1}),precise=new Intl.NumberFormat('es-ES',{maximumFractionDigits:2});
if($('pro-ficha')){
 const fields=['pregunta','hipotesis','fuentes','metodo','validacion','limites'],key='ldp-pro-borrador-v1';
 function collect(){const value={version:1};fields.forEach(field=>value[field]=$('pro-'+field).value);return core.researchDraft(value);}
 function apply(value){fields.forEach(field=>$('pro-'+field).value=value[field]);}
 try{const saved=localStorage.getItem(key);if(saved){apply(core.researchDraft(JSON.parse(saved)));$('pro-estado').textContent='Borrador recuperado de este navegador.';}}catch(e){$('pro-estado').textContent='No se pudo recuperar un borrador válido. Puedes completar la ficha y descargarla.';}
 $('pro-guardar').addEventListener('click',()=>{try{localStorage.setItem(key,JSON.stringify(collect()));$('pro-estado').textContent='Borrador guardado en este navegador.';}catch(e){$('pro-estado').textContent='No se pudo guardar el borrador. Revisa los campos y descarga una copia para conservarlo.';}});
 $('pro-ficha').addEventListener('submit',event=>{
  event.preventDefault();if(!$('pro-ficha').reportValidity())return;
  try{const text=core.researchText(collect()),url=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'})),link=document.createElement('a');link.href=url;link.download='linea-de-pase-ficha-investigacion.txt';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);$('pro-estado').textContent='Ficha descargada como borrador. Los apartados vacíos quedan pendientes.';}catch(e){$('pro-estado').textContent='Define una pregunta y revisa el tamaño de los campos antes de descargar.';}
 });
 $('pro-borrar').addEventListener('click',()=>{fields.forEach(field=>$('pro-'+field).value='');try{localStorage.removeItem(key);$('pro-estado').textContent='Borrador borrado.';}catch(e){$('pro-estado').textContent='Campos vaciados. El navegador no permitió borrar la copia guardada; elimínala desde los datos del sitio.';}});
}
})();
