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
