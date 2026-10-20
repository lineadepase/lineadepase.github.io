# Línea de pase

Análisis de datos en fútbol. Web personal de proyectos de analítica deportiva de Ángel Marqueta Alonso.

Web: https://lineadepase.com/

## Proyectos

- **Real Zaragoza 2026/27**: seguimiento semanal con datos públicos (resultados, goles, tiros, minutos y clasificación) y panel interactivo.
- **Fútbol femenino en datos**: licencias federativas (CSD) y población (INE) para decidir dónde empezar un programa de iniciación.

- **xG, sin líos**: vídeo subtitulado, explicación escrita y límites de los goles esperados.

## Estructura

- `index.html`: portada.
- `proyectos/index.html`, `videos/index.html` y `sobre-mi/index.html` (con el contacto): una página por sección, con el mismo menú y pie que la portada. `contacto/index.html` solo redirige a Sobre mí.
- `proyectos/`: además de la página de la sección, una carpeta por proyecto.
- `datos/zaragoza.json`: datos que lee el panel del Zaragoza. Lo genera el script de `analisis/real-zaragoza`.
- `assets/estilo.css`: estilos comunes.
- `analisis/`: código y datos de cada análisis. Ver [analisis/real-zaragoza](analisis/real-zaragoza/README.md) y [analisis/futbol-femenino](analisis/futbol-femenino/README.md).

Análisis personales hechos con datos públicos. Sin relación con ningún club ni competición.

## Navegación del seguimiento

Resumen y previa dan entrada al contenido. Evolución reúne los gráficos del equipo; Plantilla, los minutos y la participación; Jornadas, las fichas; Primera Federación · Grupo 2, el contexto de la competición. El informe completo queda como consulta detallada.

Las guías de los gráficos viven en `analisis/real-zaragoza/textos/guias_graficos.json`. `presentacion_web.py` las incorpora al regenerar páginas. Las lecturas de las previas se guardan por jornada en `textos/previa_jN.json` y deben revisarse antes de publicar una nueva. La tarjeta destacada de inicio y resumen contiene la fecha del encuentro y pasa a identificar el análisis como previo cuando llega esa hora.

## Dominio, Google y enlaces compartidos

GitHub Pages publica con `CNAME` apuntando a `lineadepase.com`; los enlaces al repositorio de código siguen usando GitHub. Tras generar o editar páginas, ejecuta `python herramientas/actualizar_seo.py` (requiere Pillow). Conserva el diseño y el contenido editorial; actualiza direcciones canónicas, Open Graph, tarjetas de X/Twitter, datos estructurados de la portada, `robots.txt`, `sitemap.xml` y las imágenes de 1200 × 630 en `assets/compartir/`.

El mapa incluye las páginas públicas principales; omite los fragmentos de `analisis/` y las redirecciones como `contacto/`. Los títulos y descripciones salen de cada HTML, para no duplicar textos de jornadas en la herramienta. Cuando cambie un título o se añada una página, vuelve a ejecutarla antes de publicar.

La comprobación de visitantes se gestiona en Cloudflare, no en el código. Mantén el acceso de los buscadores reconocidos, `robots.txt`, `sitemap.xml`, las tarjetas sociales y la ruta de renovación de certificados. El acceso al repositorio y las publicaciones desde GitHub son independientes del control de visitantes.
