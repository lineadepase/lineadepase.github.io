# Crear un club y gestionar su marca

En **Estadio → Fundar un club** se eligen nombre, ciudad, siglas, año, lema, afición, colores, forma y símbolo del escudo, bandera y estadio. Los diseños son gráficos originales parametrizados; no se importan marcas externas.

Se inicia una carrera nueva en Segunda sustituyendo una plaza, manteniendo 24 clubes y dos divisiones. Antes de reemplazar una carrera avanzada se pide confirmación. Exporta la partida anterior si quieres conservarla. Se generan 22 jugadores únicos y una academia. El capital fundador es de 8 millones menos el coste del estadio, que ya está construido al empezar. Las ampliaciones posteriores conservan el sistema de obras, costes y plazos existente.

Cuatro estadios: municipal, inglés, olímpico con pista y arena cubierta. Hay vista previa de cada opción, aforo y coste. El tipo también modifica la recreación 3D y los colores de las butacas.

En **Diseñar equipaciones y ropa** se personalizan camiseta local, visitante, chándal, ropa de paseo y bufanda. Cada prenda tiene dos colores y tres patrones. La colección se conserva al guardar/exportar; solo se cambia una colección existente cuando se agota su stock. El color de la camiseta local aparece en los retratos y jugadores 3D.

En **Tienda · ropa oficial** se fijan precios de 1 a 300 euros y se fabrican lotes de 1 a 1000 unidades pagando su coste. El stock limita las ventas. La demanda semanal depende del aforo, nivel de tienda y precio relativo; los precios altos reducen demanda, y vender por debajo del coste puede perder dinero. No se vende con el tiempo real del ordenador: avanza el calendario del juego. Cada fecha se liquida una vez, con un máximo de ocho semanas por salto. La pantalla muestra fabricación, facturación, flujo neto, unidades y últimas ventas; compras y ventas entran también en el balance. El ingreso de los servicios genéricos del estadio permanece separado del catálogo textil.

Pruebas: `node --test juego_futbol/tests/identidad-motor.test.cjs`; `node juego_futbol/tests/identidad.cjs` con el servidor local en 8765 y Playwright disponible. Cubren límites, costes, stock, elasticidad, liquidación única, fundación, diseños y persistencia en escritorio y móvil.
