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
