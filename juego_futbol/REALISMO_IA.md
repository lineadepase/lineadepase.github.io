# Realismo visual y perfiles deportivos

Se usó la herramienta integrada **image_gen** (habilidad imagegen) para producir recursos originales de personas y un estadio ficticios. No se usan fotos de futbolistas o empleados reales. Se conserva un banco compartido de retratos; no se genera una persona nueva para cada uno de los cientos de jugadores. El índice del retrato se guarda y permanece al fichar o recargar.

Recursos locales:
- `juego_futbol/assets/retratos-jugadores-ia.png`: atlas 6 × 6.
- `juego_futbol/assets/retratos-personal-ia.png`: atlas 4 × 4.
- `juego_futbol/assets/estadio-ambiente-ia.png`: panorámica ambiental, rotulada como ilustrativa; no representa las obras concretas del usuario.

El modelo 3D conserva los aforos, sectores y servicios, e incorpora césped con microtextura, cielo de atardecer y jugadores con torso, cuello, rostro, brazos y piernas más detallados. La fotografía ambiental no sustituye este modelo ni se presenta como una captura de un partido. La frecuencia objetivo sube a 50 fps en calidad equilibrada y aproximadamente 60 en alta; son objetivos, no garantías de rendimiento. Se evita dibujar por duplicado el campo 2D cuando el 3D está activo y se reduce la creación de objetos por fotograma. El modo 2D y la física de los goles siguen disponibles.

Alineación completa: nombres enteros, pie dominante, posición abreviada, media, condición y tres grupos. En escritorio hay un campo táctico al lado; en móvil se priorizan las listas. Se pueden intercambiar dos titulares de la misma familia para moverlos en el campo. El campo táctico de detalle muestra retratos y nombres completos en varias líneas.

Los perfiles contienen familia, especialidad, banda, pie y hasta tres posiciones secundarias. Se incluyen portero, centrales, líbero, laterales, carrileros, pivote, mediocentro, interiores, volantes, mediapunta, extremos, delantero centro y segundo delantero. El plan de adaptación cuesta 5.000 € y tarda cuatro semanas; la posición secundaria mejora el encaje en la táctica. El pie dominante es un rasgo persistente de este universo ficticio. Los guardados anteriores se migran sin reemplazar la carrera.

Referencias de diseño consultadas (se aplicaron ideas generales, sin copiar gráficos):
- Sports Interactive, Your Team: https://community.sports-interactive.com/sigames-manual/football-manager-mobile-2026/your-team-r5248/ (posiciones, pie y selección por toque).
- Sports Interactive, Tactics: https://community.sports-interactive.com/sigames-manual/football-manager-2024/tactics-r4960/ (distinción de posición y función).
- EA SPORTS FC 26, Gameplay Deep Dive: https://www.ea.com/games/ea-sports-fc/fc-26/news/pitch-notes-fc26-gameplay-deep-dive (campo y lista, roles y accesos a táctica).
- FIFA Training Centre, Position specific: https://www.fifatrainingcentre.com/en/resources/game-library/position-specific.php (familias y especialidades).

## Prompts finales utilizados

### Jugadores
Production asset for a fictional football management videogame: a perfectly regular contact sheet of 36 DIFFERENT photorealistic fictional male professional footballer headshots, 6 columns by 6 rows, equal square cells, absolutely no gutters or borders, every individual exactly centered within his own cell, full head and upper shoulders entirely inside each cell. Diverse European, African, Asian, Latin American and Middle Eastern appearances, adults ages 18-36, varied realistic hairstyles and facial hair. Natural skin texture, realistic human anatomy, neutral expressions, studio sports photography, consistent soft lighting and dark slate seamless background, plain navy training shirts, NO text, NO numbers, NO logos, NO celebrities. Uniform framing is essential because each cell will be addressed separately as a sprite atlas in a game UI. High resolution square image.

### Personal
Asset atlas for fictional football club management videogame. Photorealistic studio contact sheet, EXACTLY 4 columns and 4 rows, 16 equal square cells, NO gutters, NO border, NO text. Each cell contains a DIFFERENT fictional adult professional football club staff head and shoulders portrait, full head centered fully within its cell. 10 men and 6 women, ages 30 to 65, diverse European African Asian Latin American appearances. Staff look like sporting directors, coaches, medical doctors, physiotherapists, sports data analysts. Some wear plain dark polo shirts, others plain navy blazers, two wear white medical coats; understated realistic garments, no logos. Consistent dark slate background, editorial studio photography, natural skin pores and realistic hair. Original fictional people only, no celebrities. Uniform framing: full head with a little margin above, head at center of each cell. High resolution square contact sheet.

### Estadio
Photorealistic original stadium panorama asset for a fictional football management game. Modern European football stadium at blue hour, camera at the halfway line high in the main stand, perfectly centered view over an empty lush green football pitch with clear accurate white markings, realistic grandstands densely filled with tiny spectators, detailed steel truss canopy, floodlights, warm concourse lights, atmospheric soft haze, rich realistic grass texture, premium television broadcast architectural photography, natural proportions, no people in foreground, no text, no brands, no watermarks. Wide cinematic landscape 16:9. This is a photographic overview illustration, not an interface mockup.
