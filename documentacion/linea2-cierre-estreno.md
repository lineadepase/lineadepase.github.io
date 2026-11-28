# Línea de Pase 2.0: alcance y cierre del primer estreno

Estado del 27 de noviembre de 2026. Rama `desarrollo/linea-de-pase-2`.

## Dónde estamos

Hay un prototipo funcional de ocho áreas en `/datalab-prototipo/`, con catorce accesos directos a experiencias y herramientas. No es todavía la sustitución de la web pública. Se conserva la portada actual y el prototipo lleva `noindex,nofollow`.

La última versión funcional supera 116 pruebas: 44 de lógica, 12 de generación y 60 de Chromium en cuatro tamaños. No significa que todas las páginas históricas hayan pasado pruebas completas de interacción, ni que Safari, Firefox o dispositivos físicos estén revisados.

El inventario local registra 62 páginas HTML y 58 URLs en sitemap. Hay siete páginas asignadas a Play, cinco a DataLab, dos a Museo, dos a Studio, tres a Pro, tres a Media, 34 a Zaragoza, cinco transversales y el prototipo. Esta clasificación indica el área principal: un recurso puede enlazarse desde varias áreas sin duplicarlo. El inventario no acredita la vigencia de cada contenido.

## Alcance del estreno

Entran las ocho áreas, los cinco experimentos didácticos, las dos salas del Museo, el trivial de nueve preguntas, los juegos existentes revisados, el seguimiento del Zaragoza, los generadores existentes, los cuadernos y el pasaporte local. El estreno se apoya en contenidos y datos que ya existen; las discrepancias se muestran y los valores ausentes no se completan por inferencia.

Quedan fuera del primer estreno: un xG universal entrenado, la investigación de fortaleza «Los puntos engañan», cuentas, pagos, suscripciones, clasificación multijugador y sincronización en la nube. Los cuatro últimos no son compromisos de desarrollo posteriores: no forman parte del alcance actual. No se exige crear más vídeos, artículos o salas para poder cerrar esta primera versión.

No se añaden nuevas funciones durante el cierre salvo para resolver un fallo, un requisito de accesibilidad o una necesidad de integración.

## Estructura que se implementará en desarrollo

La portada debe orientar y ofrecer los tres recorridos existentes: curiosidad, Zaragoza y creación. Las áreas tendrán entradas claras; la portada dejará de cargar todos sus formularios y experimentos.

| Etiqueta de navegación | Entrada prevista al publicar | Decisión |
| --- | --- | --- |
| DataLab | `/datalab/` | Nueva entrada para experimentos y proyectos; enlaza las investigaciones en sus URLs actuales. |
| Museo | `/museo/` | Nueva entrada para salas y lectura de obras; utiliza los gráficos reales y la galería existente. |
| Play | `/play/` | Nueva entrada para trivial y catálogo de juegos, con instrucciones y retorno. |
| Zaragoza | `/proyectos/real-zaragoza/` | Reutiliza la entrada existente; no crea otro panel con la misma función. |
| Pro | `/seleccion/` | Reutiliza el perfil y los trabajos; incorpora el cuaderno y el acceso a métodos. No es un servicio de pago. |
| Studio | `/studio/` | Nueva entrada de selección y redacción; los generadores siguen en `/archivo-visual/` y sus rutas existentes. |
| Media | `/videos/` | Reutiliza el catálogo audiovisual; enlaza archivo, novedades y explicaciones. |
| Pasaporte | `/pasaporte/` | Nueva entrada para recorrido y nota locales, sin cuenta. Se conserva la clave de almacenamiento. |

Estas son rutas de destino previstas, no páginas ya implementadas. Primero se prepararán entradas separadas dentro de `/datalab-prototipo/`, sin indexación, para revisar el recorrido antes de activar rutas públicas. El prototipo actual se conservará durante la transición para no romper enlaces compartidos.

