# Línea de Pase 2.0 — estado y mantenimiento

El trabajo está en `desarrollo/linea-de-pase-2`. La entrada es `/datalab-prototipo/`, con `noindex,nofollow`. No se ha sustituido la portada, publicado la web ni fusionado main. Las URLs históricas y su SEO se conservan.

## Experiencias implementadas

| Área | Contenido y comportamiento |
| --- | --- |
| DataLab | Simulador de disparos; distribución binomial exacta; laboratorio de tamaño de muestra e intervalo de Wilson al 95 %. Todos son modelos didácticos con supuestos explícitos. |
| Museo | Dos salas con gráficos existentes, preguntas de observación, ampliación y lectura desplegable: redes de pases de España y superficie xT de Liga F. |
| Play | Tres retos sobre probabilidad, xG y muestras pequeñas, con explicación, recuento y reinicio; acceso a los juegos ya existentes. |
| Zaragoza | Último resultado anterior al corte y explorador de liga con filtros de sede, resultado y cobertura; medias con tamaño de muestra, tabla enlazada a las fichas y CSV de la selección. |
| Pro | Guía del proceso de análisis; acceso a proyectos, dossier, herramientas, conceptos y código. |
| Studio | Selección de jornadas desde las opciones del archivo visual; abre el generador existente con la pareja preparada y ofrece acceso al mapa de temporada. |
| Media | Vídeo existente de xG con subtítulos integrados, lectura alternativa, fuentes y conexión al simulador, sin reproducción automática ni precarga del vídeo. |
| Pasaporte | Áreas exploradas y nota locales; descarga en texto o JSON; importación validada con confirmación explícita de sustitución; borrado con aviso si el navegador lo rechaza. |

La portada del prototipo ofrece tres recorridos: curiosidad, Zaragoza y creación.

## Datos y métodos

El explorador usa los resultados de `datos/zaragoza.json` anteriores o iguales a su fecha de corte. Solo incluye liga. Las métricas de fichas incompletas se excluyen también del JSON incorporado al navegador y del CSV; no se representan como ceros. El CSV conserva corte, cobertura y enlace al análisis de cada jornada. Las medias de tiros y posesión muestran por separado su muestra disponible. Los filtros describen una selección; no demuestran causalidad ni constituyen un modelo predictivo.

La distribución de goles se calcula exactamente por convolución de ensayos Bernoulli independientes. La demostración de incertidumbre usa el intervalo de Wilson bilateral al 95 %, contrastado con la referencia metodológica del [NIST](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm). No estima el talento de futbolistas reales y advierte que los disparos reales tienen dificultad variable.

## Regeneración

Desde la raíz del repositorio:

```
python herramientas/linea2.py
node --test datalab-prototipo/pruebas/*.test.cjs
python -m unittest discover -s herramientas/pruebas -p test_linea2.py
python herramientas/auditar_enlaces.py
python herramientas/auditar_canonicos.py
python herramientas/auditar_imagenes.py
python herramientas/auditar_accesibilidad_visual.py
```

La rutina habitual `actualizar_seo.py` regenera primero la exploración existente y después este prototipo, para que Studio use las opciones actualizadas del archivo visual. La integración continua verifica pruebas, enlaces y salida generada sincronizada.

`linea2_experiencias.py` mantiene el HTML de los laboratorios y el explorador. `linea2-core.js` contiene cálculos y transformaciones sin dependencias; `linea2-experiencias.js` conecta controles y exportaciones. `linea2.js` mantiene retos, Studio y pasaporte.

## Verificación y límites

Se prueban normalización y esperanza de la distribución, límites y simetría de Wilson, filtros, muestras incompletas, selección vacía, exportaciones, recuperación de almacenamiento, importación de pasaporte, corte temporal, seguridad del JSON incorporado y regeneración sin modificar la portada pública. Las pruebas de interfaz usan un entorno simulado; no sustituyen un navegador real.

**Revisión de navegador realizada:** las 24 pruebas de Chromium han pasado en 1440, 820, 390 y 320 px. Se han inspeccionado las capturas de portada y las ocho áreas en estos tamaños, corregido la cabecera estrecha y la ocultación del enlace de salto, y repetido la ejecución con éxito. La tablet física no está accesible; los tamaños móvil/tablet son simulados. La vista previa local de esta sesión sigue sin conexión, pero la revisión se completó con los resultados del entorno de pruebas de GitHub.

Las investigaciones nuevas, como «Los puntos engañan» y un xG universal entrenado, requieren datos, desarrollo y validación independientes; no se presentan como investigaciones terminadas. Las experiencias y generadores existentes mantienen su implementación y sus rutas.

## Ampliaciones anotadas

El usuario propuso un trivial de fútbol para Play. Queda registrado como ampliación futura, todavía sin implementar.

## Continuidad de la visita y enlaces compartibles

Cada área permite marcarse o desmarcarse en el pasaporte, junto con acceso para anotar un descubrimiento y continuar a la siguiente sección. El pasaporte sincroniza botones, casillas y barra de progreso, y propone la primera área pendiente. No se marca automáticamente por hacer scroll.

