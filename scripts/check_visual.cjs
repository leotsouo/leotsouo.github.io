// Own-build regression harness: serves only _site and uses an isolated browser.
// Run with `node scripts/check_visual.cjs` after installing Playwright in the environment.
const {chromium} = require('playwright');
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve('_site');
const out = process.env.SCREENSHOT_DIR || '/tmp/leo-site-screenshots';
fs.mkdirSync(out,{recursive:true});
const types={'.html':'text/html; charset=utf-8','.css':'text/css','.svg':'image/svg+xml','.xml':'application/xml'};
const server=http.createServer((req,res)=>{
 let name=decodeURIComponent(new URL(req.url,'http://127.0.0.1').pathname);
 let f=path.join(root,name);
 if(!f.startsWith(root+path.sep)&&f!==root){res.writeHead(403);return res.end();}
 if(fs.existsSync(f)&&fs.statSync(f).isDirectory()) f=path.join(f,'index.html');
 if(!fs.existsSync(f)){res.writeHead(404);return res.end('Not found');}
 res.setHeader('Content-Type',types[path.extname(f)]||'application/octet-stream');
 res.end(fs.readFileSync(f));
});
(async()=>{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const base=`http://127.0.0.1:${server.address().port}`;
 const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_PATH});
 const report={pages:[],consoleErrors:[],externalRequests:[],navigation:[],screenshots:[]};
 try {
 const page=await browser.newPage({viewport:{width:1440,height:1050},deviceScaleFactor:1});
 page.on('pageerror',e=>report.consoleErrors.push(e.message));
 page.on('request',r=>{if(!r.url().startsWith(base))report.externalRequests.push(r.url());});
 const routes=['/','/about/','/projects/','/notes/','/notes/getting-started/','/404.html'];
 for(const width of [320,375,390,430,768,1280,1440,1920]) {
   await page.setViewportSize({width,height:width<768?844:1050});
   for(const route of routes){
     const response=await page.goto(base+route);
     assert.equal(response.status(),200,`${route} HTTP`);
     const measured=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,headings:[...document.querySelectorAll('h1')].filter(e=>e.getBoundingClientRect().height&&getComputedStyle(e).display!=='none').map(e=>e.innerText),bg:getComputedStyle(document.body).backgroundColor,lang:document.documentElement.lang}));
     assert.ok(measured.scrollWidth<=width,`${width} ${route}: horizontal overflow ${measured.scrollWidth}`);
     assert.equal(measured.lang,'zh-TW');
     assert.equal(measured.headings.length,1,`${route}: one visible main heading`);
     report.pages.push({width,route,...measured});
   }
 }
 await page.setViewportSize({width:390,height:844});
 await page.goto(base+'/');
 await page.getByRole('link',{name:'專案介紹',exact:true}).click();
 assert.ok(page.url().endsWith('/projects/')); report.navigation.push('home CTA → projects');
 await page.getByRole('navigation',{name:'主要導覽'}).getByRole('link',{name:'筆記',exact:true}).click();
 assert.ok(page.url().endsWith('/notes/')); report.navigation.push('mobile nav → notes');
 await page.getByRole('link').filter({hasText:'網站開始'}).click();
 assert.ok(page.url().endsWith('/notes/getting-started/')); report.navigation.push('notes → article');
 await page.getByRole('link',{name:'回到所有筆記',exact:true}).click();
 assert.ok(page.url().endsWith('/notes/')); report.navigation.push('article → notes');
 await page.goBack(); assert.ok(page.url().endsWith('/notes/getting-started/')); report.navigation.push('browser Back');
 await page.goForward(); assert.ok(page.url().endsWith('/notes/')); report.navigation.push('browser Forward');
 await page.goto(base+'/');
 await page.keyboard.press('Tab');
 const firstFocus=await page.locator(':focus').innerText();
 assert.equal(firstFocus,'跳至導覽'); report.navigation.push('keyboard skip link visible');
 // Simulate 200% text enlargement at a narrow viewport without changing stored source.
 await page.addStyleTag({content:'html { font-size: 32px !important; }'});
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'200% text enlargement overflow');
 report.navigation.push('200% root text enlargement at 390px');
 await page.emulateMedia({reducedMotion:'reduce'});
 report.navigation.push('reduced-motion context enabled; visual inspection still required');
 const shots=[['home-desktop.png','/',1440,1050],['home-mobile.png','/',390,844],['projects-mobile.png','/projects/',390,844],['about-desktop.png','/about/',1440,1050],['notes-mobile.png','/notes/',390,844],['note-desktop.png','/notes/getting-started/',1440,1050]];
 for(const [name,route,width,height] of shots){
   await page.setViewportSize({width,height});await page.goto(base+route);await page.screenshot({path:path.join(out,name),fullPage:true});report.screenshots.push(name);
 }
 assert.deepEqual(report.consoleErrors,[]); assert.deepEqual(report.externalRequests,[]);
 fs.writeFileSync(path.join(out,'browser-verification.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify({status:'PASS',pageViewportChecks:report.pages.length,navigationChecks:report.navigation,consoleErrors:0,externalRequests:0,screenshots:report.screenshots,output:out},null,2));
 } finally {await browser.close();server.close();}
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
