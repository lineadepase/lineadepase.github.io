# Línea de pase

Análisis de datos en fútbol con fuentes públicas: preguntas concretas, código en Python y R, comprobaciones automáticas y límites explicados. Es la web de proyectos de Ángel Marqueta Alonso, estudiante del Máster en Big Data Deportivo.

Web: https://lineadepase.com/

## Proyectos

| Proyecto | Pregunta | Técnicas | Código |
| --- | --- | --- | --- |
| [El peligro empieza antes del último pase](https://lineadepase.com/proyectos/liga-f-xt/) | ¿Qué jugadoras de la Liga F 2023/24 acercan el balón a las zonas de gol con pases y conducciones? | Modelo propio de amenaza esperada (xT), validación fuera de muestra por grupos de partidos, intervalos por remuestreo, pruebas con soluciones conocidas | [analisis/liga-f-xt](analisis/liga-f-xt/README.md) |
| [Real Zaragoza 2026/27, jornada a jornada](https://lineadepase.com/proyectos/real-zaragoza/) | ¿Cómo evoluciona el equipo y qué explica sus resultados? | Recogida y contraste de fuentes, tablas reproducibles, comprobaciones en R, panel web, comparador del grupo y datos para Tableau | [analisis/real-zaragoza](analisis/real-zaragoza/README.md) |
| [Fútbol femenino: dónde empezar a ampliar la base](https://lineadepase.com/proyectos/futbol-femenino/) | ¿En qué comunidades tendría más sentido un programa de iniciación? | Tasas por población con datos del CSD y del INE, criterios de selección explícitos, mapa | [analisis/futbol-femenino](analisis/futbol-femenino/README.md) |
| [xG, sin líos](https://lineadepase.com/proyectos/xg/) | ¿Qué miden los goles esperados y cómo se interpretan? | Divulgación: vídeo subtitulado y explicación escrita | — |

## Cómo reproducir los análisis

Cada carpeta de `analisis/` tiene su `README.md`, su `requirements.txt` y sus pruebas. Desde la raíz del repositorio:

```
# Liga F 2023/24 (xT). La primera ejecución descarga unos 600 MB de StatsBomb Open Data
pip install -r analisis/liga-f-xt/requirements.txt
python analisis/liga-f-xt/codigo/ejecutar.py --cache <carpeta para los datos>
python -m pytest analisis/liga-f-xt/pruebas

# Real Zaragoza 2026/27
pip install -r analisis/real-zaragoza/requirements.txt
python analisis/real-zaragoza/codigo/actualizar.py
Rscript analisis/real-zaragoza/codigo/comprobar.R

# Fútbol femenino
pip install -r analisis/futbol-femenino/requirements.txt
python analisis/futbol-femenino/codigo/analisis.py
```

Los datos de StatsBomb no se redistribuyen, como pide su acuerdo de uso: el código los descarga en una carpeta local.

## Forma de trabajo

- Datos públicos, con la fuente y la fecha de corte en cada análisis.
- Contraste de al menos dos fuentes en el seguimiento del Real Zaragoza; las discrepancias quedan registradas.
- Cada cifra de los textos sale de los archivos de salida, no se escribe a mano.
- Cada estudio explica lo que sus cifras no dicen.

Análisis personales hechos con datos públicos. Sin relación con ningún club ni competición.

# Mantenimiento de la web

## Estructura

- `index.html`: portada.
- `proyectos/index.html`, `videos/index.html` y `sobre-mi/index.html` (con el contacto): una página por sección, con el mismo menú y pie que la portada. `contacto/index.html` solo redirige a Sobre mí.
- `proyectos/`: además de la página de la sección, una carpeta por proyecto.
- `datos/zaragoza.json`: datos que lee el panel del Zaragoza. Lo genera el script de `analisis/real-zaragoza`.
- `assets/estilo.css`: estilos comunes.
- `analisis/`: código y datos de cada análisis. Ver [analisis/real-zaragoza](analisis/real-zaragoza/README.md) y [analisis/futbol-femenino](analisis/futbol-femenino/README.md).

## Navegación del seguimiento

Resumen y previa dan entrada al contenido. Evolución reúne los gráficos del equipo; Plantilla, los minutos y la participación; Jornadas, las fichas; Primera Federación · Grupo 2, el contexto de la competición. El informe completo queda como consulta detallada.

Las guías de los gráficos viven en `analisis/real-zaragoza/textos/guias_graficos.json`. `presentacion_web.py` las incorpora al regenerar páginas. Las lecturas de las previas se guardan por jornada en `textos/previa_jN.json` y deben revisarse antes de publicar una nueva. La tarjeta destacada de inicio y resumen contiene la fecha del encuentro y pasa a identificar el análisis como previo cuando llega esa hora.

## Ciclo de las previas

`datos/previas.json` es el registro de fechas, horas y enlaces de cada previa. `python herramientas/previas.py` actualiza portada, ficha, sitemap y una invitación `.ics` por encuentro, usando `Europe/Madrid`; el estado visible pasa de próxima cita a partido disputado con la hora local. Al terminar un partido y publicar su análisis, añade `postpartido_url` a su ficha solo después de comprobar que la página existe. El generador enlaza entonces previa y análisis en la portada y en la previa; la previa se conserva como pieza anterior al partido. Ejecuta después `python herramientas/actualizar_seo.py` y revisa los enlaces antes de publicar.

## Dominio, Google y enlaces compartidos

GitHub Pages publica con `CNAME` apuntando a `lineadepase.com`; los enlaces al repositorio de código siguen usando GitHub. Tras generar o editar páginas, ejecuta `python herramientas/actualizar_seo.py` (requiere Pillow). Conserva el diseño y el contenido editorial; actualiza direcciones canónicas, Open Graph, tarjetas de X/Twitter, datos estructurados de la portada, `robots.txt`, `sitemap.xml` y las imágenes de 1200 × 630 en `assets/compartir/`.

El mapa incluye las páginas públicas principales; omite los fragmentos de `analisis/` y las redirecciones como `contacto/`. Los títulos y descripciones salen de cada HTML, para no duplicar textos de jornadas en la herramienta. Cuando cambie un título o se añada una página, vuelve a ejecutarla antes de publicar.

## Archivo y conceptos

`python herramientas/actualizar_seo.py` ejecuta primero `actualizar_exploracion.py`: reconstruye el archivo a partir de las tarjetas de jornadas y los proyectos publicados, genera la guía de conceptos e incorpora la navegación y las lecturas relacionadas. Ejecutarlo después de actualizar las jornadas conserva estas mejoras. El archivo funciona sin JavaScript; al activarlo añade búsqueda sin distinguir tildes, filtros combinables y recuento de resultados. Los textos de la guía y sus fuentes se mantienen en `herramientas/actualizar_exploracion.py`.

La página `/archivo-visual/` guarda un gráfico por jornada y, cuando la ficha está completa, otro con las métricas validadas. Incluye filtros, resúmenes separados por temporada, insignias de cobertura y comparación compartible de dos marcadores; el enlace conserva temporada, rival y jornadas. Las tarjetas se descargan en SVG, PNG o WebP, en formato apaisado (1200×630), cuadrado (1080×1080), vertical (1080×1350) o historias (1080×1920, con zonas libres arriba y abajo). Se puede ocultar el pie de competición y resultados, quitar la cabecera y mostrar u ocultar la marca. El modo carrusel prepara dos diapositivas cuadradas independientes dentro de un ZIP, una por partido; permite añadir una frase breve y editable a la primera, con vista previa, o dejarla vacía. Cinco presets visuales ajustan estas opciones, incluidos formatos sociales compactos que conservan el marcador y la marca; se pueden guardar hasta seis presets personales en el navegador. Hay tres paletas de color y un indicador calcula el contraste mínimo del texto para avisar si baja del nivel recomendado. Una fila de miniaturas SVG permite elegir formato antes de descargar o copiar, con vistas limitadas en pantalla. Incluye un encuadre equilibrado o con el marcador destacado y tres niveles de densidad. En historias, la guía de zonas muestra el espacio que puede cubrir la interfaz y no se incorpora a la descarga; la composición conserva sus medidas de 1080×1920. Incluye dos vistas para comparar encuadre y densidad sin alterar la descarga, un kit ZIP con versiones cuadrada, vertical e historias en SVG, PNG o WebP, y texto alternativo editable. El kit adjunta ese texto en un archivo .txt y cada SVG lo incorpora en su descripción accesible. El navegador recuerda las preferencias visuales y una pareja de jornadas favorita en el dispositivo local; ambas opciones se pueden restablecer o eliminar desde la página. La hoja de contacto presenta las cinco plantillas con miniaturas ligeras que se pueden aplicar con un clic. El póster «Mapa de la temporada» muestra resultados, sede y balance casa/fuera con etiquetas explícitas de victoria, empate o derrota. Incluye vista previa ampliada y texto alternativo editable; los formatos cuadrado, vertical o historias se descargan como WebP (predeterminado), PNG o SVG. Cuando una campaña supera la cantidad legible por lámina, el póster se divide por orden de jornada y se descarga en un ZIP numerado. Omite métricas sin ficha validada. El mapa permite acotar los marcadores por rival y fechas; la forma de los cinco resultados más recientes y su racha se calculan sobre la temporada completa. El carrusel de temporada descarga tres láminas —balance global, casa y fuera— en el formato y tamaño seleccionados; para historias reserva 260 px arriba y abajo. La forma reciente del Zaragoza puede compararse con el rival seleccionado mediante los últimos marcadores válidos del grupo; al regenerar las páginas, la muestra incluida en el archivo se actualiza y el verificador comprueba su coherencia. La cantidad disponible se indica en pantalla. El mapa permite copiar enlaces con temporada, rival, fechas y formato, y guardar hasta seis selecciones con nombre en el almacenamiento local del navegador; se pueden aplicar, copiar, fijar, ordenar o borrar. Las selecciones se exportan en un ZIP ligero que contiene el JSON y un LEEME breve con los pasos de importación; se puede importar el ZIP directamente o elegir el JSON que contiene. Un QR SVG del enlace actual se genera en el navegador y no transmite la URL a un servicio externo; admite un pie opcional, descarga SVG con ancho de pantalla o de impresión (40 o 60 mm), permite elegir verde de marca (contraste 6,34:1) o tinta oscura y copia la imagen PNG al portapapeles cuando el navegador lo permite. La tabla de pesos muestra el tamaño calculado en el navegador para cada formato y la previsión del ZIP social actual. Se puede copiar la tarjeta actual como PNG al portapapeles cuando el navegador lo permite. Las métricas solo aparecen al seleccionar dos fichas completas. Los nombres de archivo e identificadores incorporan la temporada cuando se mezclan varias campañas, aunque coincidan los números de jornada. `python herramientas/actualizar_publicacion_jornada.py` ejecuta primero `actualizar_seo.py`, que regenera el archivo visual y su forma comparada a partir del último conjunto validado del grupo; después reconstruye los SVG, genera PNG de 1200×630 con metadatos y comprueba que el índice, los marcadores y las cifras coinciden con `datos/zaragoza.json` y los resultados usados para la forma rival. Los PNG del archivo se mantienen por debajo de 100 KB; los partidos sin cobertura suficiente conservan su marcador, pero no muestran gráficos estadísticos.

`python analisis/real-zaragoza/codigo/actualizar.py` ejecuta al final `herramientas/actualizar_publicacion_jornada.py`: regenera las páginas y la galería, exporta el SVG del último resultado a PNG y comprueba que portada, galería y gráfico usan la misma jornada y fecha. Si la ficha está completa y contiene posesión y tiros válidos, también genera el gráfico estadístico y su miniatura. Añade tiros a puerta solo si la ficha los da para ambos equipos, son enteros, no superan los tiros totales y alcanzan los goles marcados. Si la cobertura principal no está completa, omite el gráfico y retira exportaciones estadísticas anteriores. Para sincronizar a mano un JSON ya actualizado, ejecuta `python herramientas/actualizar_publicacion_jornada.py`. La exportación a PNG necesita Chrome o Edge instalado; `CHROME_PATH` permite indicar otra ubicación.

La misma generación integra `herramientas/experiencia.py`: mantiene las tres claves de los análisis, la selección de trabajos y el comparador. Este último deriva sus datos de `grupo2_partidos.csv`; no descarga cifras de otras webs. Conserva valores ausentes y muestra la cobertura por indicador. El filtro de fuente afecta solo a xG y utiliza Sofascore por defecto. Al publicar una nueva jornada, revisar las lecturas editoriales y los casos profesionales además de regenerar los datos.

`datos/novedades.json` es un registro editorial: añadir una entrada real con fecha, tipo (`Publicación`, `Actualización` o `Corrección`), título, texto y URL relativa a la raíz. No cambiar fechas antiguas para aparentar novedades. Las tres entradas más recientes aparecen en portada.

`experiencia.js` incorpora el menú móvil y las descargas de gráficos. Los PNG se componen en el navegador e incluyen título, periodo, fuente y marca; los gráficos interactivos conservan la sede seleccionada, sus leyendas y el estado visible. No envían los datos a servicios externos. Sin JavaScript la navegación permanece visible y las páginas de análisis siguen siendo legibles.

El archivo agrupa los análisis en carpetas desplegables por sección. La búsqueda cruza todas las carpetas, abre las coincidencias y oculta los grupos vacíos; al limpiar recupera la vista de carpetas. Los conceptos y su índice se ordenan alfabéticamente por el término visible y se presentan en dos columnas, o una en móvil. Los vídeos de explicación y los resúmenes de partidos comparten un ancho máximo de 640 píxeles, con reproducción a pantalla completa disponible. La ficha de la investigación de xT se mantiene junto a las otras dos en el catálogo.

La comprobación de visitantes se gestiona en Cloudflare, no en el código. Mantén el acceso de los buscadores reconocidos, `robots.txt`, `sitemap.xml`, las tarjetas sociales y la ruta de renovación de certificados. El acceso al repositorio y las publicaciones desde GitHub son independientes del control de visitantes.

## Portada, comparación y materiales profesionales

`herramientas/segunda_edicion.py` mantiene la portada editorial y el mapa interactivo de los veinte equipos (`mapa-grupo/`). La portada destaca el último encuentro, las herramientas y la selección profesional; el gráfico de minutos queda desplegable. Las lecturas revisadas de cada jornada se mantienen en `datos/claves-editoriales.json`, junto a la base factual usada para redactarlas.

`assets/metricas-grupo.js` comparte los cálculos entre mapa y comparador. El modo por partido pondera la referencia con todos los registros disponibles; en totales se calcula la media por equipo. La posesión conserva siempre su porcentaje medio. El periodo reciente abarca las cinco últimas jornadas del corte. Los enlaces conservan los filtros y los PNG incluyen muestra, periodo y fuente. Ejecuta `node herramientas/pruebas/metricas-grupo.test.cjs` para comprobar muestras desiguales, filtros de fuente, ausencia de datos y medias.

La selección incorpora un perfil breve en inglés. `assets/documentos/` contiene el dossier de cuatro páginas y el CV público de una página, revisados el 21 de octubre de 2026. Son documentos editoriales: requieren revisión al cambiar proyectos, formación o trayectoria. El CV público utiliza la web y LinkedIn como contacto y resume experiencia documentada, sin incluir dirección particular ni teléfono.

## Archivo visual: transferencias y QR de impresión

El mapa admite importar paquetes ZIP con compresión Store o Deflate, incluido el descriptor de datos habitual, mediante el directorio central del archivo. La lectura se hace en el navegador y limita el tamaño del archivo y de la entrada JSON. El QR informa del contraste sobre blanco y conserva una zona libre de cuatro módulos. La vista de impresión muestra el QR del enlace activo en una maqueta A4; la hoja PDF añade una jerarquía editorial y dos códigos vectoriales de 60 y 40 mm. Para generar el PDF se confirma que se imprimirá al 100 % o a tamaño real. Los errores de ZIP o JSON se explican con mensajes breves.

## Herramientas y entregas de jornada

`herramientas/index.html` reúne comparador y mapa con ejemplos de preguntas que abren los filtros adecuados. La entrada Herramientas aparece en el menú principal; Novedades conserva sus enlaces desde la portada y el pie. El glosario incorpora xT con un ejemplo numérico ilustrativo y referencia al método original.

`herramientas/entregas.py` mantiene `tras-la-jornada/index.html`, destacada desde la portada. La generación del gráfico necesita Matplotlib además de Pillow. Antes de publicar otra entrega se revisan los datos y las claves del partido y se incorpora su pregunta en `datos/entregas-zaragoza.json`. Si falta la pregunta o la lectura de la última jornada, la página indica que está pendiente de revisión; no presenta la entrega anterior como actual. Los xG del gráfico proceden de la fila documentada de Sofascore del Zaragoza; una fuente distinta exige revisión.

La entrega incluye una imagen PNG propia y texto en tercera persona para copiar. El selector de canal añade parámetros UTM al enlace del análisis; no publica ni envía mensajes. Los parámetros preparan la identificación de procedencia en una herramienta de analítica compatible: Search Console mide la búsqueda de Google, no el conjunto de visitas ni los accesos desde redes. Los datos privados de Search Console no se incorporan a la web pública.

## Fotografías

Las fotografías de los artículos usan `figure.figura.foto` (se conserva también `foto-cabecera`): contenedor de hasta 384 px e imagen de hasta 320 px de alto, sin recortes adicionales. La ampliación se identifica como «Ampliar imagen» y no recibe la descarga de gráficos. Los retratos de firma conservan su tamaño discreto. Los pies incluyen solo identificación y créditos: autor, licencia enlazada, procedencia y modificaciones relevantes, sin dimensiones en píxeles. `analisis/comun/pagina.py` mantiene este formato al regenerar investigaciones; el campo `pie` permite separar el crédito breve de la descripción accesible completa.

Las fotos ya aprobadas también dan entrada a los artículos desde la portada. `herramientas/segunda_edicion.py` mantiene esas entradas y sus créditos; `assets/fotografia-editorial.css` organiza la portada y los encabezados con imagen. La clase `apertura-con-foto` une el título y la fotografía en escritorio y los apila en móvil, conservando el tamaño discreto y «Ampliar imagen» en los artículos.

## Google Analytics y consentimiento

Analytics (`G-N6J2L7P4LP`) solo se carga tras aceptar la analítica. `assets/consentimiento.js` implementa el modo básico: antes de aceptar no se descarga gtag.js ni se envían eventos; publicidad denegada. La elección se conserva 180 días y puede cambiarse desde el pie. Al revocar se desactiva la medición, se borran las cookies de Analytics accesibles y se recarga la página. Sin JavaScript no se carga Analytics.

`herramientas/google_analytics.py` integra el cargador local, estilos y enlaces del pie al ejecutar `python herramientas/actualizar_seo.py`, sin duplicados. Las páginas de redirección y los fragmentos de análisis quedan excluidos. No añadir fragmentos de gtag directos a páginas o plantillas. Antes de publicar se comprueban: primera visita, rechazo, aceptación, persistencia, retirada y sincronización entre pestañas. Cloudflare, vídeos y fuentes externos son independientes de esta elección.

La ampliación de gráficos se comprueba con `node herramientas/pruebas/ampliacion.test.cjs`: conserva el `viewBox` de los SVG responsivos y las dimensiones de los gráficos antiguos, permite aumentar el zoom y evita presentar puntos sin acción como botones en la copia ampliada.
