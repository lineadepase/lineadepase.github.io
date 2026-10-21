const assert=require('node:assert/strict');
const fs=require('node:fs');
const root=require('node:path').resolve(__dirname,'../..');
const m=require(root+'/assets/metricas-grupo.js');
const data=JSON.parse(fs.readFileSync(root+'/datos/comparador-grupo2.json','utf8'));
const rows=data.partidos;
const home=m.filter(rows,{sede:'Casa'});
const z=home.filter(r=>r.equipo==='Real Zaragoza'),v=home.filter(r=>r.equipo==='Villarreal B');
assert.equal(m.calc(z,'puntos').value,3);
assert.equal(m.calc(v,'puntos').value,1.75);
assert.equal(m.calc(z,'puntos',{modo:'totales'}).value,9);
assert.equal(m.calc(v,'puntos',{modo:'totales'}).value,7);
assert.equal(m.filter(rows,{periodo:'ultimas5',jornada:8}).length,100);
assert.ok(m.filter(rows,{periodo:'ultimas5',jornada:8}).every(r=>r.jornada>=4));
const sample=[{equipo:'A',goles_favor:2,goles_contra:0,xg:0,posesion_pct:40,fuente_xg:'https://www.sofascore.com/x'},{equipo:'A',goles_favor:1,goles_contra:1,xg:null,posesion_pct:60},{equipo:'B',goles_favor:0,goles_contra:1,xg:3,fuente_xg:'https://other.example/x'}];
assert.deepEqual(m.calc(sample,'xg'),{value:0,count:1});
assert.deepEqual(m.calc(sample,'xg',{fuente:'todas'}),{value:1.5,count:2});
assert.equal(m.calc(sample,'posesion',{modo:'totales'}).value,50);
assert.equal(m.reference(sample,'puntos').value,4/3);
assert.equal(m.reference(sample,'puntos',{modo:'totales'}).value,2);
assert.equal(m.calc([],'xg').value,null);
assert.equal(m.official({fuente_xg:'https://sofascore.com.evil.example'}),false);
for(const id of Object.keys(m.definitions)){
 const valid=rows.filter(r=>Number.isFinite(r[m.definitions[id].key]));
 if(id!=='puntos'&&id!=='xg'&&id!=='xgc'){
  assert.ok(Math.abs(m.calc(rows,id).value-valid.reduce((s,r)=>s+r[m.definitions[id].key],0)/valid.length)<1e-9,id);
 }
}
console.log('Correctos: medias, totales, muestras desiguales, últimos cinco partidos, datos ausentes, cero real, fuentes y referencia ponderada.');
