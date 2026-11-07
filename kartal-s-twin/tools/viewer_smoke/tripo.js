// Headless check of viewer/tripo.html: placements load, every present part is placed,
// no console errors. Phone viewport. Writes front/side/top screenshots.
const { chromium } = require('playwright');
(async () => {
  const out = process.env.OUT;
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 412, height: 860 }, deviceScaleFactor: 1 });
  const errors = [];
  p.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  p.on('pageerror', e => errors.push(String(e)));
  await p.goto(`http://127.0.0.1:${process.env.PORT}/index.html`);
  await p.waitForFunction(() => window.__tripo && window.__tripo.loaded, null, { timeout: 120000 });
  const st = await p.evaluate(() => window.__tripo);
  for (const v of ['front', 'side', 'top']) {
    await p.click(`#${v}`); await p.waitForTimeout(1500);
    await p.screenshot({ path: `${out}/tripo_${v}.png`, timeout: 120000 });
  }
  console.log('placed:', st.placed, 'parts:', JSON.stringify(st.parts), 'errors:', JSON.stringify(errors.concat(st.errors)));
  await b.close();
  const expected = Number(process.env.EXPECTED_INSTANCES || 1);
  if (errors.length || st.errors.length || st.placed < expected) process.exit(1);
})();