DataLab y el explorador del Zaragoza preparan enlaces con sus controles o filtros. Al abrirlos se restauran los valores válidos; se ignoran los parámetros desconocidos o fuera de rango. Las notas y el pasaporte no forman parte de los enlaces. Si cambian los controles, el enlace preparado se oculta para evitar copiar una vista desactualizada. Los enlaces se muestran en un campo seleccionable y no se envían a ninguna red social.

Validación de esta ampliación: 31 pruebas de cálculo e interacción en entorno simulado y 10 pruebas del generador; revisión visual real todavía pendiente.

## Revisión de acceso local y adaptación

Se probó una vista previa HTTP limitada a 127.0.0.1, siguiendo la documentación de desarrollo local del navegador. La conexión no quedó accesible desde el navegador de la sesión, incluso al iniciar el servicio con permiso fuera del entorno restringido. El servicio temporal se detuvo. La revisión visual real continúa pendiente.

La revisión de estilos añadió un tamaño de título específico para pantallas estrechas, objetivos de navegación de al menos 44 px, acciones apiladas en móvil, prevención de desbordamientos en tarjetas y una hoja de impresión para consultar tablas y contenidos. Son cambios revisados en código; no se presentan como verificados visualmente.

## Del explorador a Studio

La tabla del Zaragoza permite elegir dos jornadas y abrirlas en el comparador del archivo visual. La identidad se enlaza por número de jornada, fecha y rival, usando el identificador real de temporada del archivo. Si no existe una correspondencia, no se inventa una selección. Solo pueden elegirse dos jornadas; al aplicar filtros se retiran de la pareja las jornadas que dejan de estar visibles, con aviso.

La ampliación pasa 34 pruebas de cálculo/interacción en entorno simulado y 11 del generador. Se comprueban temporadas diferentes con el mismo número de jornada, identificadores inválidos, selección de una tercera jornada y cambios de filtros.

## Revisión de navegador en integración continua

Se ha añadido una batería Playwright para Chromium con cuatro tamaños de pantalla: 1440, 820, 390 y 320 px. Comprueba ausencia de desbordamiento global, carga de imágenes, experimentos por teclado, retos, persistencia/exportación/importación del pasaporte, CSV, filtros, selección de jornadas en el archivo visual y enlaces compartibles. Genera capturas por área e informe; el trabajo no despliega la web. Las dependencias están fijadas y la prueba bloquea peticiones externas. Su ejecución y la inspección de capturas deben completarse antes de declarar resuelta la revisión visual.

## Primera ejecución real de navegador

