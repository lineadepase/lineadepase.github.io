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

## Estado y trabajo completado · 3 de noviembre de 2026

- La URL canónica `https://lineadepase.com/proyectos/` ya muestra «Todos 6» y seis proyectos. La caché se actualizó sin una purga manual; esta sesión no tiene acceso al panel de Cloudflare. Las peticiones de cabeceras desde consola reciben 403, por lo que no se pudo medir la política de caché.
- Actualicé la simulación del Grupo 2 a la J10. Usa 80 partidos con estadísticas y marcadores hasta la J8, más 20 resultados de J9-J10 en la base independiente de solo marcadores. La clasificación calculada reproduce exactamente la clasificación publicada tras la J10: 100 partidos jugados y 280 pendientes.
- Regeneré 10.000 temporadas, probabilidades, tablas, gráficos, página de la simulación, descarga CSV y borradores para Instagram, Facebook y LinkedIn. El catálogo señala ahora el corte de resultados J10 y distingue que las métricas avanzadas llegan a la J8.
- En el modelo, el Zaragoza queda primero en el 22,9 % de las simulaciones y entre los cinco primeros en el 72,8 % (49,9 % playoff); el descenso aparece en el 0,7 %. Su puntuación media simulada es 65 puntos. Son resultados del modelo, no un pronóstico.
- No añadí xG ni completé las métricas avanzadas de J9-J10, que siguen pendientes de datos verificables. La limitación se explica en la página y en el código.
- El despliegue previo del catálogo, commit `715a42a`, pasó la revisión del sitio y la publicación de Pages. Los cambios de este paquete aún deben publicarse.
- `git diff --check` no detecta errores. No ejecuté pytest; la comprobación integrada del generador sí validó todos los marcadores frente a la clasificación J10 antes de simular.

## Límites y próximos paquetes

1. Publicar este paquete y revisar en producción la página de simulación, su CSV y el catálogo en móvil y escritorio.
2. Incorporar xG y métricas avanzadas de J9-J10 solo cuando Sofascore u otra fuente permita verificar el conjunto; mientras tanto, conservar la separación entre resultados y estadísticas.
3. Tras disputarse la J11, actualizar marcadores, clasificación y simulación; volver a comprobar la URL canónica y el peso de los gráficos.
4. Revisar la política de caché HTML desde Cloudflare cuando se pueda consultar el panel; conservar la caché de recursos estáticos versionados.
