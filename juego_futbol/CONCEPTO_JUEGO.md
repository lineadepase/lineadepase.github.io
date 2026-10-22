# Concepto de producto — Línea de Pase: La Pizarra

## Fantasía y bucle principal

El usuario dirige un club de barrio disparatado y aprende a tomar decisiones de fútbol con datos sencillos. El bucle de juego es: preparar el once y el plan, disputar una jornada, revisar qué ocurrió y ajustar la estrategia. El tono es arcade y ligero; las métricas ayudan a explicar una decisión, pero no se presentan como datos oficiales.

## Identidad y nombres

- **Modo base:** clubes y jugadores inventados, con nombres humorísticos y personalidad propia. No se usan plantillas reales, escudos ajenos ni alias que identifiquen a futbolistas concretos.
- **Inspiración futbolística:** las mecánicas pueden representar situaciones observadas en fútbol masculino y femenino sin copiar identidades ni afirmar que la plantilla corresponde a una competición real.
- **Referencia editorial:** el seguimiento analítico de clubes como el Real Zaragoza se mantiene separado de las plantillas jugables. Si se quiere mostrar nombres, símbolos, datos protegidos o marcas de una competición como La Liga F, se revisarán los permisos, la fuente y la atribución antes de activar esa integración.
- **Paquete autorizado futuro:** una opción de contenido con identidades reales solo se habilitaría si se han autorizado por escrito los nombres, escudos, fotografías, datos y demás materiales incluidos en su alcance.

## Dirección artística

Estética de **pizarra de entrenador convertida en sala de análisis**: fondo azul noche, paneles azul pizarra, acentos celestes y un verde de césped reservado para el campo. Los datos importantes usan tipografía grande, contraste alto y etiquetas cortas; en móvil, los paneles pasan a una sola columna y las decisiones a botones táctiles apilados.

Los retratos de plantilla, goleadores y mercado se muestran como avatares vectoriales originales de estilo arcade: formas planas, rasgos expresivos y variaciones deterministas de pelo, tono de piel, gafas, barba y camiseta. No son fotos, no se basan en futbolistas reales ni pretenden representar una plantilla oficial. La misma persona ficticia conserva su avatar entre recargas, sin descargar imágenes externas.

## Partido y lenguaje de datos

La pestaña de partido ofrece una repetición analítica 2D/SVG para cada remate del equipo del usuario. La escena reconstruye una trayectoria esquemática y muestra minuto, rematador, equipo, desenlace y xG simulado; se puede elegir cualquier ocasión desde la crónica o desde sus controles. La animación respeta la preferencia de movimiento reducido. No es vídeo ni seguimiento real de jugadores. Como ampliación futura podrán añadirse capas de posesión, presión y ocupación del espacio sin frenar el ritmo.

Toda métrica generada se marcará como **simulada**. El xG describe la estimación del propio juego para una ocasión inventada; un futuro índice de progresión o amenaza deberá explicar su fórmula o escala y no llamarse xT oficial. Las fuentes reales, si se conectan, mostrarán su procedencia y fecha por separado.

## Entrenamiento

El laboratorio jugable ofrece cuatro ejercicios: **pase y progresión**, que pondera avance, amenaza y conservación; **presión coordinada**, que pondera recuperación, compactación y riesgo de quedar superados; **lectura del espacio**, que pondera la ventaja creada, la amenaza y el riesgo de perderla; y **finalización**, que compara la calidad de remate con el pase y el tiempo disponible. Cada situación presenta tres decisiones y explica su consecuencia. El progreso total y los resultados por ejercicio se guardan; los ejercicios no modifican las medias, la fatiga ni la moral de la plantilla.

La secuencia prevista para ampliar el laboratorio es:

1. Pase y progresión (implementado).
2. Presión: orientar al rival hacia una zona y decidir cuándo saltar (implementado).
3. Lectura del espacio: reconocer apoyos, fijaciones y espacios libres (implementado).
4. Finalización: elegir entre disparo, pase extra o conservación según el contexto (implementado).

Cada ejercicio tendrá varias soluciones plausibles; la puntuación explicará el intercambio entre riesgo y recompensa y permitirá comparar intentos. Será una herramienta didáctica del juego, no una evaluación real del talento de una persona.

## Criterios para ampliar

- Añadir un minijuego por vez, con pruebas de teclado, táctil, guardado y accesibilidad.
- Evitar nuevos datos o imágenes de terceros hasta conocer la licencia y su alcance.
- Mantener una liga ficticia de cuatro equipos hasta que el calendario, los desempates y los premios tengan cobertura de pruebas para formatos mayores.
- Conservar exportación/importación y tolerancia a partidas antiguas cuando se añadan campos opcionales al guardado.
