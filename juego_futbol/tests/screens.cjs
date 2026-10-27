// Recorre todas las vistas y páginas, detecta contenido recortado y juega una temporada.
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs/promises');
const path=require('node:path');
const base=process.env.GAME_URL||'http://127.0.0.1:8765/juego_futbol/';
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.PLAYWRIGHT_CHANNEL?{channel:process.env.PLAYWRIGHT_CHANNEL}:{})});
 const out=path.join(__dirname,'test-artifacts');await fs.mkdir(out,{recursive:true});
 try{
 for(const [name,width,height] of [['desktop',1366,900],['mobile',390,844],['small',320,568],['landscape',844,390]]){
  const page=await browser.newPage({viewport:{width,height}}),errors=[];
  page.on('pageerror',e=>errors.push(e.message));await page.goto(base);
  await page.waitForSelector('.screen-mode');await page.waitForTimeout(150);
  let count=0;
  for(const section of ['clasificacion','tactica','mercado','partido','entrenamiento','finanzas','estadio','cantera','bigdata','ajustes']){
   await page.locator('#pestana-'+section).click();
   const options=await page.locator('#screen-view option').count();
   for(let i=0;i<options;i++){
    await page.locator('#screen-view').selectOption(String(i));await page.waitForTimeout(30);
    const expected=await page.evaluate(()=>[...document.querySelector('.screen-view:not([hidden])').querySelectorAll('*')]
      .filter(n=>!n.children.length&&!n.closest('thead,svg,select,[hidden],[data-player-detail],.pass-pitch:not(.active)')&&n.textContent.trim())
      .map(n=>n.textContent.replace(/\s+/g,' ').trim()));
    const seen=new Set();
    for(let n=0;n<200;n++){
     const result=await page.evaluate(()=>{
      const root=document.querySelector('.screen-view:not([hidden])');
      return {title:root.dataset.title,page:document.getElementById('screen-page').textContent,
       overflowY:root.scrollHeight-root.clientHeight,overflowX:root.scrollWidth-root.clientWidth,
       bodyY:document.body.scrollHeight-innerHeight,bodyX:document.body.scrollWidth-innerWidth,
       footer:document.querySelector('.screen-footer').getBoundingClientRect().bottom,
       cta:document.getElementById('floating-cta').getBoundingClientRect().toJSON(),
       texts:[...root.querySelectorAll('*')].filter(n=>!n.children.length&&n.getClientRects().length).map(n=>n.textContent.replace(/\s+/g,' ').trim()),
       visible:[...root.querySelectorAll('button,input,select,canvas,svg,td,p,h2,h3')].filter(e=>e.getClientRects().length).map(e=>({id:e.id,tag:e.tagName,b:e.getBoundingClientRect().bottom,r:e.getBoundingClientRect().right})),bottom:root.getBoundingClientRect().bottom};
     });
     assert.ok(result.overflowY<=2&&result.overflowX<=2&&result.bodyY<=2&&result.bodyX<=2,`${name}/${section}/${i}: ${JSON.stringify(result)}`);
     assert.ok(result.footer<=height+1,`${name}: controles fuera de pantalla`);
     assert.ok(result.cta.left>=0&&result.cta.right<=width+1,`${name}: botón principal recortado`);
     result.texts.forEach(text=>seen.add(text));
     count++;
     if(await page.locator('#screen-next').isDisabled())break;
     await page.locator('#screen-next').click();
     assert.ok(n<199,'paginación infinita');
    }
    expected.forEach(text=>assert.ok(seen.has(text),`${name}/${section}/${i}: texto inaccesible: ${text}`));
   }
  }
  await page.locator('#pestana-tactica').click();await page.locator('#screen-view').selectOption('1');
  await page.screenshot({path:path.join(out,`screens-${name}.png`)});
  assert.deepEqual(errors,[]);console.log(`${name}: ${count} páginas sin desbordamientos`);
  await page.close();
 }
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
