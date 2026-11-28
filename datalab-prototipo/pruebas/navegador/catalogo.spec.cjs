const {test,expect}=require('@playwright/test');
const fs=require('node:fs/promises');
const resources=require('../../../datos/linea2-catalogo.json').recursos;
const entry='/datalab-prototipo/';
test.beforeEach(async({page})=>{
 await page.route('**/*',route=>new URL(route.request().url()).origin==='http://127.0.0.1:4173'?route.continue():route.abort());
});
async function dismissCookies(page){await expect(page.locator('[data-preferencias-cookies]')).toBeVisible();const panel=page.locator('section.consentimiento');if(await panel.isVisible()){await panel.getByRole('button',{name:'Rechazar',exact:true}).click();await expect(panel).toBeHidden();}}
async function downloadBytes(page,locator){await dismissCookies(page);await locator.scrollIntoViewIfNeeded();const [download]=await Promise.all([page.waitForEvent('download'),locator.click()]);return {name:download.suggestedFilename(),bytes:await fs.readFile(await download.path())};}
function zipEntries(bytes){
 const files=new Map();let offset=0;
 while(bytes.readUInt32LE(offset)===0x04034b50){
  expect(bytes.readUInt16LE(offset+8)).toBe(0);
  const size=bytes.readUInt32LE(offset+18),nameLength=bytes.readUInt16LE(offset+26),extra=bytes.readUInt16LE(offset+28);
  const name=bytes.subarray(offset+30,offset+30+nameLength).toString('utf8'),start=offset+30+nameLength+extra;
  files.set(name,bytes.subarray(start,start+size));offset=start+size;
 }
 expect(bytes.readUInt32LE(offset)).toBe(0x02014b50);return files;
}

test('catálogo conserva los 35 destinos y explica contexto y límites',async({page,request},info)=>{
 for(const area of ['datalab','museo','play','zaragoza','pro','studio','media']){
  await page.goto(entry+area+'/');
  const selected=resources.filter(r=>r.areas.includes(area)),catalogue=page.locator('#catalogo-'+area);
  await expect(catalogue.locator('[data-resource]')).toHaveCount(selected.length);
  await catalogue.locator('summary').first().click();
  await expect(catalogue.locator('details').first()).toContainText('Contexto:');
  await expect(catalogue.locator('details').first()).toContainText('Límite:');
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBe(true);
  if(['play','datalab','media'].includes(area))await catalogue.screenshot({path:info.outputPath('catalogo-'+area+'.png'),animations:'disabled',style:'nav{position:static!important;}'});
 }
 for(const item of resources){const response=await request.get('/'+item.url.split('#')[0]);expect(response.status(),item.id).toBe(200);}
 await page.goto(entry+'play/');await expect(page.locator('[data-resource="balance"] .resource-kind')).toHaveText('Registro editorial');
});

test('siete recursos de Play funcionan y permiten volver al área',async({page},info)=>{
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 for(const item of resources.filter(r=>r.areas.includes('play'))){
  await page.goto(entry+'play/');await page.locator('[data-resource="'+item.id+'"]').getByRole('link').click();await dismissCookies(page);
  await expect(page.locator('.linea2-retorno')).toContainText('Vienes de Play');
  if(item.id==='ciegas'){
   const card=page.locator('.reto-marcador').first();await card.locator('[name="local"]').fill('0');await card.locator('[name="visitante"]').fill('0');
   await card.getByRole('button',{name:'Comprobar mi marcador'}).click();await expect(card.locator('.marcador-ciego-revelar')).toHaveAttribute('open','');await expect(card.locator('button')).toBeDisabled();
  }
  if(item.id==='espejo'){await page.locator('#comparar-espejo').click();await expect(page.locator('#resultado-espejo h3')).toHaveCount(2);}
  if(item.id==='reloj'){await page.locator('#selector-reloj').selectOption({index:1});await expect(page.locator('#reloj-resultado')).toContainText('Resultado final:');}
  if(item.id==='esquemas'){await page.locator('[data-elegir-fase="presion"]').click();await expect(page.locator('[data-elegir-fase="presion"]')).toHaveAttribute('aria-pressed','true');await expect(page.locator('[data-campo-nombre]')).toContainText('Presión');}
  await page.getByRole('link',{name:'Volver a Play →',exact:true}).click();await expect(page).toHaveURL(/\/play\/$/);
 }
 expect(errors).toEqual([]);
 await page.goto('/marcador-a-ciegas/?ldp_origen=https://example.com/');await expect(page.locator('.linea2-retorno')).toHaveCount(0);
});

