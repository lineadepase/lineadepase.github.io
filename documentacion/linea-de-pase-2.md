# Línea de Pase 2.0 — estado de desarrollo

La entrada se conserva en `/datalab-prototipo/`, excluida de indexación. La portada pública y las URLs históricas se mantienen.

## Implementado

- Ocho áreas: DataLab, Museo, Play, Zaragoza, Pro, Studio, Media y pasaporte.
- Simulador de probabilidad y series aleatorias con límites didácticos explícitos.
- Reto de probabilidad con explicación de la respuesta.
- Pasaporte local: áreas exploradas, nota, descarga en texto y borrado. Tolera almacenamiento no disponible y datos corruptos.
- Acceso a análisis, juegos, generadores de láminas, formatos sociales y entregas existentes.
- Resumen del Zaragoza generado desde `datos/zaragoza.json`, con fecha de corte y aviso de cobertura.
- Diseño adaptable a móvil y escritorio, foco visible y respeto de movimiento reducido.

## Regeneración

`python herramientas/linea2.py` reconstruye el prototipo con los datos actuales. Se ejecuta también al actualizar la publicación de jornada. La integración continua comprueba que la salida está sincronizada.

## Verificación realizada

Siete pruebas automáticas: probabilidad, monotonía, simulación en los extremos, reto, persistencia, borrado y recuperación ante almacenamiento inválido o bloqueado. Pasan las auditorías existentes de enlaces, canónicas, imágenes y accesibilidad estática.

## Pendiente para dar la versión por terminada

La revisión visual y las pruebas reales de interacción móvil/escritorio no se han realizado: la política del navegador bloqueó la apertura del archivo local. Las comprobaciones estáticas no sustituyen esas pruebas. Las áreas reutilizan experiencias existentes; las nuevas investigaciones científicas requieren trabajo y validación independientes y no se presentan como modelos terminados.

No se ha publicado ni fusionado main.

## Continuación

Play incorpora tres retos sobre probabilidad, interpretación de xG y tamaño de muestra, con explicación, recuento de aciertos y reinicio. Una respuesta solo cuenta una vez. La tablet no figura entre las superficies controlables de la sesión; la revisión visual continúa pendiente.

## Integración y siguientes ideas

El prototipo se regenera desde la rutina habitual de SEO, conservando su exclusión del índice. El resumen usa el último resultado de liga anterior al corte, aunque el archivo esté desordenado; omite marcadores pendientes y rechaza marcadores inválidos. Hay contenido inicial y avisos para la navegación sin JavaScript.

Propuesta del usuario para una ampliación futura de Play: un trivial de fútbol. Anotado, sin desarrollar todavía.

## Experiencias dentro de las áreas

Museo incorpora dos salas con gráficos existentes, preguntas de observación y explicación desplegable: redes de pases de España y superficie xT de Liga F. Studio permite elegir una pareja de jornadas tomada directamente del selector del archivo visual, y abrir el generador con esa selección. Media integra el vídeo existente de xG, su contexto y una lectura alternativa, sin reproducción automática ni descarga anticipada del vídeo. Pro incorpora una guía de método.

La revisión visual real sigue pendiente; no se ha validado el aspecto en móvil o escritorio.

Validación de esta ampliación: 10 pruebas de interacción y descarga en entorno simulado, 8 pruebas del generador, auditorías de enlaces, canónicas, imágenes y accesibilidad estática superadas. No equivalen a pruebas en un navegador real.
