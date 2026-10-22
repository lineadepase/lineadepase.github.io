# Plan de recuperación y desarrollo — Juego de fútbol · Línea de Pase

Estado: trabajo en curso. No publicar ni fusionar sin pruebas.

## Fuentes preservadas
- Web avanzada: `estudio/juego-futbol:juego_futbol/index.html` (1179 líneas).
- Web alternativa y Python: `copilot/create-basic-football-management-game:juego_futbol/`.
- `main.py`: motor de consola; `consola.py`: otra implementación; `gui.py`: Tkinter para escritorio; `pygame_menu.py`: prototipo Pygame.
- La rama `main` no contiene todavía `juego_futbol/index.html` ni `juego_futbol/main.py` en esas rutas.

## Arquitectura prevista
1. Web: HTML/CSS/JS estático, adaptable a móvil y accesible, con guardado versionado en localStorage.
2. Móvil: reutilizar y desacoplar el motor Python (sin entrada/salida de consola), construir interfaz táctil y seleccionar empaquetado Android/iOS tras pruebas de viabilidad. Tkinter no es interfaz móvil.
3. Mantener dos productos diferenciados, con reglas y definiciones estadísticas coherentes.

## Revisión obligatoria antes de publicar
- Verificar la fórmula de xG por ocasión y su calibración; etiquetar los xG como simulados, no procedentes de datos reales.
- Probar partidos, calendario, clasificación, empate, fin de temporada, mercado, lesiones, presupuesto y guardado/carga.
- Comprobar que cada simulación respeta la alineación, el cansancio, el estado de los jugadores y la táctica.
- Añadir pruebas automatizadas deterministas con semillas para Python y JS cuando sea posible.
- Probar móvil: pantallas pequeñas, controles táctiles, rendimiento, orientación, persistencia y accesibilidad.
- Evitar usar marcas, escudos, imágenes o nombres de jugadores sin derechos claros.
- No fusionar ramas divergentes completas: seleccionar los archivos y cambios revisados sobre la rama main actual.
- Mantener un backup previo a publicación y probar en un entorno de previsualización.

## Próximos hitos
- H1: auditar diferencias entre las dos versiones web y escoger base con pruebas.
- H2: corregir errores del juego web y crear pruebas reproducibles.
- H3: separar motor Python de UI; pruebas unitarias.
- H4: prototipo táctil móvil y evaluación del empaquetado Android/iOS.
- H5: revisión de producto, documentación, PR y despliegue web; distribución móvil posterior.

Este documento no certifica que las aplicaciones estén terminadas ni probadas.
