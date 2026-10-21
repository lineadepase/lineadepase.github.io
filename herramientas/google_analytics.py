"""Etiqueta de Google Analytics para las páginas públicas de la web."""

ETIQUETA = '<!-- Google tag (gtag.js) -->\n<script async src="https://www.googletagmanager.com/gtag/js?id=G-N6J2L7P4LP"></script>\n<script>\n  window.dataLayer = window.dataLayer || [];\n  function gtag(){dataLayer.push(arguments);}\n  gtag(\'js\', new Date());\n\n  gtag(\'config\', \'G-N6J2L7P4LP\');\n</script>'


def incorporar_etiqueta(html):
    """Añade una sola etiqueta y conserva los finales de línea del HTML."""
    if "googletagmanager.com/gtag/js" in html:
        return html
    salto = "\r\n" if "\r\n" in html else "\n"
    return html.replace("<head>", "<head>" + salto + ETIQUETA.replace("\n", salto), 1)
