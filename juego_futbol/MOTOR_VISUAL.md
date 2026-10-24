# Motor visual y jugabilidad

## Escenas 3D

El juego incluye un render WebGL2 con Three.js r180, distribuido localmente junto a su licencia MIT. No necesita CDNs ni descargar modelos, imágenes o texturas para jugar. Los modelos, materiales y retratos del club son originales y se generan con código.

El estadio dispone de gradas con filas de asientos y público instanciado, fachada y accesos, césped a franjas, áreas, porterías con redes, torres de iluminación y vallas. Su aforo determina la altura de las gradas. Las instalaciones construidas modifican la cubierta, el césped, las luces, las vallas, el marcador, los paneles solares y los edificios de servicios. Los proyectos activos añaden una grúa. El visor permite girar con arrastre, botones o flechas; ajustar zoom y apertura de cubierta; y previsualizar la instalación seleccionada en el planificador. No contrata ni activa obras al previsualizarlas.

El visionado utiliza 22 futbolistas articulados, animación de carrera, dorsales y un balón visible. Ofrece cámaras de televisión, cenital y cercana, así como ambiente diurno o nocturno. Es una recreación de las posiciones por formación y de las ocasiones registradas por el motor estadístico; no constituye una simulación física continua de 22 agentes. Las cubiertas se ocultan en la cámara de partido para mantener la jugada visible.

Las ocasiones jugables sí muestran las posiciones reales de sus atacantes, defensas, portero y balón. Su física se calcula en el plano del campo y se representa en 3D. El modo sigue siendo de ocasiones, no un partido completo controlable de once contra once. La copa conserva el modo resultado.

## Retratos

Los retratos vectoriales tienen busto, equipación, luces, sombras y variantes de piel, ojos, pelo y barba. El nombre determina una identidad estable; los identificadores de gradientes son únicos en cada instancia para evitar colisiones al mostrar al mismo jugador varias veces. La galería está en Plantilla → Futbolistas. Son ilustraciones ficticias, sin fotografías ni semejanzas con jugadores reales.

## Controles y reglas

- Flechas o WASD: movimiento con aceleración y frenado gradual.
- Shift o botón Sprint: acelera consumiendo energía; se recupera al descansar.
- Espacio mantenido y soltado, o botón de disparo: carga la potencia. Superar el punto de control reduce la precisión lateral.
- Barra Colocación, toque en el campo o stick derecho: elegir la zona entre postes.
- X o Pasar: pase al apoyo siguiente; si has cambiado de control a un compañero, se dirige a ese jugador.
- C o Cambiar: controlar otro atacante sin teletransportar el balón.
- Mando estándar: stick izquierdo, RT para sprint, A para pase, B para carga y disparo y LB para cambiar. Las entradas del mando se leen mediante Gamepad API; no se ha verificado un mando físico específico.

Hay tres atacantes, tres defensas y un portero. Los apoyos se desplazan sin balón y pueden acercarse a una recepción si el usuario no introduce una dirección. El balón es independiente de los jugadores cuando se pasa o dispara. El portero sigue su trayectoria, puede rechazarlo y se pueden buscar rebotes. Los postes desvían el balón. Un tiro solo es gol al cruzar la boca de la portería.

La ocasión oficial dura hasta 25 segundos; el entrenamiento, 30. Hay ejercicios de combinación, contraataque y ataque por banda. El entrenamiento permite repetir y no modifica goles, dinero ni fatiga de la carrera. En un encuentro oficial, sprintar puede añadir fatiga al jugador. Al terminar se confirma el resultado antes de continuar. El modo se pausa si la ventana pierde el foco.

Cada remate jugable conserva su autor, posición de origen, xG simulado y resultado. Esos remates se incorporan al acta de liga, sin volver a sortear si hubo gol. Los remates de práctica no entran en el acta. El xG es una estimación didáctica ficticia, no un modelo calibrado con fútbol real.

## Rendimiento y compatibilidad

Solo existe un renderer 3D compartido entre estadio, visionado y ocasión. Se reutilizan geometrías y materiales, se instancia el público y no se renderiza una escena fuera de pantalla o con la pestaña oculta. La resolución se limita según calidad y densidad de píxeles; las sombras completas se activan en calidad Alta. La calidad equilibrada puede reducir resolución y público si detecta un render lento.

Si WebGL2 no está disponible o se identifica renderizado por software, se usa Canvas 2D por defecto. La física y los controles no cambian. Calidad Alta permite probar el 3D por software; 2D permite seleccionar máxima fluidez explícitamente. Una pérdida de contexto 3D descubre la vista 2D y conserva la ocasión. Las escenas 3D se prueban con SwiftShader forzado para verificar el código incluso en equipos de pruebas sin GPU.

## Verificación

Pruebas puras de aceleración, energía, carga, autor y origen de remates, postes, portero, fuera, pausa, cambio de control y escenarios. Pruebas en Chromium de render WebGL2, giro de cámara, cambios de instalaciones, retratos estables, teclado, goles físicos, independencia del entrenamiento y pérdida de contexto. Se prueba también la ausencia de WebGL, los controles sin scroll en 320 px y horizontal y dos goles calculados por la física que entran en el partido oficial. Las pruebas generales siguen cubriendo carrera, contratos, obras, cantera, estadísticas y guardados.

Biblioteca: [Three.js r180](https://github.com/mrdoob/three.js/tree/r180), licencia en `js/vendor/THREE-LICENSE.txt`. Documentación consultada: [WebGLRenderer](https://threejs.org/docs/pages/WebGLRenderer.html).
