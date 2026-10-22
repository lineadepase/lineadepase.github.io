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

Los retratos serán ilustraciones originales de estilo editorial/arcade. Se construirán con rasgos genéricos y expresivos (gesto, pelo, postura y accesorios), evitando copiar o hacer reconocible a una persona real. La variedad de edades, tonos de piel y estilos servirá para diferenciar personajes ficticios, no para representar plantillas oficiales.

## Partido y lenguaje de datos

Las jugadas y repeticiones se dibujarán con animación 2D/SVG a partir del estado del simulador. Una pausa breve podrá mostrar una ruta de pase, un mapa de tiros o la ocupación aproximada del espacio. Se podrá continuar o saltar el análisis para no frenar el ritmo.

Toda métrica generada se marcará como **simulada**. El xG describe la estimación del propio juego para una ocasión inventada; un futuro índice de progresión o amenaza deberá explicar su fórmula o escala y no llamarse xT oficial. Las fuentes reales, si se conectan, mostrarán su procedencia y fecha por separado.

## Entrenamiento

El primer prototipo jugable está en la pestaña **Laboratorio de juego**: presenta un contexto, tres líneas de pase y un balance didáctico entre avance, amenaza y conservación. Al responder, explica la consecuencia, asigna una valoración y guarda intentos, media y mejor resultado. No modifica las medias, la fatiga ni la moral de la plantilla.

La secuencia prevista para ampliar el laboratorio es:

1. Pase y progresión (prototipo actual).
2. Presión: orientar al rival hacia una zona y decidir cuándo saltar.
3. Lectura del espacio: reconocer apoyos, fijaciones y espacios libres.
4. Finalización: elegir entre disparo, pase extra o conservación según el contexto.

Cada ejercicio tendrá varias soluciones plausibles; la puntuación explicará el intercambio entre riesgo y recompensa y permitirá comparar intentos. Será una herramienta didáctica del juego, no una evaluación real del talento de una persona.

## Criterios para ampliar

- Añadir un minijuego por vez, con pruebas de teclado, táctil, guardado y accesibilidad.
- Evitar nuevos datos o imágenes de terceros hasta conocer la licencia y su alcance.
- Mantener una liga ficticia de cuatro equipos hasta que el calendario, los desempates y los premios tengan cobertura de pruebas para formatos mayores.
- Conservar exportación/importación y tolerancia a partidas antiguas cuando se añadan campos opcionales al guardado.
