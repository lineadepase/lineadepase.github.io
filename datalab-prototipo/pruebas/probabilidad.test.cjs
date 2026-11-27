const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const script=fs.readFileSync(path.join(__dirname,'../../assets/linea2.js'),'utf8');
function boot(n=5,p=15,initial=null,blocked=false){
 const elements={},store=new Map(initial?[['ldp-pasaporte-v2',initial]]:[]),answers=[];
 function el(){return {value:'',textContent:'',style:{},children:[],events:{},dataset:{},addEventListener(k,fn){this.events[k]=fn},append(...v){this.children.push(...v)},querySelectorAll(){return this.children.flatMap(c=>c.children||[]).filter(c=>c.type==='checkbox')}};}
 for(const id of ['tiros','prob','n','p','resultado','barra','esperados','simulacion','simular','respuesta','reto-pregunta','reto-progreso','reto-siguiente','reto-reiniciar','progreso','guardado','sellos','nota','exportar','borrar'])elements[id]=el();
 elements.tiros.value=n;elements.prob.value=p;
 for(const a of ['50','75','100']){const b=el();b.dataset.answer=a;answers.push(b);}
 vm.runInNewContext(script,{document:{getElementById:id=>elements[id],querySelectorAll:()=>answers,createElement:el,createTextNode:x=>x},localStorage:{getItem:k=>{if(blocked)throw Error();return store.get(k)||null},setItem:(k,v)=>{if(blocked)throw Error();store.set(k,v)},removeItem:k=>store.delete(k)},Intl,Math,Number,JSON,Array,Set});
 return {e:elements,store,answers,q:parseFloat(elements.barra.style.width)};
}
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-9);
test('bornes et calculs exacts',()=>{near(boot(30,0).q,0);near(boot(1,100).q,100);near(boot(2,50).q,75);near(boot().q,55.62946875)});
test('probabilité monotone',()=>{assert.ok(boot(10,15).q>boot(5,15).q);assert.ok(boot(5,25).q>boot(5,15).q)});
test('simulation aux bornes',()=>{for(const p of [0,100]){const {e}=boot(5,p);e.simular.events.click();assert.match(e.simulacion.textContent,new RegExp('^'+(p?5:0)+' goles'));}});
test('recorrido, bloqueo de respuestas repetidas y reinicio',()=>{const {e,answers}=boot();answers[0].events.click();assert.match(e.respuesta.textContent,/La respuesta/);answers[1].events.click();assert.match(e['reto-progreso'].textContent,/Aciertos: 0/);e['reto-siguiente'].events.click();answers[1].events.click();assert.match(e.respuesta.textContent,/Correcto/);e['reto-siguiente'].events.click();answers[1].events.click();e['reto-siguiente'].events.click();assert.match(e['reto-progreso'].textContent,/2 de 3 aciertos/);e['reto-reiniciar'].events.click();assert.match(e['reto-progreso'].textContent,/Pregunta 1 de 3/);assert.equal(answers[0].disabled,false)});
test('persistance et suppression du passeport',()=>{const {e,store}=boot();const input=e.sellos.children[0].children[0];input.checked=true;input.events.change();e.nota.value='Mi descubrimiento';e.nota.events.input();assert.equal(JSON.parse(store.get('ldp-pasaporte-v2')).nota,'Mi descubrimiento');assert.match(e.progreso.textContent,/1 de 7/);e.borrar.events.click();assert.equal(store.size,0);assert.equal(input.checked,false);assert.equal(e.nota.value,'')});
test('données locales invalides ou indisponibles',()=>{assert.doesNotThrow(()=>boot(5,15,'{'));const {e}=boot(5,15,null,true);e.nota.events.input();assert.match(e.guardado.textContent,/No se puede guardar/)});
test('restaure uniquement les zones connues',()=>{const {e}=boot(5,15,JSON.stringify({areas:['Play','inconnue'],nota:'Hola'}));assert.match(e.progreso.textContent,/1 de 7/);assert.equal(e.nota.value,'Hola')});
