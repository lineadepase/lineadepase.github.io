const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const core=require('../../assets/linea2-core.js');
const script=fs.readFileSync(path.join(__dirname,'../../assets/linea2-experiencias.js'),'utf8');
function boot(){
 const elements={},downloads=[],blobs=[];
 function element(){return {value:'',textContent:'',children:[],events:{},style:{},dataset:{},hidden:false,append(...v){this.children.push(...v)},replaceChildren(...v){this.children=v},setAttribute(){},addEventListener(k,fn){this.events[k]=fn},click(){downloads.push(this)}};}
 for(const id of ['tiros','prob','distribucion-cuerpo','distribucion-resumen','muestra-tiros','muestra-goles','muestra-n','muestra-k','muestra-resultado','muestra-intervalo','muestra-lectura','temporada-datos','temporada-sede','temporada-resultado','temporada-cobertura','temporada-resumen','temporada-metricas','temporada-vacia','temporada-csv','temporada-restablecer','temporada-controles','temporada-acciones'])elements[id]=element();
 Object.entries({tiros:5,prob:15,'muestra-tiros':20,'muestra-goles':4,'temporada-sede':'Todas','temporada-resultado':'Todos','temporada-cobertura':'Todas'}).forEach(([id,value])=>elements[id].value=value);
 elements['temporada-datos'].textContent=JSON.stringify({corte:'2026-11-21',partidos:[{jornada:1,sede:'Casa',rival:'Uno',goles_favor:2,goles_contra:1,completo:true,tiros_zaragoza:10,tiros_rival:5,posesion_pct:60},{jornada:2,sede:'Fuera',rival:'Dos',goles_favor:0,goles_contra:0,completo:false}]});
 const rows=[1,2].map(j=>Object.assign(element(),{dataset:{seasonRow:String(j)}}));
 vm.runInNewContext(script,{LDP2:core,document:{getElementById:id=>elements[id],createElement:element,createTextNode:text=>text,querySelectorAll:()=>rows},Blob,URL:{createObjectURL:b=>{blobs.push(b);return 'blob:test'},revokeObjectURL(){}},setTimeout:fn=>fn(),Intl,Number,Math,JSON,Set});
 return {e:elements,rows,downloads,blobs};
}
test('distribution se actualiza con los controles',()=>{const {e}=boot();assert.equal(e['distribucion-cuerpo'].children.length,6);e.tiros.value=2;e.prob.value=50;e.tiros.events.input();assert.equal(e['distribucion-cuerpo'].children.length,3);assert.match(e['distribucion-resumen'].textContent,/1 goles/);assert.equal(e['distribucion-cuerpo'].children[1].children[1].textContent,'50 %');});
test('la muestra limita goles cuando disminuyen los disparos',()=>{const {e}=boot();e['muestra-goles'].value=20;e['muestra-tiros'].value=2;e['muestra-tiros'].events.input();assert.equal(e['muestra-goles'].value,'2');assert.equal(e['muestra-goles'].max,'2');assert.equal(e['muestra-resultado'].textContent,'100 %');});
test('selección vacía y restablecimiento',()=>{const {e,rows}=boot();e['temporada-sede'].value='Fuera';e['temporada-resultado'].value='Victoria';e['temporada-sede'].events.change();assert.equal(e['temporada-csv'].disabled,true);assert.equal(e['temporada-vacia'].hidden,false);assert.ok(rows.every(r=>r.hidden));e['temporada-restablecer'].events.click();assert.ok(rows.every(r=>!r.hidden));assert.equal(e['temporada-csv'].disabled,false);});
test('CSV de la selección excluye partidos ocultos',async()=>{const {e,downloads,blobs}=boot();e['temporada-sede'].value='Casa';e['temporada-sede'].events.change();assert.match(e['temporada-metricas'].textContent,/n = 1/);e['temporada-csv'].events.click();assert.equal(downloads[0].download,'zaragoza-seleccion-2026-11-21.csv');const csv=await blobs[0].text();assert.match(csv,/Uno/);assert.doesNotMatch(csv,/Dos/);});
