/* Analítica opcional: la etiqueta de Google solo se carga tras aceptar. */
(() => {
  'use strict';
  const ID = 'G-N6J2L7P4LP';
  const KEY = 'lineadepase-consentimiento-v1';
  const DURACION = 180 * 24 * 60 * 60 * 1000;
  let cargada = false;
  let memoria = null;
  let focoAnterior = null;
  function gtag() {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(arguments);
  }
  window.gtag = gtag;
  gtag('consent', 'default', {
    analytics_storage: 'denied', ad_storage: 'denied',
    ad_user_data: 'denied', ad_personalization: 'denied'
  });

  function leer() {
    try {
      const dato = JSON.parse(localStorage.getItem(KEY));
      if (dato && ['aceptado', 'rechazado'].includes(dato.estado) &&
          Number.isFinite(dato.fecha) && dato.fecha <= Date.now() &&
          Date.now() - dato.fecha < DURACION) return dato.estado;
    } catch (_) { /* Sin almacenamiento, se conserva solo durante esta página. */ }
    return memoria;
  }

  function borrarCookies() {
    const nombres = document.cookie.split(';').map(c => c.trim().split('=')[0])
      .filter(n => /^_ga(?:_|$)/.test(n) || n === '_gid' || n === '_gat');
    const host = location.hostname;
    const dominios = ['', host, '.' + host, '.lineadepase.com'];
    const partes = location.pathname.split('/').filter(Boolean);
    const rutas = ['/'];
    for (let i = 1; i <= partes.length; i++) rutas.push('/' + partes.slice(0, i).join('/'));
    for (const nombre of nombres) for (const dominio of dominios) for (const ruta of rutas) {
      document.cookie = nombre + '=; Max-Age=0; path=' + ruta +
        (dominio ? '; domain=' + dominio : '') + '; SameSite=Lax; Secure';
    }
  }

  function cargar() {
    if (cargada) return;
    cargada = true;
    window['ga-disable-' + ID] = false;
    gtag('consent', 'update', {analytics_storage: 'granted'});
    gtag('js', new Date());
    gtag('config', ID, {allow_google_signals: false, allow_ad_personalization_signals: false});
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + ID;
    document.head.appendChild(script);
  }

  function iniciar() {
    const aviso = document.createElement('section');
    aviso.className = 'consentimiento';
    aviso.setAttribute('aria-labelledby', 'consentimiento-titulo');
    aviso.hidden = true;
    aviso.innerHTML = '<div class="consentimiento-texto"><h2 id="consentimiento-titulo" tabindex="-1">Tú eliges si medimos las visitas</h2>' +
      '<p>Usamos Google Analytics para conocer qué contenidos se consultan y mejorar Línea de pase. Solo se activará si aceptas. Puedes rechazarlo y seguir usando la web.</p>' +
      '<a href="/privacidad/index.html">Información sobre privacidad y cookies</a>' +
      '<p class="consentimiento-estado" aria-live="polite"></p></div>' +
      '<div class="consentimiento-acciones"><button type="button" data-eleccion="aceptado">Aceptar analítica</button>' +
      '<button type="button" data-eleccion="rechazado">Rechazar</button>' +
      '<button type="button" data-cerrar hidden>Cerrar sin cambiar</button></div>';
    const salto = document.querySelector('a.saltar[href^="#"]');
    if (salto) salto.insertAdjacentElement('afterend', aviso);
    else document.body.prepend(aviso);
    const estado = aviso.querySelector('.consentimiento-estado');
    const cerrar = aviso.querySelector('[data-cerrar]');
    const mostrar = (enfocar = false) => {
      const actual = leer();
      estado.textContent = actual ? 'Tu elección actual: analítica ' +
        (actual === 'aceptado' ? 'aceptada.' : 'rechazada.') : '';
      cerrar.hidden = !actual;
      aviso.hidden = false;
      if (enfocar) {
        focoAnterior = document.activeElement;
        aviso.querySelector('h2').focus();
      }
    };
    const ocultar = () => {
      aviso.hidden = true;
      if (focoAnterior && focoAnterior.isConnected) focoAnterior.focus();
    };
    for (const boton of document.querySelectorAll('[data-preferencias-cookies]')) {
      boton.hidden = false;
      boton.addEventListener('click', () => mostrar(true));
    }
    cerrar.addEventListener('click', ocultar);
    aviso.addEventListener('keydown', e => {
      if (e.key === 'Escape' && leer()) ocultar();
    });
    for (const boton of aviso.querySelectorAll('[data-eleccion]')) {
      boton.addEventListener('click', () => {
        const eleccion = boton.dataset.eleccion;
        memoria = eleccion;
        try { localStorage.setItem(KEY, JSON.stringify({estado: eleccion, fecha: Date.now()})); }
        catch (_) { /* No se afirma que la elección se haya guardado entre páginas. */ }
        ocultar();
        if (eleccion === 'aceptado') cargar();
        else {
          window['ga-disable-' + ID] = true;
          borrarCookies();
          if (cargada) location.reload();
        }
      });
    }
    const inicial = leer();
    if (inicial === 'aceptado') cargar();
    else {
      window['ga-disable-' + ID] = true;
      borrarCookies();
      if (!inicial) mostrar();
    }
    window.addEventListener('storage', e => {
      if (e.key !== KEY) return;
      if (leer() === 'aceptado') { cargar(); ocultar(); }
      else {
        window['ga-disable-' + ID] = true;
        borrarCookies();
        if (cargada) location.reload();
        else if (!leer()) mostrar();
      }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar);
  else iniciar();
})();
