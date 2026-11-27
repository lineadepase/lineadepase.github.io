const {defineConfig}=require('@playwright/test');
const path=require('node:path');
const root=path.resolve(__dirname,'../../..');
module.exports=defineConfig({
  testDir:__dirname,
  testMatch:'*.spec.cjs',
  fullyParallel:true,
  workers:2,
  retries:0,
  timeout:90000,
  reporter:[['list'],['html',{outputFolder:'playwright-report',open:'never'}]],
  outputDir:'test-results',
  use:{baseURL:'http://127.0.0.1:4173',locale:'es-ES',timezoneId:'Europe/Madrid',reducedMotion:'reduce',trace:'retain-on-failure',screenshot:'only-on-failure',acceptDownloads:true},
  projects:[
    {name:'escritorio',use:{browserName:'chromium',viewport:{width:1440,height:1000}}},
    {name:'tablet',use:{browserName:'chromium',viewport:{width:820,height:1180},hasTouch:true}},
    {name:'movil',use:{browserName:'chromium',viewport:{width:390,height:844},isMobile:true,hasTouch:true}},
    {name:'movil-estrecho',use:{browserName:'chromium',viewport:{width:320,height:740},isMobile:true,hasTouch:true}}
  ],
  webServer:{command:'python3 -m http.server 4173 --bind 127.0.0.1',cwd:root,url:'http://127.0.0.1:4173/datalab-prototipo/',reuseExistingServer:false,timeout:30000}
});
