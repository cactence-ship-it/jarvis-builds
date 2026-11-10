# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/). Versions follow the master spec revision.

## [Unreleased] - 2026-11-10 - High-resolution photo shell

### Changed
- Viewer can load the photo shell from a file next to the page (`package_viewer.py --shell-url`): published build now uses 4096 px textures and 30 % of the mesh triangles (was 1536 px and 9 %), outside the 16 MB page limit. Embedded mode unchanged (tests). Anisotropic filtering on the shell texture.
- Smoke test passes (embedded); external mode checked in a headless browser with no console errors.

## [Unreleased] - 2026-11-10 - Estimates for all remaining unknowns (D-044)

### Added
- Evidence type ENGINEERING_ESTIMATE and E-062: reasoned estimates for the 28 measurement-only values. Spec 169 parameters: 63 VERIFIED / 106 ESTIMATED / 0 UNKNOWN.
- Resolver: estimate-only values are refused by engineering CAD and keep visual geometry PLACEHOLDER (test added).

### Changed
- Tests made data independent (consistency NOT_EVALUATED case blanks its own inputs; CAD refusal tested on a package guess and on an estimate).
- Engineering documents, data dictionary and measurement guide regenerated.

## [Unreleased] - 2026-11-08 - Electrical layout from the owner's manual

### Changed
- Fuse box (22 positions) and relays moved to the lower right of the dashboard (manual p.59-60, VERIFIED location); main loom re-routed through the dash.
- Earthing bracket on the right inner side of the front panel added (manual p.60); ignition described as electronic, firing order 1-3-4-2 (p.90).
- Tests: build, unit tests, validate, viewer smoke test pass.

## [Unreleased] - 2026-11-08 - Fiat 131 Panorama blueprint (E-061)

### Added
- Sources checked: carblueprints.info preview (used), Scribd (bot challenge, not opened), FiatClub manuals (members only, not bypassed), Autobooks Fiat 131 on archive.org (OCR without data appendix).
- From the 1974 Panorama blueprint scaled by the wheelbase (ESTIMATED LOW, doors assumed shared): windshield base 480, windshield top 910, B-pillar 1525, rear-door edge 2400 mm behind the front wheel centre. Tripo-shell cross-check recorded in notes only (D-030).
- U-019: engine-bay rear-wall package guess now behind the windshield base.
- Spec 169 parameters: 63 VERIFIED / 78 ESTIMATED / 28 UNKNOWN.

## [Unreleased] - 2026-11-08 - Gemini research report (E-059/E-060)

### Added
- Owner-supplied Gemini report ingested (R-0037, local-only) and checked: fuse-box location VERIFIED against the owner's manual p.59; rear damper length now backed by two sources (KYB and SEAT 131 manual).
- ESTIMATED: body construction monocoque (MEDIUM), clutch 190 mm / 20 teeth, Panhard rod ~1000 mm overall (Kartal 7733924), LPG kit type (venturi mixer), cargo floor ~1340 x 1050 (forum MDF board) - all LOW.
- New parameters from the SEAT 131 workshop manual (via the report): front/rear spring heights under check load, front strut extended/compressed length.
- Spec 169 parameters: 63 VERIFIED / 74 ESTIMATED / 32 UNKNOWN. Engineering documents regenerated.

## [Unreleased] - 2026-11-08 - Factory owner's manual (D-043)

### Added
- E-058: official Tofaş owner's manual (R-0036, local-only like other originals). 35 spec values VERIFIED or ESTIMATED HIGH from it; spec 165 parameters: 62 VERIFIED / 64 ESTIMATED / 39 UNKNOWN.
- Engine 131 D1.016 (Kartal S-SLX), Weber 32/34 TLDE twin-choke carburettor, electronic ignition, gearbox ratios 3.543 / 2.139 / 1.377 / 1.000 / 0.868 (forum ratios replaced), 3 turns lock to lock (hydraulic), overhangs 765 / 1141, negative earth, alternator 55 A.

### Changed
- Body package and photo shell re-fitted to the documented overhangs (rear 1141 mm).
- Tests made data independent (consistency NOT_EVALUATED case, measurement intake, rim tolerance).
- Engineering documents regenerated.

## [Unreleased] - 2026-11-08 - Viewer engineering tools (D-042)

### Added
- Section plane, ruler, part envelope (VCS mm), wireframe, turntable, lamp simulation, focus / isolate / hide / show all, keyboard shortcuts, searchable parts list, evidence-share heat map.
- Smoke test covers list + search, list selection, envelope, section on/off, ruler (two taps), isolate/restore, wireframe, lights, heat map; passes with and without the photo shell.

## [Unreleased] - 2026-11-07 - Drivetrain and rear links from owner research (D-041)

