// Headless-Chromium functional test of the packaged viewer (T-011).
// Every interaction is asserted; any failed check exits non-zero.
const { chromium } = require('playwright');
const EXPECTED_PARTS = parseInt(process.env.EXPECTED_PARTS || '0', 10);
const fail = (m) => { console.log('ASSERTION FAILED: ' + m); process.exit(1); };
const check = (cond, m) => { if (!cond) fail(m); console.log('ok: ' + m); };

(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 412, height: 860 }, deviceScaleFactor: 2 });
  p.setDefaultTimeout(120000);   // software GL in CI containers can be slow
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

  // 3b. Sequential exploded view of one system: play moves only ENGINE parts and hides the rest;
  //     reverse play restores every original position exactly and shows everything again.
  await p.selectOption('#exScope', 'ENGINE');
  await p.click('#exPlay');
  // wait for the animation to stop itself (button back to play), not for the rounded slider value
  await p.waitForFunction(() => document.getElementById('exPlay').textContent === '▶', null, { timeout: 90000 });
  const pe = await p.evaluate(() => window.__kartalViewer.parts());
  const movedE = pe.filter(x => Math.hypot(...x.position.map((v, i) => v - pos0[x.id][i])) > 0.01);
  check(movedE.length > 0 && movedE.every(x => x.assembly === 'ENGINE'), `engine explode moves only ENGINE parts (${movedE.length})`);
  check(pe.filter(x => x.assembly !== 'ENGINE').every(x => !x.visible), 'other systems hidden during engine explode');
  await p.click('#exBack');
  await p.waitForFunction(() => document.getElementById('exPlay').textContent === '▶', null, { timeout: 90000 });
  const pr = await p.evaluate(() => window.__kartalViewer.parts());
  const backE = Math.max(...pr.map(x => Math.hypot(...x.position.map((v, i) => v - pos0[x.id][i]))));
  check(backE < 1e-9 && pr.every(x => x.visible), 'reverse play reassembles exactly and shows all systems');
  await p.selectOption('#exScope', '');

  // 3c. Engineering tools: parts list + search, list selection, section plane, ruler, isolate/restore,
  //     wireframe and lights toggles (D-042).
  let tl = await p.evaluate(() => window.__kartalViewer.tools());
  check(tl.bomRows === parts.length, `parts list shows every part (${tl.bomRows})`);
  await p.fill('#bomQ', 'ENG-0'); await p.dispatchEvent('#bomQ', 'input');
  tl = await p.evaluate(() => window.__kartalViewer.tools());
  const nEng = parts.filter(x => x.id.startsWith('ENG-0')).length;
  check(tl.bomRows === nEng, `search "ENG-0" lists the ${nEng} engine parts (got ${tl.bomRows})`);
  await p.click('#bom tr[data-id="ENG-001"]'); await p.waitForTimeout(200);
  check(await p.evaluate(() => window.__kartalViewer.selected()) === 'ENG-001', 'tapping a list row selects that part');
  check((await p.textContent('#info')).includes('Zarf (VCS)'), 'info panel shows the part envelope in VCS mm');
  await p.fill('#bomQ', ''); await p.dispatchEvent('#bomQ', 'input');
  await p.click('#t-cut'); tl = await p.evaluate(() => window.__kartalViewer.tools());
  check(tl.cut === 1, 'section plane on');
  await p.click('#t-cut'); tl = await p.evaluate(() => window.__kartalViewer.tools());
  check(tl.cut === 0, 'section plane off');
  await p.click('#v-iso'); await p.waitForTimeout(250);
  const a = await p.evaluate(() => window.__kartalViewer.screenPoint('BDY-003'));
  const w = await p.evaluate(() => window.__kartalViewer.screenPoint('WHL-001'));
  await p.click('#t-ruler'); await p.mouse.click(a.x, a.y); await p.waitForTimeout(150); await p.mouse.click(w.x, w.y); await p.waitForTimeout(150);
  tl = await p.evaluate(() => window.__kartalViewer.tools());
  check(tl.measure > 100 && tl.measure < 3000, `ruler measures between two taps (${Math.round(tl.measure)} mm)`);
  await p.click('#t-ruler');
  await p.click('#bom tr[data-id="WHL-001"]'); await p.click('#t-iso');
  let vi = await p.evaluate(() => window.__kartalViewer.parts());
  check(vi.filter(x => x.visible).map(x => x.id).join() === 'WHL-001', 'isolate leaves only the selected part');
  await p.click('#t-all');
  vi = await p.evaluate(() => window.__kartalViewer.parts());
  check(vi.every(x => x.visible), 'show all restores every part');
  await p.click('#t-wire'); await p.click('#t-lights');
  tl = await p.evaluate(() => window.__kartalViewer.tools());
  check(tl.wire && tl.lights, 'wireframe and lights on');
  await p.click('#t-wire'); await p.click('#t-lights');
  await p.click('#c-share'); await p.waitForTimeout(150);
  check(await p.evaluate(() => document.getElementById('c-share').classList.contains('on')), 'evidence-share heat map on');
  await p.click('#c-real');

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
