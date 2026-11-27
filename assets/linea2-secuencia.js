(function(){
'use strict';
const $=id=>document.getElementById(id),container=$('secuencia-controles');if(!container)return;
const fmt=new Intl.NumberFormat('es-ES',{maximumFractionDigits:1}),precise=new Intl.NumberFormat('es-ES',{maximumFractionDigits:2});let probabilities=[.1,.2,.3];
function result(){
 const values=globalThis.LDP2.variedDistribution(probabilities),expected=probabilities.reduce((a,b)=>a+b,0);
 $('secuencia-resumen').textContent=probabilities.length+' remates · '+precise.format(expected)+' goles esperados · '+fmt.format((1-values[0])*100)+' % de probabilidad de al menos un gol.';
 $('secuencia-resultados').replaceChildren(...values.map((p,k)=>{const row=document.createElement('tr'),label=document.createElement('th'),value=document.createElement('td');label.scope='row';label.textContent=String(k);value.textContent=p>0&&p<.0005?'< 0,1 %':fmt.format(p*100)+' %';row.append(label,value);return row;}));
 $('secuencia-anadir').disabled=probabilities.length===12;$('secuencia-quitar').disabled=probabilities.length===1;
}
function controls(){
 container.replaceChildren(...probabilities.map((p,index)=>{const box=document.createElement('div'),label=document.createElement('label'),input=document.createElement('input'),output=document.createElement('output');input.type='range';input.id='secuencia-p-'+index;input.min='0';input.max='100';input.step='1';input.value=String(Math.round(p*100));label.htmlFor=input.id;label.append(document.createTextNode('Remate '+(index+1)+': '),output);output.value=fmt.format(p*100)+' %';input.addEventListener('input',()=>{probabilities[index]=Number(input.value)/100;output.value=fmt.format(Number(input.value))+' %';result();});box.append(label,input);return box;}));result();
}
$('secuencia-anadir').addEventListener('click',()=>{if(probabilities.length>=12)return;probabilities.push(.1);controls();$('secuencia-p-'+(probabilities.length-1)).focus();});
$('secuencia-quitar').addEventListener('click',()=>{if(probabilities.length<=1)return;probabilities.pop();controls();$('secuencia-p-'+(probabilities.length-1)).focus();});
$('secuencia-reiniciar').addEventListener('click',()=>{probabilities=[.1,.2,.3];controls();$('secuencia-p-0').focus();});controls();
})();
