const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const html=fs.readFileSync(path.join(__dirname,'../index.html'),'utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
function calcular(n,p){
  const elements={};
  for(const id of ['tiros','prob','n','p','resultado','barra','esperados']){
    elements[id]={value:'',textContent:'',style:{},addEventListener(){}};
  }
  elements.tiros.value=String(n);
  elements.prob.value=String(p);
  vm.runInNewContext(script,{document:{getElementById:id=>elements[id]},Intl,Math,Number});
  return Number.parseFloat(elements.barra.style.width);
}
function cerca(a,b){assert.ok(Math.abs(a-b)<1e-9,`Esperado ${b}; obtenido ${a}`);}
test('probabilidad nula',()=>cerca(calcular(30,0),0));
test('gol seguro',()=>cerca(calcular(1,100),100));
test('un disparo',()=>cerca(calcular(1,15),15));
test('dos disparos al 50%',()=>cerca(calcular(2,50),75));
test('ejemplo inicial',()=>cerca(calcular(5,15),55.62946875));
test('crece con el número de disparos',()=>assert.ok(calcular(10,15)>calcular(5,15)));
test('crece con la calidad del disparo',()=>assert.ok(calcular(5,25)>calcular(5,15)));
test('rango válido para todos los controles',()=>{for(let n=1;n<=30;n++)for(let p=0;p<=100;p++){const q=calcular(n,p);assert.ok(q>=0&&q<=100);}});
