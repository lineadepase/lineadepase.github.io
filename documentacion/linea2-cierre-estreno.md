# Línea de Pase 2.0: alcance y cierre del primer estreno

Estado del 28 de noviembre de 2026. Rama `desarrollo/linea-de-pase-2`.

## Dónde estamos

Hay un prototipo funcional de ocho áreas en `/datalab-prototipo/`, con catorce accesos directos a experiencias y herramientas. No es todavía la sustitución de la web pública. Se conserva la portada actual y el prototipo lleva `noindex,nofollow`.

La ejecución [46151963572](https://github.com/lineadepase/lineadepase.github.io/actions/runs/46151963572), sobre `29db3ee`, terminó correctamente: **412 comprobaciones** (45 de lógica, 19 de generación y 116 de navegador por motor en Chromium, Firefox y WebKit). Los cuatro tamaños son 1440, 820, 390 y 320 píxeles. Se verifican recorridos, cálculos, descargas reales, notas, rutas y accesibilidad automática. No equivale a una certificación de accesibilidad ni a una prueba de todos los dispositivos físicos.

El inventario inicial registró 62 páginas HTML y 58 URLs en sitemap. Tras separar las áreas, hay 71 páginas HTML: las 62 anteriores más ocho entradas y un inicio de desarrollo. El sitemap público sigue con 58 URLs. Hay siete páginas asignadas a Play, cinco a DataLab, dos a Museo, dos a Studio, tres a Pro, tres a Media, 34 a Zaragoza, cinco transversales y el prototipo. Esta clasificación indica el área principal: un recurso puede enlazarse desde varias áreas sin duplicarlo. El inventario no acredita la vigencia de cada contenido.

## Alcance del estreno

Entran las ocho áreas, los cinco experimentos didácticos, las dos salas del Museo, el trivial de nueve preguntas, los juegos existentes revisados, el seguimiento del Zaragoza, los generadores existentes, los cuadernos y el pasaporte local. El estreno se apoya en contenidos y datos que ya existen; las discrepancias se muestran y los valores ausentes no se completan por inferencia.

Quedan fuera del primer estreno: un xG universal entrenado, la investigación de fortaleza «Los puntos engañan», cuentas, pagos, suscripciones, clasificación multijugador y sincronización en la nube. Los cuatro últimos no son compromisos de desarrollo posteriores: no forman parte del alcance actual. No se exige crear más vídeos, artículos o salas para poder cerrar esta primera versión.

No se añaden nuevas funciones durante el cierre salvo para resolver un fallo, un requisito de accesibilidad o una necesidad de integración.

## Estructura que se implementará en desarrollo

La portada debe orientar y ofrecer los tres recorridos existentes: curiosidad, Zaragoza y creación. Las áreas tendrán entradas claras; la portada dejará de cargar todos sus formularios y experimentos.

| Etiqueta de navegación | Entrada prevista al publicar | Decisión |
| --- | --- | --- |
| DataLab | `/datalab/` | Nueva entrada para experimentos y proyectos; enlaza las investigaciones en sus URLs actuales. |
| Museo | `/museo/` | Nueva entrada para salas y lectura de obras; utiliza los gráficos reales y la galería existente. |
| Play | `/play/` | Nueva entrada para trivial y catálogo de juegos, con instrucciones y retorno. |
| Zaragoza | `/zaragoza/` | Orientación, cobertura y explorador; conserva el seguimiento completo en `/proyectos/real-zaragoza/`. |
| Pro | `/pro/` | Cuaderno, métodos y acceso al perfil y trabajos en `/seleccion/`. No es un servicio de pago. |
| Studio | `/studio/` | Nueva entrada de selección y redacción; los generadores siguen en `/archivo-visual/` y sus rutas existentes. |
| Media | `/media/` | Orientación audiovisual; conserva el catálogo y explicaciones en `/videos/`. |
| Pasaporte | `/pasaporte/` | Nueva entrada para recorrido y nota locales, sin cuenta. Se conserva la clave de almacenamiento. |

Estas rutas están preparadas en una copia candidata independiente, todavía sin publicar. Las entradas de desarrollo continúan dentro de `/datalab-prototipo/`, sin indexación. Se ajusta la propuesta inicial de reutilizar tres entradas para conservar íntegros sus documentos históricos. El prototipo actual se conservará durante la transición para no romper enlaces compartidos.

Las URLs existentes no se renombrarán para que coincidan con las etiquetas del menú. `/archivo/`, `/proyectos/`, `/conceptos/`, `/herramientas/`, `/galeria-visual/`, `/sobre-mi/`, privacidad, previas y fichas mantienen su dirección y su función. El alias de contacto y las excepciones de canonical deben mantenerse.

## Inventario e integraciones que hay que cerrar

| Área | Reutilización prevista | Trabajo pendiente del cierre |
| --- | --- | --- |
| DataLab | xG divulgativo, xT, perfiles de Liga F, fútbol femenino y conceptos | Separar proyectos reales de modelos didácticos; incorporar acceso al proyecto de perfiles, que no está destacado en el prototipo. |
| Museo | Redes de España, superficie xT, galería y archivo visual | Mantener obra, contexto, fuente y metodología; evitar duplicar la biblioteca de descargas. |
| Play | Marcador a ciegas, Partidos espejo, Reloj del marcador, Balance de preguntas, Preguntas del partido, Mapa de lo que cambió y Esquemas del juego | Revisar qué hace realmente cada pieza, añadir entrada e instrucciones coherentes y probar sus recorridos. No presentar todas como juegos competitivos. |
| Zaragoza | Panel, jornadas, previas, evolución, plantilla, grupo, simulación y goles en vídeo | Ordenar accesos, comprobar corte y discrepancias; mantener exportaciones y enlaces a las fuentes. |
| Pro | Selección, proyectos, sobre mí, conceptos y herramientas | Presentar propósito, métodos y resultados demostrables, con acceso al cuaderno de investigación. |
| Studio | Archivo visual, entrega de jornada y pizarrón | Verificar los formatos de descarga y el traslado Zaragoza → redacción; conservar texto alternativo y datos de cobertura. |
| Media | Vídeos, archivo, novedades e intros del autor | Revisar catálogo, subtítulos o alternativa escrita, atribuciones y relación con cada proyecto. |
| Pasaporte | Guardado local, texto, JSON, importación y borrado | Comprobar continuidad al cambiar de página y retorno desde herramientas; no mezclar notas de los otros cuadernos sin una acción explícita. |

Fuentes de datos locales a conservar: `zaragoza.json`, `comparador-grupo2.json`, `previas.json`, `claves-editoriales.json`, `momentos-partido.json`, `entregas-zaragoza.json`, `novedades.json` y `sofascore.json`. No se presupone que todas tengan el mismo corte ni la misma cobertura.

Generadores existentes: `actualizar_exploracion.py`, `actualizar_publicacion_jornada.py`, `actualizar_seo.py`, `previas.py`, `entregas.py`, `experiencia.py`, `segunda_edicion.py` y `exportar_lamina.py`; análisis en `analisis/` y cierre audiovisual en `contenidos/generar_cierre.py`. Su presencia en esta lista no implica que se hayan ejecutado ahora: hay que revisar su función antes de modificar sus salidas.

## Paquetes pendientes y condición de cierre

### A. Alcance, inventario y estructura — completado

- [x] Clasificar las 62 páginas y registrar ruta, título, canonical, indexación y scripts.
- [x] Fijar el contenido del primer estreno y separar investigaciones pendientes.
- [x] Elegir entradas reutilizadas y nuevas, sin renombrar URLs históricas.
- [x] Registrar las auditorías actuales y los límites de la verificación.

### B. Separar las áreas y conectar el recorrido — completado

- [x] Crear entradas de área dentro del prototipo y una portada de orientación.
- [x] Compartir cabecera, navegación y pie sin copiar ocho implementaciones diferentes.
- [x] Cargar cada herramienta solo en su área; los scripts no deben exigir elementos de otras páginas.
- [x] Conservar enlaces compartidos, selección de jornadas y continuidad del pasaporte al navegar.
- [x] Comprobar portada → área → herramienta → retorno, con teclado y en móvil.

Se cierra cuando las ocho áreas tienen una entrada funcional en desarrollo y los recorridos no dependen de la página larga actual. Las rutas finales siguen sin activarse.

### C. Integrar catálogo y presentación — completado

- [x] Completar el catálogo de proyectos, juegos y vídeos con los recursos inventariados.
- [x] Aplicar los ambientes acordados a las entradas y a los puntos de transición; conservar gráficos y datos legibles.
- [x] Revisar instrucciones, fuentes, corte y límites de cada recurso incluido.
- [x] Verificar las descargas que se anuncian: SVG, PNG, WebP, ZIP y textos según la herramienta.
- [x] Revisar la regeneración: las actualizaciones habituales no deben borrar la estructura 2.0.

Se cierra cuando cada recurso del estreno tiene una ubicación, una entrada comprensible y un recorrido probado. No exige nuevas investigaciones.

### D. Datos, SEO y revisión final — completado

- [x] Resolver o etiquetar cada discrepancia relevante; no convertir datos ausentes en ceros.
- [x] Preparar metadatos, sitemap y entradas finales conservando las 58 URLs actuales del mapa, salvo corrección justificada registrada.
- [x] Probar las rutas históricas y sus excepciones de canonical y alias.
- [x] Revisar accesibilidad, teclado, formularios, impresión y rendimiento medido; la estimación de peso no sustituye una medición de red.
- [x] Ampliar la revisión a Firefox y WebKit, y usar dispositivo físico cuando sea accesible; registrar cualquier limitación pendiente.
- [x] Entregar una versión candidata con capturas, pruebas y pendientes clasificados.

Se cierra cuando no quedan fallos que impidan navegar, interpretar datos o descargar los resultados anunciados, y los riesgos restantes están documentados.

### E. Aprobación y publicación — requiere aprobación del usuario

- [ ] Presentar la candidata y obtener aprobación explícita para publicar o fusionar.
- [ ] Preparar respaldo y procedimiento para volver a la versión anterior.
- [ ] Activar las rutas finales y metadatos públicos únicamente dentro del proceso aprobado.
- [ ] Publicar, verificar páginas y descargas principales, y registrar el resultado.

No se solicita aprobación durante A–D para trabajos reversibles dentro de la rama autorizada.

## Evidencia de este paquete

Las auditorías ejecutadas sobre el árbol local informan de 61 páginas con canonical correcto, 58 URLs indexables en sitemap y una 404 sin canonical por diseño. La auditoría de enlaces comprueba 62 páginas, 2.922 enlaces y recursos locales y 141 imágenes, sin incidencias. La auditoría de imágenes no encuentra atributos alternativos ausentes ni páginas por encima de su presupuesto estimado. La auditoría visual estática comprueba nombres accesibles, foco y ciertos controles, pero no sustituye una auditoría manual completa. Su universo incluye fragmentos y por eso cuenta 67 páginas, frente a las 62 del inventario.

El informe no certifica disponibilidad en Internet de cada enlace externo ni actualidad editorial de todas las páginas. No se han descargado de nuevo datos científicos ni ejecutado los análisis pesados para elaborar este inventario. No se ha publicado ni fusionado main.

## Seguimiento y estimación

A, B, C y D están completados. Queda E: revisión de la candidata por el usuario, aprobación y publicación. El avance se informa por condiciones de cierre, no por número de herramientas añadidas o cantidad de pruebas.

La estimación inicial de 5–8 jornadas queda sustituida por el cierre comprobado de A–D. No quedan funciones del estreno pendientes de implementar. La fecha de publicación depende de la revisión y aprobación de la candidata; las estadísticas históricas pendientes continúan identificadas y no bloquean el estreno con su cobertura actual.

Inventario detallado: [tabla de rutas](linea2-inventario.md), [CSV](linea2-inventario.csv) y [JSON](linea2-inventario.json). Regeneración: `python herramientas/inventario_linea2.py`.


## Implementación del paquete B

Entrada nueva: `/datalab-prototipo/inicio/`. Desde allí se accede a `/datalab-prototipo/datalab/`, `museo/`, `play/`, `zaragoza/`, `pro/`, `studio/`, `media/` y `pasaporte/`. Todas siguen sin indexación y comparten cabecera, navegación, pie y contenido con la vista continua. La portada pública y las rutas finales previstas no se han activado.

Los scripts de cada área se cargan por separado. La vista continua conserva sus archivos de compatibilidad, generados a partir de los mismos módulos para evitar dos versiones divergentes. La regeneración comprueba también las páginas separadas y los scripts compuestos.

El pasaporte utiliza la misma clave local y permite continuar entre entradas y vista continua. El borrador de Pro también mantiene su clave. Los borradores temporales de Studio y Museo siguen requiriendo descarga para conservarse; no se guardan automáticamente al navegar.

Zaragoza transmite a Studio dos identificadores de jornadas, sin notas personales. Studio solo acepta una pareja distinta y disponible en su catálogo real. Las fuentes de los textos descargados y los enlaces a generadores resuelven desde la nueva profundidad de las páginas. El índice y los formularios que ya eran nativos siguen navegables sin JavaScript.


## Cierre verificado de B

La ejecución [46128006801](https://github.com/lineadepase/lineadepase.github.io/actions/runs/46128006801), sobre `5e6af25`, terminó correctamente: 45 pruebas de lógica, 13 de generación y 80 de navegador (138 en total). Se probaron inicio y ocho áreas, continuidad del pasaporte y de Pro, compatibilidad con la vista continua, transferencia Zaragoza → Studio, enlaces compartidos, fuentes en descargas y navegación sin JavaScript.

Se revisaron las capturas del nuevo inicio en escritorio y móvil estrecho, los ocho ambientes en escritorio, Studio y Pro en móvil estrecho y Zaragoza en tablet simulada. La primera revisión detectó títulos del directorio móvil demasiado estrechos; se corrigió su disposición y la segunda ejecución incorporó una comprobación de ancho disponible. Las capturas largas desactivan temporalmente la posición fija del menú para evitar superposiciones de la captura; la navegación se comprueba con su comportamiento habitual.

Las auditorías locales verifican 71 páginas, 3.212 enlaces y recursos locales y 153 imágenes sin incidencias, 70 páginas con canonical correcto y las mismas 58 entradas indexables del sitemap. No se ha revisado una tablet física ni completado Firefox y WebKit. No se ha publicado ni fusionado main.


## Implementación del paquete C

El catálogo único `datos/linea2-catalogo.json` reúne 35 recursos existentes. Cada entrada indica qué hacer, su tipo, contexto y límites, y las áreas desde las que se ofrece. Los perfiles de Liga F se incorporan a DataLab. Play distingue siete recursos: reto de marcador, comparador, reloj, esquema y tres lecturas o registros editoriales. Media ofrece las tres piezas audiovisuales existentes más archivo y novedades; no presenta el vídeo de construcción de xG como validación de un nuevo modelo de 2.0.

Los catálogos se generan para la vista continua y las entradas separadas desde el mismo origen. Conservan sus ambientes de área y se pueden leer sin JavaScript. Las instrucciones y notas proceden de revisar las páginas locales, no de una nueva validación científica ni de una comprobación de vigencia normativa.

Cuando se abre una pieza desde el catálogo, el parámetro `ldp_origen` permite mostrar un enlace para volver a su área del prototipo. Solo acepta siete nombres conocidos y construye un destino local; no copia notas ni puntuaciones. Los recursos conservan sus rutas y canonicals. Sin JavaScript, el enlace del catálogo abre el contenido original y el regreso puede hacerse con la navegación del navegador; el retorno contextual añadido requiere JavaScript.

Se ejecutó `actualizar_seo.py` en una copia independiente de los archivos versionados. Finalizó correctamente y las nueve entradas de desarrollo quedaron idénticas byte a byte, incluyendo catálogos e indexación desactivada. No se trasladaron al repositorio las otras salidas regeneradas de esa copia.

La revisión final de D debe comprobar vigencia y discrepancias de datos y reglas, Firefox/WebKit y dispositivos físicos cuando estén disponibles. La reproducción de vídeos de YouTube y la disponibilidad de sus servicios externos no quedan certificadas por las pruebas locales, que bloquean peticiones externas. Las instrucciones nuevas no añaden afirmaciones sobre las reglas del FVS.


## Cierre verificado de C

La ejecución [46129942787](https://github.com/lineadepase/lineadepase.github.io/actions/runs/46129942787), sobre `a6f83e6`, superó 45 pruebas de lógica, 15 de generación y 96 de navegador: 156 en total. También pasaron las cuatro suites auxiliares existentes de ampliación, consentimiento, métricas y previas, y ocho pruebas del paquete C en Chrome local para escritorio y móvil estrecho. Estas ejecuciones adicionales no se suman al total principal.

Se comprobaron los 35 destinos locales, el catálogo de las siete áreas con recursos, interacción y retorno en los siete recursos de Play, los enlaces y atributos de los vídeos y los archivos descargados de Studio. La prueba de exportación inspecciona SVG, firma y dimensiones PNG de 1200 × 630, firma WebP, los cuatro archivos del kit social, las dos diapositivas del carrusel, las dos láminas WebP del mapa y el texto de comparación. No certifica reproducción de YouTube, impresión física ni todos los formatos auxiliares del taller.

La primera prueba de carrusel elegía un botón del formato anterior que había quedado oculto. Se corrigió el selector para pulsar el visible. Otra ejecución detectó que el aviso de cookies interceptaba una descarga en móvil estrecho; la prueba espera la interfaz de consentimiento y rechaza la analítica antes de continuar. No se modificaron los generadores ni el comportamiento de consentimiento para superar esas pruebas.

Se inspeccionaron los catálogos de Play y Media en escritorio y Play y DataLab en móvil estrecho, con contexto desplegado y enlaces completos. Las auditorías de rutas, canonicals, imágenes y accesibilidad estática siguen pasando: 71 páginas, 3.250 enlaces y recursos locales, 153 imágenes y las mismas 58 URLs del sitemap. No se ha publicado ni fusionado main. Sigue pendiente el paquete D.


## Cierre verificado de D

La ejecución [46151963572](https://github.com/lineadepase/lineadepase.github.io/actions/runs/46151963572), sobre `29db3ee`, terminó correctamente: **412 comprobaciones** (45 de lógica, 19 de generación y 116 de navegador por motor en Chromium, Firefox y WebKit). Los cuatro tamaños son 1440, 820, 390 y 320 píxeles. Se verifican recorridos, cálculos, descargas reales, notas, rutas y accesibilidad automática. No equivale a una certificación de accesibilidad ni a una prueba de todos los dispositivos físicos.

La copia independiente conserva las 58 URLs previas y prepara 65 indexables; supera la auditoría de 79 páginas y 3.496 enlaces y recursos locales. El informe [de candidata](linea2-candidata.md) registra fuentes, cortes, ajustes de rutas, correcciones y límites. Se han revisado capturas de escritorio y móvil y la impresión sobre blanco. No hay dispositivo accesible por ADB. La edición pública, main y el sitemap del árbol de desarrollo permanecen sin activar.
