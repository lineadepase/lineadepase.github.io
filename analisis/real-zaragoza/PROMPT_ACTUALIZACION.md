# Actualización del Real Zaragoza y análisis de vídeo pendiente

Trabajas sobre el repositorio GitHub `lineadepase/lineadepase.github.io`, mi web «Línea de pase»: https://lineadepase.github.io/.

No uses conectores salvo Google Sheets para el apartado Tableau. No envíes correos, no hagas pagos ni modifiques otros servicios. Se autorizan las herramientas de acceso al repositorio, lectura web, notificación al usuario y entrega de archivos indicadas abajo. No publiques el dato de la jornada ni el texto para LinkedIn.

## 0. Preparación, siempre en este orden

a) Busca `add_repo` mediante ToolSearch. Si existe, añade owner `lineadepase`, repo `lineadepase.github.io`, access `push`, y clona con el comando devuelto. Si no existe, usa `git clone https://github.com/lineadepase/lineadepase.github.io.git`. Si ya hay una copia local de esta tarea, comprueba remoto, rama y cambios antes de reutilizarla; conserva el trabajo pendiente. Ejecuta `git push --dry-run origin main` y registra el resultado. Si falla, continúa con el trabajo y entrega un parche en el punto 8.

b) Desde la raíz ejecuta `pip install -q -r analisis/real-zaragoza/requirements.txt openpyxl --break-system-packages`. Si `which Rscript` no devuelve nada, instala con `apt-get install -y -qq r-base-core`; si falla, ejecuta antes `apt-get update -qq`. Usa `LANG=C.UTF-8` al ejecutar scripts. Si el entorno impide instalar R, registra el error exacto; no declares superada la validación ni publiques sin ella.

c) Lee `analisis/real-zaragoza/README.md`, las instrucciones aplicables del repositorio y los registros de seguimiento que existan. Mantén plantillas, firma y estructura actuales.

d) Carga mediante ToolSearch `PushNotification` y `SendUserFile`. Si una herramienta no existe, registra su ausencia y usa un enlace al archivo para la entrega cuando sea posible; nunca afirmes haber enviado una notificación inexistente.

## 1. Detectar trabajo nuevo y vídeo pendiente

Comprueba si hay partidos oficiales del Real Zaragoza ausentes de `analisis/real-zaragoza/datos/entrada/partidos.csv`: Primera Federación grupo 2, jornadas intersemanales, Copa del Rey u otra competición oficial. Contrasta al menos dos fuentes.

Si no hay partido nuevo, limita el mantenimiento estadístico al marcador del punto 6 (horarios y TV del siguiente partido) y al punto 3b si faltan partidos terminados del grupo, incluidos aplazados. Si cambia algo, ejecuta actualizar.py, valida, haz commit y procede según el punto 8. Si nada cambia y no hay fallos ni vídeo pendiente, termina sin notificación.

Además, comprueba si el último partido tiene un análisis visual realmente terminado siguiendo el punto 7b. La existencia de una ficha estadística, un enlace de YouTube o una fila en resumenes_youtube.csv NO demuestra que el análisis de vídeo esté hecho. Si está terminado, no lo repitas. Si está pendiente, haz únicamente ese trabajo adicional aunque no haya partido nuevo, sin reescribir análisis anteriores. Registra si se termina o por qué queda pendiente.

## 2. Recopilar el partido nuevo

Obtén resultado final y al descanso; goles con minuto, añadido, parte, penalti, propia puerta y asistencia; once inicial; cambios con minuto; tarjetas; tiros, tiros a puerta, posesión y estadísticas completas disponibles.

Prioridad de fuentes: ficha oficial en https://www.realzaragoza.com/partidos, FotMob, futboltotal.futbol y BeSoccer. Si el club no publica el once, busca Sport Aragón u otro medio y contrástalo con las sustituciones. Contrasta al menos dos fuentes. Diferencias, datos ausentes y decisiones se anotan en incidencias.csv; lo desconocido se deja vacío. No conviertas ceros de una ficha incompleta en datos observados.

