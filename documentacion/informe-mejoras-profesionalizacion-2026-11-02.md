# Informe de mejoras de profesionalización

**Línea de pase · 2 de noviembre de 2026**

## Resumen

Se completaron, en el orden previsto, siete paquetes de mejora: guía visual; portada y navegación; catálogo y archivo; lectura de artículos; herramientas interactivas; registro de imágenes; y mantenimiento técnico, accesibilidad y rendimiento. Los cambios priorizan consistencia visual, orientación del lector y controles claros, manteniendo la voz editorial en tercera persona y los límites de los datos a la vista.

## Cambios realizados

1. **Sistema visual y cubiertas piloto.** Se definió en `guia-visual.md` una escala de color, tipografía, espaciado y radios, más el uso puntual de líneas del campo. Se incorporó un divisor gráfico discreto en portada y catálogo. Los sellos y portadas existentes se documentaron como patrón para temporadas, territorio y ocasiones.
2. **Portada y navegación.** Se hizo más visible la entrada a Herramientas y se actualizó la franja de novedades con la ficha de la J10 y enlaces a las publicaciones anteriores.
3. **Catálogo y archivo.** El catálogo muestra cuántas fichas hay, permite filtrar por tipo, guarda el filtro en la URL y explica cuando no hay resultados. El archivo conserva su búsqueda y filtros existentes; se uniformó su presentación visual.
4. **Artículos.** Se afinó la jerarquía del encabezado, el ancho de lectura y las fichas de contexto. Se revisaron páginas representativas del Zaragoza y análisis temáticos, que ya distinguen claves, método y límites.
5. **Herramientas.** El comparador y el mapa incluyen un botón para volver a su configuración inicial. La selección vuelve a actualizar la URL compartible.
6. **Derechos de imagen.** Se añadió `registro-imagenes.md` con autoría, licencia, origen y modificaciones comprobados para las dos fotografías editoriales de Riazor y Graham Hansen. Los créditos ya acompañan las imágenes publicadas.
7. **Calidad y mantenimiento.** Se añadió una página 404 de Línea de pase con rutas útiles, una lista editorial para futuras publicaciones y una comprobación técnica general.

## Comprobaciones

- `auditar_enlaces.py`: 52 páginas, 2.275 enlaces y recursos locales, 113 imágenes; no detectó rutas rotas, anclas ausentes, `alt` problemáticos ni IDs duplicados.
- `auditar_imagenes.py`: 91 imágenes informativas, 22 decorativas, ninguna pendiente de revisión o sin texto alternativo. La portada usa 385 KiB estimados de imágenes a 800 px (presupuesto: 1.200 KiB). No hay páginas por encima del presupuesto de imagen configurado.
- `auditar_accesibilidad_visual.py`: siete grupos de controles cumplen el mínimo de 44 px; comprobó foco, contraste SVG en claro y oscuro, nombres accesibles en 57 páginas y 23 SVG exportables con título y descripción.
- `calidad_web.py`: completó su recorrido sin proponer cambios adicionales.
- `node --check` de `assets/comparador.js` y `assets/mapa-grupo.js`, y `git diff --check`: sin errores.
- En navegador local, el comparador recuperó Zaragoza–Villarreal B y dejó un mensaje de estado. El mapa volvió a Zaragoza, xG a favor, xG en contra, casa y fuera, temporada completa y Sofascore.

## Revisión de producción · 3 de noviembre de 2026

- La portada y una ruta inexistente abren correctamente; la ruta inexistente muestra la página 404 de Línea de pase.
- En móvil (390 px), la portada, el catálogo, el comparador y el mapa no provocan desbordamiento horizontal de página.
- El filtro por trabajos del máster conserva `?tipo=master`, deja un único proyecto visible y actualiza el recuento dinámico.
- Encontré una cifra fija desactualizada en el botón «Todos»: decía 5 con seis proyectos publicados. La corregí a 6 en el catálogo.
- En el comparador y el mapa probé cambiar filtros y restablecerlos. Ambos recuperan su configuración inicial, conservan filtros en la URL y muestran la información esperada.

## Aspectos pendientes que requieren datos o acceso externo

- La comparación de grupo está cortada en la jornada 8, mientras que el seguimiento individual del Zaragoza llega a la J10. El sitio ya lo declara de forma visible. Para sincronizarlo se necesita revisar e incorporar fuentes actuales y actualizar datos, análisis y visualizaciones en conjunto.
- GitHub Actions completó con éxito la revisión del sitio y la publicación de Pages para `715a42a` (`Corrige el total de proyectos en el catálogo`). La 404 y el catálogo se comprobaron en producción.
- Los auditores comprueban código y recursos locales; no sustituyen mediciones reales de velocidad, lectores de pantalla ni revisión jurídica de las licencias originales.

## Seguimiento de caché del catálogo · 3 de noviembre de 2026

- El código publicado ya muestra «Todos 6». La URL de comprobación con parámetro de versión también muestra seis, pero la ruta canónica `https://lineadepase.com/proyectos/` continuó mostrando «Todos 5» durante la revisión. Esto apunta a una respuesta antigua en caché.
- No se pudo confirmar una purga: la sesión disponible no tiene acceso al panel de Cloudflare. La publicación y el despliegue de GitHub Pages sí finalizaron correctamente; la actualización visible en la ruta canónica queda pendiente de purgar y verificar.
- Purga puntual recomendada: Cloudflare → Caching → Configuration → Purge Cache → Custom Purge → Purge by URL, con `https://lineadepase.com/proyectos/`. Evitar una purga global. Si sigue sirviendo la cifra antigua, revisar la regla de caché HTML y purgar también `https://lineadepase.com/proyectos/index.html`.

## Próximo paquete de pasos

1. Purgar la URL canónica del catálogo en Cloudflare.
2. Volver a abrir `/proyectos/` en móvil y escritorio y confirmar que el botón y la lista muestran seis proyectos.
3. Revisar si otras páginas HTML tienen una política de caché demasiado larga; mantener la caché de recursos estáticos con nombres versionados.
4. Después, actualizar el corte de datos del Grupo 2 y regenerar sus comparativas.