// Headless check of the packaged Blender studio page (build/viewer/kartal_studio.html).
// Phone viewport; waits for window.__kartalStudio.loaded, fails on console errors.
const { chromium } = require('playwright');
(async () => {
  const out = process.env.OUT;
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 412, height: 860 }, deviceScaleFactor: 2 });
  const errors = [];
  p.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  p.on('pageerror', e => errors.push(String(e)));
  await p.goto(`http://127.0.0.1:${process.env.PORT}/index.html`);
  await p.waitForFunction(() => window.__kartalStudio && window.__kartalStudio.loaded, null, { timeout: 120000 });
  const meshes = await p.evaluate(() => window.__kartalStudio.meshes);
  for (const v of ['front', 'side', 'rear']) {
    await p.click(`#${v}`); await p.waitForTimeout(2500);
    await p.screenshot({ path: `${out}/studio_${v}.png`, timeout: 120000 });
  }
  console.log('meshes:', meshes, 'errors:', JSON.stringify(errors));
  await b.close();
  if (errors.length || meshes < 50) process.exit(1);
})();
