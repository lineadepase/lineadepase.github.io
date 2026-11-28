# Línea de Pase 2.0: revisión de la candidata

Revisión posterior: [nueva identidad y Museo histórico](linea2-revision-identidad.md). Esa revisión sustituye el diseño descrito en este informe base.

Fecha: 28 de noviembre de 2026. Estado: paquete D completado y candidata verificada. No publicada.

## Qué se está revisando

El recorrido completo: inicio → área → experimento, ficha o generador → resultado → descarga o regreso. La web es estática: los cálculos, filtros y notas funcionan en el navegador; no hay una base de datos de cuentas que deba sincronizarse.

La candidata se prepara fuera del repositorio con `python herramientas/linea2_candidata.py --destino CARPETA_VACIA`. El proceso rechaza carpetas ocupadas o situadas dentro del repositorio, copia los archivos versionados, prepara las entradas y ejecuta la rutina habitual de actualización en esa copia. No publica ni fusiona main.

## Estructura preparada

| Entrada | Función |
| --- | --- |
| `/` | Inicio por recorridos y directorio de las áreas. |
| `/datalab/` | Cinco experimentos e investigaciones existentes. |
| `/museo/` | Obras, lectura guiada y cuaderno de visita. |
| `/play/` | Trivial y siete recursos diferenciados por tipo. |
| `/zaragoza/` | Resumen, explorador, cobertura y acceso al seguimiento completo. |
| `/pro/` | Métodos, trabajos y cuaderno de investigación. |
| `/studio/` | Entrada a los generadores y redacción de publicaciones. |
| `/media/` | Vídeo destacado, intros y catálogo audiovisual/editorial. |
| `/pasaporte/` | Recorrido y nota locales; no indexable. |

Se ajusta la propuesta inicial de reutilizar las entradas de Zaragoza, Pro y Media: sus páginas históricas se conservan como recursos completos en `/proyectos/real-zaragoza/`, `/seleccion/` y `/videos/`. Las entradas nuevas sirven de orientación y acceso a herramientas; no sustituyen esos documentos. Así se evita perder paneles, perfil o explicaciones al cambiar la portada.

Las 58 URLs del sitemap anterior se mantienen. La candidata prepara 65 URLs indexables al incorporar siete entradas; el pasaporte conserva `noindex,follow`. El prototipo sigue separado y sin indexación. La rama de desarrollo aún mantiene la portada pública anterior y su sitemap de 58 URLs: estos cambios de publicación solo existen en la copia candidata.

## Datos y fuentes

`herramientas/linea2_datos.py` contrasta los 13 resultados con `partidos.csv` y las métricas completas con `tiros.csv` y, donde están disponibles, con `estadisticas.csv`. No encuentra discrepancias internas. Es una comprobación de procedencia y consistencia local, no una certificación de todas las cifras externas.

- Seguimiento del Zaragoza: corte del **21/11/2026**, jornada 13.
- Comparación del grupo: corte del **18/10/2026**, jornada 8.
- Seis fichas estadísticas completas; pendientes las jornadas 1, 3, 9, 10, 11, 12 y 13.
- Las fichas pendientes no aportan métricas a las medias ni al CSV del explorador. No se completan con ceros.
- Los cortes distintos se muestran ahora antes de comparar. La discrepancia de tiros de J9 mantiene su registro y enlace de revisión.

