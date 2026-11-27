const {test,expect}=require('@playwright/test');
const fs=require('node:fs/promises');
const entry='/datalab-prototipo/';
test.beforeEach(async({page})=>{
  await page.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
});

test('portada, áreas, imágenes y capturas sin desbordamiento global',async({page},info)=>{
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(entry);
  await expect(page.locator('.skip')).toHaveCSS('opacity','0');
  await expect(page.locator('#distribucion-cuerpo tr')).toHaveCount(6);
  await expect(page.locator('#temporada-controles')).toBeVisible();
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBe(true);
  await page.screenshot({path:info.outputPath('portada.png'),animations:'disabled'});
  for(const area of ['datalab','museo','play','zaragoza','pro','studio','media','pasaporte']){
    const section=page.locator('section#'+area);
    await section.scrollIntoViewIfNeeded();
    await expect(section).toBeVisible();
    await section.screenshot({path:info.outputPath(area+'.png'),animations:'disabled',style:'nav { position: static !important; }'});
    expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBe(true);
  }
  for(const img of await page.locator('#museo img').all())expect(await img.evaluate(el=>el.complete&&el.naturalWidth>0)).toBe(true);
  expect(errors).toEqual([]);
});

test('restauración del experimento y cambios por teclado',async({page})=>{
  await page.goto(entry+'?n=2&p=50&mn=200&mk=40#datalab');
  await expect(page.locator('#resultado')).toHaveText('75 %');
  await expect(page.locator('#n')).toHaveText('2');
  await expect(page.locator('#muestra-resultado')).toHaveText('20 %');
  await page.locator('#prob').press('Home');
  await expect(page.locator('#resultado')).toHaveText('0 %');
  await page.locator('#prob').press('End');
  await expect(page.locator('#resultado')).toHaveText('100 %');
  await page.locator('#simular').click();
  await expect(page.locator('#simulacion')).toContainText('2 goles');
});

test('reto completo y reinicio',async({page})=>{
  await page.goto(entry+'#play');
  await page.getByRole('button',{name:'75 %',exact:true}).click();
  await page.getByRole('button',{name:'Siguiente pregunta',exact:true}).click();
  await page.getByRole('button',{name:'Sus ocasiones suman 2 goles esperados',exact:true}).click();
  await page.getByRole('button',{name:'Siguiente pregunta',exact:true}).click();
  await page.getByRole('button',{name:'No, un solo partido no basta',exact:true}).click();
  await page.getByRole('button',{name:'Ver resultado',exact:true}).click();
  await expect(page.locator('#reto-progreso')).toContainText('3 de 3 aciertos');
  await expect(page.locator('#reto-historial li')).toHaveCount(3);
  await expect(page.locator('#reto-resumen')).toContainText('Has acertado 3 de 3');
  await page.getByRole('button',{name:'Volver a empezar',exact:true}).click();
  await expect(page.locator('#reto-progreso')).toContainText('Pregunta 1 de 3');
});