Las URLs existentes no se renombrarán para que coincidan con las etiquetas del menú. `/archivo/`, `/proyectos/`, `/conceptos/`, `/herramientas/`, `/galeria-visual/`, `/sobre-mi/`, privacidad, previas y fichas mantienen su dirección y su función. El alias de contacto y las excepciones de canonical deben mantenerse.

## Inventario e integraciones que hay que cerrar

| Área | Reutilización prevista | Trabajo pendiente del cierre |
| --- | --- | --- |
| DataLab | xG divulgativo, xT, perfiles de Liga F, fútbol femenino y conceptos | Separar proyectos reales de modelos didácticos; incorporar acceso al proyecto de perfiles, que no está destacado en el prototipo. |
| Museo | Redes de España, superficie xT, galería y archivo visual | Mantener obra, contexto, fuente y metodología; evitar duplicar la biblioteca de descargas. |
| Play | Marcador a ciegas, Partidos espejo, Reloj del marcador, Balance de preguntas, Preguntas del partido, Mapa de lo que cambió y Esquemas del juego | Revisar qué hace realmente cada pieza, añadir entrada e instrucciones coherentes y probar sus recorridos. No presentar todas como juegos competitivos. |
| Zaragoza | Panel, jornadas, previas, evolución, plantilla, grupo, simulación y goles en vídeo | Ordenar accesos, comprobar corte y discrepancias; mantener exportaciones y enlaces a las fuentes. |
| Pro | Selección, proyectos, sobre mí, conceptos y herramientas | Presentar propósito, métodos y resultados demostrables, con acceso al cuaderno de investigación. |
| Studio | Archivo visual, entrega de jornada y pizarrón | Verificar los formatos de descarga y el traslado Zaragoza → redacción; conservar texto alternativo y datos de cobertura. |
| Media | Vídeos, archivo, novedades e intros del autor | Revisar catálogo, subtítulos o alternativa escrita, atribuciones y relación con cada proyecto. |
| Pasaporte | Guardado local, texto, JSON, importación y borrado | Comprobar continuidad al cambiar de página y retorno desde herramientas; no mezclar notas de los otros cuadernos sin una acción explícita. |

Fuentes de datos locales a conservar: `zaragoza.json`, `comparador-grupo2.json`, `previas.json`, `claves-editoriales.json`, `momentos-partido.json`, `entregas-zaragoza.json`, `novedades.json` y `sofascore.json`. No se presupone que todas tengan el mismo corte ni la misma cobertura.

Generadores existentes: `actualizar_exploracion.py`, `actualizar_publicacion_jornada.py`, `actualizar_seo.py`, `previas.py`, `entregas.py`, `experiencia.py`, `segunda_edicion.py` y `exportar_lamina.py`; análisis en `analisis/` y cierre audiovisual en `contenidos/generar_cierre.py`. Su presencia en esta lista no implica que se hayan ejecutado ahora: hay que revisar su función antes de modificar sus salidas.

## Paquetes pendientes y condición de cierre

### A. Alcance, inventario y estructura — completado

- [x] Clasificar las 62 páginas y registrar ruta, título, canonical, indexación y scripts.
- [x] Fijar el contenido del primer estreno y separar investigaciones pendientes.
- [x] Elegir entradas reutilizadas y nuevas, sin renombrar URLs históricas.
- [x] Registrar las auditorías actuales y los límites de la verificación.

### B. Separar las áreas y conectar el recorrido — siguiente

- [ ] Crear entradas de área dentro del prototipo y una portada de orientación.
- [ ] Compartir cabecera, navegación y pie sin copiar ocho implementaciones diferentes.
- [ ] Cargar cada herramienta solo en su área; los scripts no deben exigir elementos de otras páginas.
- [ ] Conservar enlaces compartidos, selección de jornadas y continuidad del pasaporte al navegar.
- [ ] Comprobar portada → área → herramienta → retorno, con teclado y en móvil.

