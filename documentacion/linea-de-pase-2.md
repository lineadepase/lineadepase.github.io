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

**Pendiente:** revisión visual y pruebas de interacción reales en móvil y escritorio. La política del navegador bloqueó la apertura del archivo local y la tablet no aparece entre las superficies controlables de la sesión. No se ha intentado eludir ese bloqueo.

Las investigaciones nuevas, como «Los puntos engañan» y un xG universal entrenado, requieren datos, desarrollo y validación independientes; no se presentan como investigaciones terminadas. Las experiencias y generadores existentes mantienen su implementación y sus rutas.

## Ampliaciones anotadas

El usuario propuso un trivial de fútbol para Play. Queda registrado como ampliación futura, todavía sin implementar.
