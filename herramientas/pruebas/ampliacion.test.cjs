const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

// Ejecuta los controles reales con un DOM mínimo: SVG responsivo y SVG con dimensiones.
function check(attributes, expected) {
  class Element {
    constructor(attrs = {}) { this.attrs = {...attrs}; this.style = {}; this.listeners = {}; }
    setAttribute(k,v) { this.attrs[k] = v; }
    getAttribute(k) { return this.attrs[k] ?? null; }
    hasAttribute(k) { return k in this.attrs; }
    removeAttribute(k) { delete this.attrs[k]; }
    addEventListener(k,fn) { this.listeners[k] = fn; }
    append(child) { this.child = child; }
    replaceChildren() { this.child = null; }
    focus() {}
    querySelectorAll() { return []; }
  }
  const role = new Element({role:'button'}), tab = new Element({tabindex:'0'});
  const copy = new Element(attributes); copy.tagName = 'svg';
  copy.querySelectorAll = selector => selector === '[role="button"]' ? [role] : selector === '[tabindex]' ? [tab] : [];
  const source = new Element(attributes);
  source.width = {baseVal:{value:Number(attributes.width)}};
  source.height = {baseVal:{value:Number(attributes.height)}};
  source.cloneNode = () => copy;
  const content = new Element(), output = new Element(), title = new Element();
  const minus = new Element(), plus = new Element(), close = new Element();
  const dialog = new Element(); dialog.showModal = () => {};
  dialog.querySelector = key => ({'.contenido-ampliacion':content,output,'h2':title,'[data-zoom="menos"]':minus,'[data-zoom="mas"]':plus,'[data-cerrar]':close}[key]);
  const holder = new Element(); holder.querySelector = () => ({textContent:'El mapa'});
  const chart = new Element(); chart.classList = {contains:()=>true}; chart.parentElement = holder;
  chart.querySelector = () => source;
  const document = {
    documentElement:new Element(),body:{append(){},classList:{add(){}}},
    querySelector:()=>null,
    querySelectorAll:selector=>selector === '.grafico,.figura img' ? [chart] : [],
    createElement:tag=>tag === 'dialog' ? dialog : new Element()
  };
  vm.runInNewContext(fs.readFileSync('assets/mejoras.js','utf8'), {document,matchMedia:()=>({matches:false}),window:{}});
  holder.child.listeners.click();
  assert.equal(copy.getAttribute('viewBox'), expected);
  assert.equal(copy.hasAttribute('width'), false);
  assert.equal(copy.hasAttribute('height'), false);
  assert.equal(role.hasAttribute('role'), false);
  assert.equal(tab.hasAttribute('tabindex'), false);
  assert.equal(content.child, copy);
  plus.listeners.click(); assert.equal(content.style.width,'150%');
}
check({viewBox:'0 0 850 540'},'0 0 850 540');
check({width:'960',height:'480'},'0 0 960 480');
check({viewBox:'10 20 850 540',width:'960',height:'480'},'10 20 850 540');
console.log('Ampliación: SVG responsivo, dimensiones antiguas, origen del viewBox, zoom y controles de lectura comprobados.');