test('pasaporte persistente, descarga e importación con confirmación',async({page})=>{
  await page.goto(entry);
  await page.locator('#sello-datalab').click();
  await page.locator('#nota').fill('Nota de prueba del navegador');
  await page.reload();
  await expect(page.locator('#nota')).toHaveValue('Nota de prueba del navegador');
  await expect(page.locator('#sello-datalab')).toHaveAttribute('aria-pressed','true');
  await page.getByText('Llevar mi pasaporte a otro navegador',{exact:true}).click();
  const downloadEvent=page.waitForEvent('download');
  await page.locator('#pasaporte-json').click();
  const download=await downloadEvent;
  const backup=JSON.parse(await fs.readFile(await download.path(),'utf8'));
  expect(backup.nota).toBe('Nota de prueba del navegador');
  expect(backup.areas).toContain('DataLab');
  await page.locator('#borrar').click();
  await expect(page.locator('#nota')).toHaveValue('');
  await page.locator('#pasaporte-archivo').setInputFiles({name:'pasaporte.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(backup))});
  await expect(page.locator('#pasaporte-aplicar')).toBeEnabled();
  await expect(page.locator('#nota')).toHaveValue('');
  await page.locator('#pasaporte-aplicar').click();
  await expect(page.locator('#nota')).toHaveValue('Nota de prueba del navegador');
});

test('filtros, descarga CSV y comparación real de dos jornadas',async({page})=>{
  await page.goto(entry+'#zaragoza');
  await page.locator('#temporada-sede').selectOption('Casa');
  await page.locator('#temporada-cobertura').selectOption('Solo completas');
  const visibleRows=page.locator('[data-season-row]:visible');
  expect(await visibleRows.count()).toBeGreaterThanOrEqual(2);
  const downloadEvent=page.waitForEvent('download');
  await page.locator('#temporada-csv').click();
  const csv=await fs.readFile(await(await downloadEvent).path(),'utf8');
  expect(csv).toContain('Fuente por jornada');
  const checks=page.locator('[data-compare-id]:visible');
  const first=await checks.nth(0).getAttribute('data-compare-id'),second=await checks.nth(1).getAttribute('data-compare-id');
  await checks.nth(0).check();await checks.nth(1).check();
  await page.locator('#temporada-studio').click();
  await expect(page).toHaveURL(/archivo-visual\/\?jornada_a=/);
  await expect(page.locator('#comparar-jornada-a')).toHaveValue(first);
  await expect(page.locator('#comparar-jornada-b')).toHaveValue(second);
});

test('enlace compartible y acceso por teclado',async({page})=>{
  await page.goto(entry+'?sede=Fuera&resultado=Victoria#zaragoza');
  await expect(page.locator('#temporada-sede')).toHaveValue('Fuera');
  await page.locator('#temporada-enlace').click();
  const link=await page.locator('#temporada-url').inputValue();
  expect(link).not.toContain('nota');
  await page.goto(link);
  await expect(page.locator('#temporada-sede')).toHaveValue('Fuera');
  await expect(page.locator('#temporada-resultado')).toHaveValue('Victoria');
  await page.goto(entry);
  await page.keyboard.press('Tab');
  await expect(page.getByRole('link',{name:'Saltar al contenido',exact:true})).toBeFocused();
  await expect(page.locator('.skip')).toHaveCSS('opacity','1');
});

test('Studio transfiere temporada y formato al mapa existente',async({page})=>{
  await page.goto(entry+'#studio');
  const season=await page.locator('#studio-mapa-temporada').inputValue();
  await page.locator('#studio-mapa-formato').selectOption('historias');
  await page.getByRole('button',{name:'Preparar mapa en el taller →',exact:true}).click();
  await expect(page).toHaveURL(/archivo-visual\/\?mapa-temporada=/);
  await expect(page.locator('#temporada-mapa')).toHaveValue(season);
  await expect(page.locator('#formato-mapa')).toHaveValue('historias');
});

test('DataLab compara escenarios y permite restablecerlos',async({page})=>{
 await page.goto(entry+'#titulo-escenarios');
 await expect(page.locator('#escenario-a-xg')).toHaveText('1');
 await expect(page.locator('#escenario-b-xg')).toHaveText('1');
 await expect(page.locator('#escenario-a-gol')).toHaveText('65,1 %');
 await expect(page.locator('#escenario-b-gol')).toHaveText('75 %');
 await page.locator('#escenario-a-p').press('Home');
 await expect(page.locator('#escenario-a-gol')).toHaveText('0 %');
 await page.locator('#escenarios-restablecer').click();
 await expect(page.locator('#escenarios-lectura')).toContainText('Ambos escenarios suman 1');
});

test('Pro guarda, recupera y descarga una ficha sin inventar apartados',async({page})=>{
 await page.goto(entry+'#pro');
 await page.locator('#pro-pregunta').fill('¿Cómo cambia el rendimiento entre casa y fuera?');
 await page.locator('#pro-metodo').fill('Comparación descriptiva con cobertura y fecha de corte.');
 await page.locator('#pro-guardar').click();
 await page.reload();
 await expect(page.locator('#pro-pregunta')).toHaveValue('¿Cómo cambia el rendimiento entre casa y fuera?');
 const event=page.waitForEvent('download');
 await page.getByRole('button',{name:'Descargar ficha de investigación',exact:true}).click();
 const content=await fs.readFile(await(await event).path(),'utf8');
 expect(content).toContain('Pendiente de definir.');
 expect(content).toContain('Comparación descriptiva');
 await page.locator('#pro-borrar').click();
 await page.reload();
 await expect(page.locator('#pro-pregunta')).toHaveValue('');
});


test('trivial cambia de tema, explica respuestas y enlaza al pasaporte',async({page})=>{
 await page.goto(entry+'#play');
 await page.locator('#reto-tema').selectOption('lectura');
 await expect(page.locator('#reto-pregunta')).toContainText('posesión');
 await page.locator('[data-answer]').nth(2).click();
 await expect(page.locator('#respuesta')).toContainText('Correcto.');
 await page.locator('#reto-siguiente').click();
 await page.locator('[data-answer]').nth(1).click();
 await expect(page.locator('#respuesta')).toContainText('Ausencia de dato no significa cero');
 await page.locator('#reto-siguiente').click();
 await page.locator('[data-answer]').nth(2).click();
 await page.locator('#reto-siguiente').click();
 await expect(page.locator('#reto-resumen')).toContainText('3 de 3');
 await expect(page.locator('#reto-resumen a').first()).toHaveAttribute('href','#sello-play');
 await page.locator('#reto-tema').selectOption('metodo');
 await expect(page.locator('#reto-progreso')).toContainText('Aciertos: 0');
 await expect(page.locator('#reto-historial li')).toHaveCount(0);
 await expect(page.locator('#reto-resumen')).toBeHidden();
 await page.locator('[data-answer]').nth(0).click();
 await expect(page.locator('#respuesta')).toContainText('definición');
 await page.locator('#reto-reiniciar').click();
 await expect(page.locator('[data-answer]').nth(0)).toBeEnabled();
});


test('Studio prepara un borrador trazable y descarta vistas antiguas',async({page})=>{
 await page.goto(entry+'#studio');
 await page.locator('#editorial-pregunta').fill('¿Qué cambia entre estas jornadas?');
 await page.locator('#editorial-nota').fill('Una comparación para revisar, sin concluir causalidad.');
 await page.getByRole('button',{name:'Preparar borrador',exact:true}).click();
 await expect(page.locator('#editorial-texto')).toHaveValue(/Estadísticas pendientes de validación/);
 await expect(page.locator('#editorial-texto')).toHaveValue(/jornada-1.html/);
 await expect(page.locator('#editorial-texto')).toHaveValue(/CORTE DE LOS DATOS/);
 const download=page.waitForEvent('download');
 await page.getByRole('button',{name:'Descargar borrador de publicación',exact:true}).click();
 const text=await fs.readFile(await(await download).path(),'utf8');
 expect(text).toContain('BORRADOR DE PUBLICACIÓN');expect(text).toContain('sin concluir causalidad');
 await page.locator('#editorial-a').selectOption('1');
 await expect(page.locator('#editorial-salida')).toBeHidden();
 await page.getByRole('button',{name:'Preparar borrador',exact:true}).click();
 await expect(page.locator('#editorial-estado')).toContainText('dos jornadas distintas');
 await page.reload();
 await expect(page.locator('#editorial-nota')).toHaveValue('');
});


test('Zaragoza traslada la pareja a redacción conservando texto e invalidando salida',async({page})=>{
 await page.goto(entry+'#studio');
 await page.locator('#editorial-pregunta').fill('Mi pregunta');
 await page.locator('#editorial-nota').fill('Mi lectura personal');
 await page.getByRole('button',{name:'Preparar borrador',exact:true}).click();
 await expect(page.locator('#editorial-salida')).toBeVisible();
 const boxes=page.locator('[data-compare-id]');
 await boxes.nth(2).check();
 await expect(page.locator('#temporada-redaccion')).toBeHidden();
 await boxes.nth(3).check();
 await page.locator('#temporada-redaccion').click();
 await expect(page.locator('#editorial-a')).toHaveValue('2');
 await expect(page.locator('#editorial-b')).toHaveValue('3');
 await expect(page.locator('#editorial-pregunta')).toHaveValue('Mi pregunta');
 await expect(page.locator('#editorial-pregunta')).toBeFocused();
 await expect(page.locator('#editorial-nota')).toHaveValue('Mi lectura personal');
 await expect(page.locator('#editorial-salida')).toBeHidden();
 await boxes.nth(2).uncheck();
 await expect(page.locator('#temporada-redaccion')).toBeHidden();
});
