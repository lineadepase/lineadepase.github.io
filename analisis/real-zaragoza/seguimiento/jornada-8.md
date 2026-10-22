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

https://lineadepase.com/

#LíneaDePase #AnálisisDeDatos #RealZaragoza

## Reintento del vídeo y autorización de publicación

El usuario confirma publicación y análisis del resumen aunque termine sin goles. Se verifica en YouTube el canal oficial @RFEFutbol, el título y la duración de 155 segundos. El navegador carga la ficha pero no reproduce imágenes: permanece negro en 0:00 tras un reintento. La descarga del formato de vídeo devuelve HTML «Site Unavailable», de 195 bytes; no es un vídeo válido. Sigue pendiente observar las jugadas. La prueba de subida vuelve a fallar por falta de credenciales; la autorización del usuario está concedida, el bloqueo es técnico.

## Análisis visual completado con el archivo aportado

El usuario ha facilitado videoplayback.mp4, de 154,6 segundos, 1280×720 y sin pista de audio. Revisión visual mediante fotogramas de todo el resumen y capturas más próximas en las secuencias relevantes. El estado actual de textos/video/jornada-8.json es completado: los bloqueos de vídeo descritos antes quedan resueltos para este análisis.

Se incorpora textos/video/jornada-8.html a jornada-8.html y ultimo-partido.html mediante una función que exige estado completado y partido_id coincidente. Se añaden fuente y duración a resumenes_youtube.csv. No se modifican goles_video.csv ni las métricas de Sofascore.

Se distinguen seis bloques: progresión del Zaragoza (0:11–0:26), falta del Murcia y repetición (0:29–0:47), llegada del Murcia por su derecha y repetición (0:49–1:06), Ademo y revisión (1:07–1:46), salida por banda y disputa posterior (1:47–2:14), y falta del Zaragoza (2:15–2:22). No se atribuye un minuto de partido a partir del tiempo del archivo. El córner final al larguero no aparece y no se analiza como observado.

actualizar.py vuelve a terminar correctamente. Se comprueba que el análisis aparece una sola vez en J8 y Último partido y que no se carga para otros partidos. R sigue sin estar instalado y la subida carece de credenciales: publicación pendiente pese a estar autorizada.


## Validación para publicación · 19 de octubre de 2026

Los tres parches se aplican sobre main actualizado. El acceso de subida a GitHub queda comprobado con git push --dry-run. actualizar.py y previa.py 9 terminan correctamente. La comprobación independiente comprobar.R, ejecutada con R 4.6.1, termina correctamente: ocho partidos, 17 puntos y balance 16-10. Queda resuelto el bloqueo previo de validación en R.

La regeneración conserva los datos y el contenido del análisis visual. Se verifica una sola sección de análisis en jornada-8.html y ultimo-partido.html, y ninguna en J1-J7. Se conservan los gráficos y el Excel entregados en los parches. Siguen vigentes los pendientes de cobertura avanzada del grupo (corte J7), Sofascore y contraste de fuentes de la previa descritos arriba.


## Revisión editorial del análisis general · 19 de octubre de 2026

Se sustituye el desglose de secuencias por un análisis general en tercera persona. Se contrastan las crónicas de ambos clubes y de Radio Zaragoza, Radio Murcia, Sport Aragón y Región Online Murcia. El cabezazo de Moyita al larguero se sitúa en el descuento, sin asignar un minuto exacto porque las crónicas difieren. Se enlazan las fuentes al final y se actualizan las entradillas de portada y del resumen del proyecto. Las estadísticas no cambian.