### Added
- Evidence E-056 (owner research summary) and E-057 (spot-check); 16 spec parameters (gearbox bearings, clutch UNKNOWN, propshaft, coupling, cross, half-shaft, bearings, rear links, Panhard UNKNOWN, steering-gear length): spec 165 parameters, 27 VERIFIED / 92 ESTIMATED / 46 UNKNOWN.
- Geometry: two-piece propshaft (coupling, centre bearing, crosses), drive flange, wheel bearings, half-shafts; rear four-link axle (617 / 315 mm) with Panhard rod, bushes and body mounts.
- U-018: quoted 690 mm half-shaft contradicts the rear track.
- OEM_CROSS_REFERENCE.md extended; engineering documents regenerated.
- Tests: build (STEP 507 solids valid), unit tests, validate, viewer smoke test pass.

## [Unreleased] - 2026-11-07 - 52 unknown values pass, engineering documents (D-040)

### Added
- Evidence E-049..E-055 (battery label photo, booster/ignition/handbrake photos, Fiat 131 clearance and wheel data, OEM cross references).
- Spec: battery 72 Ah / 700 A VERIFIED; battery case 278 x 175 x 175 (LOW); brake booster, parking brake, ignition type, ground clearance, wheel ET and centre bore ESTIMATED. Spec 149 parameters: 27 VERIFIED / 78 ESTIMATED / 44 UNKNOWN.
- docs/engineering/: MASTER_SPECIFICATION, OEM_CROSS_REFERENCE, UNKNOWN_VALUES_REGISTER, DIMENSION_MEASUREMENT_GUIDE, CAD_COORDINATE_SYSTEM, SOURCE_REGISTER, ENGINEERING_CHANGELOG.
- Battery CAD and Tripo battery skin resized to the 72 Ah case.
- Tests: build, unit tests, validate, viewer smoke test pass.

## [Unreleased] - 2026-11-07 - Front suspension and steering from listings (D-039)

### Added
- Evidence E-045..E-048; 5 spec parameters (tie rod, lower arm, front bearing, strut bore and rod): spec 149 parameters, 25 VERIFIED / 72 ESTIMATED / 52 UNKNOWN.
- Geometry: catalogue-length track-control arms with ball joints, struts sized from bore/rod, hubs with taper bearings and spindles, rack-and-pinion with boots and pinion housing, tie rods of catalogue length with ball joints.
- U-017: rack vs engine package interference and unrealistic sump ground clearance of the package guess.
- Tests: build (STEP 487 solids valid, no open bodies), unit tests, validate, viewer smoke test pass; page 15.3 MB.

## [Unreleased] - 2026-11-07 - Dimensions from spare-part listings (D-038)

### Added
- Evidence E-041..E-044; 9 new spec parameters (radiator core, battery case, rear drum width, front disc thickness, rear damper lengths) and rear drum diameter filled: spec 144 parameters, 25 VERIFIED / 67 ESTIMATED / 52 UNKNOWN.
- Geometry now reads them: radiator core and fan sized to the core, front discs with hat and caliper, rear drums with back plates, battery case with terminals, rear dampers at catalogue mid-stroke length.
- U-016 (rear damper upper eye vs placeholder cargo floor).

### Changed
- Confidence of listing-based values lowered to LOW (D-020).
- Tests: build (STEP 471 solids valid, no open bodies), unit tests, validate and viewer smoke test pass; page 15.1 MB.

## [Unreleased] - 2026-11-07 - Engine bay rev 2, sequential exploded view (D-037)

### Changed
- Parametric engine bay (same IDs, PLACEHOLDER): ribbed block, timing cover, head with plug leads, cam cover with cap, stepped sump, exhaust runners, radiator tanks and cap, 7-blade fan with shroud, hoses, accessory belt over four pulleys, starter solenoid, mount bushes. Build: STEP 462 solids valid, GLB 154 k triangles, no open bodies or flipped normals.
- Viewer: exploded view per system (dropdown) or whole car, sequential outside-in, play/pause/reverse; smoke test covers it (engine-only motion, other systems hidden, exact reassembly) and passed 3 runs in a row.
- Tripo: Studio credits (≈3 145) not usable from this cloud session (no browser/computer link); API wallet 30 credits, no generation this stage.

## [Unreleased] - 2026-11-07 - Phase 5 start: engine bay and LPG tank skins

### Added
- Tripo v3.1 skins: air-filter housing (ENG-005, from engine-bay photo, replaces only the housing mesh), battery (ELE-001, text-to-model after the photo crop gave only lid and cables), LPG toroidal tank (FUL-005, from trunk photo). Sizes ESTIMATED (0.42 / 0.24 / 0.60 m). 150 credits; 30 left.
- Viewer: engine close view hides body panels and glass; skin config option `box` (replace only placeholder meshes inside a box).
- All six interior/engine skins reduced (384 px textures, ~1.4 % triangles) so the packaged page stays at 14.1 MB (< 16 MB).
- Tests: viewer smoke test passes, no console errors.

