# Panel en Tableau Public

Guía para montar el panel del Zaragoza en Tableau Public con las tablas que genera `actualizar.py`. Tableau Public es gratuito, pero hay que crear una cuenta y publicar desde Tableau Public Desktop.

## Archivos

Todos están en `datos/salida/` (UTF-8):

| Archivo | Una fila por… |
|---|---|
| `partidos_liga.csv` | partido de liga |
| `goles.csv` | gol (a favor y en contra) |
| `minutos_partido.csv` | jugador y partido |
| `jugadores.csv` | jugador (totales) |
| `clasificacion.csv` | equipo |

## Conexión

1. Abrir Tableau Public Desktop → *Archivo de texto* → `partidos_liga.csv`.
2. Arrastrar `goles.csv` y relacionarlo por `partido_id`.
3. Arrastrar `minutos_partido.csv` y relacionarlo también por `partido_id`.
4. `jugadores.csv` y `clasificacion.csv` van como fuentes de datos aparte (no se relacionan).

## Campos calculados

- **Puntos por partido:** `SUM([Puntos]) / COUNTD([Partido Id])`
- **Diferencia de goles:** `SUM([Goles Favor]) - SUM([Goles Contra])`
- **Gol desde el banquillo:** `[Rol Goleador] = "Suplente"`
- **Cuota de tiros:** `SUM([Tiros Zaragoza]) / (SUM([Tiros Zaragoza]) + SUM([Tiros Rival]))` (formato porcentaje)

## Hojas

1. **Puntos acumulados:** `Jornada` en columnas, `Puntos Acumulados` en filas, línea.
2. **Marcadores:** `Jornada` en columnas, `Goles Favor` y `Goles Contra` en barras dobles.
3. **Goles por tramo:** `Tramo` en columnas, recuento de goles, color por `Sentido`.
4. **Minutos:** `jugadores.csv`, `Jugador` en filas, `Minutos` en barras, ordenado de mayor a menor.
5. **Clasificación:** tabla con `Posicion`, `Equipo`, `Puntos`; resaltar al Real Zaragoza.

## Panel

- Filtro de `Sede` (Casa / Fuera) aplicado a las hojas 1 a 3.
- Mismos colores que la web: azul `#213e96` (a favor) y naranja `#ff6a2b` (en contra).
- Título: «Real Zaragoza 2026/27 · Línea de pase». Fuente al pie: «Datos públicos: web del club, FotMob, futboltotal y BeSoccer».

## Publicar

*Archivo → Guardar en Tableau Public*. Después, en el perfil de Tableau Public, copiar el enlace y añadirlo a la web.

Cada semana, después de ejecutar `actualizar.py`, basta con abrir el libro, *Datos → Actualizar* y volver a guardarlo en Tableau Public.

## Libro actualizado · jornada 8 (20-10-2026)

Libro autónomo: [Real_Zaragoza_extracciones.twbx](datos/tableau/Real_Zaragoza_extracciones.twbx). Conserva las cinco hojas originales y contiene cuatro extracciones Hyper activas, además del Excel con cinco tablas. Las cuatro extracciones se han leído y comparado íntegramente con los CSV, sin diferencias. Incluye ocho partidos de liga, 26 goles (el Murcia–Zaragoza acabó 0–0), 25 jugadores, 128 registros jugador-partido y la clasificación de los veinte equipos tras la J8.

Para reproducir la actualización desde un libro anterior:

```bash
python -m pip install pandas openpyxl tableauhyperapi
python analisis/real-zaragoza/codigo/actualizar_tableau.py anterior.twbx actualizado.twbx
```

El script conserva el esquema y el diseño de las hojas; actualiza los datos, las extracciones, sus recuentos y la ruta del Excel incluido. Las extracciones permiten abrir el libro sin Google Sheets ni acceso a archivos externos. Se ha verificado su contenido con Hyper API; la apertura visual en Tableau Desktop y la publicación en Tableau Public no se han ejecutado en este entorno. La publicación en Tableau Public requiere abrir el libro actualizado y guardarlo en la cuenta correspondiente.

La hoja de Google Sheets «Línea de pase · Real Zaragoza 2026/27 (datos para Tableau)» también está sincronizada con los cinco CSV, sin las columnas fuente_url. No sustituye las extracciones del TWBX automáticamente.
