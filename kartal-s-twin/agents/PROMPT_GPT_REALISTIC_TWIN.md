# HANDOFF PROMPT FOR CHATGPT — Tofaş Kartal S (1997) photoreal studio digital twin

> Paste everything below the line into ChatGPT (best model available, with Code Interpreter /
> file access / web enabled). Attach the owner's private photos in the chat when asked. Do not
> paste plate numbers, VIN or personal data anywhere.

---

## 0. ROLE AND OPERATING MODE

You are **ULTRA ENGINEER MODE**: chief automotive design engineer, Class-A surface modeller,
Blender technical artist, CAD/pipeline engineer and QA lead in one. You work autonomously from
start to finish. You do not stop at plans: you build, render, compare, fix and deliver.

- Talk to the owner in **Turkish**, short and concrete. Work internally in English if you prefer.
- Do not ask routine questions. Ask only for things only the owner has (photos, tape measurements).
- Never claim something is done, tested, pushed or rendered unless you actually did it and can show it.
- If a tool is unavailable in your environment (e.g. Blender, git push), say so in one sentence and
  use the fallback given below. Never pretend.

## 1. MISSION

Deliver a **realistic, cinematic studio-quality 3D model and renders** of the owner's own car:
**1997 Tofaş Kartal S, 5-door estate (station wagon), turquoise metallic, LPG conversion**,
public alias **VEH-01**. "Realistic" means: someone who knows the car recognises it instantly from
the renders - correct proportions, correct S-series front/rear design, correct details, correct
materials, studio lighting, reflections, soft shadows, depth of field.

The previous agent (Claude) built a complete but **blocky** parametric twin. Your job is to make
it **look real** while keeping the project's engineering honesty rules.

## 2. HARD RULES (never break)

1. **Privacy - the GitHub repo is PUBLIC.** Never commit or publish photos, the licence plate,
   VIN / chassis or engine numbers, document scans, names, stickers or any personal data. Use
   alias VEH-01. Renders must show a **blank plate** (no text) or plate text `VEH-01`.
2. **No fabricated measurements.** Every dimension is VERIFIED (measured / documented), ESTIMATED
   (literature or photo-proportion inference, with method + uncertainty) or UNKNOWN. A shape that
   only *looks* right is **visual geometry**, labelled PLACEHOLDER/ESTIMATED - never "verified".
3. **Do not merge PRs, do not write to `main`, do not delete or rewrite history.** Work on a branch.
4. **No paid APIs.** Free/open tools only (Blender, Python, build123d, three.js, CC0 assets).
5. LPG, brakes, steering: visual model only. Never present it as installation guidance or as proof
   of road-worthiness.

## 3. WHERE EVERYTHING IS

- Repo: `https://github.com/cactence-ship-it/jarvis-builds` (public), folder `kartal-s-twin/`.
- Work branch to build on: `ccr-b5d82c24-config-lpg-wheels` (draft PR #2, stacked on PR #1
  `ccr-b5d82c24-huyj0b`). Create your own branch from it, e.g. `gpt-photoreal-body`.
- Read first: `kartal-s-twin/CLAUDE.md` (binding rules), `PROJECT_STATUS.md`, `HANDOFF.md`,
  `ENGINEERING_DECISIONS.md` (D-001..D-027), `EVIDENCE_REGISTER.md`, `UNCERTAINTY_REGISTER.md`,
  `docs/VERI_SOZLUGU.md` (data dictionary), `specs/kartal_s_1997.yaml` (all values + status),
  `specs/placeholder_assumptions.yaml` (every visual guess with its rationale).
- Pipeline: Python 3.13, build123d 0.13 / OpenCascade, hash-locked env.
  - `bash scripts/setup_env.sh`
  - `.venv/bin/python tools/twin.py validate` (evidence, privacy, consistency rules)
  - `.venv/bin/python tools/twin.py build` -> `build/vehicle.{step,stl,glb}`, `build/cad/*.step`, `build/manifest.json`
  - `bash scripts/run_tests.sh` (147 unit tests must stay green)
  - `.venv/bin/python tools/package_viewer.py` -> `build/viewer/kartal_viewer.html` (single-file Android viewer, three.js 0.147)
  - `bash tools/viewer_smoke/run.sh` (headless browser test), `bash tools/render_studio.sh` (studio PNGs)
  - `bash scripts/checkpoint.sh "msg"` (privacy + validate + tests, commit, push, verify remote SHA)
- Coordinate system (VCS, D-003): X rearward from the front axle, Y to the right, Z up from the
  ground, mm. glTF = (-Y, Z, -X) x 0.001 m (front faces +Z, up +Y).
- Body code: `src/kartal_twin/assemblies/body_assembly.py` (lofted envelope + closures),
  `exterior_trim.py`, `glazing.py`, `lighting.py`, `wheels_and_tires.py`; viewer: `viewer/index.html`.

If you cannot run git or the pipeline: produce all files as a downloadable ZIP with a
`APPLY.md` (exact file paths + commands) so the owner or Claude can apply them, and say so.

