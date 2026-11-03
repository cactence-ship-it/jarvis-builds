// Studio renders of the packaged viewer (headless Chromium, software WebGL).
// Writes OUT/{cinema,front,rear,left,iso,mechanical}.png of the 3D stage only.
const { chromium } = require('playwright');
(async () => {
  const out = process.env.OUT;
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1600, height: 1900 }, deviceScaleFactor: 1 });
  const errors = [];
  p.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  p.on('pageerror', e => errors.push(String(e)));
  await p.goto(`http://127.0.0.1:${process.env.PORT}/index.html`);
  await p.waitForFunction(() => window.__kartalViewer && window.__kartalViewer.loaded, null, { timeout: 60000 });
  await p.addStyleTag({ content: '#stage{height:1000px!important;flex:none!important}' });
  await p.evaluate(() => window.dispatchEvent(new Event('resize')));
  const shot = async (name) => {
    await p.waitForTimeout(2500);
    const r = await p.evaluate(() => { const b = document.getElementById('stage').getBoundingClientRect(); return { x: b.x, y: b.y, width: b.width, height: b.height }; });
    await p.screenshot({ path: `${out}/${name}.png`, clip: r, timeout: 120000 });
  };
  for (const v of ['cinema', 'front', 'rear', 'left', 'iso']) { await p.click(`#v-${v}`); await shot(v); }
  for (const a of ['body_assembly', 'glazing', 'exterior_trim', 'lighting']) await p.click(`#a-${a}`);
  await p.click('#v-cinema'); await shot('mechanical');
  console.log('errors:', JSON.stringify(errors));
  await b.close();
  if (errors.length) process.exit(1);
})();
