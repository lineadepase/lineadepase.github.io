# Línea de pase

Análisis de datos en fútbol. Web personal de proyectos de analítica deportiva de Ángel Marqueta Alonso.

Web: https://lineadepase.com/

## Proyectos

- **Real Zaragoza 2026/27**: seguimiento semanal con datos públicos (resultados, goles, tiros, minutos y clasificación) y panel interactivo.
- **Fútbol femenino en datos**: licencias federativas (CSD) y población (INE) para decidir dónde empezar un programa de iniciación.

- **xG, sin líos**: vídeo subtitulado, explicación escrita y límites de los goles esperados.

## Estructura

- `index.html`: portada.
- `proyectos/index.html`, `videos/index.html` y `sobre-mi/index.html` (con el contacto): una página por sección, con el mismo menú y pie que la portada. `contacto/index.html` solo redirige a Sobre mí.
- `proyectos/`: además de la página de la sección, una carpeta por proyecto.
- `datos/zaragoza.json`: datos que lee el panel del Zaragoza. Lo genera el script de `analisis/real-zaragoza`.
- `assets/estilo.css`: estilos comunes.
- `analisis/`: código y datos de cada análisis. Ver [analisis/real-zaragoza](analisis/real-zaragoza/README.md) y [analisis/futbol-femenino](analisis/futbol-femenino/README.md).

Análisis personales hechos con datos públicos. Sin relación con ningún club ni competición.

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
