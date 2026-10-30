const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const source=fs.readFileSync(path.resolve(__dirname,'../../assets/previas.js'),'utf8');
function run(instant){
  const cards=['2026-10-31','2026-10-23','2026-10-27'].map(fecha=>({dataset:{fecha,hora:fecha.endsWith('27')?'21:00':''},label:{},querySelector(){return this.label;}}));
  const grid={children:cards,appendChild(card){this.children.splice(this.children.indexOf(card),1);this.children.push(card);}};
  let update;
  class FixedDate extends Date{constructor(...args){super(args.length?args[0]:instant);}}
  vm.runInNewContext(source,{Date:FixedDate,Intl,document:{querySelector:()=>grid,addEventListener(){}},setInterval(fn){update=fn;}});
  update();
  assert.equal(grid.children.length,3);
  return grid.children;
}
let cards=run('2026-10-26T23:30:00Z');
assert.equal(cards[0].dataset.fecha,'2026-10-27');
assert.equal(cards[0].label.textContent,'Hoy · 21:00');
cards=run('2026-10-27T23:30:00Z');
assert.equal(cards[0].dataset.fecha,'2026-10-31');
assert.equal(cards[1].label.textContent,'Previa del 27/10');
console.log('Previas: cambio de día en Madrid, prioridad del siguiente partido, etiquetas e idempotencia correctos.');
