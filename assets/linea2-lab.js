(function(){
'use strict';
const $=id=>document.getElementById(id),fmt=new Intl.NumberFormat('es-ES',{maximumFractionDigits:1});
if(!$('tiros'))return;
const tiros=$('tiros'),prob=$('prob');
if(globalThis.location&&globalThis.LDP2){const view=globalThis.LDP2.readView(globalThis.location.search);if(view.shots!==undefined)tiros.value=String(view.shots);if(view.probability!==undefined)prob.value=String(view.probability);}
function actualizar(){const n=Number(tiros.value),p=Number(prob.value)/100,q=1-Math.pow(1-p,n);$('n').value=n;$('p').value=fmt.format(p*100)+' %';$('resultado').textContent=fmt.format(q*100)+' %';$('barra').style.width=q*100+'%';$('esperados').textContent='Goles esperados: '+fmt.format(n*p);$('simulacion').textContent='';}
tiros.addEventListener('input',actualizar);prob.addEventListener('input',actualizar);actualizar();
$('simular').addEventListener('click',()=>{let goles=0;for(let i=0;i<Number(tiros.value);i++)if(Math.random()<Number(prob.value)/100)goles++;$('simulacion').textContent=goles+' goles en esta serie. Repite: el azar produce resultados distintos incluso con la misma probabilidad.';});

})();
