(function(){
'use strict';
const $=id=>document.getElementById(id),fmt=new Intl.NumberFormat('es-ES',{maximumFractionDigits:1});
const studioForm=$('studio-form');
if(studioForm)studioForm.addEventListener('submit',event=>{if($('studio-jornada_a').value===$('studio-jornada_b').value){event.preventDefault();$('studio-estado').textContent='Elige dos jornadas distintas para comparar.';$('studio-jornada_b').focus();}});

})();
