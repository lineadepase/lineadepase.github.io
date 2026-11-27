const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const core=require('../../assets/linea2-core.js');
const script=fs.readFileSync(path.join(__dirname,'../../assets/linea2-cuaderno.js'),'utf8');
const fields=['pregunta','hipotesis','fuentes','metodo','validacion','limites'];
function boot(saved=null,blocked=false){
 const e={},store=new Map(saved?[['ldp-pro-borrador-v1',saved]]:[]),blobs=[],downloads=[];
 function el(){return {value:'',textContent:'',events:{},addEventListener(k,fn){this.events[k]=fn},reportValidity(){return Boolean(e['pro-pregunta'].value.trim())},click(){downloads.push(this)}};}
 for(const code of ['a','b'])for(const key of ['n','p','n-valor','p-valor','xg','gol'])e['escenario-'+code+'-'+key]=el();
 for(const id of ['escenarios-lectura','escenarios-restablecer','pro-ficha','pro-estado','pro-guardar','pro-borrar',...fields.map(x=>'pro-'+x)])e[id]=el();
 for(const [id,value] of Object.entries({'escenario-a-n':10,'escenario-a-p':10,'escenario-b-n':2,'escenario-b-p':50}))e[id].value=String(value);
 vm.runInNewContext(script,{LDP2:core,document:{getElementById:id=>e[id],createElement:el},localStorage:{getItem:k=>{if(blocked)throw Error();return store.get(k)||null},setItem:(k,v)=>{if(blocked)throw Error();store.set(k,v)},removeItem:k=>{if(blocked)throw Error();store.delete(k)}},Blob,URL:{createObjectURL:b=>{blobs.push(b);return 'blob:ficha'},revokeObjectURL(){}},setTimeout:fn=>fn(),Intl,Math,Number,JSON});
 return {e,store,blobs,downloads};
}
test('comparación de 1 xG, cambios de controles y reinicio',()=>{const {e}=boot();assert.equal(e['escenario-a-xg'].textContent,'1');assert.equal(e['escenario-b-xg'].textContent,'1');assert.equal(e['escenario-a-gol'].textContent,'65,1 %');assert.equal(e['escenario-b-gol'].textContent,'75 %');assert.match(e['escenarios-lectura'].textContent,/Ambos escenarios/);e['escenario-a-p'].value='0';e['escenario-a-p'].events.input();assert.equal(e['escenario-a-gol'].textContent,'0 %');e['escenarios-restablecer'].events.click();assert.equal(e['escenario-a-p'].value,'10');});
test('Pro no guarda automáticamente, guarda y recupera a petición',()=>{const {e,store}=boot();e['pro-pregunta'].value='Pregunta';assert.equal(store.size,0);e['pro-guardar'].events.click();const recovered=boot(store.get('ldp-pro-borrador-v1'));assert.equal(recovered.e['pro-pregunta'].value,'Pregunta');recovered.e['pro-borrar'].events.click();assert.equal(recovered.store.size,0);assert.equal(recovered.e['pro-pregunta'].value,'');});
test('descarga de ficha exige pregunta y mantiene apartados pendientes',async()=>{const {e,blobs,downloads}=boot();e['pro-ficha'].events.submit({preventDefault(){}});assert.equal(downloads.length,0);e['pro-pregunta'].value='¿Qué cambia?';e['pro-ficha'].events.submit({preventDefault(){}});const content=await blobs[0].text();assert.match(content,/¿Qué cambia\?/);assert.match(content,/Pendiente de definir/);assert.match(content,/BORRADOR/);});
test('almacenamiento inválido o bloqueado no pierde las respuestas en pantalla',()=>{const invalid=boot('{mal');assert.equal(invalid.e['pro-pregunta'].value,'');const {e}=boot(null,true);e['pro-pregunta'].value='Conservar';e['pro-guardar'].events.click();assert.equal(e['pro-pregunta'].value,'Conservar');assert.match(e['pro-estado'].textContent,/No se pudo guardar/);e['pro-borrar'].events.click();assert.match(e['pro-estado'].textContent,/no permitió borrar/);});
