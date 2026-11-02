const {chromium}=require('playwright');(async()=>{
 const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const p=await b.newPage({viewport:{width:412,height:860},deviceScaleFactor:2});
 const errs=[];p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('http://127.0.0.1:'+(process.env.PORT||8765)+'/index.html');await p.waitForFunction(()=>document.getElementById('msg').hidden,null,{timeout:30000});
 await p.waitForTimeout(800);
 const n=await p.$$eval('#asm .tog',e=>e.map(x=>x.textContent.trim()));console.log('assemblies:',n.join(' | '));
 await p.screenshot({path:'iso.png'});
 const c=await p.$('canvas');const bb=await c.boundingBox();
 await p.mouse.click(bb.x+bb.width*0.5,bb.y+bb.height*0.5);await p.waitForTimeout(300);
 console.log('info after tap:',(await p.textContent('#info')).slice(0,160));
 await p.click('#v-left');await p.fill('#explode','70');await p.dispatchEvent('#explode','input');await p.click('#c-status');await p.waitForTimeout(500);
 await p.screenshot({path:'exploded.png'});
 console.log('errors:',JSON.stringify(errs));await b.close();})();
