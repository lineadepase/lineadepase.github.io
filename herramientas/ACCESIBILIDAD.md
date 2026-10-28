# Auditoría estática de accesibilidad

`python herramientas/auditar_accesibilidad_visual.py` se ejecuta en cada revisión del sitio. No instala dependencias ni sustituye una revisión con lector de pantalla.

## Qué comprueba

- Siete grupos CSS de controles con altura mínima de 44 px.
- Reglas de foco de 3 px y contraste de los tokens de foco y texto de gráficos en temas claro y oscuro.
- Nombres de `button`, `input`, `select` y `textarea` en los documentos HTML: texto del botón, `aria-label`, `aria-labelledby`, `title`, valores de botones de entrada, texto alternativo de imágenes dentro de botones, etiquetas `<label for>` y etiquetas que envuelven el campo. Los `input type="hidden"` quedan fuera.
- Autocomprobaciones de nombres válidos y de dos fallos conocidos: botón sin nombre y campo sin etiqueta. Si la heurística deja de detectar cualquiera de ellos, la auditoría falla en CI.
- Nombres de enlaces `<a href>` en los documentos HTML: texto descendiente, `aria-label`, `aria-labelledby`, `title` y texto alternativo no vacío de imágenes o de `input type="image"`. Un `alt=""` no da nombre al enlace por sí mismo; se omite el texto dentro de elementos `hidden` o `aria-hidden="true"`, y se omiten los enlaces ocultos. La autocomprobación cubre enlaces textuales, enlaces con imagen informativa, imágenes decorativas acompañadas por texto, etiquetas ARIA, enlaces ocultos y falsos positivos de texto oculto.
- Comprobaciones de estructura para el mapa de equipos: ayuda de teclado, relación del gráfico con sus notas, encabezados de columna y descripción de la tabla alternativa.
- Comprobaciones de la salida imprimible SVG: imagen con título y descripción tomados de la pieza original; versión HTML con título específico para las jornadas seleccionadas.

## Límites y revisión manual

El analizador HTML es deliberadamente pequeño. No calcula el nombre accesible completo que produce el navegador y puede no reconocer controles personalizados con `role="button"`, nombres derivados de contenido SVG, campos cuyo único texto es un `placeholder`, contenido oculto por CSS, controles creados en ejecución ni relaciones ARIA más complejas. Solo comprueba enlaces HTML `<a href>`; no certifica áreas de imagen ni enlaces construidos en ejecución. Tampoco evalúa la calidad editorial del texto alternativo, todos los estados de contraste ni la experiencia con un lector de pantalla.

El mapa publica una alternativa en tabla con encabezados de columna, una nota que explica `n` y los mismos filtros que el gráfico. Cada punto es operable con Tab, Enter y Espacio; el estado comunica el equipo destacado. Conviene validar estos anuncios con lector de pantalla real, porque el árbol accesible de un navegador no equivale a una sesión con NVDA, JAWS o VoiceOver.

La ficha HTML imprimible conserva un título de documento, un `h1`, secciones de jornada con `h2` y métricas en listas de definición; su orden es el orden visual del documento, con el botón de impresión fuera del contenido de los partidos y oculto al imprimir. Los SVG imprimibles exponen título y descripción en el elemento raíz. El generador PDF marca el idioma español y una estructura de documento, incluye el título en metadatos y marca como párrafos los textos en el orden del SVG; los trazos y fondos son artefactos. Este chequeo de código no demuestra por sí solo la calidad de lectura en un lector PDF ni certifica PDF/UA. La CI no abre el diálogo nativo de impresión.

Para los casos que no alcanza la auditoría estática hay que revisar el árbol de accesibilidad y operar la interfaz con teclado y un lector de pantalla. Las descargas se revisan por su nombre accesible y destino; no es necesario guardar archivos para comprobar los nombres.
