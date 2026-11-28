(function(){
'use strict';
const $=id=>document.getElementById(id),fmt=new Intl.NumberFormat('es-ES',{maximumFractionDigits:1});
if(!$('reto-pregunta'))return;
const intuitionQuestions=[
 {text:'Con dos disparos independientes al 50 %, ¿cuál es la probabilidad de marcar al menos una vez?',options:['50 %','75 %','100 %'],correct:1,why:'Solo no marcas si fallas ambos: 0,5 × 0,5 = 0,25. Por tanto, marcas al menos una vez en el 75 % de las series.'},
 {text:'Un equipo acumula 2 xG. ¿Qué significa?',options:['Marcará exactamente 2 goles','Sus ocasiones suman 2 goles esperados','Tiene un 200 % de probabilidad de ganar'],correct:1,why:'El xG suma probabilidades de los remates. No garantiza un marcador ni mide directamente la probabilidad de victoria.'},
 {text:'Un jugador marca 3 goles con 1 xG en un partido. ¿Demuestra que siempre define mejor que la media?',options:['Sí, ya está demostrado','No, un solo partido no basta','Sí, si su equipo gana'],correct:1,why:'Una muestra pequeña mezcla habilidad y variación aleatoria. Necesitamos más remates, contexto y una evaluación de la incertidumbre.'}
];
const banks={intuicion:intuitionQuestions,lectura:[
 {text:'Dos equipos tienen un 60 % y un 40 % de posesión. ¿Quién ha creado más peligro?',options:['El del 60 %','El del 40 %','La posesión sola no permite saberlo'],correct:2,why:'La posesión mide una parte del juego. Para describir el peligro necesitamos conocer las ocasiones y su calidad.'},
 {text:'Una ficha no tiene datos de tiros. ¿Cómo debe aparecer en una media de tiros?',options:['Como cero tiros','Como dato ausente, indicando la muestra disponible','Con la media del rival'],correct:1,why:'Ausencia de dato no significa cero. La media debe informar cuántos partidos tienen ese dato disponible.'},
 {text:'El equipo gana más en casa en una selección de partidos. ¿Qué podemos concluir?',options:['Jugar en casa causa todas esas victorias','Ganará su próximo partido en casa','La selección describe una asociación, no demuestra causalidad'],correct:2,why:'El rival, el calendario y otras variables pueden influir. Una comparación descriptiva no aísla sus efectos.'}
],metodo:[
 {text:'Antes de comparar dos estadísticas de proveedores distintos, ¿qué conviene revisar?',options:['Solo los colores del gráfico','Que las definiciones y la cobertura sean comparables','Que ambos números sean altos'],correct:1,why:'Una misma etiqueta puede usar criterios diferentes. Hay que comprobar definición, periodo, unidades y cobertura.'},
 {text:'¿Para qué se reserva una muestra que no se usó al ajustar un modelo?',options:['Para evaluar su capacidad de generalizar','Para garantizar que siempre acierte','Para ocultar los errores'],correct:0,why:'Evaluar con datos separados ayuda a detectar sobreajuste. La separación debe respetar el tiempo cuando se pretende predecir el futuro.'},
 {text:'¿Qué debe acompañar una conclusión de investigación?',options:['Solo un titular rotundo','Únicamente los resultados favorables','Fuentes, método, incertidumbre y límites'],correct:2,why:'Estos elementos permiten valorar la evidencia y reproducir el análisis. Un resultado no elimina sus limitaciones.'}
]};
let questions=banks.intuicion;
const answerButtons=[...document.querySelectorAll('[data-answer]')];let round=0,score=0,answered=false,history=[];
function showQuestion(){const q=questions[round];$('reto-pregunta').textContent=q.text;$('reto-progreso').textContent='Pregunta '+(round+1)+' de '+questions.length+' · Aciertos: '+score;answerButtons.forEach((b,i)=>{b.textContent=q.options[i];b.disabled=false;b.dataset.state=''});$('respuesta').textContent='';$('reto-siguiente').disabled=true;$('reto-siguiente').textContent=round===questions.length-1?'Ver resultado':'Siguiente pregunta';answered=false;if($('reto-resumen'))$('reto-resumen').hidden=true;}
function review(){
 if($('reto-historial'))$('reto-historial').replaceChildren(...history.map((correct,i)=>{const item=document.createElement('li');item.textContent='Pregunta '+(i+1)+' · '+(correct?'Acierto':'Para repasar');return item;}));
}
function summary(){
 const panel=$('reto-resumen');if(!panel)return;panel.replaceChildren();panel.hidden=false;const title=document.createElement('h3');title.textContent=score===questions.length?'Has completado el reto':'Ahora, a revisar la jugada';const text=document.createElement('p');text.textContent='Has acertado '+score+' de '+questions.length+'. Puedes repetir o profundizar en los conceptos.';panel.append(title,text);const passportLink=document.createElement('a');passportLink.href='#sello-play';passportLink.textContent='Guardar Juegos en mi pasaporte →';panel.append(passportLink);const sources=[['Experimentar con la probabilidad',globalThis.LDP2.areaLink('datalab',document.body?.dataset.areaRoot)],['Comprender los goles esperados',(document.body?.dataset.siteRoot||'../')+'proyectos/xg/'],['Leer los conceptos y sus límites',(document.body?.dataset.siteRoot||'../')+'conceptos/']];sources.forEach(([label,href])=>{const p=document.createElement('p'),link=document.createElement('a');link.textContent=label;link.href=href;p.append(link);panel.append(p);});
}
answerButtons.forEach((b,i)=>b.addEventListener('click',()=>{if(answered)return;answered=true;const q=questions[round],correct=i===q.correct;if(correct)score++;history.push(correct);answerButtons.forEach((button,index)=>{button.dataset.state=index===q.correct?'correct':index===i?'incorrect':'neutral';if(index===q.correct)button.textContent='✓ '+q.options[index];else if(index===i)button.textContent='× '+q.options[index];});review();$('respuesta').textContent=(correct?'Correcto. ':'La respuesta es «'+q.options[q.correct]+'». ')+q.why;answerButtons.forEach(button=>button.disabled=true);$('reto-siguiente').disabled=false;$('reto-progreso').textContent='Pregunta '+(round+1)+' de '+questions.length+' · Aciertos: '+score;}));
$('reto-siguiente').addEventListener('click',()=>{if(!answered)return;if(round<questions.length-1){round++;showQuestion();$('reto-pregunta').focus();}else{$('reto-progreso').textContent='Recorrido completado: '+score+' de '+questions.length+' aciertos.';$('reto-siguiente').disabled=true;summary();$('reto-progreso').focus();}});
function restart(){round=0;score=0;history=[];review();showQuestion();$('reto-pregunta').focus();}
$('reto-reiniciar').addEventListener('click',restart);
$('reto-tema').addEventListener('change',()=>{questions=banks[$('reto-tema').value]||banks.intuicion;restart();});showQuestion();

})();
