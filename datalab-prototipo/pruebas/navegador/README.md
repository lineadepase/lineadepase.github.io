# Revisión en navegador

Estas pruebas se ejecutan en GitHub Actions sobre la rama de desarrollo. No despliegan la web ni modifican main.

Se usa Chromium en cuatro tamaños: escritorio (1440), tablet (820), móvil (390) y móvil estrecho (320). El contexto es nuevo en cada prueba, la hora local es Europe/Madrid y se bloquean las peticiones a servicios externos. Los datos y notas usados para probar el pasaporte son ficticios.

El informe guarda capturas por área y trazas de los fallos durante 14 días. Generar una captura no equivale a revisarla visualmente: el resultado debe inspeccionarse antes de dar la revisión visual por terminada.

Desde esta carpeta, en un entorno Linux con Python 3:

```
npm ci --ignore-scripts
npx playwright install --with-deps chromium
npm test
```

Las dependencias están fijadas en package-lock.json. No se requiere ningún secreto de producción. El servidor de prueba se limita a 127.0.0.1.