## [Unreleased] - 2026-11-07 - Shell symmetry and lamp glass (D-036)

### Changed
- Photo shell: plan-view shear removed (front fascia and rear face now centred, lamps symmetric).
- Viewer: glass lenses over headlamps and tail lamps of the shell.
- Tests: viewer smoke test passes, no console errors.

## [Unreleased] - 2026-11-07 - Shell proportions fixed (D-035)

### Changed
- Photo shell: pitch levelled (3.8°) and length re-proportioned to the twin's wheel centres (rear overhang 17.5 % -> 24.5 % of length). Then width/height scale node (1, 0.869, 0.850). Tool: `tools/meshfit/scripts/reprop.mjs`.

## [Unreleased] - 2026-11-07 - Rear bench replaced

### Changed
- Rear bench skin (INT-011) replaced by a text-to-model bench (photo of the bench is blocked by the front seat; colours described from owner photos), rotated -90 deg so the backrest faces the rear. Second dashboard attempt (centre-stack crop) returned only a radio box: not used, dashboard stays PLACEHOLDER. 70 credits; 180 left.

## [Unreleased] - 2026-11-07 - Interior skins from owner photos (D-034)

### Added
- Tripo v3.1 interior meshes from cropped owner photos: steering wheel (INT-003), front seat (INT-009/010, same mesh), rear bench (INT-011). Rejected: dashboard (Tripo returned only the steering wheel); first front-seat attempt (two seats merged). 200 credits; 290 left.
- Viewer: interior skins (`--skins assembly/tripo_interior.json`), "Kabin" and "Motor" close cameras, cabin view opens the car (no roof/panels/glass/headliner/shell).
- Sizes used for skins are ESTIMATED (wheel 0.35 m, front seat 0.95 m, rear bench 1.30 m); no spec value changed.
- Packaged page 15.3 MB (shell textures 1536 px, interior textures 512 px) to stay under the 16 MB publish limit.
- Tests: viewer smoke test passes with shell and skins, no console errors; unit tests and validate pass.

## [Unreleased] - 2026-11-07 - Interactive body + real-look layer (D-033)

### Added
- Viewer: "Gerçek görünüm" layer (photo-based Tripo shell) with X-ray opacity slider; engineering parts stay selectable under it (three.js layer 1).
- Viewer: open/close buttons for the four doors, hood (front-hinged, from owner photos) and tailgate, with eased hinge animation; door mirrors, handles, glass and door cards move with their door (closure map from vehicle_master.yaml dependencies).
- Viewer: underside camera ("Alt") with the floor hidden and brighter ground light.
- `tools/package_viewer.py --shell/--place` embeds the shell; closure map always embedded.
- Tests: `tools/viewer_smoke/run.sh` passes with and without the shell (no console errors); a separate headless check confirmed taps select BDY-003, BDY-008, WHL-001 after the shell has loaded and that opening a door drops the shell to 25 %.

## [Unreleased] - 2026-11-07 - Tripo v3.1 multiview (front fixed)

### Changed
- Owner feedback: the front of the rear-photo mesh was wrong (front was hallucinated). Regenerated with Tripo v3.1 multiview from four owner photos (front-left, rear-left, rear, front-right three-quarters): front lamps, grille and bumper now match the car. Pre-correction residual width +17.0 %, height +21.2 % (INCONSISTENT); corrected with scale node (1, 0.825, 0.855) per D-032; heading front +x checked visually. Alternative v3.1 from the front photo alone: +9.8 % / +11.3 %. 80 credits.

## [Unreleased] - 2026-11-07 - Tripo v3.1 model, no correction

### Changed
- Owner decision 2026-11-07: plates may stay visible in Tripo uploads and textures; owner originals are never edited. GLBs still stay out of the public repository (D-012).
- Earlier API calls used Tripo's default (older) model version. Regenerated with the Tripo CLI (`tripo make`, v3.1-20260211, PBR, detailed texture) from the original rear three-quarter photo: width -4.3 %, height -3.8 % (WARN), so the mesh is used unedited (uniform scale only, no D-031/D-032 correction). Heading front -x, checked visually; wheels sit on the reference wheel centres. Other candidates: v3.1 from the front three-quarter photo (+12.2 % / +13.2 %), P2 (+18.2 % / +7.7 %, no texture). 200 credits.
- Phone viewer: mesh simplified to 15 %, textures 2048 px WebP, embedded (7.9 MB page).

## [Unreleased] - 2026-11-07 - Tripo model from owner photos