Lee con WebFetch o la herramienta disponible de lectura web `https://api.sofascore.com/api/v1/event/<id>/statistics`, periodo ALL. Nunca consultes Sofascore desde curl ni Python. Añade las métricas a sofascore.csv con el formato y nombres existentes: Zaragoza en `zaragoza`, rival en `valor_rival`; aciertos/intentos en `_ok` y `_total`. Si no responde, registra la incidencia y sigue sin inventar xG.

NO rellenes `datos/entrada/video/goles_video.csv`: los goles los anoto yo viendo el resumen cuando se me pide. No ejecutes goles_video.py si faltan goles de una jornada y no trates esa falta como un error. En un 0-0 no hay goles que anotar; puede seguir pendiente el análisis visual general.

## 3. Actualizar entradas

Añade filas a los CSV de entrada respetando formato, separador y nombres de jugadores ya usados de la web del club. En liga, partido_id es la jornada: añade clasificación del grupo tras esa jornada y actualiza proximos.csv. En Copa u otra competición, partido_id empieza en 101 y jornada queda vacía.

No cambies esquemas salvo que sea necesario para un dato real. Si añades una columna, documenta su significado en TABLAS de preparar_tablas.py y adapta las comprobaciones afectadas. Las expulsiones deben terminar los minutos del jugador sin inventar sustituciones: usa minuto en tarjetas.csv y las reglas existentes. Una segunda amarilla cuenta como amonestación y causa expulsión, sin tratarla como roja directa.

## 3b. Grupo 2 completo

`datos/entrada/grupo2_partidos.csv` contiene dos filas por partido terminado, una por equipo. Para cada jornada o aplazado pendiente, lee con WebFetch `https://api.sofascore.com/api/v1/unique-tournament/17073/season/97382/events/round/<jornada>` y usa solo status.type `finished`. Lee las estadísticas ALL de cada evento.

Copia exactamente columnas y formato existentes, fecha AAAA-MM-DD y xG con dos decimales. Usa las etiquetas de sede que ya contiene el CSV (no introduzcas sinónimos nuevos), y métricas del rival en *_rival. Posesión y duelos son porcentajes. Si falta una métrica, queda vacía, no a cero. Usa nombres de clasificacion.csv: Gimnàstic, Hércules, Alcorcón, Villarreal B, Sant Andreu, SD Huesca, Real Madrid Castilla, etc.

Comprueba que cada evento aparece dos veces con rivales, sede, goles y métricas cruzados. Compara partidos por equipo con PJ de la clasificación de ese corte y registra discrepancias. Si la fuente falla, conserva el último corte verificable y muéstralo claramente: no presentes el grupo como actualizado a una jornada que no está completa.

## 4. Regenerar y comprobar

Desde la raíz:

```bash
LANG=C.UTF-8 python analisis/real-zaragoza/codigo/actualizar.py
LANG=C.UTF-8 Rscript analisis/real-zaragoza/codigo/comprobar.R
```

Incluye jornadas.html, jornada-N.html, ultimo-partido.html, grupo-2.html, gráficos, tablas de salida, Excel y diccionario regenerados. Si preparar_tablas.py detecta una columna sin descripción, documéntala en TABLAS. Si Python o R fallan, corrige si el error es tuyo. Si no puedes resolverlo, no publiques: entrega el error exacto y el trabajo preparado con su estado de validación.

## 5. Textos

Actualiza `textos/conclusiones.html`, `textos/grupo2.html` y, si han cambiado, los «Tres datos» y la entradilla de `proyectos/real-zaragoza/index.html`. No hace falta editar la portada raíz: sus cifras se actualizan solas.

Comprueba cada cifra contra datos/salida. En grupo2.html contrasta todas las afirmaciones con grupo2_equipos.csv y retira o modifica lo que deje de ser cierto; menciona al próximo rival si encaja. Si hay cortes distintos, indícalos. Estilo natural, en castellano de España, sin exagerar ni opinar sobre el club. Ejecuta actualizar.py otra vez para incorporar los textos y repite la validación necesaria.

## 6. Previa, marcador y Tableau