La ejecución [46036801246](https://github.com/lineadepase/lineadepase.github.io/actions/runs/46036801246) sobre `22b9c70` superó 24 pruebas en Chromium (6 recorridos × 4 tamaños), además de las 45 pruebas previas y la regeneración sincronizada. Se inspeccionaron las capturas de portada en los cuatro tamaños y áreas en escritorio y móvil. Se detectó una cabecera comprimida a 320 px y la aparición del enlace de salto en capturas largas; se ajustaron la distribución de cabecera y la ocultación del salto sin foco. Las capturas individuales desactivan la posición sticky del menú durante la toma para evitar que la barra se dibuje sobre el área completa; la portada conserva la navegación normal. Se ha solicitado una segunda ejecución tras estos ajustes.

## Resultado verificado de la segunda ejecución

La ejecución [46037290703](https://github.com/lineadepase/lineadepase.github.io/actions/runs/46037290703), sobre `4667ada`, terminó correctamente: 45 pruebas de lógica/generación y 24 pruebas de Chromium, con regeneración sincronizada y auditoría de enlaces. Se inspeccionaron las 36 capturas resultantes (portada y ocho áreas en cuatro tamaños), con revisión ampliada de cabecera estrecha, pasaporte, DataLab y Museo. La cabecera ya no fragmenta el enlace de pasaporte y el enlace de salto permanece oculto salvo foco. No se ha desplegado ni fusionado main.

## Dirección visual editorial

A petición del usuario, se sustituye la estética de panel tecnológico oscuro y verde neón por una dirección de revista de fútbol y cuaderno de investigación: papel cálido, tinta oscura, rojo teja, titulares serif, numeración editorial, reglas y composición asimétrica. Las entradas de contenido son columnas abiertas; los experimentos funcionan como hojas de trabajo y las salas del Museo conservan la presencia de los gráficos reales. Se retiran el campo decorativo con brillo y la repetición de tarjetas redondeadas. No se incorporan fotografías de archivo ni gráficos ficticios para decorar. Las funciones y las URLs se mantienen.

## Logo e intros facilitados por el autor

Se incorpora el logotipo original extraído de la intro corta horizontal: futbolista, denominación y texto de especialidad, conservando el fondo original sin reconstrucción generativa. La cabecera usa esta marca y el lema «Del campo al dato». Media ofrece la intro corta de forma opcional y una descarga vertical. Se mantienen intactos los cuatro originales; las versiones web cortas pesan aproximadamente 375 y 388 KB, frente a unos 15 MB por original, y no se precargan ni se reproducen automáticamente. La procedencia y el proceso están registrados en `assets/marca/README.md`.

## Validación de la dirección editorial y marca original

La ejecución [46038983204](https://github.com/lineadepase/lineadepase.github.io/actions/runs/46038983204), sobre `12d1dcd`, superó las 45 pruebas de lógica/generación y las 24 de Chromium. Se revisaron las capturas de la nueva portada con el logo original en escritorio y móvil estrecho, Studio en tablet y Media en móvil, además de DataLab y Museo de la primera ejecución editorial. La paleta mantiene contrastes de 13,35:1 para el texto principal, 5,71:1 para el secundario y 6,30:1 para el texto de los botones. Las versiones cortas de las intros quedan accesibles desde Media sin autoplay.

## Ambientes por área

Se aplica la distribución indicada por el usuario: Museo y contenidos editoriales conservan papel cálido y tipografía de revista; DataLab usa un laboratorio científico de grafito, retícula sutil, lecturas monoespaciadas y controles diferenciados; Zaragoza usa blanco, azul y escudo del club existente; Play se presenta como un programa deportivo con marcador de progreso y área de juego. No indica que exista una emisión en directo. Studio se propone como mesa de edición neutra y Pro como informe técnico claro. Las dos últimas direcciones son propuestas de diseño del asistente.

Las variantes viven en `assets/linea2-areas.css`, limitadas al contenedor de cada área, y mantienen la navegación, el logo y las funciones comunes.

La ejecución [46040079753](https://github.com/lineadepase/lineadepase.github.io/actions/runs/46040079753), sobre `2036592`, superó las 69 pruebas. Se inspeccionaron las capturas de DataLab y Zaragoza en escritorio, Play y Pro en móvil, y Studio en tablet. No se ha publicado ni fusionado main.

## Respuesta de Play y preparación de mapas en Studio

Play marca la respuesta elegida y la correcta con texto y símbolos además del color, conserva un historial de aciertos y preguntas para repasar, y ofrece enlaces de aprendizaje en el resumen. Al avanzar, el foco pasa a la pregunta; al terminar, al resultado. Reiniciar limpia historial y resumen.

Studio añade un formulario de mapa de temporada que toma las temporadas del generador existente y transfiere temporada, formato y tipo WebP mediante una URL GET. El formulario funciona sin JavaScript. Se amplía la prueba real de navegador para verificar los valores recibidos por el taller.

La primera prueba del nuevo mapa encontró que el selector de temporadas del taller se rellena con JavaScript y no contiene opciones estáticas. Se corrigió el generador de Studio para obtener las temporadas de los identificadores de las jornadas cuando ese selector está vacío, y se añadió una prueba de regresión. La ejecución [46071615634](https://github.com/lineadepase/lineadepase.github.io/actions/runs/46071615634), sobre `f6e25cc`, superó 47 pruebas de lógica/generación y 28 de navegador: 75 en total. Se revisaron las capturas de Studio en escritorio y móvil estrecho y Play en escritorio. No se ha publicado ni fusionado main.

## Escenarios de DataLab y cuaderno de Pro

DataLab incorpora el experimento «Mismo xG, distinta historia»: compara número de remates y probabilidad constante por remate en dos escenarios independientes. Muestra esperanza y probabilidad de al menos un gol, diferencias en puntos porcentuales y un reinicio al ejemplo de 1 xG. Se explican los supuestos y no se presenta como una recomendación táctica.

Pro incorpora una ficha de investigación con pregunta, hipótesis, fuentes, método, validación y límites. Permite guardar y recuperar un borrador local de forma explícita, descargarlo en texto y borrarlo. No hay guardado automático ni transmisión externa. Los campos vacíos se exportan como «Pendiente de definir» y el documento se identifica como borrador. Los textos y su longitud se validan al recuperar o exportar.

La ejecución [46072289256](https://github.com/lineadepase/lineadepase.github.io/actions/runs/46072289256), sobre `b5b47cc`, superó 41 pruebas de lógica, 12 de generación y 36 de navegador: 89 en total. Se revisaron las capturas completas de DataLab y Pro en escritorio y móvil estrecho: los escenarios y campos se apilan, los controles permanecen dentro de su área y las acciones de descarga, guardado y borrado resultan accesibles. La revisión usa tamaños simulados de navegador, no una tablet física. No se ha publicado ni fusionado main.

## Trivial temático de Play

El reto inicial se amplía a tres rondas de tres preguntas: intuición y goles esperados, lectura del partido e investigación con criterio. Cada respuesta explica el razonamiento; al cambiar de tema se reinician puntuación, historial y resumen. El resultado enlaza al botón existente para guardar Play en el pasaporte, sin añadir sellos automáticamente. La puntuación no se persiste. Se conservan el bloqueo de respuestas repetidas, el foco al avanzar y los indicadores de acierto con texto y símbolos.

La ejecución [46072832453](https://github.com/lineadepase/lineadepase.github.io/actions/runs/46072832453), sobre `c24a626`, superó 42 pruebas de lógica, 12 de generación y 40 de navegador: 94 en total. Se revisaron las capturas de Play en escritorio y móvil estrecho; el selector, las respuestas y las acciones se mantienen dentro del área. No se ha publicado ni fusionado main.
