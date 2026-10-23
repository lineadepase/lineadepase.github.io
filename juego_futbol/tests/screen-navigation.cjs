// Los recorridos de motor ahora deben abrir la vista y página del control.
// La prueba screens.cjs comprueba por separado toda la navegación visible.
let installed=false;
exports.installScreenNavigation=page=>{
 if(installed)return;installed=true;
 const prototype=Object.getPrototypeOf(page.locator('body'));
 async function reveal(locator){
  const page=locator.page();
  if(!await page.locator('.screen-mode').count()||!await locator.count())return;
  const destination=await locator.first().evaluate(el=>{
   const view=el.closest('.screen-view');if(!view)return null;
   return {section:view.closest('.tab-content').id.replace('tab-',''),index:[...view.parentNode.children].indexOf(view)};
  });
  if(!destination)return;
  const section=page.locator('#pestana-'+destination.section);
  if(await section.getAttribute('aria-selected')!=='true')await section.click();
  if(await page.locator('#screen-view').inputValue()!==String(destination.index))await page.selectOption('#screen-view',String(destination.index));
  await page.waitForTimeout(25);
  if(await locator.first().isVisible())return;
  while(!await page.locator('#screen-previous').isDisabled())await page.locator('#screen-previous').click();
  for(let i=0;i<100;i++){
   if(await locator.first().isVisible())return;
   if(await page.locator('#screen-next').isDisabled())break;
   await page.locator('#screen-next').click();
  }
 }
 for(const method of ['click','fill','selectOption','focus','scrollIntoViewIfNeeded']){
  const original=prototype[method];prototype[method]=async function(...args){await reveal(this);return original.apply(this,args);};
 }
};
