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

- El catálogo de producción ya muestra seis proyectos y «Todos 6», pero todavía sirve una etiqueta antigua para el proyecto del Zaragoza. El código actualizado indica resultados y clasificación J10, con métricas avanzadas hasta J8.
- Actualicé la simulación del Grupo 2 a la J10. Usa marcadores hasta J8 desde la base estadística y añade 20 resultados de J9-J10 en la base separada de solo marcadores. La clasificación calculada coincide exactamente con la publicada: 100 partidos jugados y 280 pendientes.
- Regeneré 10.000 temporadas, probabilidades, tablas, gráficos, página, CSV y borradores de redes. El Zaragoza queda primero en el 22,9 % y entre los cinco primeros en el 72,8 % de las simulaciones (49,9 % en playoff); el descenso aparece en el 0,7 %. La puntuación media simulada es 65 puntos. Son resultados del modelo, no un pronóstico.
- No completé xG ni estadísticas avanzadas para J9-J10 porque no hay un conjunto verificable. La página separa ese corte del corte de resultados.
- La revisión y Pages finalizaron correctamente para `bbca564` (`Corrige metadatos y cortes de la simulacion`). Sin embargo, la versión que devuelve Cloudflare aún muestra el canonical de `grupo-2.html` en la página de simulación y la etiqueta antigua del catálogo. La comprobación con parámetro de versión también devuelve esa copia anterior.
- En ese momento no se pudo purgar: no había credenciales de Cloudflare API ni acceso confirmado al panel. La situación posterior queda registrada en la sección de verificación.
- Imágenes web de la simulación: 1200×630 para compartir (75 KB), 1600×900 para los gráficos (86–106 KB). `git diff --check` está limpio. No ejecuté pytest; el generador comprobó los marcadores contra la clasificación J10 antes de calcular.

## Verificación posterior a la purga · 3 de noviembre de 2026

- El usuario confirmó que la purga selectiva ya se realizó.
- Al volver a abrir el catálogo, Cloudflare mostró su verificación de seguridad anti-bots; las solicitudes de comprobación desde consola devolvieron HTTP 403.
- Por ese bloqueo no fue posible leer el HTML servido ni confirmar el canonical de la simulación o la etiqueta del catálogo después de la purga. La confirmación de la purga queda registrada, pero la comprobación del contenido publicado sigue pendiente.
- Próximo paso: revisar las dos rutas desde un navegador que haya superado la verificación de Cloudflare y confirmar el recuento, los cortes J10/J8 y el canonical. Después, revisar la política de caché HTML y conservar la caché de recursos estáticos versionados.

## Próximo paquete de pasos

1. Verificar desde un navegador autorizado `https://lineadepase.com/proyectos/` y `https://lineadepase.com/proyectos/real-zaragoza/simulacion.html`.
2. Confirmar «Todos 6», la etiqueta de resultados y clasificación J10 / métricas avanzadas J8, y el canonical propio de la simulación.
3. Revisar la política de caché HTML para reducir la posibilidad de que se repita la discrepancia, manteniendo la caché de recursos estáticos versionados.
4. Cuando haya datos avanzados verificables, completar J9-J10; después de J11, actualizar marcadores y simulación.
