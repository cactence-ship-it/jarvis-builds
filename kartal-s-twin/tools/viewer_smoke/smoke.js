// Headless-Chromium functional test of the packaged viewer (T-011).
// Every interaction is asserted; any failed check exits non-zero.
const { chromium } = require('playwright');
const EXPECTED_PARTS = parseInt(process.env.EXPECTED_PARTS || '0', 10);
const fail = (m) => { console.log('ASSERTION FAILED: ' + m); process.exit(1); };
const check = (cond, m) => { if (!cond) fail(m); console.log('ok: ' + m); };

(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 412, height: 860 }, deviceScaleFactor: 2 });
  const errs = [];
  p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  p.on('pageerror', e => errs.push(String(e)));
  await p.goto('http://127.0.0.1:' + (process.env.PORT || 8765) + '/index.html');

  // 1. The model must really load (no pass before the GLB is parsed).
  try {
    await p.waitForFunction(() => window.__kartalViewer && window.__kartalViewer.loaded, null, { timeout: 30000 });
  } catch (e) { fail('model did not load within 30 s: ' + e.message); }
  const parts = await p.evaluate(() => window.__kartalViewer.parts());
  check(EXPECTED_PARTS > 0 && parts.length === EXPECTED_PARTS, `viewer has ${parts.length} parts, manifest has ${EXPECTED_PARTS}`);
  const toggles = await p.$$eval('#asm .tog', e => e.map(x => x.textContent.trim()));
  console.log('assemblies: ' + toggles.join(' | '));
  const toggleSum = toggles.reduce((s, t) => s + parseInt(t.split(' ').pop(), 10), 0);
  check(toggleSum === parts.length, `assembly toggle counts sum to ${toggleSum}`);
  await p.screenshot({ path: 'iso.png' });

  // 2. Selection, independent of the camera: tap the projected visible point of a part and
  //    require that exact part to be selected - for two different parts and two views.
  const tapAndCheck = async (id, view) => {
    const pt = await p.evaluate((x) => window.__kartalViewer.screenPoint(x), id);
    check(pt !== null, `${id} has a visible point in the ${view} view`);
    await p.mouse.click(pt.x, pt.y);
    await p.waitForTimeout(250);
    const sel = await p.evaluate(() => window.__kartalViewer.selected());
    check(sel === id, `${view} view: tap on ${id} selects ${id} (got ${sel})`);
    const info = await p.textContent('#info');
    check(info.includes(id) && info.includes('PLACEHOLDER'), `${view} view: info panel shows ${id} and its status`);
  };
  await tapAndCheck('BDY-003', 'iso');
  await tapAndCheck('WHL-001', 'iso');
  await p.click('#v-left'); await p.waitForTimeout(250);
  await tapAndCheck('BDY-008', 'left');
  await p.click('#v-iso'); await p.waitForTimeout(250);

  // 3. Explode moves parts; returning the slider to 0 restores them exactly.
  const pos0 = Object.fromEntries((await p.evaluate(() => window.__kartalViewer.parts())).map(x => [x.id, x.position]));
  await p.fill('#explode', '70'); await p.dispatchEvent('#explode', 'input');
  const pos1 = await p.evaluate(() => window.__kartalViewer.parts());
  const moved = Math.max(...pos1.map(x => Math.hypot(...x.position.map((v, i) => v - pos0[x.id][i]))));
  check(moved > 0.05, `explode moves parts (max displacement ${moved.toFixed(3)} m)`);
  await p.fill('#explode', '0'); await p.dispatchEvent('#explode', 'input');
  const pos2 = await p.evaluate(() => window.__kartalViewer.parts());
  const back = Math.max(...pos2.map(x => Math.hypot(...x.position.map((v, i) => v - pos0[x.id][i]))));
  check(back < 1e-9, 'explode 0 restores the original positions');

  // 4. Assembly visibility: hiding GLAZING hides exactly its parts; showing restores them.
  const glazing = parts.filter(x => x.assembly === 'GLAZING').length;
  check(glazing > 0, `GLAZING has ${glazing} parts`);
  await p.click('#a-glazing');
  let vis = await p.evaluate(() => window.__kartalViewer.parts());
  check(vis.filter(x => x.assembly === 'GLAZING').every(x => !x.visible), 'GLAZING parts hidden');
  check(vis.filter(x => x.assembly !== 'GLAZING').every(x => x.visible), 'other assemblies still visible');
  await p.click('#a-glazing');
  vis = await p.evaluate(() => window.__kartalViewer.parts());
  check(vis.every(x => x.visible), 'GLAZING parts visible again');

  await p.click('#v-left'); await p.click('#c-status'); await p.waitForTimeout(300);
  await p.screenshot({ path: 'exploded.png' });
  check(errs.length === 0, 'no console errors ' + JSON.stringify(errs));
  console.log('errors: []');
  await b.close();
})().catch(e => fail('unexpected: ' + e.message));