test('Studio exporta archivos SVG, PNG, WebP, ZIP y texto con contenido real',async({page},info)=>{
 await page.goto(entry+'studio/');await page.locator('[data-resource="archivo-visual"]').getByRole('link').click();await dismissCookies(page);
 await expect(page.locator('.linea2-retorno')).toContainText('Studio');
 await page.locator('#formato-comparacion').selectOption('apaisado');
 let file=await downloadBytes(page,page.locator('[data-descargar-comparacion="svg"]:visible').first());
 expect(file.name).toMatch(/\.svg$/);expect(file.bytes.toString()).toContain('<svg');expect(file.bytes.toString()).toContain('<desc');
 file=await downloadBytes(page,page.locator('[data-descargar-comparacion="png"]').first());
 expect(file.bytes.subarray(0,8)).toEqual(Buffer.from([137,80,78,71,13,10,26,10]));expect(file.bytes.readUInt32BE(16)).toBe(1200);expect(file.bytes.readUInt32BE(20)).toBe(630);
 await fs.writeFile(info.outputPath('comparacion.png'),file.bytes);
 file=await downloadBytes(page,page.locator('[data-descargar-comparacion="webp"]').first());expect(file.bytes.subarray(0,4).toString()).toBe('RIFF');expect(file.bytes.subarray(8,12).toString()).toBe('WEBP');
 await page.locator('#formato-kit').selectOption('svg');file=await downloadBytes(page,page.locator('[data-descargar-kit]'));
 const files=zipEntries(file.bytes);expect([...files.keys()].sort()).toEqual(['cuadrado.svg','historias.svg','texto-alternativo.txt','vertical.svg']);
 for(const name of ['cuadrado.svg','historias.svg','vertical.svg'])expect(files.get(name).toString()).toContain('<svg');
 expect(files.get('texto-alternativo.txt').toString().length).toBeGreaterThan(30);
 await page.locator('#formato-comparacion').selectOption('carrusel');
 file=await downloadBytes(page,page.locator('[data-descargar-comparacion="svg"]:visible').first());
 const slides=zipEntries(file.bytes);expect(slides.size).toBe(2);for(const bytes of slides.values())expect(bytes.toString()).toContain('<svg');
 await page.locator('#tipo-mapa').selectOption('webp');await page.locator('#formato-mapa').selectOption('cuadrado');
 file=await downloadBytes(page,page.locator('[data-descargar-mapa]'));expect(file.name).toMatch(/\.zip$/);const mapPages=zipEntries(file.bytes);expect(mapPages.size).toBe(2);for(const bytes of mapPages.values())expect(bytes.subarray(8,12).toString()).toBe('WEBP');
 file=await downloadBytes(page,page.locator('[data-descargar-comparacion-texto]'));expect(file.bytes.toString()).toContain('Zaragoza');
 await page.getByRole('link',{name:'Volver a Studio →',exact:true}).click();
 await page.locator('[data-resource="pizarron"]').getByRole('link').click();
 await expect(page.locator('[data-estado-jugada]')).toContainText('Paso 3 de 3');await page.locator('[data-retroceder]').click();await expect(page.locator('[data-estado-jugada]')).toContainText('Paso 2 de 3');
});

test('Media enlaza los tres vídeos sin convertirlos en investigaciones nuevas',async({page})=>{
 await page.goto(entry+'media/');
 for(const id of ['video-xg','video-modelo','video-fvs'])await expect(page.locator('[data-resource="'+id+'"]')).toBeVisible();
 await page.locator('[data-resource="video-modelo"] summary').click();await expect(page.locator('[data-resource="video-modelo"]')).toContainText('no acredita');
 await page.locator('[data-resource="video-xg"]').getByRole('link').click();await dismissCookies(page);
 await expect(page.locator('#xg-sin-lios video')).toHaveAttribute('preload','none');
 await expect(page.locator('#xg-sin-lios video')).not.toHaveAttribute('autoplay');
 await expect(page.locator('#modelo-xg iframe')).toHaveAttribute('src',/youtube-nocookie/);
 await page.getByRole('link',{name:'Volver a Media →',exact:true}).click();await expect(page).toHaveURL(/\/media\/$/);
});