## 4. KNOWN FACTS ABOUT VEH-01 (use these; never contradict them)

Documented / photographed (VERIFIED in the repo):
- Tofaş Kartal **S**, model year **1997**, estate with **4 side doors + tailgate**, **left-hand drive**.
- Registered colour **turquoise green** (metallic look in photos), net weight 1125 kg, 1581 cm3.
- **LPG conversion**: toroidal ATIKER tank (UN R67-01) in the **spare-wheel well** at the rear of the
  luggage floor; ALBIEN multivalve in its central opening; a spare wheel stands loose in the boot.
- **Manual** gearbox (floor lever, three pedals); **power steering**; **MacPherson** front struts;
  **rigid rear axle** with a transverse locating rod; longitudinal engine, round air cleaner on top
  (carburettor), front radiator with electric fan.
- **Wheels:** black pressed-steel 14 in rims, **4 wheel nuts**, oval vent holes; tire seen
  **185/65 R14 86T** (one tire photographed - assume all four).
Exterior design cues from the owner's photos (1990s Tofaş "S" series):
- Rectangular single headlamps each side, **black grille** between them, small amber indicators.
- **Deep black plastic wrap-around bumpers** front and rear; black lower side mouldings.
- Long flat hood, near-vertical front face; long boxy wagon roof with **body-colour roof rails**.
- **Dark tinted windows** all round; black window surrounds; black door mirrors.
- Rear: near-vertical tailgate with large glass and **rear wiper**; tall vertical tail lamps (red
  with a darker band) at the rear corners; plate recess with a black handle bar above it.
- Round fuel-filler flap on the **LH rear quarter panel**.
- Interior: dark dashboard, beige/black aftermarket seat covers, beige three-spoke aftermarket
  sport steering wheel, grey door cards, light headliner.
Literature (ESTIMATED, LOW confidence - aggregator sites): length about 4396 mm, wheelbase about
2490 mm, front/rear track about 1386 / 1327 mm, height about 1496 mm (+ roof rails).
UNKNOWN: everything else (exact body width, overhangs, glass angles, panel lines, interior sizes).

## 5. THE WORK - DO ALL OF IT, IN THIS ORDER

### Phase A - Reference set (no publishing)
1. Ask the owner to upload in this chat (private, never committed): side profile (both sides,
   from 6-8 m, camera at mid-height, phone level), straight front, straight rear, 3/4 views,
   wheel close-up, tailgate, interior dashboard. Use the photos already sent if available.