Previa: añade los resultados de esta temporada del próximo rival de liga a partidos_rivales.csv, mismo formato que Real Murcia; contrasta futbolme y BeSoccer. Si no accedes a esas fuentes, registra cuáles has usado y el contraste pendiente. Ejecuta `LANG=C.UTF-8 python analisis/real-zaragoza/codigo/previa.py <jornada>` y verifica rival, jornada y datos de previa.html. Retira o actualiza cualquier previa caducada destacada en la página del proyecto.

Marcador: lee con WebFetch `https://api.sofascore.com/api/v1/team/2815/events/next/0`. No uses terminal para consultar ese dominio. En datos/sofascore.json conserva el último de partidos.csv y los oficiales pendientes con id, inicio UTC, local, visitante, competición, jornada (null en Copa) y tv. Nombres existentes sin U23/U21; competición «Primera Federación» o «Copa del Rey». Quita anteriores, añade nuevos y actualiza actualizado. Contrasta horas con club o FotMob y priorízalos frente a fechas provisionales de Sofascore. Si Sofascore no responde, conserva el archivo sin cambios y avisa.

TV del siguiente partido: cada canal con su nombre y abierto true/false, contrastado en dos fuentes (futbolhoy.es, club, Aragón Digital, Sport Aragón u otro medio). Si no hay confirmación, lista vacía. No modifiques el código del marcador. Valida con `python -m json.tool datos/sofascore.json`.

Tableau: usa solo el conector Google Sheets, cargado con ToolSearch, para la hoja «Línea de pase · Real Zaragoza 2026/27 (datos para Tableau)», id `1_uRF1U6fPqoXpaG_ZZ0ABXTIAfiFQhSxL3ezbYzRZOY`. Inspecciona metadatos y cabeceras antes de escribir. Sustituye todo el contenido de partidos_liga, goles, minutos_partido, jugadores y clasificacion por sus CSV completos en datos/salida, con cabecera y sin columnas que empiecen por fuente_url. Vacíos realmente vacíos, nunca nan. Conserva nombres de pestañas y columnas. Verifica después contra CSV. Hazlo aunque falle GitHub y registra si el conector no está disponible.

## 7. El dato de la jornada

Solo si hay partido nuevo, elige un dato llamativo verificado contra salida, actualiza textos/dato_jornada.json y ejecuta `LANG=C.UTF-8 python analisis/real-zaragoza/codigo/tarjeta_dato.py`. Revisa visualmente dato_jornada.png; no lo publiques. Prepara el archivo para el punto 10.

## 7b. Análisis del vídeo, solo si no está hecho

Antes de analizar, busca en el repositorio el análisis del partido por partido_id, rival, fecha y jornada. Revisa también seguimiento/jornada-N.md y los registros de vídeo. Considéralo hecho solo si existe un análisis que documenta un vídeo realmente revisado y observaciones con marcas temporales; no basta una plantilla ni estado «pendiente».

Si falta, localiza el partido completo o un resumen oficial (club, RFEF, plataforma o titular autorizado). No eludas accesos de pago ni autenticación. Usa únicamente herramientas permitidas. Conserva URL, título, canal, duración si se conoce, fecha de revisión y alcance (partido completo o resumen). Si no puedes reproducir y observar las imágenes, registra «pendiente» y la causa; solicita el archivo del resumen al usuario. Si lo adjunta, utiliza ese archivo y continúa sin repetir la búsqueda. Un archivo revisado permite marcar completado aunque siga bloqueado el acceso directo a YouTube. Nunca redactes un supuesto análisis visual a partir de estadísticas, crónicas, subtítulos o miniaturas.

El análisis es obligatorio aunque termine 0-0: revisa oportunidades, errores, aciertos defensivos, decisiones con balón y acciones que puedan mejorarse. Prioriza el resumen de YouTube del canal oficial de la Real Federación Española de Fútbol (@RFEFutbol), verificando canal, partido y temporada. No necesitas goles para realizar este trabajo.

Cuando puedas verlo, revisa el vídeo y prepara un análisis en castellano natural con el estilo de los anteriores. Identifica salida de balón, progresión y ataques, defensa organizada y presión observable, transiciones, balón parado, ocasiones relevantes, cambios y efecto visible de la inferioridad numérica si existe. Incluye solo aspectos observables. En cada secuencia indica tiempo del vídeo y minuto de partido cuando se vea; no confundirlos. Describe qué ocurre, qué permite interpretar y qué no se puede asegurar. Distingue observación de hipótesis y contrasta el contexto con las estadísticas verificadas. No inventes posiciones exactas, PPDA, tracking ni patrones recurrentes desde una sola jugada.

