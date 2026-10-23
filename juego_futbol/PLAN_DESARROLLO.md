# Auditoría y estado — Juego de fútbol · Línea de Pase

## Estado del repositorio

- Trabajo sobre `desarrollo/juego-futbol-revision-20261022`, PR #3 hacia `main`.
- El PR debe seguir como borrador; no se fusiona ni se publica desde este trabajo.
- `juego_futbol/index.html` es la versión web jugable y adaptable.
- `main.py` y `consola.py` son motores de consola independientes. `gui.py` es una interfaz Tkinter de escritorio y `pygame_menu.py` un prototipo; ninguno es una aplicación móvil.

## Lo que incluye la versión web

- Liga ficticia de cuatro equipos, calendario de ida y vuelta y clasificación con desempates.
- Tres formaciones, tres estilos, selección automática y rotación manual.
- Rotación manual accesible: cada jugador apto tiene un control de selección operable con teclado, informa si está seleccionado y explica por qué una baja no se puede elegir.
- Rotación asistida opcional para titulares con fatiga desde el 75 %: elige suplentes aptos menos fatigados de la misma posición y comunica cada cambio o la falta de relevo.
- Rivales con identidades tácticas distintas: bloque defensivo 5-3-2, propuesta ofensiva 4-3-3 y perfil equilibrado 4-4-2.
- Laboratorio de juego con ejercicios interactivos de pase y progresión, presión coordinada, lectura del espacio y finalización, explicación de las decisiones y progreso separado por ejercicio.
- Simulación de ocasiones, tiros, goles, xG interno, cansancio, lesiones, taquilla y salarios. El partido distribuye 18 ventanas de ataque y la relación entre ataque y defensa rival afecta tanto a la selección de rematador y al volumen de remates como a la calidad estimada de las ocasiones. La clasificación muestra los remates simulados acumulados; los guardados previos migran sin reiniciar la temporada.
- Repeticiones analíticas esquemáticas de los remates del equipo del usuario, enlazadas desde la crónica y etiquetadas como contenido ficticio del simulador.
- Crónica y resumen accesibles que distinguen gol/remate sin gol, ocasiones claras según el motor, remates totales y xG por equipo; cada repetición muestra también la categoría interna de la ocasión.
- Tabla de balance posterior al partido con una fila por equipo para goles, remates, xG, diferencia goles−xG y ocasiones claras, utilizable sin depender del mapa de tiros.
- Descarga CSV del balance final, con cabeceras en castellano, separador de hoja de cálculo y codificación compatible con tildes; se habilita cuando termina el partido.
- En móvil, la plantilla se presenta en fichas compactas para consultar posición, rendimiento, fatiga, goles, xG y estado sin desplazamiento horizontal.
- Avatares vectoriales originales, estables para cada nombre ficticio, en las tablas de plantilla, goleadores y mercado.
- Mercado, venta de jugadores, preparación, premios y continuidad de temporada.
- Guía rápida desplegable para el primer uso, previa comparativa con fuerzas propias y del rival, cruces ataque-defensa, localía y estado físico de la plantilla para orientar rotaciones (sin presentar los valores como pronóstico), y botón de jornada que distingue entre jugar una fecha y pasar a la temporada siguiente.
- Archivo local de hasta 20 temporadas cerradas, con partidos, puntos, goles, remates, xG a favor/en contra, diferencia entre goles y xG a favor, y máximos goleadores (incluye empates). Los datos estadísticos que no existían en un guardado antiguo se indican como no disponibles; las copias exportadas incluyen los resúmenes.
- Renovación anual del mercado con cuatro perfiles de jugador, cobertura de posiciones y un límite de doce opciones.
- Plantillas con un máximo operativo de 25 futbolistas para conservar rotaciones manejables; el mercado explica y bloquea compras cuando falta presupuesto o se alcanza el límite.
- Guardado local en navegador y recuperación con validación estructural. Se admite el presupuesto negativo como estado válido.
- Copia JSON exportable e importable, con comprobación de estructura antes de sustituir la partida.

## Reglas de presentación

Todos los clubes y futbolistas del juego usan nombres ficticios con tono humorístico. La interfaz web utiliza un balón genérico y no incorpora escudos de clubes reales. Las valoraciones, resultados y xG pertenecen al simulador: el xG es una estimación didáctica por tipo de ocasión, no una métrica oficial ni calculada a partir de datos reales.

## Pruebas y limitaciones conocidas

- Python: compilación y pruebas unitarias para calendario, integridad de temporada, mercado/guardado, xG y plantillas sin jugadores aptos.
- Navegador: Playwright en Chromium para escritorio y móvil, preferencia de movimiento reducido, rotación manual con Enter y Espacio, relevo asistido de titulares fatigados y estado accesible de jugadores seleccionados o lesionados, tabla compacta móvil con todos los datos de plantilla, guía rápida, previa de rival y estado del botón al cerrar temporada, controles, persistencia, mercado, lesiones, calendario, premios, resumen accesible del partido con remates, ocasiones claras y xG, tabla comparativa completa y descarga CSV verificada, categorías legibles en la crónica y la ficha de repetición, archivo multitemporada con sus métricas y diferencia goles-xG, empates de goleadores, migración de resúmenes antiguos, importación/exportación y errores JavaScript. El workflow guarda capturas de la pizarra inicial y del informe de partido en escritorio y móvil.
- La comprobación local requiere el ejecutable Chromium de Playwright; en este entorno no está instalado. El resultado definitivo de navegador debe confirmarse en GitHub Actions.
- La simulación web es un prototipo jugable de cuatro equipos, no una base de datos de una competición real. El cliente Python no comparte todavía un único motor con la web ni constituye una app iOS/Android.

