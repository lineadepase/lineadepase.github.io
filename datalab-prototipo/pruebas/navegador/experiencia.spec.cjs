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
