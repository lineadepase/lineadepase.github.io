const {defineConfig}=require('@playwright/test');
const path=require('node:path');
const root=path.resolve(__dirname,'../../..');
const servedRoot=process.env.LDP_CANDIDATE_DIR||root;
const engine=process.env.LDP_ENGINE||'chromium';
if(!['chromium','firefox','webkit'].includes(engine))throw new Error('Motor de navegador desconocido');
module.exports=defineConfig({
  testDir:__dirname,
  testMatch:'*.spec.cjs',
  fullyParallel:true,
  workers:2,
  retries:0,
  timeout:90000,
  reporter:[['list'],['html',{outputFolder:'playwright-report',open:'never'}]],
  outputDir:'test-results',
  use:{baseURL:'http://127.0.0.1:4173',locale:'es-ES',timezoneId:'Europe/Madrid',reducedMotion:'reduce',trace:'retain-on-failure',screenshot:'only-on-failure',acceptDownloads:true,launchOptions:engine==='firefox'?{firefoxUserPrefs:{'browser.download.viewableInternally.enabledTypes':'','browser.helperApps.neverAsk.saveToDisk':'application/octet-stream,image/webp,image/png,image/svg+xml,application/zip,text/plain'}}:{}},
  projects:[
    {name:'escritorio',use:{browserName:engine,viewport:{width:1440,height:1000}}},
    {name:'tablet',use:{browserName:engine,viewport:{width:820,height:1180},hasTouch:engine!=='firefox'}},
    {name:'movil',use:{browserName:engine,viewport:{width:390,height:844},isMobile:engine!=='firefox',hasTouch:engine!=='firefox'}},
    {name:'movil-estrecho',use:{browserName:engine,viewport:{width:320,height:740},isMobile:engine!=='firefox',hasTouch:engine!=='firefox'}}
  ],
  webServer:{command:'python3 -m http.server 4173 --bind 127.0.0.1',cwd:servedRoot,url:'http://127.0.0.1:4173/datalab-prototipo/',reuseExistingServer:false,timeout:30000}
});