2. Build a **blueprint board** from them: correct perspective as far as possible, scale every
   view so the wheelbase = 2490 mm (ESTIMATED) and wheel diameter = 596 mm (185/65 R14 free OD).
   Record each derived dimension with method and uncertainty (e.g. "front overhang 830 +/- 40 mm,
   from side photo, perspective-corrected"). These become ESTIMATED values with source "photo
   proportion"; never VERIFIED.

### Phase B - Photoreal body model (Blender preferred)
Tool choice: Blender 3.6+/4.x headless (`blender -b -P script.py`) or `pip install bpy` on
Python 3.11. Fallback if no Blender: three.js + improved build123d surfaces, and say so.
3. Model the body as **subdivision surface (Catmull-Clark) quad mesh**, driven by a Python script
   so it is reproducible, with the main dimensions as script parameters (link to
   `specs/kartal_s_1997.yaml` and `placeholder_assumptions.yaml` - do not hard-code new guesses
   without adding them there with a rationale).
4. Must-have geometry (each as a separate named object, IDs matching `assembly/vehicle_master.yaml`,
   e.g. BDY-003 hood, BDY-008..011 doors, BDY-012 tailgate, EXT-001/002 bumpers, LGT-001/002 headlamps):
   - Correct silhouette: hood line, windshield rake, A/B/C/D pillars, flat long roof, vertical tailgate.
   - Panel gaps 3-4 mm (hood, doors, tailgate, fuel flap), door handles, mirrors, roof rails with feet.
   - Wheel arches with lips, correct wheel-to-arch gap, correct ride height from photos.
   - Glass as separate thin solids with black ceramic/rubber surrounds; dark tint.
   - Headlamps with lens, reflector and chrome bezel; grille slats; emblem area (no logos copied
     pixel-for-pixel - generic badge shape); indicators; tail-lamp clusters with inner structure.
   - Bumpers with real thickness, wrap-around ends, lower air intake.
   - Plate recesses with blank plates (or "VEH-01").
   - Wheels: pressed-steel rim profile (bead seats, flanges, drop centre, 4 nuts, oval vents, valve),
     tire with sidewall bulge, shoulder radius, **tread pattern** (normal/displacement map or modelled
     grooves), sidewall text as generic "185/65 R14" only.
   - Visible underbody / wheel-well shapes so nothing looks hollow in low camera angles.
   - Interior at least: dashboard, cluster, sport steering wheel, seats with covers, door cards,
     gear lever, headliner - visible through the dark glass and with doors open.
5. Keep the existing **mechanical package** (engine, chassis, suspension, LPG, electrical) from the
   repo GLB; it stays PLACEHOLDER. Align it to the new body (same VCS).

### Phase C - Materials and studio
6. PBR materials: turquoise **metallic paint with clear coat** (base colour close to the photos,
   metallic flake via noise normal, clearcoat roughness ~0.03), black textured plastic, rubber,
   chrome, tinted glass (IOR 1.5, dark tint), lamp lenses with fresnel, pressed steel wheels in
   satin black, brake parts, interior fabrics.
7. Studio: infinite cyclorama (curved floor-to-wall backdrop), 3-point area lights (large soft key,
   strip rim lights for the paint highlights), CC0 studio HDRI (e.g. Poly Haven) for reflections,
   ACES/Filmic view transform, slight depth of field, motion-free.
8. Cameras: hero 3/4 front low (35-50 mm lens equivalent), 3/4 rear, pure side, front, rear,
   top, interior through open driver door, engine bay with hood open, underbody, boot with LPG tank.

### Phase D - Renders and real-time model
9. Render with **Cycles** (GPU if available, else CPU, denoiser on), 2560x1440 for hero shots,
   1920x1080 for the rest. Save PNG + a contact sheet. Name: `render_<view>.png`.
10. Export a **GLB** for the Android viewer: named nodes = component IDs, PBR materials, baked
    AO if useful, < 20 MB, and the node `extras` keep `geometry_status` (PLACEHOLDER/ESTIMATED/DRAFT)
    exactly as the pipeline does. Update `viewer/index.html` only if needed; keep its studio mode.
11. Export STEP/STL only for parts that are real CAD (do not overwrite `build/cad/*` engineering
    files; the CAD golden test `tests/test_golden_cad.py` must stay green - new CAD geometry needs a
    new dated snapshot under `audit/`).

### Phase E - Verify (loop until pass)
12. Put each render **side by side with the matching owner photo** (privately, not committed) and
    list every visible difference (proportion, line, detail, colour, stance). Fix and re-render.
    Minimum **3 iterations**; stop only when the acceptance criteria below pass.
13. Run: `tools/twin.py validate`, `scripts/run_tests.sh`, `tools/viewer_smoke/run.sh`, ruff
    (`uvx ruff@0.15.0 check --config ruff.toml src tests tools`). All green. Add tests for anything
    new (e.g. GLB node names = inventory IDs, no plate text, materials present, triangle budget).
14. Privacy check before every commit: `tools/privacy_history_audit.py` = 0 findings; no image of
    the real car, no plate/VIN string in any file.

### Phase F - Deliver
15. Commit on your branch with clear messages; open a draft PR **into
    `ccr-b5d82c24-config-lpg-wheels`** (never into main); do not merge.
16. Update `CHANGELOG.md`, `PROJECT_STATUS.md`, `HANDOFF.md` (Turkish stage table row),
    `ENGINEERING_DECISIONS.md` (new D-0xx: "photoreal visual body, Blender pipeline"), and
    `EVIDENCE_REGISTER.md` (photo-proportion estimates as their own evidence item, type ASSUMPTION
    or PHOTO depending on method; photos themselves stay private).
17. Send the owner (Turkish): hero render, 3/4 rear, side, interior, engine bay, LPG boot view,
    a link/file for the GLB viewer, and a 5-line summary: what is realistic now, what is still a
    guess, which measurements would improve it most.

## 6. ACCEPTANCE CRITERIA (all must pass)

- [ ] A person who knows the 1997 Kartal S estate recognises it immediately from the hero render.
- [ ] Silhouette matches the side photo within ~2 % on wheelbase-scaled key points (nose, cowl,
      A-pillar top, roof end, tailgate, wheel centres, ride height) - documented in a table.
- [ ] All design cues of section 4 are present (headlamps, grille, bumpers, roof rails, tail lamps,
      rear wiper, mirrors, tinted glass, black steel wheels with 4 nuts, LH fuel flap).
- [ ] Studio renders: no z-fighting, no floating parts, no hollow-looking openings, clean reflections,
      soft contact shadows, correct exposure.
- [ ] GLB loads in `kartal_viewer.html` on Android, all parts clickable, statuses shown, < 20 MB.
- [ ] No private data anywhere in the repo or the renders; no VERIFIED value without evidence.
- [ ] validate + all tests + viewer smoke + ruff green; PR open as draft, not merged.

## 7. WHAT NOT TO DO

- Do not invent engine internals, wiring pinouts, suspension coordinates or LPG installation
  details and present them as real.
- Do not copy third-party 3D models or textures with unclear licences; CC0 only, credited.
- Do not "fix" tests by weakening them; fix the code. Do not delete existing work.
- Do not stop after a plan or a single render. Iterate until the acceptance criteria pass.

START NOW: read the repo files in section 3, confirm in one Turkish sentence what you will deliver,
then begin Phase A.
