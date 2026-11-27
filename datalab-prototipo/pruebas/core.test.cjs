const {test}=require('node:test');
const assert=require('node:assert/strict');
const core=require('../../assets/linea2-core.js');
const near=(a,b,tolerance=1e-12)=>assert.ok(Math.abs(a-b)<tolerance,`${a} != ${b}`);
test('distribución exacta para dos remates y extremos',()=>{assert.deepEqual(core.distribution(2,.5),[.25,.5,.25]);assert.deepEqual(core.distribution(3,0),[1,0,0,0]);assert.deepEqual(core.distribution(3,1),[0,0,0,1]);assert.deepEqual(core.distribution(0,.5),[1]);});
test('distribución normalizada y esperanza para todo el rango del laboratorio',()=>{for(let n=1;n<=30;n++)for(const p of [0,.01,.15,.5,.95,1]){const values=core.distribution(n,p);near(values.reduce((a,b)=>a+b,0),1);near(values.reduce((a,b,k)=>a+b*k,0),n*p);assert.ok(values.every(x=>x>=0&&x<=1));}});
test('parámetros inválidos rechazados',()=>{for(const args of [[-1,.5],[2.5,.5],[101,.5],[10,-.1],[10,NaN]])assert.throws(()=>core.distribution(...args),RangeError);for(const args of [[0,0],[3,2],[1.5,20],[-1,20]])assert.throws(()=>core.wilson(...args),RangeError);});
test('Wilson conserva límites y simetría incluso con cero o todos goles',()=>{for(let n=1;n<=50;n++)for(let k=0;k<=n;k++){const a=core.wilson(k,n),b=core.wilson(n-k,n);assert.ok(a.low>=0&&a.high<=1);assert.ok(a.low<=a.rate+1e-12&&a.high>=a.rate-1e-12);near(a.low,1-b.high);near(a.high,1-b.low);}near(core.wilson(0,1).high,.7934506856227626);});
test('más muestra reduce incertidumbre a igual proporción',()=>{const small=core.wilson(4,20),large=core.wilson(40,200);near(small.rate,large.rate);assert.ok(large.high-large.low<small.high-small.low);});
const matches=[
 {jornada:1,fecha:'2026-09-01',rival:'Uno',sede:'Casa',goles_favor:2,goles_contra:1,completo:true,tiros_zaragoza:10,tiros_rival:4,posesion_pct:60},
 {jornada:2,fecha:'2026-09-08',rival:'Dos',sede:'Fuera',goles_favor:0,goles_contra:0,completo:false,tiros_zaragoza:99,tiros_rival:99,posesion_pct:99},
 {jornada:3,fecha:'2026-09-15',rival:'Tres',sede:'Casa',goles_favor:0,goles_contra:1,completo:true,tiros_zaragoza:0,tiros_rival:6,posesion_pct:null}
];
test('filtros combinables y conteos sin pérdida de ceros',()=>{assert.equal(core.filterMatches(matches,'Casa','Victoria','Solo completas').length,1);assert.equal(core.filterMatches(matches,'Fuera','Derrota').length,0);const s=core.summarize(matches);assert.equal(s.points,4);assert.equal(s.games,3);assert.equal(s.shots,5);assert.equal(s.against,5);assert.equal(s.possession,60);assert.equal(s.possessionCount,1);assert.equal(s.shotsCount,2);});
test('selección vacía conserva ausencia de estadísticas',()=>{const s=core.summarize([]);assert.equal(s.games,0);assert.equal(s.shots,null);assert.equal(s.possession,null);});
test('CSV incluye corte y oculta métricas no validadas',()=>{const csv=core.csv(matches,'2026-09-20');assert.ok(csv.startsWith('\ufeff'));assert.match(csv,/2026-09-20/);assert.doesNotMatch(csv,/99/);assert.match(csv,/"0";"6"/);});
test('CSV escapa comillas, separadores y fórmulas',()=>{const csv=core.csv([{...matches[0],rival:' =HYPERLINK("x");equipo'}],'2026-09-20');assert.match(csv,/"' =HYPERLINK\(""x""\);equipo"/);});
test('pasaporte valida versión, tamaño y áreas',()=>{assert.deepEqual(core.passport({version:1,areas:['Play','Play'],nota:'Hola'},['Play']),{areas:['Play'],nota:'Hola'});for(const bad of [null,{version:2,areas:[],nota:''},{version:1,areas:['Desconocida'],nota:''},{version:1,areas:[],nota:'a'.repeat(2001)}])assert.throws(()=>core.passport(bad,['Play']),TypeError);});

test('enlaces aceptan solo controles válidos e ignoran notas y parámetros ajenos',()=>{const state=core.readView('?n=999&p=-1&mn=20&mk=4&sede=Casa&resultado=Victoria&cobertura=Solo+completas&nota=secreto');assert.equal(state.shots,undefined);assert.equal(state.probability,undefined);assert.equal(state.venue,'Casa');assert.equal(state.sampleShots,20);assert.equal(state.nota,undefined);const url=core.viewUrl('https://lineadepase.com/datalab-prototipo/?nota=secreto',{...state,nota:'privada'},'season');assert.ok(!url.includes('nota'));assert.equal(new URL(url).searchParams.get('sede'),'Casa');});

test('enlace de comparación conserva temporadas e impide identificadores inválidos',()=>{const url=new URL(core.comparisonUrl('https://lineadepase.com/datalab-prototipo/?n=2',['2025/26|1','2026/27|1']));assert.equal(url.searchParams.get('jornada_a'),'2025/26|1');assert.equal(url.searchParams.get('jornada_b'),'2026/27|1');assert.equal(url.searchParams.get('n'),null);for(const ids of [[],['2026/27|1','2026/27|1'],['https://otro','2026/27|1']])assert.throws(()=>core.comparisonUrl(url.href,ids),TypeError);});
