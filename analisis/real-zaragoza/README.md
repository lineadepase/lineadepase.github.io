# Real Zaragoza 2026/27: seguimiento con datos públicos

Código y datos del seguimiento del Real Zaragoza en Primera Federación (grupo 2). El resultado se publica en [Línea de pase](https://lineadepase.com/proyectos/real-zaragoza/).

## Cómo está organizado

```
real-zaragoza/
├── datos/
│   ├── entrada/   CSV que relleno a mano después de cada partido
│   └── salida/    tablas calculadas por el script (no se tocan a mano)
├── codigo/
│   ├── actualizar.py      script principal: ejecuta todo en orden
│   ├── cargar_datos.py    lectura de los CSV de entrada
│   ├── comprobaciones.py  cruces entre tablas para detectar errores
│   ├── calculos.py        puntos, tramos, minutos, participación en goles…
│   ├── graficos.py        gráficos del informe
│   ├── informe.py         página del informe completo
│   ├── previa.py          previa del próximo partido
│   ├── previa_redes.py    imagen y cifras de la previa para redes
│   ├── previa_portada.py  portada de la previa (imagen de fondo en codigo/recursos/portada_previa.jpg, sin escudos)
│   ├── previa_carrusel.py diapositivas de la previa: rival, jugador, expectativa y cierre
│   ├── tarjeta_dato.py    imagen de «El dato de la jornada» para LinkedIn
│   ├── comprobar.R        repite los cálculos en R y los compara (ejecuta las piezas de R/)
│   └── R/
│       ├── utilidades.R   leer CSV en UTF-8 y comparar una tabla de R con la de Python
│       ├── datos.R        carga entrada y salida y se queda con la liga
│       ├── sede.R         comprobación de puntos, goles y porterías a cero por sede
│       ├── minutos.R      comprobación de minutos por jugador
│       ├── goles.R        comprobación de goles, asistencias y goles desde el banquillo
│       └── resumen.R      resumen que se imprime cuando todo cuadra
├── textos/
│   ├── conclusiones.html  conclusiones del informe, escritas a mano
│   └── dato_jornada.json  texto de la tarjeta de la semana
└── TABLEAU.md             cómo montar el panel en Tableau Public
```

El script escribe también en la web:

- `datos/zaragoza.json`: datos del panel interactivo.
- `proyectos/real-zaragoza/informe-completo.html` y la carpeta `graficos/`.

El marcador de la página del proyecto lee `datos/sofascore.json` (calendario mantenido a mano) y las fichas de `datos/zaragoza.json`. Muestra el último resultado revisado, con goles, tarjetas y estadísticas al pulsar, hasta el martes a las 8:00 si hay partido entre semana o hasta el miércoles a las 8:00 en caso contrario. Después muestra el siguiente encuentro. Los cambios de tarjeta siguen la hora de Madrid y se revisan mientras la página permanece abierta.

La hora programada nunca se usa para afirmar que el partido ha empezado o terminado. El seguimiento en directo se abre en Sofascore. El 12 de octubre de 2026 el módulo incrustado devolvió un error, por lo que no se activa hasta verificar un proveedor operativo. Las fichas revisadas siguen funcionando sin ese módulo. «Dónde verlo» muestra solo los canales incluidos en `tv`; un campo vacío se presenta como emisión pendiente de confirmar.

Las páginas y sus plantillas conservan el selector de tema, los gráficos ampliables, el índice del informe, los resultados táctiles y la firma **Ángel Marqueta Alonso**. Al actualizar otra jornada, se parte siempre de la versión actual del repositorio para no recuperar plantillas anteriores.

## Datos de entrada

| Archivo | Qué contiene |
|---|---|
| `partidos.csv` | Fecha, rival, sede, resultado final y al descanso de cada partido (liga y copa) |
| `goles.csv` | Cada gol: minuto, parte, goleador, asistencia, penalti y propia puerta |
| `alineaciones.csv` | Once inicial de cada partido |
| `cambios.csv` | Minuto, jugador que entra y jugador que sale |
| `tarjetas.csv` | Tarjetas del Zaragoza y minuto cuando se conoce; las expulsiones cierran los minutos jugados |
| `tiros.csv` | Tiros, tiros a puerta y posesión, con aviso si el dato está incompleto |
| `estadisticas.csv` | Estadísticas completas de los partidos que las tienen (incluso por partes) |
| `clasificacion.csv` | Clasificación del grupo tras cada jornada apuntada |
| `proximos.csv` | Próximos partidos |
| `partidos_rivales.csv` | Resultados del próximo rival, para la previa |
| `incidencias.csv` | Diferencias entre fuentes y qué dato me quedo |
| `sofascore.csv` | Estadísticas de cada partido en Sofascore, xG incluido (una fila por métrica) |
| `video/goles_video.csv` | Cada gol de liga apuntado viendo los resúmenes de YouTube: tipo de jugada, carril, último pase, zona de remate… |
| `video/resumenes_youtube.csv` | Los vídeos que he usado para cada jornada |
| `avanzadas_j4_provisional.csv` | xG y otras métricas de un solo partido, de una fuente poco fiable (no se usan) |

Fuentes, por este orden: web oficial del club, FotMob, futboltotal y BeSoccer. Cuando dos fuentes no coinciden lo apunto en `incidencias.csv`. Si un dato no aparece en ninguna fuente fiable, se queda vacío: nunca lo relleno con un cero.

## Tablas para Excel y diccionario de datos

En `datos/tablas/` están las mismas tablas listas para abrir con doble clic en un Excel en español: `datos_real_zaragoza.xlsx` (una hoja por tabla, con una hoja «Diccionario» que explica cada columna) y `csv_excel/` (UTF-8 con BOM, punto y coma y coma decimal, para que las tildes y la ñ salgan bien). El diccionario también está en [`datos/tablas/DICCIONARIO.md`](datos/tablas/DICCIONARIO.md). Todo lo genera `codigo/preparar_tablas.py`; los CSV originales de `datos/entrada` no se tocan.

## Cómo se actualiza

### Previas con imagen y presencia en portada

Cada previa se publica con una ilustración editorial propia y su noticia. Antes de generar una nueva jornada con `codigo/previa.py`, se añade su entrada a `datos/previas.json` (en la raíz de la web): jornada, fecha del partido, título, resumen, página permanente, imagen, dimensiones y texto alternativo. La imagen debe existir; el generador se detiene si falta para evitar publicar una previa sin portada o con la ilustración de otro rival.

`herramientas/previas.py` incorpora la imagen y el texto editorial a la noticia, conserva una URL por jornada y actualiza el bloque de previas de la página principal. La dirección `previa.html` sigue mostrando la jornada más reciente; las noticias anteriores mantienen su propia dirección. El bloque muestra las cuatro previas más recientes. Las previas de Copa se añaden al mismo registro con una página propia, sin campo `jornada`, para mantener separadas las competiciones.

La regeneración de portada y la actualización SEO también sincronizan este bloque. La portada prioriza el partido pendiente más cercano; las etiquetas se actualizan con la fecha de Madrid sin deducir si el encuentro ha comenzado o terminado. El archivo recoge las previas de liga y Copa, y la simulación. `previa.html` comparte la canónica de su noticia permanente.

Para sincronizar páginas ya publicadas: `python herramientas/previas.py`. La actualización SEO termina con `herramientas/calidad_web.py`: elimina metadatos duplicados, conserva la imagen editorial, incorpora dimensiones y genera versiones ligeras de las imágenes grandes sin sustituir los originales. Para comprobar el ciclo de publicación: `python -m unittest discover -s herramientas/pruebas -p 'test_*.py'` y `node herramientas/pruebas/previas.test.cjs`.

1. Añadir el partido nuevo a los CSV de `datos/entrada` (y la clasificación de esa jornada).
2. Ejecutar desde la raíz del repositorio:
   ```
   pip install -r analisis/real-zaragoza/requirements.txt
   python analisis/real-zaragoza/codigo/actualizar.py
   Rscript analisis/real-zaragoza/codigo/comprobar.R
   ```
3. Si alguna comprobación falla, el script para y no cambia nada de la web.
   `actualizar.py` también regenera las pestañas «Jornada a jornada» (una página por partido, `paginas_partidos.py`) y «Último partido», las tablas para Excel (`preparar_tablas.py`) y la publicación visual del partido más reciente. Su paso final reconstruye portada y galería, exporta el marcador SVG a PNG y comprueba que las piezas usan la misma jornada y fecha. Solo añade posesión y tiros cuando la ficha está completa y ambas métricas son válidas. Los tiros a puerta son opcionales y se incluyen si pasan las comprobaciones frente a tiros totales y goles. Si la cobertura principal no está completa, omite y retira el gráfico estadístico. Para ese paso se necesita Chrome o Edge instalado; también se puede indicar con `CHROME_PATH`.
   Para los goles en vídeo y el xG, después de apuntar los goles de la jornada en `video/goles_video.csv` y sus estadísticas en `sofascore.csv`:
   ```
   python analisis/real-zaragoza/codigo/goles_video.py
   ```
4. Revisar `textos/conclusiones.html` y los textos de la página del proyecto.
5. Previa del siguiente partido: añadir los resultados del rival a `partidos_rivales.csv` y ejecutar `python analisis/real-zaragoza/codigo/previa.py <jornada>`. Para redes, `python analisis/real-zaragoza/codigo/previa_redes.py <jornada> --estadio "<estadio>"` crea `datos/salida/previa_redes.png` y `previa_redes.json` con las mismas cifras; después, `python analisis/real-zaragoza/codigo/previa_portada.py` crea la portada `previa_portada.png` (primera imagen del carrusel de Instagram).

Los partidos de copa van en los mismos archivos con su competición; no cuentan para los puntos ni para la clasificación.

El índice `/archivo-visual/` conserva una tarjeta descargable por jornada y una tarjeta estadística solo cuando las métricas pasan las validaciones de cobertura. Resume cada temporada por separado, permite comparar dos jornadas y comparte su selección y filtros mediante el enlace de la página. La comparación se exporta en SVG o PNG. Los nombres incluyen temporada si se acumulan campañas con jornadas repetidas. Al actualizar datos, `herramientas/actualizar_publicacion_jornada.py` regenera esas piezas sin sustituir la tarjeta vigente de portada.

## Límites

- Los minutos no cuentan el descuento: un titular que juega todo el partido suma 90.
- Las asistencias salen de una sola fuente y no están todas.
- No hay datos públicos fiables de eventos con coordenadas, tracking ni presión.
- Los datos de vídeo están apuntados a ojo a partir de resúmenes de pocos segundos. Las posiciones del mapa de remates son estimaciones con un error de varios metros y cada gol lleva su nivel de confianza.

Análisis personal. Sin relación con el Real Zaragoza ni con ninguna competición.