### Changed
- 25 owner photos ingested (local-only, D-012); 6 exterior photos blurred (plates, plate frames, rear-window name sticker) before upload to Tripo.
- Phone viewer now shows the photo-based mesh (task 7d6dae58, image_to_model from the rear three-quarter photo). Pre-correction residual width +16.4 %, height +21.1 % (INCONSISTENT); corrected with scale node (0.859, 0.826, 1), heading set to front -z after visual check (D-032). Visual check: wheels sit about 0.25-0.3 m forward of the reference wheel centres (overhangs of the generated mesh differ from the twin). Rejected: front three-quarter candidate (broken geometry), multiview candidate (+28.3 % / +32.0 %, plate blur turned into geometry). Credits used: 120.

## [Unreleased] - 2026-11-07 - Automatic Tripo model and literature pass 2

### Added
- Evidence E-037..E-040: front disc 227.5 mm (OEM 4208311, up to MY2000), rack-and-pinion steering, Fiat 131 turning circle 10.3 m, engine-code and alternator candidates. 3 parameters UNKNOWN -> ESTIMATED.
- Automatic Tripo pipeline (D-031): 5 text-to-model candidates via the Tripo API (150 credits). Best candidate (task 75965f78) residual before correction: width +13.4 %, height +6.5 % (INCONSISTENT). Corrected with one scale node (0.882, 0.939, 1); after correction CONSISTENT by construction. Heading and wheel centres checked visually in the viewer.
- Phone viewer with the corrected model embedded (texture 2048 px, mesh simplified to 40 %, quantized): https://claude.ai/artifact/N6Wiwb9pzGy2QmLDPF2Xq3

## [Unreleased] - 2026-11-07 - Public-literature data pass

### Added
- Evidence E-029..E-036 (literature, via search summaries; source pages not readable from the build environment).
- 18 parameters moved from UNKNOWN to ESTIMATED, each with source, tolerance and a verify-by note: engine bore 86.4 mm and stroke 67.4 mm (MEDIUM; 4 cylinders give 1580.6 cm3 against the registered 1581 cm3), compression ratio 9.2, power/torque speeds 5500/3000 rpm, 5 forward gears with ratios 3.667/2.1/1.361/1.0/0.881, reverse 3.526, final drive 4.10, cable clutch, coil springs front and rear, front anti-roll bar, front disc brakes, 4x98 PCD, 846 L luggage volume, 12 V system, H4 headlamps.

