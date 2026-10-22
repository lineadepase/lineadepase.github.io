# Auditoría y estado — Juego de fútbol · Línea de Pase

## Estado del repositorio

- Trabajo sobre `desarrollo/juego-futbol-revision-20261022`, PR #3 hacia `main`.
- El PR debe seguir como borrador; no se fusiona ni se publica desde este trabajo.
- `juego_futbol/index.html` es la versión web jugable y adaptable.
- `main.py` y `consola.py` son motores de consola independientes. `gui.py` es una interfaz Tkinter de escritorio y `pygame_menu.py` un prototipo; ninguno es una aplicación móvil.

## Lo que incluye la versión web

- Liga ficticia de cuatro equipos, calendario de ida y vuelta y clasificación con desempates.
- Tres formaciones, tres estilos, selección automática y rotación manual.
- Simulación de ocasiones, tiros, goles, xG interno, cansancio, lesiones, taquilla y salarios.
- Mercado, venta de jugadores, preparación, premios y continuidad de temporada.
- Guardado local en navegador y recuperación con validación estructural. Se admite el presupuesto negativo como estado válido.
- Copia JSON exportable e importable, con comprobación de estructura antes de sustituir la partida.

## Reglas de presentación

Los nombres, valoraciones, resultados y xG pertenecen al simulador. El xG es una estimación didáctica por tipo de ocasión, no una métrica oficial ni calculada a partir de datos reales. Revisar los derechos del escudo, imágenes y nombres reales antes de publicar una versión promocional.

## Pruebas y limitaciones conocidas

- Python: compilación y pruebas unitarias para calendario, integridad de temporada, mercado/guardado, xG y plantillas sin jugadores aptos.
- Navegador: Playwright en Chromium para escritorio y móvil, controles, persistencia, mercado, lesiones, calendario, temporadas, importación/exportación y errores JavaScript. El workflow guarda capturas de ambos tamaños como artefacto temporal.
- La comprobación local requiere el ejecutable Chromium de Playwright; en este entorno no está instalado. El resultado definitivo de navegador debe confirmarse en GitHub Actions.
- La simulación web es un prototipo jugable de cuatro equipos, no una base de datos de una competición real. El cliente Python no comparte todavía un único motor con la web ni constituye una app iOS/Android.

## Antes de publicar

1. Confirmar en el PR que las pruebas Python y navegador pasan y revisar las capturas.
2. Revisar licencias y permisos de los activos gráficos y los nombres de jugadores.
3. Decidir si se amplía la liga y el mercado; no ampliar la competición hasta tener pruebas para continuidad multitemporada.
4. Publicar únicamente tras autorización expresa.
