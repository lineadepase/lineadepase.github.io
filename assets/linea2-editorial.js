(function(){
'use strict';
const $=id=>document.getElementById(id),form=$('editorial-form');if(!form)return;
const payload=JSON.parse($('temporada-datos').textContent),matches=payload.partidos;
for(const code of ['a','b']){
 const select=$('editorial-'+code);
 matches.forEach((m,index)=>{const option=document.createElement('option');option.value=String(index);option.textContent='J'+m.jornada+' · '+m.fecha+' · '+m.rival;select.append(option);});
}
if(matches.length>1)$('editorial-b').selectedIndex=1;
function invalidate(){$('editorial-salida').hidden=true;$('editorial-texto').value='';$('editorial-estado').textContent='Prepara de nuevo el borrador para incorporar los cambios.';}
['editorial-a','editorial-b','editorial-pregunta','editorial-nota'].forEach(id=>$(id).addEventListener('input',invalidate));
form.addEventListener('submit',event=>{
 event.preventDefault();if(!form.reportValidity())return;
 const a=matches[Number($('editorial-a').value)],b=matches[Number($('editorial-b').value)];
 if(!a||!b||a===b){invalidate();$('editorial-estado').textContent='Elige dos jornadas distintas.';return;}
 const question=$('editorial-pregunta').value.trim();if(!question){$('editorial-estado').textContent='Escribe una pregunta para tu publicación.';return;}
 const fmt=value=>value===null||value===undefined?'No disponible':new Intl.NumberFormat('es-ES',{maximumFractionDigits:1}).format(value);
 function describe(m){
 const source=new URL('../proyectos/real-zaragoza/jornada-'+m.jornada+'.html',location.href).href;
 const stats=m.completo?'Tiros Zaragoza–rival: '+fmt(m.tiros_zaragoza)+'–'+fmt(m.tiros_rival)+'. Posesión: '+fmt(m.posesion_pct)+' %.':'Estadísticas pendientes de validación; no se incluyen tiros ni posesión.';
 return 'J'+m.jornada+' · '+m.fecha+' · '+m.sede+' · '+m.rival+'\nMarcador Zaragoza–rival: '+m.goles_favor+'–'+m.goles_contra+'\n'+stats+'\nFicha y fuentes: '+source;
 }
 $('editorial-texto').value='LÍNEA DE PASE · BORRADOR DE PUBLICACIÓN\n\n'+question+'\n\nCORTE DE LOS DATOS: '+payload.corte+'\n\n'+describe(a)+'\n\n'+describe(b)+'\n\nMI LECTURA\n'+($('editorial-nota').value.trim()||'Pendiente de redactar.')+'\n\nLÍMITES\nComparación descriptiva de dos partidos. Los rivales, la sede y el contexto pueden ser distintos. Los marcadores no demuestran causalidad ni predicen otro encuentro. Consulta las fichas para revisar la procedencia y las discrepancias de los datos.\n\nRevisa texto y fuentes antes de publicar.\n';
 $('editorial-salida').hidden=false;$('editorial-estado').textContent='Borrador preparado. Revisa los datos y tu interpretación antes de usarlo.';
});
$('editorial-descargar').addEventListener('click',()=>{if($('editorial-salida').hidden)return;const url=URL.createObjectURL(new Blob([$('editorial-texto').value],{type:'text/plain;charset=utf-8'})),link=document.createElement('a');link.href=url;link.download='linea-de-pase-borrador-publicacion.txt';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
})();