Si es un resumen, titúlalo «Análisis de las secuencias del resumen» y limita las conclusiones a las acciones seleccionadas; no atribuyas al partido completo frecuencias o conductas que no has visto. No incrustes ni redistribuyas imágenes sin comprobar el permiso; se puede enlazar la fuente y citar tiempos.

Guarda el análisis siguiendo la estructura existente; si no hay ninguna, usa `analisis/real-zaragoza/textos/video/jornada-N.md` y un registro JSON contiguo con partido_id, jornada, rival, fecha, estado (`pendiente` o `completado`), fuente_url, alcance, fecha_revision y archivo_analisis. Marca completado solo tras observar y documentar las secuencias. Si ya existía un análisis completo, consérvalo y evita duplicarlo. Enlázalo desde la ficha del partido si la estructura existente lo permite, conservando estilos y navegación.

No modifiques goles_video.csv. Si faltan anotaciones manuales de goles, recuérdamelo; si fue 0-0, aclara que no hay goles que anotar. Haber terminado el análisis general no significa que la codificación manual de los goles esté terminada.

## 8. Revisión, commit y entrega alternativa

Revisa git diff completo. Conserva las versiones ?v= de estilo.css, real-zaragoza.css y mejoras.js en todos los HTML y en sus plantillas para que la regeneración no las vuelva a alterar. Evita cambios de fin de línea ajenos al trabajo. Comprueba que no se han tocado servicios o archivos fuera de alcance.

Commit con mensaje corto en castellano, por ejemplo «Jornada 8: Real Murcia 0-0 Real Zaragoza», autor `Ángel G. Marqueta Alonso <72544138+AngelMarqueta@users.noreply.github.com>`:

```bash
git -c user.name='Ángel G. Marqueta Alonso' -c user.email='72544138+AngelMarqueta@users.noreply.github.com' -c commit.gpgsign=false commit
```

Sin coautorías ni referencias a herramientas de IA en commits, código o textos. Si las validaciones pasan y la subida funciona: `git pull --rebase origin main` y `git push origin main`. Resuelve conflictos sin perder cambios remotos.

Si falla la subida, genera `git format-patch origin/main -o <carpeta temporal>`, envíalo con SendUserFile y explica que se aplica con `git am <archivo>.patch` desde la raíz. Incluye el error exacto. Si falta validación, etiqueta el parche como pendiente de validar antes de publicar. Salta el punto 9.

## 9. Verificación pública solo tras subir

Espera dos minutos, sin bloquear la comunicación más de un minuto seguido. Abre https://lineadepase.github.io/proyectos/real-zaragoza/, verifica nueva jornada y marcador. Abre ultimo-partido.html y grupo-2.html; deben mostrar el partido y corte realmente incorporados. Si el grupo no pudo actualizarse, no debe atribuirse un corte nuevo. Comprueba también el enlace al análisis visual si se añadió. No afirmes que se ve actualizado sin haberlo comprobado.

## 10. Entrega

Si hubo partido nuevo, se terminó un análisis de vídeo pendiente o falló algún paso (GitHub, scripts, Sofascore, Sheets o vídeo), usa PushNotification. Resumen máximo cinco líneas: resultado, dato destacado, cambio respecto a jornada anterior y pendientes. Recuerda los goles manuales en vídeo solo cuando falten goles; en un 0-0 no inventes esa tarea.

Si hubo partido nuevo, entrega dato_jornada.png con SendUserFile y un texto corto para LinkedIn, natural, sin exagerar ni opinar sobre el club. No lo publiques. Entrega o enlaza el análisis visual si se completó; si no, explica que sigue pendiente y qué falta. Nunca presentes el conjunto como terminado si quedan bloqueos.

Como último paso de esta ejecución, revisa este prompt para conservar las reglas aprendidas y la condición de no repetir un análisis visual ya completado. Entrega su versión completa reutilizable.
