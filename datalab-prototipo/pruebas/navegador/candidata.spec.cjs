const {test,expect}=require('@playwright/test');
const AxeBuilder=require('@axe-core/playwright').default;
const fs=require('node:fs/promises');
test.beforeEach(async({page})=>{await page.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());});
test('accesibilidad automática de inicio y áreas con sus controles activos',async({page},info)=>{
 const paths=['inicio','datalab','museo','play','zaragoza','pro','studio','media','pasaporte'];
 if(info.project.use.viewport.width>=1000)paths.push('historico-videos','historico-jornada','historico-archivo','historico-perfiles');
 const legacy={'historico-videos':'/videos/','historico-jornada':'/proyectos/real-zaragoza/jornada-13.html','historico-archivo':'/archivo-visual/','historico-perfiles':'/proyectos/liga-f-perfiles/'};
 for(const area of paths){
  const url=legacy[area]||(process.env.LDP_CANDIDATE_DIR?(area==='inicio'?'/':'/'+area+'/'):'/datalab-prototipo/'+area+'/');
  await page.goto(url);
  if(legacy[area]){await expect(page.locator('[data-preferencias-cookies]')).toBeVisible();const panel=page.locator('section.consentimiento');if(await panel.isVisible())await panel.getByRole('button',{name:'Rechazar',exact:true}).click();}
  const results=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']).analyze();
  await fs.writeFile(info.outputPath('axe-'+area+'.json'),JSON.stringify({url:page.url(),violations:results.violations,incomplete:results.incomplete},null,2));
  expect(results.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))})),area).toEqual([]);
 }
});


test('candidata conserva las 58 rutas previas y prepara metadatos de las nuevas',async({page,request},info)=>{
 test.skip(!process.env.LDP_CANDIDATE_DIR,'Necesita copia de candidata');
 const inventory=require('../../../documentacion/linea2-inventario.json');
 for(const item of inventory.rutas.filter(r=>r.en_sitemap)){
  const response=await request.get(item.ruta);expect(response.status(),item.ruta).toBe(200);
  expect(await response.text(),item.ruta).toContain('href="'+item.canonical+'"');
 }
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 for(const area of ['','datalab','museo','play','zaragoza','pro','studio','media','pasaporte']){
  await page.goto('/'+(area?area+'/':''));
  await expect(page.locator('link[rel="canonical"]')).toHaveAttribute('href','https://lineadepase.com/'+(area?area+'/':''));
  await expect(page.locator('meta[property="og:url"]')).toHaveAttribute('content','https://lineadepase.com/'+(area?area+'/':''));
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute('content',area==='pasaporte'?'noindex,follow':'index,follow');
  expect(await page.locator('meta[name="description"]').getAttribute('content')).not.toContain('desarrollo');
  if(['','zaragoza','media'].includes(area))await page.screenshot({path:info.outputPath('candidata-'+(area||'inicio')+'.png'),fullPage:true,style:'nav{position:static!important;}',animations:'disabled'});
 }
 const sitemap=await(await request.get('/sitemap.xml')).text();expect((sitemap.match(/<loc>/g)||[]).length).toBe(65);expect(sitemap).not.toContain('https://lineadepase.com/pasaporte/');
 await page.goto('/contacto/');await expect(page).toHaveURL(url=>url.pathname==='/sobre-mi/'&&url.hash==='#contacto');
 await page.goto('/play/');await page.locator('[data-resource="ciegas"]').getByRole('link').click();
 await expect(page.locator('[data-preferencias-cookies]')).toBeVisible();const panel=page.locator('section.consentimiento');if(await panel.isVisible())await panel.getByRole('button',{name:'Rechazar',exact:true}).click();
 await page.getByRole('link',{name:'Volver a Juegos →',exact:true}).click();await expect(page).toHaveURL(url=>url.pathname==='/play/');
 expect(errors).toEqual([]);
});

test('teclado e impresión conservan el acceso y las explicaciones',async({page},info)=>{
 const prefix=process.env.LDP_CANDIDATE_DIR?'':'/datalab-prototipo';
 await page.goto(prefix+'/datalab/');await page.keyboard.press('Tab');await expect(page.locator('.skip')).toBeFocused();
 await page.keyboard.press('Enter');await expect(page.locator('#contenido')).toBeFocused();
 const first=page.locator('main details').first();await expect(first).not.toHaveAttribute('open');
 await page.evaluate(()=>window.dispatchEvent(new Event('beforeprint')));await page.emulateMedia({media:'print'});
 await expect(page.locator('nav')).toBeHidden();await expect(first).toHaveAttribute('open','');
 await expect(page.locator('#datalab')).toHaveCSS('background-color','rgb(255, 255, 255)');
 await page.screenshot({path:info.outputPath('impresion-datalab.png'),fullPage:true,animations:'disabled'});
 await page.evaluate(()=>window.dispatchEvent(new Event('afterprint')));await page.emulateMedia({media:'screen'});await expect(first).not.toHaveAttribute('open');
});

test('primera carga mide recursos reales y no envía datos a servicios externos',async({page},info)=>{
 const responses=[];page.on('response',r=>responses.push(r));
 const url=process.env.LDP_CANDIDATE_DIR?'/':'/datalab-prototipo/inicio/';await page.goto(url);
 const resources=await Promise.all(responses.map(async r=>({url:r.url(),status:r.status(),bytes:Number(await r.headerValue('content-length')||0)})));
 const navigation=await page.evaluate(()=>{const e=performance.getEntriesByType('navigation')[0];return e?{domContentLoaded:e.domContentLoadedEventEnd,response:e.responseEnd}:null;});
 const total=resources.reduce((a,r)=>a+r.bytes,0);
 await fs.writeFile(info.outputPath('rendimiento-local.json'),JSON.stringify({url:page.url(),resources,totalBodyBytes:total,navigation,limitacion:'Servidor estático local, sin compresión ni red móvil; no son métricas de campo.'},null,2));
 expect(total).toBeGreaterThan(10000);expect(total).toBeLessThan(1024*1024);
 expect(resources.every(r=>new URL(r.url).hostname==='127.0.0.1')).toBe(true);
});

test('sin almacenamiento se conserva la nota en pantalla y se informa del fallo',async({page})=>{
 await page.addInitScript(()=>{Storage.prototype.setItem=function(){throw new DOMException('Bloqueado en la prueba','SecurityError');};});
 const prefix=process.env.LDP_CANDIDATE_DIR?'':'/datalab-prototipo';await page.goto(prefix+'/pasaporte/');
 await page.locator('#nota').fill('Mi nota sigue disponible para descargar.');
 await expect(page.locator('#guardado')).toContainText('No se puede guardar');await expect(page.locator('#nota')).toHaveValue('Mi nota sigue disponible para descargar.');
 const download=page.waitForEvent('download');await page.locator('#exportar').click();expect((await fs.readFile(await(await download).path(),'utf8'))).toContain('Mi nota sigue disponible');
});
