# Auditoría estática de accesibilidad

`python herramientas/auditar_accesibilidad_visual.py` se ejecuta en cada revisión del sitio. No instala dependencias ni sustituye una revisión con lector de pantalla.

## Qué comprueba

- Siete grupos CSS de controles con altura mínima de 44 px.
- Reglas de foco de 3 px y contraste de los tokens de foco y texto de gráficos en temas claro y oscuro.
- Nombres de `button`, `input`, `select` y `textarea` en los documentos HTML: texto del botón, `aria-label`, `aria-labelledby`, `title`, valores de botones de entrada, texto alternativo de imágenes dentro de botones, etiquetas `<label for>` y etiquetas que envuelven el campo. Los `input type="hidden"` quedan fuera.
- Autocomprobaciones de nombres válidos y de dos fallos conocidos: botón sin nombre y campo sin etiqueta. Si la heurística deja de detectar cualquiera de ellos, la auditoría falla en CI.

## Límites y revisión manual

El analizador HTML es deliberadamente pequeño. No calcula el nombre accesible completo que produce el navegador y puede no reconocer controles personalizados con `role="button"`, nombres derivados de contenido SVG, campos cuyo único texto es un `placeholder`, controles creados en ejecución ni relaciones ARIA más complejas. Tampoco evalúa el orden de lectura, la calidad del texto alternativo, todos los estados de contraste o la experiencia con un lector de pantalla. Los enlaces se revisan por rutas y destinos en la auditoría de enlaces, pero sus nombres no se certifican aquí.

Para esos casos hay que revisar el árbol de accesibilidad y operar la interfaz con teclado y un lector de pantalla. Los diálogos de impresión lanzan el panel nativo del navegador: la CI no los abre ni confirma trabajos de impresión. Las descargas se revisan por su nombre accesible y destino; no es necesario descargar archivos para esta auditoría.
