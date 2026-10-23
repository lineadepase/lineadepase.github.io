# Auditoría y estado — Juego de fútbol · Línea de Pase

## Estado del repositorio

- Trabajo sobre `desarrollo/juego-futbol-revision-20261022`, PR #3 hacia `main`.
- El PR debe seguir como borrador; no se fusiona ni se publica desde este trabajo.
- `juego_futbol/index.html` es la versión web jugable y adaptable.
- `main.py` y `consola.py` son motores de consola independientes. `gui.py` es una interfaz Tkinter de escritorio y `pygame_menu.py` un prototipo; ninguno es una aplicación móvil.

## Lo que incluye la versión web

- Liga ficticia de cuatro equipos, calendario de ida y vuelta y clasificación con desempates.
- Tres formaciones, tres estilos, selección automática y rotación manual.
- Rivales con identidades tácticas distintas: bloque defensivo 5-3-2, propuesta ofensiva 4-3-3 y perfil equilibrado 4-4-2.
- Laboratorio de juego con ejercicios interactivos de pase y progresión, presión coordinada, lectura del espacio y finalización, explicación de las decisiones y progreso separado por ejercicio.
- Simulación de ocasiones, tiros, goles, xG interno, cansancio, lesiones, taquilla y salarios. El partido distribuye 18 ventanas de ataque y la relación entre ataque y defensa rival afecta tanto a la selección de rematador y al volumen de remates como a la calidad estimada de las ocasiones. La clasificación muestra los remates simulados acumulados; los guardados previos migran sin reiniciar la temporada.
- Repeticiones analíticas esquemáticas de los remates del equipo del usuario, enlazadas desde la crónica y etiquetadas como contenido ficticio del simulador.
- Avatares vectoriales originales, estables para cada nombre ficticio, en las tablas de plantilla, goleadores y mercado.
- Mercado, venta de jugadores, preparación, premios y continuidad de temporada.
- Guía rápida desplegable para el primer uso, previa del rival con formación, estilo y fuerzas del simulador, y botón de jornada que distingue entre jugar una fecha y pasar a la temporada siguiente.
- Archivo local de hasta 20 temporadas cerradas, con partidos, puntos, goles, remates, xG a favor/en contra, diferencia entre goles y xG a favor, y máximos goleadores (incluye empates). Los datos estadísticos que no existían en un guardado antiguo se indican como no disponibles; las copias exportadas incluyen los resúmenes.
- Renovación anual del mercado con cuatro perfiles de jugador, cobertura de posiciones y un límite de doce opciones.
- Plantillas con un máximo operativo de 25 futbolistas para conservar rotaciones manejables y bloquear fichajes al alcanzar el límite.
- Guardado local en navegador y recuperación con validación estructural. Se admite el presupuesto negativo como estado válido.
- Copia JSON exportable e importable, con comprobación de estructura antes de sustituir la partida.

## Reglas de presentación

Todos los clubes y futbolistas del juego usan nombres ficticios con tono humorístico. La interfaz web utiliza un balón genérico y no incorpora escudos de clubes reales. Las valoraciones, resultados y xG pertenecen al simulador: el xG es una estimación didáctica por tipo de ocasión, no una métrica oficial ni calculada a partir de datos reales.

## Pruebas y limitaciones conocidas

- Python: compilación y pruebas unitarias para calendario, integridad de temporada, mercado/guardado, xG y plantillas sin jugadores aptos.
- Navegador: Playwright en Chromium para escritorio y móvil, preferencia de movimiento reducido, guía rápida, previa de rival y estado del botón al cerrar temporada, controles, persistencia, mercado, lesiones, calendario, premios, resumen accesible del partido con remates y xG, crónica de ocasiones, archivo multitemporada con sus métricas y diferencia goles-xG, empates de goleadores, migración de resúmenes antiguos, importación/exportación y errores JavaScript. El workflow guarda capturas de ambos tamaños como artefacto temporal.
- La comprobación local requiere el ejecutable Chromium de Playwright; en este entorno no está instalado. El resultado definitivo de navegador debe confirmarse en GitHub Actions.
- La simulación web es un prototipo jugable de cuatro equipos, no una base de datos de una competición real. El cliente Python no comparte todavía un único motor con la web ni constituye una app iOS/Android.

## Antes de publicar

1. Confirmar en el PR que las pruebas Python y navegador pasan y revisar las capturas.
2. Revisar las licencias de cualquier activo gráfico de terceros que se añada en el futuro.
3. Decidir si se amplía la liga y el mercado; no ampliar la competición hasta tener pruebas para continuidad multitemporada.
4. Publicar únicamente tras autorización expresa.

## Próxima ampliación de producto

El laboratorio ya contiene ejercicios jugables de pase y progresión, presión coordinada, lectura del espacio y finalización. Miden decisiones ficticias mediante escalas didácticas explicadas en pantalla; no cambian las valoraciones de los jugadores ni se presentan como métricas oficiales. La pestaña de partido también incorpora repeticiones esquemáticas de remates, generadas por el motor y claramente diferenciadas de un vídeo o dato oficial. La plantilla usa avatares vectoriales originales sin fotografías ni referencias a futbolistas concretos. Una ampliación posterior podría explorar mapas de presión y ocupación espacial. Los nombres humorísticos y las caras ilustradas originales siguen siendo el modo base; cualquier contenido identificable de clubes, competiciones o futbolistas reales requeriría una revisión de permisos antes de incorporarse.


## Criterio de desempate

La clasificación y los premios usan el mismo orden en la web, la consola y la interfaz de escritorio: puntos, diferencia de goles, goles a favor y nombre del equipo. El último criterio hace que las posiciones no dependan del orden interno de la plantilla cuando todos los datos deportivos coinciden. Las pruebas cubren los cuatro niveles y el reparto de premios web.

## Navegación accesible

Las cinco secciones web se anuncian como pestañas vinculadas a sus paneles. El teclado permite recorrerlas con las flechas izquierda y derecha y saltar al principio o al final con Inicio y Fin; el foco visible se distingue con un contorno amarillo. Las pruebas de navegador recorren las cinco secciones y comprueban su estado accesible en escritorio y móvil.
