"""Integra el consentimiento básico de Analytics en las páginas públicas."""
import re

ETIQUETA = '<!-- Consentimiento de analítica -->\n<link rel="stylesheet" href="/assets/consentimiento.css?v=20261021">\n<script src="/assets/consentimiento.js?v=20261021" defer></script>\n<!-- /Consentimiento de analítica -->'
PIE = '<!-- Preferencias de cookies -->\n<div class="cookies-enlaces"><a href="/privacidad/">Privacidad y cookies</a><button type="button" data-preferencias-cookies hidden>Preferencias de cookies</button></div>\n<!-- /Preferencias de cookies -->'


def incorporar_etiqueta(html):
    """Sustituye la carga directa y mantiene una única integración y pie."""
    salto = "\r\n" if "\r\n" in html else "\n"
    html = re.sub(r'<!-- Google tag \(gtag\.js\) -->\s*<script\b[^>]*></script>\s*<script>.*?</script>\r?\n?', '', html, flags=re.S)
    html = re.sub(r'<!-- Consentimiento de analítica -->.*?<!-- /Consentimiento de analítica -->\r?\n?', '', html, flags=re.S)
    html = re.sub(r'<!-- Preferencias de cookies -->.*?<!-- /Preferencias de cookies -->\r?\n?', '', html, flags=re.S)
    html = html.replace('<head>', '<head>' + salto + ETIQUETA.replace('\n', salto), 1)
    return html.replace('</footer>', PIE.replace('\n', salto) + salto + '</footer>', 1)
