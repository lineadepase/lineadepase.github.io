# Jornada 8 · Real Murcia 0-0 Real Zaragoza

Actualización preparada el 19 de octubre de 2026. No publicada.

## Datos y comprobaciones

- Resultado final y al descanso: 0-0. Once, cinco sustituciones y tarjetas incorporados.
- Clasificación: segundo, 17 puntos; cinco victorias, dos empates y una derrota. 16 goles a favor y 10 en contra. Primera igualada sin goles; cuarta portería a cero.
- BeSoccer publica 9 tiros por equipo y 3-1 a puerta para el Zaragoza. Se han incorporado las estadísticas disponibles, también por partes. El club coincide en tiros y tiros a puerta; discrepa en posesión (50 % frente a 49 %). Sus ceros aparentes no se han trasladado.
- Ademo: primera amarilla 45, segunda amarilla 82. Se añade minuto a tarjetas.csv y se calcula la salida sin sustitución en Python y R. Python comprueba 82 minutos para Ademo y 982 para el equipo. Se comprueban también los casos de sustitución de un suplente y expulsión de un suplente.
- actualizar.py y previa.py 9 terminan correctamente. Diccionario y Excel regenerados. JSON del marcador válido y sin cambios, conforme a la regla ante el fallo de Sofascore.
- Google Sheets: las cinco tablas completas sustituidas y verificadas con lecturas posteriores; cabeceras conservadas, sin columnas fuente_url ni textos nan.

## Bloqueos y pendientes

1. Subida: `fatal: could not read Username for 'https://github.com': No such device or address`. No existe add_repo/ToolSearch en esta sesión. Se entrega un parche del commit local; no es una publicación validada.
2. R: `Rscript: command not found`. La instalación estándar no encuentra candidato; apt-get update falla por setgroups. La actualización con usuario de descarga root termina, pero la instalación posterior no se completa y se cancela. Es obligatorio ejecutar `LANG=C.UTF-8 Rscript analisis/real-zaragoza/codigo/comprobar.R` antes de publicar.
3. Sofascore no accesible mediante lectura web en statistics, events/round/8 ni team/2815/events/next/0. No hay xG nuevo ni diez partidos de J8 del grupo. Cada equipo conserva siete partidos avanzados frente a ocho en la clasificación. Grupo 2 muestra explícitamente corte J7. Calendario intacto por instrucción.
4. Previa Europa: resultados de Goal contrastados J1-J7 con los registros Sofascore ya existentes y balance completo con clasificación oficial. Sigue pendiente el contraste solicitado con futbolme y BeSoccer. No se presenta como realizado.
5. El enlace de vídeo de BeSoccer es https://www.youtube.com/watch?v=Eq-htl0RmVs. La lectura devuelve `Online fetch throttled`. No se ha visto el vídeo: análisis visual pendiente. No se ha creado un análisis táctico atribuido a imágenes no observadas.
6. No se modifica goles_video.csv ni se ejecuta goles_video.py. J8 termina 0-0: no faltan goles de esta jornada para anotar, aunque sí su revisión visual.
7. PushNotification y SendUserFile no están disponibles. Los archivos se entregan mediante enlaces en la respuesta.
8. Sin subida no procede la comprobación del despliegue. La web pública no se ha actualizado con este trabajo.

## Fuentes

- https://www.realzaragoza.com/partidos/temporada-2026-2027-primera-federacion-8-real-murcia-cf-vs-real-zaragoza-3920
- https://es.besoccer.com/partido/real-murcia/real-zaragoza/202724302
- https://futboltotal.futbol/partido/real-murcia-vs-zaragoza-primera-rfef-g2-1571172
- https://www.sportaragon.com/articulo/real-zaragoza/1x1-real-zaragoza-real-murcia/20261018203312161278.html
- https://www.goal.com/es-ar/equipo/ce-europa/partidos-resultados/8wr1fkahj2tx6zqk6e1qi4jq5

## Borrador para LinkedIn

Del 4-4 en Alcalá al 0-0 en Murcia. Dos jornadas seguidas y dos marcadores muy distintos.

El Real Zaragoza suma 17 puntos en ocho partidos y queda segundo, empatado con el Villarreal B. En Murcia hubo nueve tiros por equipo; tres a puerta del Zaragoza y uno del rival.

Estoy preparando la actualización de Línea de pase. El xG y el análisis del vídeo siguen pendientes de revisión.

https://lineadepase.github.io/

#LíneaDePase #AnálisisDeDatos #RealZaragoza

## Reintento del vídeo y autorización de publicación

El usuario confirma publicación y análisis del resumen aunque termine sin goles. Se verifica en YouTube el canal oficial @RFEFutbol, el título y la duración de 155 segundos. El navegador carga la ficha pero no reproduce imágenes: permanece negro en 0:00 tras un reintento. La descarga del formato de vídeo devuelve HTML «Site Unavailable», de 195 bytes; no es un vídeo válido. Sigue pendiente observar las jugadas. La prueba de subida vuelve a fallar por falta de credenciales; la autorización del usuario está concedida, el bloqueo es técnico.
