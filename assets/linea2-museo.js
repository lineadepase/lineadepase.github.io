(function(){
'use strict';
const $=id=>document.getElementById(id),form=$('museo-cuaderno');if(!form)return;
const works={red:{name:'Sala 01 · Red de pases',path:'../proyectos/espana-eurocopa-redes/',context:'España · final de la Eurocopa femenina 2025. Pases completados en juego hasta el primer cambio, minuto 70; enlaces desde cuatro pases. Fuente: StatsBomb Open Data. Elaboración: Línea de Pase.'},territorio:{name:'Sala 02 · Superficie de amenaza',path:'../proyectos/liga-f-xt/',context:'Liga F 2023/24. Superficie ajustada con toda la temporada para explicar el método. Dirección de ataque hacia la derecha. Fuente: StatsBomb Open Data. Modelo: Línea de Pase.'}};
form.addEventListener('submit',event=>{
 event.preventDefault();if(!form.reportValidity())return;
 const work=works[$('museo-obra').value],observation=$('museo-observo').value.trim();
 if(!work||!observation){$('museo-cuaderno-estado').textContent='Escribe una observación y elige una obra.';return;}
 const text='LÍNEA DE PASE · CUADERNO DE VISITA\nLectura personal, no validada\n\n'+work.name+'\n'+work.context+'\nObra y metodología: '+new URL(work.path,location.href).href+'\n\nLO QUE OBSERVO\n'+observation+'\n\nMI INTERPRETACIÓN\n'+($('museo-interpreto').value.trim()||'Pendiente de formular.')+'\n\nLO QUE NECESITO COMPROBAR\n'+($('museo-falta').value.trim()||'Pendiente de revisar.')+'\n\nConsulta el contexto y los límites en la metodología de la obra.\n';
 const url=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'})),link=document.createElement('a');link.href=url;link.download='linea-de-pase-cuaderno-'+$('museo-obra').value+'.txt';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);$('museo-cuaderno-estado').textContent='Cuaderno descargado. Tus notas siguen aquí hasta recargar o cerrar la página.';
});
})();
