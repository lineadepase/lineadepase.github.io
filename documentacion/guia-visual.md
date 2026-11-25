# Guía visual de Línea de pase

## Idea

Una libreta de análisis dibujada sobre el campo: papel claro para leer, verde para ordenar la navegación y naranja para señalar una acción o un dato. Las líneas del terreno aparecen como motivo ligero en la marca y en piezas seleccionadas; el fondo no debe convertirse en una textura permanente.

## Tipografía

- **Big Shoulders Display:** titulares, cifras de marcador y sellos breves.
- **Archivo:** párrafos, navegación, botones y tablas.
- Titulares cortos y equilibrados; párrafos de lectura con un máximo aproximado de 70 caracteres por línea.

## Color

- `--papel`, `--panel`, `--tinta` y `--tinta-suave`: lectura y superficies.
- `--cesped` y `--cesped-noche`: navegación, categorías y piezas de apertura.
- `--senal` / `--senal-texto`: énfasis puntual y estados importantes; nunca como color de párrafo largo.
- En oscuro se mantienen equivalentes de contraste; los gráficos deben identificar sus series además del color.

## Espaciado y formas

La escala compartida vive en `assets/estilo.css`: pasos de 4, 8, 12, 16, 24, 32, 48 y 72 px. Controles pequeños usan 6 px de radio, tarjetas 12 px y piezas gráficas 14 px. Lectura: 70ch; ancho de página: 72rem.

## Portadas piloto

- **Temporada:** azul y verde, marcador y secuencia temporal; usar datos del Zaragoza con jornada y corte visibles.
- **Territorio:** mapa legible y tono malva; conservar la silueta y las unidades de población/licencias.
- **Ocasiones:** naranja moderado, trayectoria del tiro o zonas de peligro; no confundir una ilustración con una medición.

Las tarjetas del catálogo usan estas tres familias como pilotos. Sus miniaturas siguen mostrando las gráficas o mapas reales del proyecto; los sellos, bandas y patrones identifican la colección.

## Uso de líneas de campo

El círculo central, la línea media y las trayectorias se reservan para divisores o ilustraciones puntuales. Deben quedar por detrás del texto, usar bajo contraste y desaparecer si dificultan la lectura o la impresión.

## Imágenes

Priorizar gráficas originales, SVG y fotografías propias o con licencia registrada. Las miniaturas informativas se muestran completas; los recortes se reservan a fotografía. Texto, cifras y rótulos se componen en HTML/SVG editable para evitar letras defectuosas incrustadas en imágenes generadas.
