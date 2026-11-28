const {test,expect}=require('@playwright/test');
const fs=require('node:fs/promises');
const entry='/datalab-prototipo/';
test.beforeEach(async({page})=>{
 await page.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
});

test('inicio y ocho áreas funcionan aisladas y con navegación de retorno',async({page},info)=>{
 const errors=[];page.on('pageerror',error=>errors.push(error.message));
 await page.goto(entry+'inicio/');
 await expect(page.locator('h1')).toHaveText('Elige tu recorrido');
 await expect(page.locator('#tiros')).toHaveCount(0);
 await page.screenshot({path:info.outputPath('inicio.png'),fullPage:true,animations:'disabled'});
 for(const area of ['datalab','museo','play','zaragoza','pro','studio','media','pasaporte']){
  await page.getByRole('navigation',{name:'Áreas de Línea de Pase'}).getByRole('link',{name:new RegExp('^'+area+'$','i')}).click();
  await expect(page).toHaveURL(new RegExp('/'+area+'/$'));
  await expect(page.locator('nav [aria-current="page"]')).toHaveCount(1);
  await expect(page.locator('main section')).toHaveCount(1);
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute('content','noindex,nofollow');
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBe(true);
  if(area==='play'){
   await expect(page.locator('#tiros')).toHaveCount(0);
   await page.locator('[data-answer]').nth(1).click();
   await expect(page.locator('#respuesta')).toContainText('Correcto');
  }
  if(area==='datalab'){
   await page.locator('#prob').press('End');
   await expect(page.locator('#resultado')).toHaveText('100 %');
   await expect(page.locator('#temporada-datos')).toHaveCount(0);
  }
  await page.screenshot({path:info.outputPath(area+'.png'),fullPage:true,animations:'disabled'});
 }
 await page.getByRole('link',{name:'← Inicio por recorridos',exact:true}).click();
 await expect(page).toHaveURL(/\/inicio\/$/);
 expect(errors).toEqual([]);
});

test('pasaporte y borrador de Pro continúan entre páginas',async({page})=>{
 await page.goto(entry+'datalab/');
 await page.locator('#sello-datalab').click();
 await page.getByRole('navigation').getByRole('link',{name:'Pasaporte',exact:true}).click();
 await expect(page.locator('#progreso')).toHaveText('1 de 7 áreas exploradas');
 await page.locator('#nota').fill('Mi nota permanece entre áreas.');
 await expect(page.locator('#pasaporte-retomar')).toHaveAttribute('href','../museo/');
 await page.locator('#pasaporte-retomar').click();await page.locator('#sello-museo').click();
 await page.getByRole('navigation').getByRole('link',{name:'Pro',exact:true}).click();
 await page.locator('#pro-pregunta').fill('Mi investigación');await page.locator('#pro-guardar').click();
 await page.getByRole('navigation').getByRole('link',{name:'Pasaporte',exact:true}).click();
 await expect(page.locator('#progreso')).toHaveText('2 de 7 áreas exploradas');
 await expect(page.locator('#nota')).toHaveValue('Mi nota permanece entre áreas.');
 await page.getByRole('navigation').getByRole('link',{name:'Pro',exact:true}).click();
 await expect(page.locator('#pro-pregunta')).toHaveValue('Mi investigación');
 // La vista continua conserva las mismas claves de almacenamiento.
 await page.goto(entry+'#pasaporte');
 await expect(page.locator('#progreso')).toHaveText('2 de 7 áreas exploradas');
 await expect(page.locator('#nota')).toHaveValue('Mi nota permanece entre áreas.');
});

test('Zaragoza pasa dos identificadores a Studio y sus fuentes conservan la ruta',async({page})=>{
 await page.goto(entry+'zaragoza/');
 const boxes=page.locator('[data-compare-id]');await boxes.nth(1).check();await boxes.nth(2).check();
 const compare=new URL(await page.locator('#temporada-studio').getAttribute('href'));
 expect(compare.pathname).toBe('/archivo-visual/');
 await page.locator('#temporada-redaccion').click();
 await expect(page).toHaveURL(/\/studio\/\?partido_a=.*partido_b=/);
 expect(page.url()).not.toContain('nota=');
 await expect(page.locator('#editorial-a')).toHaveValue('1');await expect(page.locator('#editorial-b')).toHaveValue('2');
 await page.locator('#editorial-pregunta').fill('¿Qué muestran estas jornadas?');
 await page.getByRole('button',{name:'Preparar borrador',exact:true}).click();
 const download=page.waitForEvent('download');await page.locator('#editorial-descargar').click();
 const text=await fs.readFile(await(await download).path(),'utf8');
 expect(text).toContain('/proyectos/real-zaragoza/jornada-2.html');
 expect(text).not.toContain('/datalab-prototipo/proyectos/');
 await page.goto(entry+'studio/?partido_a=invalido&partido_b=invalido');
 await expect(page.locator('#editorial-estado')).toContainText('no está disponible');
});

test('vistas compartidas y cuaderno de Museo conservan enlaces desde las áreas',async({page})=>{
 await page.goto(entry+'datalab/?n=2&p=50&mn=20&mk=4#datalab');
 await expect(page.locator('#resultado')).toHaveText('75 %');
 await page.locator('#laboratorios-enlace').click();
 const link=await page.locator('#laboratorios-url').inputValue();expect(new URL(link).pathname).toBe(entry+'datalab/');
 await page.goto(link);await expect(page.locator('#resultado')).toHaveText('75 %');
 await page.getByRole('navigation').getByRole('link',{name:'Museo',exact:true}).click();
 await page.locator('#museo-observo').fill('Mi observación.');
 const download=page.waitForEvent('download');await page.getByRole('button',{name:'Descargar mi cuaderno de visita'}).click();
 const text=await fs.readFile(await(await download).path(),'utf8');
 expect(text).toContain('/proyectos/espana-eurocopa-redes/');expect(text).not.toContain('/datalab-prototipo/proyectos/');
});


test('inicio por recorridos y entradas siguen navegables sin JavaScript',async({browser,baseURL},info)=>{
 const context=await browser.newContext({javaScriptEnabled:false,baseURL,viewport:info.project.use.viewport});
 const page=await context.newPage();await page.goto(entry+'inicio/');
 await page.getByRole('link',{name:'Entrar en Studio →',exact:true}).click();
 await expect(page).toHaveURL(/studio\/#studio$/);
 await expect(page.locator('#studio-form')).toHaveAttribute('action','../../archivo-visual/#titulo-comparar');
 await page.getByRole('link',{name:'← Inicio por recorridos',exact:true}).click();
 await page.locator('#indice-experiencias summary').click();
 await page.locator('#indice-experiencias').getByRole('link',{name:'Preparar mi cuaderno de visita',exact:true}).click();
 await expect(page).toHaveURL(/museo\/#museo-cuaderno-titulo$/);
 await context.close();
});