Se consultaron las fichas oficiales del club de [J4](https://www.realzaragoza.com/partidos/temporada-2026-2027-primera-federacion-4-real-zaragoza-vs-fc-cartagena-3837) y [J13](https://www.realzaragoza.com/partidos/temporada-2026-2027-primera-federacion-13-real-zaragoza-vs-cf-rayo-4022) para contrastar los marcadores. Esa consulta no cambia automáticamente las banderas de cobertura ni el corte del conjunto de datos. Los ceros de campos incompletos en una web de origen no se interpretan como mediciones confirmadas.

La explicación del FVS se ha precisado con el [protocolo FIFA de junio de 2026 difundido por la FPF](https://www.fepafut.com/wp-content/uploads/2026/10/Football-Video-Support_Protocol_JUN26_V2_ES-1.pdf), la [implantación comunicada por la RFEF](https://rfef.es/es/noticias/la-rfef-incorpora-el-sistema-football-video-support-para-el-arbitraje-en-primera) y su [actualización del chequeo de goles](https://rfef.es/es/noticias/actualizacion-en-el-protocolo-football-video-support-en-primara-federacion-y-primera). El texto distingue cuatro categorías e incluye la condición específica de las expulsiones derivadas de una segunda amarilla claramente incorrecta. No generaliza a cualquier amonestación ni confunde el FVS con el VAR.

## Correcciones realizadas

| Problema detectado | Corrección |
| --- | --- |
| Etiquetas de tarjetas sin un rol válido | Se asigna rol de imagen a los símbolos y se corrige también su generador. |
| Ayudas de cifras insertadas directamente en una lista de definiciones | Se alojan en una descripción válida y se conserva su disposición visual. |
| Nombre accesible distinto del texto «Datos PNG/SVG» | Se incluye el texto visible en el nombre accesible de cada enlace. |
| Paneles científicos oscuros al imprimir | Se prepara una presentación de tinta oscura sobre blanco y se abren las explicaciones temporalmente. |
| Actualización de previas dependiente de la portada anterior | La edición 2.0 conserva el inicio por recorridos y continúa sincronizando fichas y calendarios. |
| Auditorías que incluían dependencias locales de pruebas | Se excluyen dependencias e informes del universo de páginas del sitio. |
| Posible pérdida de nuevas entradas al regenerar el sitemap | La edición preparada incorpora sus áreas durante la actualización y evita metadatos duplicados. |

La marca `.linea2-publicada.json` existe únicamente en la copia candidata. Permite verificar el mantenimiento de la edición preparada. No se ha creado esa marca en el repositorio de trabajo ni se ha activado la nueva portada pública.

## Compatibilidad entre navegadores

La primera matriz detectó restauración nativa de notas temporales en Firefox y comprobaciones prematuras de imágenes diferidas en pantallas pequeñas. Se borra únicamente el texto transitorio tras una carga nueva, conservando el historial de navegación y el borrador guardado de Pro. Las pruebas desplazan cada imagen a la vista y esperan su carga.

Las descargas generadas se entregan como archivos binarios y se conserva su enlace durante 60 segundos. Firefox se configura en las pruebas para guardar los tipos de archivo comprobados: su apertura automática de WebP producía una pestaña local en lugar del evento de descarga esperado. Se siguen verificando los bytes y el contenido de cada archivo, sin omitir formatos.

## Resultado completo

La ejecución [46151963572](https://github.com/lineadepase/lineadepase.github.io/actions/runs/46151963572), sobre `29db3ee`, terminó correctamente: **412 comprobaciones** (45 de lógica, 19 de generación y 116 de navegador por motor en Chromium, Firefox y WebKit). Los cuatro tamaños son 1440, 820, 390 y 320 píxeles. Se verifican recorridos, cálculos, descargas reales, notas, rutas y accesibilidad automática. No equivale a una certificación de accesibilidad ni a una prueba de todos los dispositivos físicos.

## Evidencia local

Las pruebas locales de Chrome han pasado en escritorio y móvil estrecho sobre la candidata tras ejecutar la actualización completa. Comprueban metadatos y rutas históricas, navegación de regreso, accesibilidad automática, teclado, impresión y conservación de una nota cuando falla el almacenamiento.

La auditoría de la copia verifica **79 páginas, 65 URLs indexables y 3.496 enlaces y recursos locales**, sin incidencias de rutas o canónicos. Las capturas del inicio y de la impresión de DataLab se han inspeccionado.

La primera carga del inicio recibió **76.317 bytes de cuerpos de respuestas HTTP** en la prueba local, sin respuestas de servicios externos. No incluye cabeceras, no usa una red móvil y no mide Core Web Vitals de usuarios reales. No se presenta como una promesa de tiempo de carga en producción.

## Límites que deben acompañar a la entrega

- La comprobación automática de accesibilidad no equivale a una certificación completa con lectores de pantalla.
- Los tamaños de tablet y móvil son simulados. La comprobación de conexión no encontró un dispositivo disponible por ADB en esta sesión.
- WebKit es un motor de prueba; no equivale a probar todas las versiones de Safari o un iPhone físico.
- Los vídeos externos dependen de YouTube. Las pruebas bloquean peticiones externas y no certifican su reproducción completa.
- Los datos se publican con sus cortes y cobertura, no como información en directo.
- «Los puntos engañan» y el xG universal entrenado siguen fuera del estreno; no se presentan como investigaciones terminadas.

## Paso de publicación, aún pendiente

La verificación ha terminado y se entregan las capturas, los resultados y la copia candidata. La publicación requiere aprobación explícita del usuario. Entonces se preparará el respaldo, se trasladará la edición aprobada a la rama correspondiente y se comprobará el resultado tras publicar. Hasta ese momento no se modifica main ni la web pública.
