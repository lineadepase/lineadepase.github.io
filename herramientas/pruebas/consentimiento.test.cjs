const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const fuente = fs.readFileSync(path.join(__dirname, '../../assets/consentimiento.js'), 'utf8');
const clave = 'lineadepase-consentimiento-v1';

function entorno(inicial = null, bloqueado = false) {
  const eventos = {}, nodos = {}, scripts = [], borrados = [];
  let almacenado = inicial, recargas = 0;
  const nodo = () => ({hidden: false, dataset: {}, textContent: '', isConnected: true,
    addEventListener(tipo, fn) { this[tipo] = fn; },
    setAttribute() {}, focus() {}});
  const aceptar = nodo(), rechazar = nodo(), cerrar = nodo(), titulo = nodo(), estado = nodo();
  aceptar.dataset.eleccion = 'aceptado'; rechazar.dataset.eleccion = 'rechazado';
  const aviso = nodo();
  aviso.querySelector = s => ({'h2': titulo, '[data-cerrar]': cerrar, '.consentimiento-estado': estado}[s]);
  aviso.querySelectorAll = () => [aceptar, rechazar];
  const preferencias = nodo();
  const doc = {
    readyState: 'complete', activeElement: nodo(),
    head: {appendChild(s) { scripts.push(s); }}, body: {appendChild(n) { nodos.aviso = n; }},
    createElement(tipo) { return tipo === 'section' ? aviso : nodo(); },
    querySelectorAll() { return [preferencias]; }
  };
  Object.defineProperty(doc, 'cookie', {
    get() { return '_ga=anterior; _ga_N6J2L7P4LP=sesion; tema=oscuro'; },
    set(valor) { borrados.push(valor); }
  });
  const win = {addEventListener(tipo, fn) { eventos[tipo] = fn; }};
  const contexto = {window: win, document: doc, Date, Number, JSON,
    localStorage: {
      getItem() { if (bloqueado) throw Error('Bloqueado'); return almacenado; },
      setItem(k, v) { if (bloqueado) throw Error('Bloqueado'); almacenado = v; }
    },
    location: {hostname: 'lineadepase.com', pathname: '/proyectos/index.html', reload() {recargas++;}}
  };
  vm.runInNewContext(fuente, contexto);
  return {win, scripts, borrados, aviso, aceptar, rechazar, preferencias, eventos,
    setAlmacenado(v) {almacenado = v;},
    get almacenado() {return almacenado;}, get recargas() {return recargas;}};
}

const primera = entorno();
assert.equal(primera.scripts.length, 0, 'Sin elección no se descarga gtag');
assert.equal(primera.aviso.hidden, false);
primera.rechazar.click();
assert.equal(primera.scripts.length, 0, 'Rechazar no carga Analytics');
assert.equal(JSON.parse(primera.almacenado).estado, 'rechazado');
assert(primera.borrados.some(c => c.startsWith('_ga=;') && c.includes('domain=.lineadepase.com')));
assert(!primera.borrados.some(c => c.startsWith('tema=')), 'No se borran cookies ajenas a Analytics');
primera.aceptar.click(); primera.aceptar.click();
assert.equal(primera.scripts.length, 1, 'Aceptar repetidamente no duplica la etiqueta');
assert.equal(primera.scripts[0].src, 'https://www.googletagmanager.com/gtag/js?id=G-N6J2L7P4LP');
const comandos = primera.win.dataLayer.map(x => Array.from(x));
assert.equal(comandos[0][2].analytics_storage, 'denied');
assert.equal(comandos[0][2].ad_storage, 'denied');
assert.equal(comandos.find(x => x[0] === 'consent' && x[1] === 'update')[2].analytics_storage, 'granted');
assert.equal(comandos.find(x => x[0] === 'config')[2].allow_google_signals, false);
primera.rechazar.click();
assert.equal(primera.win['ga-disable-G-N6J2L7P4LP'], true);
assert.equal(primera.recargas, 1, 'La retirada descarga la etiqueta recargando la página');

const vigente = JSON.stringify({estado: 'aceptado', fecha: Date.now()});
const otra = entorno(vigente);
assert.equal(otra.scripts.length, 1, 'Se conserva una aceptación vigente');
otra.setAlmacenado(JSON.stringify({estado: 'rechazado', fecha: Date.now()}));
otra.eventos.storage({key: clave});
assert.equal(otra.recargas, 1, 'La revocación en otra pestaña desactiva esta página');
const caducada = entorno(JSON.stringify({estado: 'aceptado', fecha: Date.now() - 181 * 86400000}));
assert.equal(caducada.scripts.length, 0, 'Una elección caducada no autoriza seguimiento');
assert.equal(caducada.aviso.hidden, false);
const noDisponible = entorno(null, true);
noDisponible.rechazar.click();
assert.equal(noDisponible.scripts.length, 0, 'Sin almacenamiento se respeta el rechazo en la página');
console.log('Consentimiento: primera visita, rechazo, aceptación única, caducidad, cookies, retirada y sincronización comprobados.');