## Antes de publicar

1. Confirmar en el PR que las pruebas Python y navegador pasan y revisar las capturas.
2. Revisar las licencias de cualquier activo gráfico de terceros que se añada en el futuro.
3. Decidir si se amplía la liga y el mercado; no ampliar la competición hasta tener pruebas para continuidad multitemporada.
4. Publicar únicamente tras autorización expresa.

## Primera versión: definición y pendientes

### Alcance incluido

La primera versión es un juego web local de gestión para una liga inventada de cuatro equipos. Incluye el ciclo de temporada completo, gestión de plantilla y presupuesto, táctica y rotaciones, mercado, preparación, simulación de partidos, clasificación, métricas explicadas como simuladas, repetición esquemática, archivo de temporadas y guardado, reinicio e importación/exportación de partidas. No depende de clubes, jugadores ni estadísticas reales.

### Estado del código

- **Implementado:** el alcance anterior, con interfaz adaptable, controles de teclado, guardados validados y pruebas de motor y navegador.
- **Verificación automatizada:** CI #191, commit `00ddb94254baafe277d77504827900739b1706b5`: pruebas de Python y recorridos Playwright en Chromium de escritorio y móvil correctos; artefacto de capturas generado.
- **Mejora en curso:** el control visual de la plantilla en móvil y nuevas capturas del informe de partido se incorporarán en el siguiente CI.

### Lo que falta para cerrar la primera versión

1. Pasar el nuevo CI tras el ajuste móvil de plantilla y revisar las cuatro capturas (pizarra e informe, escritorio y móvil).
2. Hacer una aceptación manual de una temporada completa en un ordenador y en un móvil real; el CI usa Chromium móvil emulado y no sustituye la comprobación en Safari de iPhone.
3. Confirmar que el ritmo, los textos y el equilibrio de dificultad resultan claros y entretenidos en una partida real; solo entonces ajustar parámetros si hace falta.
4. Mantener el PR como borrador hasta que Ángel dé por buena esa revisión. La integración con la web pública o la publicación requieren una decisión posterior y no forman parte del trabajo de este PR.

### Fuera del alcance de la primera versión

Aplicación nativa para iOS o Android, motor Python compartido con la web, guardado en la nube, juego multijugador, liga ampliada y datos o identidades reales. Se podrán valorar en versiones posteriores.

## Próxima ampliación de producto

El laboratorio ya contiene ejercicios jugables de pase y progresión, presión coordinada, lectura del espacio y finalización. Miden decisiones ficticias mediante escalas didácticas explicadas en pantalla; no cambian las valoraciones de los jugadores ni se presentan como métricas oficiales. La pestaña de partido también incorpora repeticiones esquemáticas de remates, generadas por el motor y claramente diferenciadas de un vídeo o dato oficial. La plantilla usa avatares vectoriales originales sin fotografías ni referencias a futbolistas concretos. Una ampliación posterior podría explorar mapas de presión y ocupación espacial. Los nombres humorísticos y las caras ilustradas originales siguen siendo el modo base; cualquier contenido identificable de clubes, competiciones o futbolistas reales requeriría una revisión de permisos antes de incorporarse.


## Criterio de desempate

La clasificación y los premios usan el mismo orden en la web, la consola y la interfaz de escritorio: puntos, diferencia de goles, goles a favor y nombre del equipo. El último criterio hace que las posiciones no dependan del orden interno de la plantilla cuando todos los datos deportivos coinciden. Las pruebas cubren los cuatro niveles y el reparto de premios web.

## Navegación accesible

Las cinco secciones web se anuncian como pestañas vinculadas a sus paneles. El teclado permite recorrerlas con las flechas izquierda y derecha y saltar al principio o al final con Inicio y Fin; el foco visible se distingue con un contorno amarillo. Las pruebas de navegador recorren las cinco secciones y comprueban su estado accesible en escritorio y móvil.

La rotación manual usa un botón por jugador apto, con nombre accesible y estado de selección; Enter y Espacio permiten elegir e intercambiar titulares y suplentes. Los jugadores lesionados muestran el motivo y quedan desactivados. La prueba de navegador comprueba este flujo en escritorio y móvil.

La herramienta de relevo asistido es voluntaria: solo sustituye a titulares aptos con fatiga igual o superior al 75 % y busca un suplente apto, menos fatigado y de su misma posición. No cambia el sistema ni fuerza una adaptación posicional; un mensaje accesible resume los cambios y señala a quien no haya podido relevar.
