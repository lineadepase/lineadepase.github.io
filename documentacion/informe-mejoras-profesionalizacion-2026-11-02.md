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
- En una sesión normal de Chrome posterior a la purga, confirmé en portada y catálogo que `canonical` y `og:url` coinciden con sus rutas públicas limpias (`https://lineadepase.com/` y `https://lineadepase.com/proyectos/`). En ambas páginas, la hoja de Google Fonts servida usa `display=optional`.
- Una pestaña antigua del panel de Cloudflare mostraba Browser Cache TTL «4 horas». En una pestaña nueva confirmé el valor vigente: «Respetar los encabezados existentes», en línea con el cambio registrado el 3 de noviembre. No cambié ese ajuste.
- Tras enviar a Cloudflare una purga selectiva de `https://lineadepase.com/` y `https://lineadepase.com/proyectos/`, el panel confirmó que recibió la petición y que debía aplicarse en menos de cinco segundos. No purgué otras rutas.
- La medición posterior a la purga, a las 14:44, dio en portada rendimiento 94 móvil y 97 escritorio, accesibilidad/prácticas/SEO 100, CLS 0 móvil y 0,100 escritorio. En catálogo, a las 14:45, dio rendimiento 98 móvil y 97 escritorio, accesibilidad/prácticas/SEO 100, CLS 0 móvil y 0,100 escritorio. FCP/LCP/TBT: portada 1,5/2,8/0 ms en móvil y 0,4/0,7/0 ms en escritorio; catálogo 1,5/1,5/0 ms en móvil y 0,4/0,7/0 ms en escritorio. No hay datos de usuarios reales para estas URL. [Informe actualizado del catálogo](https://pagespeed.web.dev/analysis/https-lineadepase-com-proyectos/4o8w282dwe?form_factor=desktop).
- En la tabla nueva del catálogo ya no aparecen los archivos de fuente entre los causantes; solo figura `<main id="contenido">` con CLS 0,100. En portada, la ilustración tampoco vuelve a aparecer como imagen sin tamaño; el único elemento señalado es `<main id="contenido">`. La nueva medida confirma que los cambios se sirven tras la purga, pero el CLS restante requiere una traza de DevTools para identificar su origen.
- PageSpeed es una medición de laboratorio y cambia entre pasadas; sin datos de campo, no se debe interpretar una única diferencia como mejora estable. La revisión en Chrome completó la carga pública sin pantalla de comprobación. El único pendiente técnico de esta pasada es aislar el CLS de escritorio con una traza; el diagnóstico genérico de Lighthouse no basta para cambiar estilos con seguridad.

## Revisión de contenido y adaptación de imágenes · 4 de noviembre de 2026

- La portada pública mantiene como próxima cita Zaragoza–Huesca (7 de noviembre, 21:00) y como último partido el 2–2 ante Villarreal B. El catálogo muestra seis proyectos; el seguimiento del Zaragoza diferencia resultados hasta J10 y métricas avanzadas hasta J8. Las fotos editoriales visibles incluyen crédito y licencia. No encontré en esta pasada una fecha o ficha claramente caducada.
- Los auditores locales encontraron 53 páginas y 2.319 enlaces o recursos sin rutas, anclas, atributos `alt` o IDs problemáticos. Los canonicals son correctos en 52 páginas; la 404 los omite por diseño. El auditor de imágenes contó 116 imágenes: 94 informativas, 22 decorativas, ninguna sin `alt` ni pendiente de revisión; ninguna página supera el presupuesto de 1.200 KiB. La revisión de accesibilidad visual pasó en 58 páginas.
- `herramientas/calidad_web.py` añadió variantes WebP y `srcset` a las imágenes grandes de la simulación J10. Ajusté además `sizes` para reflejar el ancho real de las dos ilustraciones limitadas a 360 y 560 px, evitando pedir candidatos de 800 px en escritorio. El auditor estima que las imágenes de esa página pasan de 655 KiB a 259 KiB a 800 px (aprox. 60 % menos) y la carga inicial estimada de 84 KiB a 31 KiB. Es una estimación del auditor según los tamaños declarados, no una medición de red real.
- Los metadatos sociales se mantienen: el generador eliminó únicamente etiquetas Open Graph duplicadas. `git diff --check` y las auditorías de enlaces, canonicals, imágenes y accesibilidad visual terminaron sin incidencias.
- El workflow «pages build and deployment» terminó correctamente para el commit `6b37d8a` el 4 de noviembre. Sin embargo, al abrir la ruta de la simulación en una sesión Chrome nueva, Cloudflare mostró una verificación de seguridad; la petición HTTP directa también respondió 403. No intenté resolver ni evadir esa comprobación, así que falta comprobar visualmente en producción que ya se sirven los nuevos `srcset`. El control de Windows también detuvo el intento de traza porque no pudo identificar con confianza la URL de Chrome. El CLS de escritorio sigue pendiente de localizar; no hice cambios basados solo en la atribución genérica de Lighthouse.
- En el HTML local, las imágenes de portada y catálogo tienen `width` y `height`. En el catálogo, los filtros empiezan con `hidden` y un script al final los muestra; esto es una posible fuente de reflujo, no una causa confirmada y no explica por sí sola la portada. No cambié el comportamiento sin una traza. Una consulta nueva a PageSpeed API devolvió HTTP 429; no hay puntuación nueva. El entorno también bloqueó iniciar una instancia aislada de Chrome con depuración remota para obtener la traza. La vista local de la simulación abrió con el contenido esperado; comprobé las 14 rutas WebP declaradas en sus `srcset`: todas respondieron HTTP 200 con tipo `image/webp`. Esta comprobación valida los recursos del repositorio y del servidor local, no la entrega pública tras Cloudflare.

## Recuento inicial del catálogo · 4 de noviembre de 2026

- La guía visual y los sellos de las tres familias ya están aplicados en las tarjetas; no hacía falta repetir ese trabajo. Encontré que el texto de respaldo del catálogo indicaba «5 proyectos» aunque hay seis fichas. Lo corregí a seis, de modo que el mensaje sea correcto antes de que JavaScript actualice el recuento.
- Aclaré también que la lámina anual muestra una selección de cuatro trabajos, aunque el catálogo reúna seis; así se entiende mejor la relación entre la pieza destacada y el archivo completo.
- Las auditorías pasaron: 53 páginas y 2.319 enlaces/recursos sin problemas, 52 canonicals correctos, y git diff --check limpio.

## Revisión de derechos de imagen en portada · 4 de noviembre de 2026

- La portada usa como imagen social una tarjeta gráfica original, no una fotografía. Revisé la imagen compartida y no contiene a Ander Herrera ni otra foto editorial.
- Las dos fotografías identificables de la portada corresponden a Graham Hansen y a la selección española en Riazor. Ambas constan en el registro de imágenes con licencia CC BY-SA 4.0 y tienen crédito y enlace de licencia junto a la foto. El retrato del autor también está identificado.
- No hizo falta sustituir imágenes ni modificar créditos.

## Diagnóstico y corrección del CLS de escritorio · 4 de noviembre de 2026

- Capturé una traza de la portada local en Chrome a 1365 × 900. El salto reproducía un CLS de 0,0944; los elementos afectados eran la navegación y el `<main>`.
- Aislé el cambio bloqueando recursos y scripts de uno en uno. El salto desapareció al bloquear `mejoras.js`, mientras bloquear las fuentes o `experiencia.js` no lo eliminó. El selector de tema se insertaba después del primer dibujo: la cabecera crecía unos 5 px y el menú se desplazaba unos 136 px.
- Reservé en escritorio el espacio del selector antes de ejecutar ese script. Al crearlo, se retira la reserva en el mismo paso. La siguiente captura local registró cero saltos de diseño en escritorio y conservó la altura final de la cabecera; la página no desbordó el ancho disponible.
- Actualicé las versiones de caché del CSS y del JavaScript en 51 páginas y tres plantillas para que se soliciten los recursos corregidos.
- En la captura móvil local de 390 px no hubo desbordamiento horizontal, pero apareció un CLS de 0,080. No coincide con el CLS de escritorio ya localizado; no atribuí ese movimiento a una causa sin aislarla. PageSpeed había medido CLS móvil 0 en las comprobaciones públicas anteriores.
- Las auditorías locales siguen sin incidencias: 53 páginas y 2.319 enlaces/recursos locales; 52 canonicals correctos; 116 imágenes sin `alt` ausentes ni páginas por encima del presupuesto; controles y nombres accesibles correctos en la revisión visual. `node --check assets/mejoras.js` terminó correctamente.
- El commit `0f72efe` pasó la revisión del sitio y el despliegue de GitHub Pages terminó correctamente ([revisión](https://github.com/lineadepase/lineadepase.github.io/actions/runs/41901888109) · [Pages](https://github.com/lineadepase/lineadepase.github.io/actions/runs/41901888184)). Tras el despliegue, la portada de `lineadepase.com` todavía responde HTTP 403 a las solicitudes desde esta sesión; falta confirmar visualmente los recursos servidos desde una sesión pública normal. No se ha enviado ni purgado nada de Cloudflare en esta pasada.

## Estabilidad del menú en móvil · 4 de noviembre de 2026

- La traza móvil local confirmó el segundo origen del CLS: el menú completo se dibujaba antes de convertirse en menú plegable. Preparé el estado de inicialización en el script temprano y reservé la altura final de la cabecera antes del primer dibujo; si JavaScript está desactivado, la navegación sigue visible.
- Tras ajustar el espacio al relleno real en ambos rangos móviles, Chrome local registró CLS 0 a 390, 768 y 1365 px. El ancho desplazable coincidió con el viewport en los tres tamaños. Con JavaScript desactivado, los siete enlaces de navegación siguen visibles a 390 px.
- Versioné los recursos actualizados en las páginas y ajusté los archivos de generación. `node --check` pasó para los dos JavaScript modificados; las auditorías locales de enlaces, canonicals, imágenes y accesibilidad visual siguen sin incidencias.
- La lectura pública permanece bloqueada por HTTP 403 en esta sesión. Todavía no hay PageSpeed posterior a este ajuste; el cero de CLS corresponde a las capturas locales y no a una medición de visitantes o de producción.

## Revisión tras la previa de la J11 · 5 de noviembre de 2026

- Integré la última revisión de `main` (`8c09572`), que actualiza la previa social de Zaragoza–Huesca y corrige los horarios de J12 y J13. La agenda del club confirma J12 el sábado 14 de noviembre a las 21:00 y J13 el sábado 21 de noviembre a las 16:30; la noticia del club confirma el Huesca el sábado 7 a las 21:00. [Calendario oficial](https://www.realzaragoza.com/partidos) · [Horario del derbi](https://www.realzaragoza.com/noticias/prioridad-para-nuestros-socios-en-la-venta-de-entradas-para-el-partido-contra-el-huesca-en-ibercaja-estadio).
- La tarjeta de redes es 1080 × 1350 y pesa 186.969 bytes; la imagen WebP que usa la previa de la web pesa 163.088 bytes. Ambas quedan en tamaños razonables para su uso.
- Repetí la revisión estática sobre la versión actual: 53 páginas y 2.319 enlaces/recursos sin errores; 52 canonicals correctos; 116 imágenes, sin `alt` ausentes ni páginas por encima del presupuesto; controles y enlaces accesibles correctos en la revisión visual. Los scripts modificados pasan `node --check`.
- La publicación de `c9ca227` y la última revisión de datos `8c09572` tienen ambos workflows de revisión y Pages en éxito. En esta sesión, la pestaña pública sigue detenida en la verificación de seguridad de Cloudflare; no la resolví ni la eludí, así que la observación visual en producción queda pendiente.

## Revisión de herramientas y CLS del mapa · 5 de noviembre de 2026

- Extendí la captura local a portada, catálogo, previa, comparador y mapa a 390, 768 y 1365 px. Portada, catálogo y previa registraron CLS 0 en los tres tamaños; el comparador, 0,0049 en una captura móvil y 0 en escritorio, sin desbordamiento.
- El mapa llegó a 0,112 de CLS en 768 px porque filtros ocultos y el gráfico SVG aparecían tras cargar los datos. Reservé el espacio responsive de los controles y la proporción 850:540 del gráfico; el menú mantiene una reserva vertical acorde a la anchura.
- Tras el ajuste, el mapa registra CLS 0 a 390, 768 y 1365 px y no amplía el ancho de página. Con JavaScript desactivado, los controles siguen ocultos y el contenido alternativo queda disponible.
- Actualicé las versiones de caché y los generadores `herramientas/experiencia.py` y `herramientas/segunda_edicion.py` para conservar los cambios al regenerar las páginas. Las auditorías volvieron a pasar: 53 páginas y 2.319 enlaces/recursos sin errores; 52 canonicals; 116 imágenes; accesibilidad visual correcta. `node --check` pasó en los scripts modificados.
- Sigue pendiente confirmar la vista pública porque Cloudflare presenta la comprobación de seguridad; no se intentó resolverla ni eludirla. Estas medidas corresponden a Chrome local, no a visitantes ni a PageSpeed en producción.

## Estado final del ajuste del mapa · 5 de noviembre de 2026

- El commit `f10175e` está en `main`. Los workflows de revisión del sitio ([resultado](https://github.com/lineadepase/lineadepase.github.io/actions/runs/41999196181)) y publicación en GitHub Pages ([resultado](https://github.com/lineadepase/lineadepase.github.io/actions/runs/41999196230)) finalizaron correctamente.
- La comprobación pública de https://lineadepase.com/ desde esta sesión responde HTTP 403 por la capa de seguridad. No fue posible comprobar visualmente en producción ni lanzar una medición PageSpeed posterior; la confirmación visual de CLS se limita a Chrome local.

## Reserva del comparador · 5 de noviembre de 2026

- La pasada local anterior dejó un CLS móvil de 0,0049 en el comparador. Su HTML mantiene los filtros con hidden hasta que llega el JSON; al aparecer, podrían empujar contenido. Reservé el mismo espacio de la cuadrícula mientras permanece invisible, mediante CSS condicionado a JavaScript activo, para evitar ese cambio de geometría.
- Actualicé la versión de caché de experiencia.css en las páginas y en herramientas/experiencia.py, de modo que las visitas reciban la regla nueva y se conserve al regenerar las páginas.
- La revisión del sitio y la publicación de GitHub Pages para el commit 65e8b4d terminaron correctamente. La comprobación pública del comparador responde HTTP 403 desde esta sesión. No obtuve una captura de navegador posterior al ajuste; por tanto, 0,0049 sigue siendo la medición anterior y no asigno un CLS nuevo.

## Indexación y coherencia del sitemap · 5 de noviembre de 2026

- robots.txt permite el rastreo y declara el sitemap correcto. La revisión encontró una URL antigua de la previa que apuntaba a un alias con canonical hacia la noticia de la J11.
- Retiré el alias del sitemap y actualicé herramientas/previas.py para que la sincronización no vuelva a añadir URLs de alias. La página canónica de la previa J11 permanece incluida.
- La comprobación final encontró 50 URLs en el sitemap; todas resuelven a un archivo HTML y cada URL coincide con el canonical de su página. La auditoría independiente de canonicals pasó en 52 páginas. Contacto permanece fuera del sitemap por noindex.

## Próximo paquete de pasos

1. Confirmar que el sitemap actualizado se sirve en producción cuando la sesión permita acceder sin HTTP 403.
2. Medir el comparador en navegador a 390, 768 y 1365 px; confirmar su CLS y revisar controles tras la carga.
3. Tras el Zaragoza–Huesca del 7 de noviembre, incorporar el marcador y estadísticas verificadas; revisar después la simulación y coherencia de datos entre páginas.