### Added (Tripo assembly, D-030)
- `tools/meshfit` (Rust, std-only): reads a GLB's bounds, turns the car front onto +Z, scales it to the twin's length (wheel: tire diameter), places it (car on the ground, body from the roof line, wheel at the four wheel centres) and reports width/height deviation: CONSISTENT < 3 %, WARN < 8 %, INCONSISTENT otherwise. 8 unit tests.
- `viewer/tripo.html`: phone page for the placed meshes, with a measurement frame, wheel-centre circles and a FRONT arrow; `tools/viewer_smoke/tripo.sh` fits and checks it in headless Chromium (`--self-test` uses the twin's own GLB: 0.0 % width, +0.7 % height deviation).
- `assembly/tripo_parts.json` (plan A, whole car) and `tripo_parts_split.json` (plan B, body + wheel); `docs/TRIPO_URETIM.md`, the owner's phone guide.

### Not filled (no consistent public source)
- Engine type code, ignition type, steering-gear type, brake disc/drum diameters, wheel offset and centre bore, battery and alternator ratings; all vehicle-specific measurements (arch gaps, axle loads, LPG tank position, body profile). They stay UNKNOWN.

### Changed
- `tests/test_pipeline.py`: `test_unknown_without_placeholder_raises` now forces `engine.bore` to UNKNOWN in a copy of the spec, like the neighbouring placeholder test, so the rule stays tested when real data arrives.
- Regenerated `docs/VERI_SOZLUGU.md` and `docs/OLCUM_REHBERI.md`.

## [0.13.0] - 2026-11-03 - Realistic rotatable studio model (owner priority)

### Added
- D-028: realistic visual body in Blender (`tools/blender/`): smooth body, glass and pillars, S-series front (grille, lamps, indicators), bumpers, roof rails, tail lamps, revolved tires and black steel rims, simple interior. Cycles studio preview and GLB (125 meshes, about 1.3 MB).
- `viewer/studio.html`: phone studio page (dark studio, reflections, floor shadow, auto-rotate, Front/Side/Rear buttons); packaged with the GLB embedded by `tools/blender/package_studio.py`; `tools/blender/smoke_studio.sh` checks it in headless Chromium at phone size. Published: https://claude.ai/artifact/9D8o5byLmjc6xJ6ba2BzVR
- Read-only test hook `window.__kartalStudio` (`state()`, `pick(x, y)`) for camera and part checks.

### Fixed (found by the headless check before publishing)
- Hidden loading overlay still covered the page and swallowed touches (CSS `display` overrode `hidden`).
- Canvas drawn at device-pixel size without CSS size: on phones only the top-left corner was visible.
- Portrait framing: camera distance now fits the car length to the horizontal field of view.
- B and C pillars were slanted 45 degrees (positioned by row fraction); now at fixed x.

### Changed
- Placeholders from photo proportions (E-026, no scale): cowl_x 1060 -> 850, windshield_top_x 1660 -> 1450; package guesses (firewall, dash, steering wheel, front seat, pedals, gear lever, handbrake) moved with the cowl. docs/OLCUM_REHBERI.md regenerated.

## [0.12.1] - 2026-11-03 - Studio rendering (owner feedback: "realistic, cinematic studio")

### Added
- Viewer studio look: image-based lighting (three.js RoomEnvironment), ACES filmic tone mapping, soft shadow-casting key light and rim light, dark studio floor, "Sinema" camera; materials by part class (clear-coated metallic paint, dark tinted glass as on VEH-01, chrome, rubber, black plastic, lamp lenses). Visual only.
- `tools/render_studio.sh` + `tools/viewer_smoke/studio.js`: studio renders to build/renders/*.png (cinema, front, rear, left, iso, mechanical).
- Visual detail: wrap-around black bumpers, wheel nuts and vent marks on the visual rims (CAD rims unchanged).

- Smooth body envelope: lower body lofted (ruled) through 8 rounded sections - rounded nose, hood edge, shoulders and ends; a smooth B-spline loft was rejected because it sagged ~40 mm over the hood and split the hood panel in two; rounded cabin plan corners were rejected because their mesh seams did not close. All meshes closed, STEP 385/385.

### Changed
- Placeholders from photo proportions (E-026, no scale): nose_top_z 760 -> 840 (flatter hood), bumper height 130 -> 180, bumper bottom 300 -> 280. CAD output unchanged (byte-identical to audit r4).

## [0.12.0] - 2026-11-03 - Complete-vehicle PLACEHOLDER package (T-023)

### Added
- Visual geometry for all 17 assemblies (0 skipped): engine, transmission, drivetrain, chassis (floor pan with spare-wheel well, rails, crossmembers), MacPherson front suspension, rigid-axle rear suspension, steering, brakes, exhaust, electrical architecture (schematic looms, battery, fuses, relays, ignition, grounds), interior (dashboard, cluster, sport wheel, column, pedals, gear lever, handbrake, console, seats, door cards, headliner, carpets, trim), petrol system and LPG kit parts; roof rails, rear wiper, tailgate handle, mouldings, side repeaters, plate and interior lamps; separate visual rims with valve stems and the loose spare wheel. 150 visual parts (all PLACEHOLDER) + 9 CAD parts (DRAFT) = 159 built parts.
- 31 package assumptions `pkg_*` and `roof_rail_height` in `specs/placeholder_assumptions.yaml` (visual only, each with a rationale).
- `src/kartal_twin/cad/mech.py` primitives; `tests/test_full_vehicle.py` (completeness, PLACEHOLDER-only mechanical package, cabin parts inside the body); mechanical and interior preview sheets in `tools/render_preview.py`.
- D-027; audit snapshot `audit/2026-11-02-r4`.

### Fixed
- CAD STEP bytes depended on the number of visual solids (OpenCascade occurrence counter shared across exports); CAD is now exported first. Geometry identical to r3 (only the occurrence id lines differ).
- Viewer test hook `screenPoint` used stale camera matrices after a slow frame; it now refreshes them (smoke test passed 4/4 runs after the fix, failed 1 of 2 before).
- Cabin parts spilled into the rear wheel-arch cut-outs (found by measuring volume outside the body envelope); now kept inside the arch line.

## [0.11.0] - 2026-11-02 - Owner photo evidence: LPG tank, interior, underbody, engine bay, tire size (T-022)

### Added
- 28 owner photos ingested as R-0004..R-0031 (originals local-only; SHA-256 in `refs/MANIFEST.csv`; plate, VIN stamping, names and stickers never transcribed): evidence E-022 (luggage compartment / LPG tank), E-023 (multivalve), E-024 (interior), E-025 (rear underbody), E-026 (exterior), E-027 (engine bay), E-028 (tire sidewall).
- `validate`: a RECEIVED evidence item must cite refs/MANIFEST.csv ids in its Ref column (ranges like `R-0004..R-0007` allowed); 5 tests.
- Spec 0.8.0 (134 parameters, 25 VERIFIED / 35 ESTIMATED / 74 UNKNOWN): VERIFIED from photos - body style, side doors, LHD, manual gearbox, MacPherson front, rigid rear axle, power steering, cooling system, longitudinal engine, rim 14 in, pressed-steel black wheels with 4 nuts, LPG tank type/location/mounting/multivalve, new `lpg_system.tank_marking` (ATIKER, E7 67R-01 0049401). ESTIMATED: rear drum brakes (MEDIUM), spare-wheel location.
- Inventory: 32 components CONFIRMED from photos (history appended); FUL-005 and FUL-006 VERIFIED.
- Audit snapshot `audit/2026-11-02-r3` (tire envelopes now 185/65 R14).

### Changed
- Tire size 185/70 R14 (owner provisional) -> 185/65 R14 (photo of one tire, ESTIMATED MEDIUM per axle); free OD 614.6 -> 596.1 mm.
- Visual-only LPG tank placeholder moved towards the tailgate sill (X 3150 mm), per photo E-022.
- U-010, U-012 (partly resolved), U-013, U-014 updated.

### Fixed
- Two tests depended on live data (BDY-001 had no photo evidence; unitless counts have no tolerance); they now test the rule.

## [0.10.0] - 2026-11-02 - Owner configuration, LPG tank and steel-rim CAD (T-021, branch ccr-b5d82c24-config-lpg-wheels)

### Added
- E-017 (owner configuration statement), E-018 (owner provisional CAD values, type ASSUMPTION), E-019 (engineering assumptions), E-020 (toroidal tank listings), E-021 (J flange height).
- D-026: derived data classes (USER_CONFIRMED, DOCUMENT_CONFIRMED, MEASURED, SOURCE_SUPPORTED, ESTIMATED, UNKNOWN); evidence type ASSUMPTION (LOW only, enforced); engine-variant separation rule (`specs/configuration_rules.yaml`, `kartal_twin.configuration`, part of `validate`); unplaced CAD parts.
- Spec 0.7.0: group `lpg_system` (16 parameters) and 5 rim parameters; 133 parameters, 7 VERIFIED / 40 ESTIMATED / 86 UNKNOWN.
- CAD: steel rims WHL-006..009 (simplified J-contour section, DRAFT, placed); LPG toroidal tank FUL-005 (parametric stadium-section shell, DRAFT, local frame, NOT placed); visual tank at a placeholder position; inventory FUL-005..014 (LPG, separate from petrol FUL-001..004), ENG-007 = carburettor.
- Consistency DC-016..DC-020 (rim vs tire width, tank capacity vs geometry, tank vs rear tire gap, tank vs arch width); clearance CL-003..CL-012 (rims inside tires; tank vs tires, floor, rear axle, exhaust, suspension - BLOCKED with reasons); new rule kind `within_bbox`.
- `tools/data_dictionary.py` -> `docs/VERI_SOZLUGU.md` (generated, sync test); measurement guide codes M32-M38 (tank and luggage compartment) and tank-label / rim-stamping photos.
- `tests/test_configuration_cad.py` (29 tests); audit snapshot `audit/2026-11-02-r2`.

### Changed
- Tire size 175/70 R14 (listing, LOW) -> 185/70 R14 (owner provisional, LOW); free OD 614.6 mm. Rim diameter 14 in owner-confirmed (tolerance 0.5 in), material pressed steel, colour black; engine fuel system carburettor and base fuel petrol owner-confirmed (still ESTIMATED).
- Visual paint is a turquoise-green approximation of the registered colour name (RGB still a guess).
- Tests that hard-coded 175/70 R14 now pin their own inputs or compute expected values from the spec designation.

### Findings
- DC-018 INDETERMINATE: 600 x 180 mm holds about 38.2 L in the simplified shape (listings: 38 L), below the owner's 40 L at nominal values (U-013).

## [0.9.1] - 2026-11-02 - ChatGPT batch-3 review: T-018 and T-020 reworked

### Recorded
- ChatGPT batch-3 verdicts (relayed by the owner): ACCEPT T-011, T-012, T-013, T-019 on bf31d4d; CHANGES_REQUESTED T-018 (bf31d4d) and T-020 (4284df3).

### Fixed
- T-018: a missing `refs/MANIFEST.csv`, a manifest without its header, no `audit/<date>/SHA256SUMS` at all, an empty SHA256SUMS, or an absent SHA256SUMS passed in directly now FAIL (MISSING / MALFORMED / EMPTY) instead of reading as clean; 6 new tests, 5 of which fail on the old code (the sixth is a positive control).
- T-020: `engine.fuel_type` holds only what the document prints, "LPG (registered conversion)"; the petrol base engine is a new ESTIMATED LOW parameter `engine.base_fuel`. `verify_by` texts name the real document fields ('Cinsi', 'İstiap haddi').
- Measurement guide summary printed a hard-coded "0 VERIFIED"; it now counts, and a test compares it with the spec. Spec 0.6.1: 112 parameters, 7 VERIFIED / 24 ESTIMATED / 81 UNKNOWN.

## [0.9.0] - 2026-11-02 - Registration documents as primary evidence (T-020)

### Added
- E-014..E-016: owner photos of the registration documents and the emission form, ingested as R-0001..R-0003 (originals local-only, SHA-256 in `refs/MANIFEST.csv`; plate, VIN, engine number, serials and dates withheld).
- D-025: a registration document verifies the registered value, not the car's present physical state.

### Changed
- Spec 0.6.0: VERIFIED model, variant, model year, colour name, net weight 1125 kg (was ESTIMATED 1060 kg), displacement 1581 cm3, fuel type LPG (registered conversion); seating 5 ESTIMATED from 'İstiap haddi 04 kişi'. Totals 7 VERIFIED / 23 ESTIMATED / 81 UNKNOWN.
- U-001 and U-010 updated: LPG conversion registered; 'Motor gücü' and 'Azami yüklü ağırlığı' are empty on the documents.

### Fixed
- Two tests assumed a fixed number of VERIFIED values (0 and 2) and failed once real evidence arrived. `test_no_verified_values_without_received_evidence` now checks that every VERIFIED value cites RECEIVED primary evidence; the measurement test compares against the count before recording.

## [0.8.0] - 2026-11-02 - Record integrity, hash verification, wider privacy guard

### Added
- T-018 `kartal_twin.hashes`: SHA-256 verification of audit snapshots and the reference manifest, in `validate`; negative tests for every failure mode.
- T-019 privacy: VIN and credential patterns, `tools/privacy_history_audit.py` (0 findings in 364 blobs), CI step with full history.
- Validator rule and test: recorded commits must be real SHAs that exist in git (D-023).

### Changed
- T-013: `relative_difference_below` is strict; exact-limit and metre/cm entry tests.
- T-011: selection test taps the projected visible point of a part (camera-independent), for three parts in two views.

### Fixed
- Four task results carried placeholder text instead of a commit SHA (T-011, T-013, T-014, T-015); replaced with the real SHAs (bbeefcf, cf87630).

## [0.7.1] - 2026-11-02 - ChatGPT batch-2 review: T-011 and T-013 reworked

### Changed
- T-013: worst-case interval semantics (D-022) - PASS / FAIL / INDETERMINATE; boundary tests for clearance and sum_at_most.
- T-011: the viewer smoke test asserts every interaction (load, part count vs manifest, BDY-003 selection, explode and restore, GLAZING visibility, no console errors) and exits non-zero on failure; read-only test hook in the viewer.
- Recorded ChatGPT ACCEPT for T-001, T-010, T-014, T-015, T-017.

## [0.7.0] - 2026-11-02 - Phase 0 audit, consistency rules, CAD regression gate

### Added
- T-013 dimensional consistency rules DC-001..DC-015 (D-021), wired into `validate` and the measurement intake.
- T-015 golden CAD regression test against `audit/2026-11-02` (proven sensitive to a 1 mm wheelbase change).
- Task schema: description, priority, timestamps, error, evidence; owner-facing status mapping; `tasks/tasks.json` export for orchestrators (n8n). T-013..T-016.

### Fixed
- T-014: misleading measurement examples (`M05 = 2488` and `M20=955` pointed at the wrong quantities) in the guide, intake tool and status file.

## [0.6.0] - 2026-11-02 - Kartal Jarvis organisation: clearance checks, task registry

### Added
- T-001: exact B-rep clearance/interference module (`interfaces.py`, `specs/clearance_rules.yaml`, D-018). CL-001 and CL-002 PASS; values match analytic results.
- Task registry `tasks/T-001..T-009` with an enforced cross-review rule (no self-approval, D-019); generated `TASKS.md`; `ROADMAP.md`; `docs/AUTOMATION_ARCHITECTURE.md`; `agents/REVIEW_REQUEST_T-002.md`. 68 tests.

## [0.5.0] - 2026-11-02 - Independent review and first engineering CAD

### Added
- First engineering CAD: tire design envelopes WHL-001..004 (175/70 R14 designation, ESTIMATED inputs only, DRAFT), per-part and assembly STEP with re-open checks (D-016). Resolver forbids placeholders outside the visual representation.
- `COLLAB_REVIEW_CLAUDE.md`: evidence-backed review for a ChatGPT cross-check. `audit/2026-11-02/` snapshot with SHA256SUMS (D-017).
- Reproducibility tests (separate processes) and a stale-output test: 55 tests.

### Fixed
- `manifest.json` listed stale files from earlier runs and the delivery staging folder; outputs are now cleaned and only this run's files are listed.
- STEP header timestamp is fixed, so CAD STEP files are byte-reproducible (the coloured visual STEP is not, because of OCCT style ordering; it is checked geometrically).
- `tests/test_legacy.py` leaked temporary archives; spec and inventory revision fields updated (were 0.1.0).

## [0.4.0] - 2026-11-02 - Autonomous mode, more literature evidence

### Added
- `tools/photo_scale.py`: side-photo pixel points to VCS mm (wheelbase scale, camera-roll removal, tolerance with a perspective allowance); `--apply` writes ESTIMATED values and never replaces VERIFIED ones. Synthetic tests (50 tests in total).
- `checkpoint.sh` writes an AUTO-CHECKPOINT record into HANDOFF.md on every commit and supports `--wip` emergency saves; `twin.py privacy`; autonomous work protocol in CLAUDE.md.
- Literature evidence E-011..E-013: front/rear track 1386/1327 mm (replacing placeholders), gross mass 1550 kg, engine family (4-cylinder inline SOHC carburettor 1.6, 1581 cm3, ~61 kW, ~131 N·m). 27 ESTIMATED values, still 0 VERIFIED.

## [0.3.2] - 2026-11-02 - Exterior detail (PLACEHOLDER)

### Added
- Rounded roof edges, door handles EXT-006..009, front wipers EXT-015 and wheel hub caps. 35 components built; viewer version 3 published.

## [0.3.1] - 2026-11-02 - Delivery and legacy-archive analysis

### Added
- `scripts/package_delivery.sh`: build, render and package STEP/STL/GLB, per-assembly GLBs, previews, viewer, manifest and the measurement guide into one ZIP (sent to the owner).
- `tools/analyze_legacy.py`: read-only analysis of the legacy archive (three.js JSON, glTF or generic JSON; procedural vs mesh geometry; embedded-image privacy warning). Tested on synthetic archives, since the real ZIP has not been received.

## [0.3.0] - 2026-11-02 - Measurement intake

### Added
- `docs/OLCUM_REHBERI.md` (generated): 31 coded measurements, registration fields and the required photo list.
- `body_profile` spec group (15 UNKNOWN slots; placeholders now `replaces` them). 111 spec parameters in total.
- `tools/record_measurement.py`: owner measurement log, then a MEASUREMENT evidence row, then VERIFIED values (D-015).
- Resolver guard: a stand-in placeholder can only be read through its spec key. 46 tests.

## [0.2.1] - 2026-11-02 - Closures as separate components

### Added
- Hood BDY-003, doors BDY-008..011 and tailgate BDY-012 are cut from the envelope as separate PLACEHOLDER components with 3 mm panel gaps (30 components in total).

### Fixed
- Viewer smoke test: a stale http-server on a fixed port could serve old files to later runs. The test now uses a random port and its own server process.

## [0.2.0] - 2026-11-02 - CAD pipeline and first PLACEHOLDER envelope

### Added
- Literature evidence E-007..E-010 and 11 ESTIMATED spec values (length 4396, width 1642, height 1496, wheelbase 2490, tire 175/70 R14 and others). None are VERIFIED.
- `specs/placeholder_assumptions.yaml`, the provenance-tracking `Resolver`, `layout.py` (wheels, profile, greenhouse) and `cad/` helpers.
- Builders for BODY_ASSEMBLY (BDY-001 envelope), GLAZING (8), WHEELS_AND_TIRES (4), LIGHTING (6) and EXTERIOR_TRIM (5): 24 components, all visual PLACEHOLDER.
- `pipeline.py` and `twin.py build`: STEP, STL, full and per-assembly GLB, manifest.json, and an independent re-open of every export. `twin.py sync-inventory`.
- `gltf_writer.py` (metadata-rich GLB), `tools/render_preview.py` (PNG previews, no GPU) and `tools/spec_set.py`.
- `scripts/run_tests.sh`: records results in `test-results/latest.txt`. `checkpoint.sh` now refuses to commit when tests fail.

### Fixed
- Negative spec tests depended on current data and broke when wheelbase became ESTIMATED (commit 183c608 was pushed with 2 failing tests; fixed in 9b76991).

## [0.1.0] - 2026-11-01 - Phase 0/1: environment, persistence and infrastructure

### Added
- Persistence workflow: `scripts/checkpoint.sh` (validate, commit, push, then verify that the remote SHA equals local HEAD) and `persistence/checkpoint.json` nonce.
- Reproducible environment: `requirements.in` (2 direct dependencies), `requirements.lock` (59 hash-pinned packages), and the idempotent `scripts/setup_env.sh`.
- Master spec `specs/kartal_s_1997.yaml`: 96 parameters, VCS and units. Only 6 identity values are set (ESTIMATED, owner-declared); the rest are UNKNOWN.
- VEHICLE_MASTER inventory `assembly/vehicle_master.yaml`: 17 assemblies, 143 components, no geometry. Generated `COMPONENT_INVENTORY.md`.
- Registers: evidence, uncertainty and engineering decisions; project status.
- Tooling: `tools/twin.py` (validate / inventory / status), `tools/ingest_refs.py` (byte-identical, read-only, checksummed ingestion).
- Library: `kartal_twin.spec`, `.inventory`, `.export_check` (numpy STL/GLB re-open), `.privacy`; 17 assembly builder stubs.
- 32 unit tests, including negative tests proving that fabricated or unsourced data is rejected, and CAD STEP/STL/GLB round-trips.

### Verified
- Push to GitHub, read-back through the GitHub API, fresh clone, and a fresh separate cloud container all returned identical checkpoint content (E-005).
