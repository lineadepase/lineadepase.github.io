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
- Tras la verificación de Cloudflare, el catálogo público muestra «Todos 6», «6 proyectos» y la ficha del Zaragoza con resultados y clasificación tras J10 y métricas avanzadas hasta J8.
- La simulación pública muestra el título de J10, 100 partidos jugados y 280 pendientes. También muestra el Zaragoza con 23 % de ascenso directo, 50 % de playoff y 1 % de descenso; sus datos explican que los marcadores llegan a J10 y las métricas avanzadas a J8.
- La portada pública ya presenta la previa Zaragoza–Huesca como primera tarjeta, con imagen, hora y botón para añadirla al calendario. La imagen pesa 163 KB y la página completa de la previa abre correctamente.
- La jornada 11 todavía no se ha disputado. El calendario consultado el 3 de noviembre sitúa el Real Zaragoza–Huesca el sábado 7 de noviembre a las 21:00; no corresponde regenerar aún la simulación con marcadores de J11. [Calendario de Primera Federación, AS](https://as.com/resultados/futbol/primera_rfef/2026_2027/jornada/grupos_a_11/).
- No pude leer el canonical en el HTML público porque el navegador conectado no permite abrir la vista de código fuente. En el archivo generado local, el canonical y `og:url` apuntan a `https://lineadepase.com/proyectos/real-zaragoza/simulacion.html`; queda pendiente contrastar ese metadato en producción.
- La previsualización local de `127.0.0.1:8879` no respondía al abrir la ruta del proyecto de Eurocopa. Inicié el servidor local; `proyectos/espana-eurocopa-redes/` devuelve HTTP 200 y el título esperado. Esto valida la copia del repositorio, no la versión pública.
- Próximo paso: confirmar el canonical de producción y revisar la política de caché HTML, conservando la caché de recursos estáticos versionados.

## Revisión de la configuración de caché · 3 de noviembre de 2026

- El repositorio publica con GitHub Pages y contiene el dominio personalizado en `CNAME`; no hay archivo `_headers`, configuración de Wrangler ni Worker de Cloudflare que controle cabeceras o caché.
- Revisé el panel de Cloudflare: nivel de caché `Standard`, sin reglas de caché ni reglas de respuesta, y Development Mode desactivado.
- Cambié Browser Cache TTL de cuatro horas a `Respect Existing Headers`. Esto permite que Cloudflare siga las cabeceras que envía el origen en vez de imponer cuatro horas a las copias guardadas por los navegadores. La documentación de Cloudflare confirma que esta opción no inserta ni sobrescribe `Cache-Control` salvo que una regla lo indique: [Browser Cache TTL](https://developers.cloudflare.com/cache/how-to/edge-browser-cache-ttl/).
- Ejecuté una purga selectiva por URL de `https://lineadepase.com/proyectos/espana-eurocopa-redes/`. Cloudflare confirmó que recibió la petición y que debía surtir efecto en menos de cinco segundos; no usé «Purge Everything».
- Volví a abrir la página pública tras la purga. Carga con el título, resumen, datos, gráficos y secciones esperados. La herramienta de navegador sigue sin permitir leer el HTML de origen, así que no doy por confirmado el canonical/`og:url` servido aunque el código local y la auditoría de CI sí los validan.

## Protección de metadatos · 3 de noviembre de 2026

- La auditoría local detectó que la página de España en la Eurocopa tenía `og:url` con `/index.html`, mientras su canonical usaba la ruta limpia. Corregí la plantilla compartida para no heredar tarjetas sociales del proyecto usado como plantilla y generar `og:url` con la misma ruta que el canonical.
- Añadí `herramientas/auditar_canonicos.py` al flujo de revisión de GitHub. Comprueba canonical y `og:url` en 52 páginas; admite la 404 sin canonical y las rutas especiales de contacto y la previa más reciente.
- La auditoría local termina sin errores. Tras el despliegue purgué en Cloudflare la URL pública de la página para retirar cualquier HTML almacenado antes de la corrección.

## Revisión visual de portada y recursos · 3 de noviembre de 2026

- Revisé la portada pública en escritorio: la cabecera, el mensaje principal y los accesos a proyectos y herramientas mantienen una jerarquía clara; la previa Zaragoza–Huesca encabeza la sección y los dos partidos ya disputados aparecen con sus marcadores y enlaces de análisis.
- La tarjeta de J11 conserva la imagen original optimizada de 159 KB y usa versiones responsivas entre 26 KB y 131 KB, para que el navegador elija un tamaño acorde a la pantalla.
- La ilustración del comparador pesa 291 KB en su versión maestra, pero la portada ofrece `srcset` con derivados WebP de 480, 800, 1200, 1600 y 1672 píxeles; el navegador no tiene que descargar el archivo grande en todas las pantallas.
- No encontré en la portada un problema visual o de contenido que justifique cambiar el diseño en esta pasada. La ruta del catálogo mostró el control de seguridad de Cloudflare en una sesión nueva, por lo que no intenté sortearlo; el catálogo ya se había comprobado públicamente en la revisión anterior.
- La revisión de escritorio se complementa con la comprobación móvil de las tres páginas descrita en el apartado siguiente.

## Comprobación móvil · 3 de noviembre de 2026

- Revisé la portada, el catálogo y la previa Zaragoza–Huesca con un viewport de 390 px; también comprobé la portada a 320 px. En las mediciones de las tres rutas, el ancho desplazable coincide con el ancho visible, sin desbordamiento horizontal de página.
- La portada coloca el titular, las llamadas principales y la ilustración en una columna; la tarjeta de la previa conserva imagen, fecha, hora y enlaces legibles.
- El catálogo mantiene una columna para las fichas. Sus filtros forman una fila desplazable propia, sin ensanchar la página; aparecen los seis proyectos y el contador coincide.
- La previa mantiene sus secciones y tablas dentro del ancho de pantalla. No vi una corrección móvil concreta que justificara cambiar el CSS en esta pasada.
- Restablecí el navegador al tamaño normal y lo dejé de nuevo en la portada.

## Auditoría técnica general · 3 de noviembre de 2026

- En 53 páginas, el auditor revisó 2.305 enlaces y recursos locales y 116 imágenes: no encontró rutas rotas, anclas inválidas, textos alternativos ausentes ni identificadores duplicados problemáticos.
- La comprobación de metadatos encontró canonical correctos en 52 páginas; la 404 no lleva canonical por diseño.
- La revisión de accesibilidad visual no detectó errores en grupos de controles de 44 px, indicadores de foco, contraste de los SVG en tema claro y oscuro, nombres accesibles de 1.744 enlaces o títulos y descripciones de 23 SVG exportables.
- El auditor de imágenes no detectó textos alternativos pendientes ni páginas por encima del presupuesto. La simulación estima 655 KiB de imágenes a un ancho máximo de 800 px frente a un presupuesto de 1.200 KiB. Portada estima 2 KiB de imagen prioritaria y 436 KiB diferidos; el catálogo, 10 KiB iniciales y 229 KiB diferidos. Son estimaciones basadas en atributos y `srcset`, no mediciones de red ni de rendimiento real.
- Los cuatro auditores locales terminaron correctamente dentro de los criterios que revisan. PageSpeed Insights encontró después un problema de contraste en el texto duplicado del comparador; la corrección queda detallada en el apartado siguiente.

## PageSpeed y corrección de contraste · 3 de noviembre de 2026

- PageSpeed Insights midió la portada con Lighthouse 13.6.0. En móvil obtuvo 95 en rendimiento, 96 en accesibilidad, 100 en prácticas recomendadas y 100 en SEO; FCP 1,5 s, LCP 2,6 s, TBT 0 ms y CLS 0,083. En escritorio obtuvo 97, 96, 100 y 100; FCP 0,4 s, LCP 0,7 s, TBT 0 ms y CLS 0,102. El informe no encontró datos de usuarios reales para esta página, así que son pruebas de laboratorio y no mediciones de experiencia de visitantes. [Informe de PageSpeed](https://pagespeed.web.dev/analysis?url=https%3A%2F%2Flineadepase.com%2F&form_factor=mobile) · [Cómo funciona PageSpeed Insights](https://developers.google.com/speed/docs/insights/v5/about).
- Lighthouse señaló contraste insuficiente en el texto «Abrir el comparador de equipos» y en su enlace. El texto estaba duplicado junto a la ilustración y la clase `solo-lectores` no lo ocultaba. Lo retiré del HTML y de `herramientas/segunda_edicion.py`; el enlace conserva su `aria-label` y la descripción de la imagen.
- La auditoría local de accesibilidad visual pasa tras el cambio. Publiqué el arreglo en el commit `267f58c`.
- Lighthouse también atribuye el CLS de escritorio (0,102) al bloque principal y marca la ilustración SVG de portada como imagen sin tamaño durante el desplazamiento, aunque el HTML declara `width="720"` y `height="540"`. Lo dejo pendiente de análisis antes de tocar dimensiones o estilos.
- El intento de volver a cargar la portada para verificar el despliegue encontró la página de comprobación de seguridad de Cloudflare. No intenté resolverla ni sortearla; la presencia del cambio en producción queda pendiente de una sesión normal.

## Medición posterior y diagnóstico del CLS · 3 de noviembre de 2026

- Repetí PageSpeed Insights tras la publicación. En la portada, accesibilidad quedó en 100 tanto en móvil como en escritorio; rendimiento fue 94 en móvil y 97 en escritorio. En móvil: FCP 1,5 s, LCP 2,7 s, TBT 0 ms y CLS 0. En escritorio: FCP 0,4 s, LCP 0,7 s, TBT 0 ms y CLS 0,102.
- En el catálogo, PageSpeed dio 98 en rendimiento móvil y 97 en escritorio, con accesibilidad, prácticas recomendadas y SEO en 100. El CLS fue 0 en móvil y 0,103 en escritorio. [Informe móvil del catálogo](https://pagespeed.web.dev/analysis?url=https%3A%2F%2Flineadepase.com%2Fproyectos%2F&form_factor=mobile).
- Los diagnósticos de CLS atribuyen aproximadamente 0,102 al `<main id="contenido">` tanto en portada como en catálogo; en portada también muestran el SVG principal. No aíslan un elemento descendiente responsable. La ilustración de portada declara `width="720"` y `height="540"`; por ahora no hay evidencia suficiente para cambiar dimensiones o estilos sin alterar su presentación.
- Estos son resultados de laboratorio Lighthouse, no datos de usuarios reales. El patrón repetido de CLS solo en escritorio merece una traza de rendimiento en una sesión normal para localizar qué elemento cambia de posición. No hice más cambios visuales basados en una atribución imprecisa.
- La prueba anterior en Chrome encontró un control de seguridad de Cloudflare; no lo sorteé. Por tanto, la comprobación directa en una sesión normal sigue pendiente aunque PageSpeed ya mida la página publicada.

## CLS de fuentes y nueva revisión · 4 de noviembre de 2026

- La nueva pasada de PageSpeed Insights para la portada, a las 14:32, obtuvo 94 en rendimiento móvil y 97 en escritorio; accesibilidad, prácticas recomendadas y SEO quedaron en 100. FCP/LCP/TBT/CLS fueron 1,5 s / 2,7 s / 0 ms / 0 en móvil y 0,4 s / 0,7 s / 0 ms / 0,102 en escritorio. No hay datos de usuarios reales para la URL.
- El ajuste anterior añadió `aspect-ratio: 4/3` a la ilustración de portada. PageSpeed dejó de listarla como imagen sin tamaño, pero el CLS global siguió en 0,102; el único elemento desplazado que identifica es `<main id="contenido">`. La causa del salto restante en la portada aún no queda localizada.
- En el catálogo, PageSpeed identificó como fuentes del salto a dos archivos de Google Fonts. Antes del cambio, la medición de las 14:29 dio CLS 0,084 en móvil y 0,125 en escritorio. Cambié `display=swap` por `display=optional` en las 53 páginas y plantillas que cargan Archivo y Big Shoulders Display. Google Fonts admite `optional`; web.dev explica que evita sustituir la fuente si llega tarde, aunque en la primera visita lenta puede mantenerse la fuente de respaldo. [Google Fonts CSS API](https://developers.google.com/fonts/docs/css2) · [Reducir CLS](https://web.dev/articles/optimize-cls/).
- En la nueva medición del catálogo a las 14:33, PageSpeed dio 98 en rendimiento móvil y 97 en escritorio, 100 en accesibilidad, prácticas recomendadas y SEO, y CLS 0 en móvil y 0,100 en escritorio. La tabla aún muestra las fuentes como origen del salto. Frente a la pasada inmediatamente anterior, el CLS de escritorio bajó 0,025; hace falta una traza para confirmar cuánto corresponde al cambio y cuánto a la variación de laboratorio. [Informe PageSpeed del catálogo](https://pagespeed.web.dev/analysis/https-lineadepase-com-proyectos/yzbyxax74w?form_factor=desktop).
- El HTML de portada confirma canonical y `og:url` como `https://lineadepase.com/`. Una recarga posterior mostró la verificación de seguridad de Cloudflare; no la resolví ni la evadí. No pude confirmar el HTML actual del catálogo en una sesión normal.
- Al revisar la configuración de Cloudflare, el panel mostraba Browser Cache TTL «4 horas», en contraste con el cambio a «Respect Existing Headers» descrito en el apartado anterior. Dejo anotada esta discrepancia para reconciliarla; no hice una purga ni modifiqué esa opción en esta revisión.
- PageSpeed es una medición de laboratorio y cambió entre pasadas; sin datos de campo, no se debe interpretar una única diferencia como mejora estable. La traza de DevTools sigue pendiente para localizar el CLS que Lighthouse atribuye al bloque principal.

## Próximo paquete de pasos

1. Grabar una traza DevTools de la carga en escritorio para identificar el CLS residual de portada y catálogo.
2. Reconciliar en Cloudflare el Browser Cache TTL actual de cuatro horas con el valor «Respect Existing Headers» que figuraba en la revisión anterior; confirmar luego la política aplicada.
3. Confirmar canonical y `og:url` del catálogo en una sesión normal, cuando la protección de Cloudflare permita abrirlo.
4. Tras disputarse la jornada 11, actualizar el seguimiento y la simulación con marcadores oficiales; añadir métricas avanzadas solo con datos verificables.