Se cierra cuando las ocho áreas tienen una entrada funcional en desarrollo y los recorridos no dependen de la página larga actual. Las rutas finales siguen sin activarse.

### C. Integrar catálogo y presentación — después de B

- [ ] Completar el catálogo de proyectos, juegos y vídeos con los recursos inventariados.
- [ ] Aplicar los ambientes acordados a las entradas y a los puntos de transición; conservar gráficos y datos legibles.
- [ ] Revisar instrucciones, fuentes, corte y límites de cada recurso incluido.
- [ ] Verificar las descargas que se anuncian: SVG, PNG, WebP, ZIP y textos según la herramienta.
- [ ] Revisar la regeneración: las actualizaciones habituales no deben borrar la estructura 2.0.

Se cierra cuando cada recurso del estreno tiene una ubicación, una entrada comprensible y un recorrido probado. No exige nuevas investigaciones.

### D. Datos, SEO y revisión final — después de C

- [ ] Resolver o etiquetar cada discrepancia relevante; no convertir datos ausentes en ceros.
- [ ] Preparar metadatos, sitemap y entradas finales conservando las 58 URLs actuales del mapa, salvo corrección justificada registrada.
- [ ] Probar las rutas históricas y sus excepciones de canonical y alias.
- [ ] Revisar accesibilidad, teclado, formularios, impresión y rendimiento medido; la estimación de peso no sustituye una medición de red.
- [ ] Ampliar la revisión a Firefox y WebKit, y usar dispositivo físico cuando sea accesible; registrar cualquier limitación pendiente.
- [ ] Entregar una versión candidata con capturas, pruebas y pendientes clasificados.

Se cierra cuando no quedan fallos que impidan navegar, interpretar datos o descargar los resultados anunciados, y los riesgos restantes están documentados.

### E. Aprobación y publicación — requiere aprobación del usuario

- [ ] Presentar la candidata y obtener aprobación explícita para publicar o fusionar.
- [ ] Preparar respaldo y procedimiento para volver a la versión anterior.
- [ ] Activar las rutas finales y metadatos públicos únicamente dentro del proceso aprobado.
- [ ] Publicar, verificar páginas y descargas principales, y registrar el resultado.

No se solicita aprobación durante A–D para trabajos reversibles dentro de la rama autorizada.

## Evidencia de este paquete

Las auditorías ejecutadas sobre el árbol local informan de 61 páginas con canonical correcto, 58 URLs indexables en sitemap y una 404 sin canonical por diseño. La auditoría de enlaces comprueba 62 páginas, 2.922 enlaces y recursos locales y 141 imágenes, sin incidencias. La auditoría de imágenes no encuentra atributos alternativos ausentes ni páginas por encima de su presupuesto estimado. La auditoría visual estática comprueba nombres accesibles, foco y ciertos controles, pero no sustituye una auditoría manual completa. Su universo incluye fragmentos y por eso cuenta 67 páginas, frente a las 62 del inventario.

El informe no certifica disponibilidad en Internet de cada enlace externo ni actualidad editorial de todas las páginas. No se han descargado de nuevo datos científicos ni ejecutado los análisis pesados para elaborar este inventario. No se ha publicado ni fusionado main.

## Seguimiento y estimación

Hay cuatro paquetes después de A: B, C, D y E. B es el trabajo inmediato. El avance se informa por condiciones de cierre, no por número de herramientas añadidas o cantidad de pruebas.

La referencia anterior de 5–8 jornadas efectivas era una estimación provisional del cierre completo, no una fecha comprometida. El inventario concreta el alcance, pero aún falta implementar B para medir el coste de separación y continuidad; no se reduce esa estimación por haber terminado solo la documentación. Se revisará al cerrar B y al detectar cualquier problema en los generadores existentes.

Inventario detallado: [tabla de rutas](linea2-inventario.md), [CSV](linea2-inventario.csv) y [JSON](linea2-inventario.json). Regeneración: `python herramientas/inventario_linea2.py`.
