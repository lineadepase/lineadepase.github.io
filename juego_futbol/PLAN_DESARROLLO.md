# Auditoría y estado — Juego de fútbol · Línea de Pase

## Ampliación de carrera y gestión clásica · 23 octubre 2026

Esta revisión amplía la anterior navegación sin scroll a **ocho departamentos**: Despacho, Plantilla/Táctica, Secretaría/Fichajes, Entrenador, Partido, Finanzas, Estadio y Ajustes. Las capturas aportadas por el usuario inspiran las fichas claras, las cabeceras azules y la media 1–100, con gráficos originales propios. La vista de plantilla prioriza la media y permite abrir sus atributos mediante un botón. No se reutilizan escudos, retratos ni interfaces gráficas de PC Fútbol.

### Carrera y continuidad

- Se conservan los cumpleaños por calendario y ahora también envejece la cantera.
- Los menores de 25 años que juegan al menos el 55 % de los partidos oficiales pueden mejorar hasta tres puntos, limitados por su potencial. En nuestra liga corta son cuatro de seis partidos; en una de 38 serían 21. No se presenta este balance como una reproducción exacta del juego histórico.
- Desde los 31 años desciende la habilidad; en porteros comienza a los 34. La edad de retirada individual se fija entre 35 y 38, o 37 y 40 para porteros.
- El relevo generacional tiene nombre e identidad nuevos, entre 18 y 24 años, y conserva el perfil base y el potencial. Su habilidad actual, contrato y sueldo se ajustan a una promesa; no hereda el salario de la estrella. Puede pasar a cantera, primer equipo o mercado según su edad y las plazas disponibles.
- La CPU repone puestos prioritarios y mantiene dos porteros y al menos catorce jugadores. Los identificadores de los jugadores base retirados quedan registrados para que el mercado estacional no los resucite desde el JSON. La cantera tiene doce plazas; el primer equipo, veinticinco. El mercado y los archivos tienen límites de tamaño.
- Contratos de 1–5 temporadas, salario por jornada, primas por gol y cláusula económica. Oferta, contraoferta o rechazo inmediatos, con firma separada que aplica el gasto. La renovación exige más sueldo si la cláusula supera tres veces el valor. Los rivales pueden pagar cláusulas inferiores al 65 % del valor durante el mercado; el dinero llega al vendedor y se cubre el puesto.

### Gestión del club

- Entradas y abonos: demanda sensible al precio y al rival, previsión antes de guardar y campaña de abonos una vez antes del estreno. No se vuelve a cobrar entrada a un abonado.
- Gradas independientes: +1.000 localidades por obra; coste 250.000 €, dos jornadas de ejecución. Parking, comida, tienda y transporte tienen tres niveles y dos jornadas de obra. El aumento de capacidad o servicio se aplica al terminar, no al pagarlo.
- Acuerdos de camiseta y vallas con fijo, victoria o goles; son contratos de temporada. Los patrocinios puntuales anteriores siguen siendo acuerdos de una jornada.
- Médico, psicólogo, entrenador de cantera y comercial de nivel 0–3. Altas y nóminas explícitas; sus efectos modifican recuperación, moral, desarrollo e ingresos. El balance de cada encuentro separa entradas, servicios, publicidad, sueldos, empleados, primas y neto. Una liquidación no se puede cobrar dos veces.

### Partido

- Se mantiene el visionado 2D, con líneas que responden a la mentalidad, energía visible, nombres asociados a las acciones de la crónica y trayectorias de recreación.
- La mentalidad cambia ataque y defensa durante el partido; «Pedir gol» da +10 ataque y −5 defensa una vez. No garantiza marcar. Los poderes también se incorporan al cálculo de fuerzas.
- **Modo jugable de ocasiones 2D**, no un partido completo de control de once futbolistas: en dos ataques oficiales se controla al jugador con flechas/WASD o cruceta táctil, Espacio para disparar y X para pasar. Hay balón independiente, rebotes, defensores, portero y límite de 18 segundos. Los goles de estas ocasiones se añaden al marcador real de la simulación. La práctica es independiente y no modifica la liga.

### Implementación y comprobación

`club-motor.js` contiene reglas sin DOM; `club-manager.js` las conecta con las pantallas y migra guardados anteriores; `partido-2d.js` separa física y controles; `club-manager.css` aporta el estilo de fichas y departamentos. Se conserva el motor Python como cliente independiente.

Las pruebas de Node incluyen cien temporadas, crecimiento, jubilación, relevos, límites e identidad de jugadores, contratos y pagos atómicos, cláusulas, previsiones de taquilla, abonos, obras, personal y física 2D. El navegador recorre las nuevas operaciones, guardado antiguo, una temporada completa y una ocasión jugable conectada al marcador en escritorio y móvil. Se mantiene la batería anterior y la inspección de todas las páginas en cuatro tamaños.

Referencia de diseño aportada por el usuario: [experiencia de cien temporadas de PC Fútbol 6.0](https://www.elgeneralfailure.com/2024/06/he-llegado-la-temporada-20962097-100.html). Se usan sus observaciones de continuidad como casos que prevenir, sin reproducir sus fallos como reglas.

Pendiente: afinar economía y dificultad con juego humano, probar dispositivos físicos/Safari y mando, ampliar la competición y terminar recursos visuales. El modo de once contra once con control continuo, las jugadas a balón parado dibujables y el clima con física propia quedan para una ampliación posterior. El PR sigue en borrador y no se publica.

## Recuperación y navegación sin desplazamiento · 23 octubre 2026

Se recuperó la rama a partir de `da0ae47`, incluyendo edades, cumpleaños y compatibilidad de guardados. La interfaz dispone de seis secciones: Despacho, Fichajes, Táctica, Partido, Entrenar y club, y Ajustes y ayuda. Cada sección ofrece un selector de pantallas concretas. Calendario, decisiones, poderes, plan de partido, patrocinadores, finanzas, tablas, crónica y repeticiones tienen destinos propios.

`css/pantallas.css` distribuye la interfaz dentro de la altura del dispositivo. `js/pantallas.js` conserva los nodos y controles existentes y reparte su contenido en páginas medidas, con Anterior/Siguiente y contador. También divide fichas y explicaciones cuando cambia el espacio disponible. La navegación, los controles de página y el siguiente paso ocupan filas propias. Los accesos directos abren la página de la acción, sin `scrollIntoView`. El guardado continúa siendo el anterior.

Se corrigió la animación de descarte que podía dejar la siguiente tarjeta fuera de pantalla. La introducción utiliza términos de juego en lugar de CTA/QTE.

Las pruebas de navegador existentes navegan ahora a la pantalla y página de cada control antes de utilizarlo. `tests/screens.cjs` recorre todas las páginas en 1366×900, 390×844, 320×568 y 844×390, comprueba límites del contenido y del botón principal, y verifica que los textos sean consultables. El workflow ejecuta ambos recorridos y conserva sus capturas. La validación en dispositivos físicos continúa pendiente.

## Estado del repositorio

- Trabajo sobre `desarrollo/juego-futbol-revision-20261022`, PR #3 hacia `main`.
- El PR debe seguir como borrador; no se fusiona ni se publica desde este trabajo.
- `juego_futbol/index.html` es la versión web jugable y adaptable.
- `main.py` y `consola.py` son motores de consola independientes. `gui.py` es una interfaz Tkinter de escritorio y `pygame_menu.py` un prototipo; ninguno es una aplicación móvil.

## Lo que incluye la versión web

- Liga paródica de cuatro clubes basada en plantillas de Primera 2026/27, con calendario de ida y vuelta y clasificación con desempates. Los alias y rasgos son humorísticos; las edades de carrera, cumpleaños y atributos son ficticios.
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
- En móvil, la plantilla y el balance del partido se presentan en fichas compactas para consultar todos sus datos sin desplazamiento horizontal.
- Avatares vectoriales originales, estables para cada nombre ficticio, en las tablas de plantilla, goleadores y mercado.
- Mercado disponible en agosto y diciembre, venta de jugadores, preparación, premios y continuidad de temporada. El calendario avanza cuatro semanas al jugar; los cumpleaños de carrera suman un año y se conservan al guardar la partida.
- Guía rápida desplegable para el primer uso, previa comparativa con fuerzas propias y del rival, cruces ataque-defensa, localía y estado físico de la plantilla para orientar rotaciones (sin presentar los valores como pronóstico), y botón de jornada que distingue entre jugar una fecha y pasar a la temporada siguiente.
- Archivo local de hasta 20 temporadas cerradas, con partidos, puntos, goles, remates, xG a favor/en contra, diferencia entre goles y xG a favor, y máximos goleadores (incluye empates). Los datos estadísticos que no existían en un guardado antiguo se indican como no disponibles; las copias exportadas incluyen los resúmenes.
- Renovación anual del mercado con cuatro perfiles de jugador, cobertura de posiciones y un límite de doce opciones.
- Plantillas con un máximo operativo de 25 futbolistas para conservar rotaciones manejables; el mercado explica y bloquea compras cuando falta presupuesto o se alcanza el límite.
- Guardado local en navegador y recuperación con validación estructural. Se admite el presupuesto negativo como estado válido.
- Copia JSON exportable e importable, con comprobación de estructura antes de sustituir la partida.

## Reglas de presentación

Los clubes llevan nombres paródicos y los jugadores, alias humorísticos de integrantes de plantillas de Primera 2026/27 identificados en el JSON. No se incorporan escudos ni fotografías oficiales. Edades, cumpleaños, atributos, salarios, resultados y xG son inventados; el xG es una estimación didáctica del simulador, no una métrica oficial ni calculada con datos reales.

## Pruebas y limitaciones conocidas

- Python: compilación y pruebas unitarias para calendario, integridad de temporada, mercado/guardado, xG y plantillas sin jugadores aptos.
- Navegador: Playwright en Chromium para escritorio y móvil, preferencia de movimiento reducido, rotación manual con Enter y Espacio, relevo asistido de titulares fatigados y estado accesible de jugadores seleccionados o lesionados, edad visible, progresión real de fecha y cumpleaños, apertura estacional del mercado, calendario y temporadas, guía rápida, controles, persistencia, resumen accesible del partido, tabla comparativa y descarga CSV, repeticiones, archivo multitemporada, migración e importación/exportación. El workflow guarda capturas de la pizarra inicial y del informe de partido en escritorio y móvil.
- La comprobación local requiere el ejecutable Chromium de Playwright; en este entorno no está instalado. El resultado definitivo de navegador debe confirmarse en GitHub Actions.
- La simulación web es un prototipo jugable de cuatro equipos, no una base de datos de una competición real. El cliente Python no comparte todavía un único motor con la web ni constituye una app iOS/Android.

## Antes de publicar

1. Confirmar en el PR que las pruebas Python y navegador pasan y revisar las capturas.
2. Revisar las licencias de cualquier activo gráfico de terceros que se añada en el futuro.
3. Decidir si se amplía la liga y el mercado; no ampliar la competición hasta tener pruebas para continuidad multitemporada.
4. Publicar únicamente tras autorización expresa.

## Primera versión: definición y pendientes

### Alcance incluido

La primera versión es un juego web local de gestión para cuatro clubes paródicos basados en integrantes de plantillas de Primera 2026/27. Incluye el ciclo de temporada completo, gestión de plantilla y presupuesto, táctica y rotaciones, mercado estacional, calendario, edades de carrera, preparación, simulación de partidos, clasificación, métricas simuladas, repetición esquemática, archivo de temporadas y guardado, reinicio e importación/exportación de partidas.

### Estado del código

- **Implementado:** el alcance anterior, con interfaz adaptable, controles de teclado, guardados validados y pruebas de motor y navegador.
- **Acceso desde la web:** el catálogo de Proyectos enlaza al juego con una llamada a la acción que indica que se juega en el navegador; el aviso del simulador enlaza a la explicación de xG ya existente. No se ofrecen descargas nativas ni enlaces a tiendas móviles.
- **Verificación automatizada:** CI #195, commit `89a1ca4cbaa9270bde63192e1aece1869df12014`: compilación y 11 pruebas de Python correctas; Playwright en Chromium de escritorio y móvil también pasó, incluidos los destinos del CTA y del enlace de xG, además de los flujos de juego, CSV y diseño móvil. Se generaron capturas para escritorio y móvil.
- **Revisión visual:** inspeccionadas las cuatro capturas del CI #193 (pizarra e informe de partido en escritorio y móvil). Las fichas conservan sus datos sin desbordar el ancho del móvil; el informe compara ambos equipos y deja visible la descarga.
- **Estado de la primera versión:** el alcance de juego web descrito arriba está implementado y supera sus controles automáticos. No queda una función de producto identificada como bloqueante; falta la aceptación manual de la experiencia.

### Lo que falta para cerrar la primera versión

1. Jugar una temporada completa en un ordenador y en un móvil real; el CI usa Chromium móvil emulado y no sustituye la comprobación en Safari de iPhone.
2. Confirmar que el ritmo, los textos y el equilibrio de dificultad resultan claros y entretenidos en una partida real; ajustar únicamente lo que revele esa prueba.
3. Mantener el PR como borrador hasta que Ángel dé por buena la experiencia. Integrar el juego en la web pública o publicarlo requiere una decisión posterior y queda fuera de este PR.

### Fuera del alcance de la primera versión

Aplicación nativa para iOS o Android, motor Python compartido con la web, guardado en la nube, juego multijugador y ampliación a una liga más extensa. Se podrán valorar en versiones posteriores. Las identidades paródicas actuales son alias de futbolistas de Primera; no se muestran retratos ni escudos oficiales.

## Próxima ampliación de producto

El laboratorio ya contiene ejercicios jugables de pase y progresión, presión coordinada, lectura del espacio y finalización. Miden decisiones ficticias mediante escalas didácticas explicadas en pantalla; no cambian las valoraciones de los jugadores ni se presentan como métricas oficiales. La pestaña de partido también incorpora repeticiones esquemáticas de remates, generadas por el motor y claramente diferenciadas de un vídeo o dato oficial. La plantilla usa avatares vectoriales originales sin fotografías ni referencias a futbolistas concretos. Una ampliación posterior podría explorar mapas de presión y ocupación espacial. Los nombres humorísticos y las caras ilustradas originales siguen siendo el modo base; cualquier contenido identificable de clubes, competiciones o futbolistas reales requeriría una revisión de permisos antes de incorporarse.


## Criterio de desempate

La clasificación y los premios usan el mismo orden en la web, la consola y la interfaz de escritorio: puntos, diferencia de goles, goles a favor y nombre del equipo. El último criterio hace que las posiciones no dependan del orden interno de la plantilla cuando todos los datos deportivos coinciden. Las pruebas cubren los cuatro niveles y el reparto de premios web.

## Navegación accesible

Las cinco secciones web se anuncian como pestañas vinculadas a sus paneles. El teclado permite recorrerlas con las flechas izquierda y derecha y saltar al principio o al final con Inicio y Fin; el foco visible se distingue con un contorno amarillo. Las pruebas de navegador recorren las cinco secciones y comprueban su estado accesible en escritorio y móvil.

La rotación manual usa un botón por jugador apto, con nombre accesible y estado de selección; Enter y Espacio permiten elegir e intercambiar titulares y suplentes. Los jugadores lesionados muestran el motivo y quedan desactivados. La prueba de navegador comprueba este flujo en escritorio y móvil.

La herramienta de relevo asistido es voluntaria: solo sustituye a titulares aptos con fatiga igual o superior al 75 % y busca un suplente apto, menos fatigado y de su misma posición. No cambia el sistema ni fuerza una adaptación posicional; un mensaje accesible resume los cambios y señala a quien no haya podido relevar.
