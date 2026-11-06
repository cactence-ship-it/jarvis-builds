# VEH-01 engine-bay photographic engineering inspection — 2026-11-06

**Vehicle:** 1997 Tofaş Kartal S; owner-reported carburettor petrol/LPG configuration.
**Inspection input:** seven owner-supplied engine-bay photographs received 2026-11-06 (conversation image assets 11849.jpg–11855.jpg).
**Purpose:** record visible configuration, identify CAD subassemblies, safety/condition observations, and define the next evidence gates.
**Evidence class:** direct vehicle photographs. These photographs support visible presence and approximate packaging only; they do not establish hidden geometry, part numbers, exact dimensions, operating condition, or factory originality.

## 1. Executive disposition

The photographs provide useful multi-angle coverage of the engine bay, radiator/fan package, air-cleaner/intake assembly, belt-driven accessories, battery, strut towers, fluid reservoirs, and parts of the electrical harness.

**Disposition: ACCEPT AS PHOTOGRAPHIC PACKAGING EVIDENCE; NOT ACCEPTED AS DIMENSIONAL OR FUNCTIONAL VERIFICATION.**

Do not release the engine-bay CAD as manufacturing-ready. The engine code/architecture, carburettor identity, accessory identities, pulley planes, hose routing, wiring pinouts, reservoir functions, and all hard dimensions remain unresolved unless separately measured or identified.

## 2. Directly visible observations

| ID | Observation | Confidence / CAD treatment |
|---|---|---|
| EB-01 | A large round, clamp-retained air-cleaner housing sits above the engine. | High for visible shape/location; model outer envelope only after measurement. |
| EB-02 | A large black intake duct runs from the air-cleaner area toward the front/side of the bay. A conspicuous white wrap/patch is present at a duct junction. | High for visible routing; treat white patch as an as-found repair/covering of unknown material, not factory geometry. Inspect duct underneath before restoring. |
| EB-03 | A front-mounted radiator with pressure cap and upper/lower coolant hoses is visible. | High for presence; radiator core dimensions, cap rating, hose IDs and flow orientation UNKNOWN. |
| EB-04 | An electric fan and shroud are visible behind the radiator. | High for presence; fan diameter, blade count, motor rating, control logic and clearance UNKNOWN. |
| EB-05 | Multiple belt-driven pulleys/accessories are visible at the front of the engine. | High for presence; accessory identities, belt count/profile, pulley diameters, alignment and tensioning geometry UNKNOWN. Do not label a close-up pump as water or steering pump without tracing its ports/hoses. |
| EB-06 | A dark round reservoir cap near the rear/side of the bay appears marked for power steering fluid. A belt-driven accessory and hoses are also visible in the same general region. | Medium; hydraulic steering is strongly suggested, but pump-to-reservoir hose tracing and rack/box identity are still required. |
| EB-07 | A battery branded İnci Akü is installed. The label appears to contain “44/5” and “258”, but the exact rating string is not reliably legible in the supplied images. | High for brand/presence; voltage, Ah, CCA, dimensions and polarity must be read from a square-on label photo. |
| EB-08 | Left and right front suspension strut-tower top mounts are visible. | High for position; mount pattern, fastener size, tower coordinates and suspension type dimensions UNKNOWN. |
| EB-09 | A translucent rectangular fluid container with a top cap is visible near a strut tower; other small reservoirs/containers are visible toward the firewall. | High for presence; functions must be confirmed by tracing hoses and reading moulded labels. Do not assign coolant/brake/washer function from colour alone. |
| EB-10 | A small electrical box/relay-like unit and several exposed or loosely routed wires are visible near the inner wing/firewall. | High for presence; circuit identity, connector pinout, wire gauge, fuse rating and grounding UNKNOWN. |
| EB-11 | Ignition leads and/or distributor-area hardware are partly visible below/behind the air-cleaner assembly. | Medium; obtain unobstructed close-up before assigning distributor and ignition architecture. |
| EB-12 | The engine is longitudinally installed; the bay has a front radiator package and a round air-cleaner assembly. | High for general packaging; engine family and internal architecture UNKNOWN. |

## 3. Condition and safety observations — inspection required

These are visual inspection prompts, not a remote roadworthiness verdict.

1. **Intake duct patch:** white material at the intake duct joint may be a temporary repair or foreign covering. With engine cold and off, inspect for loose material, air leaks, collapse, unfiltered-air entry and contact with hot/moving parts. Replace with a correctly sized automotive intake coupling if defective.
2. **Electrical routing:** visible loose wiring and non-uniform routing near the firewall/inner wing should be checked for abrasion, heat exposure, unsupported spans, unfused battery feeds, poor grounds and proximity to belts/fan. Photograph and map each conductor before disturbing it.
3. **Battery terminals:** inspect terminal tightness, corrosion, cable insulation, hold-down and positive-terminal protection. Do not short tools across terminals.
4. **Coolant system:** inspect radiator seams, cap neck, hose clamps, hose cracking and fan clearance only when cold and engine off. Never remove a hot radiator cap.
5. **Belts and pulleys:** inspect belt cracking/fraying, alignment, guarding/clearance and accessory bearing noise with engine off. Keep hands, clothing and tools away from belts/fan whenever the engine can run; electric fans can start unexpectedly.
6. **Fluid reservoirs/hoses:** identify each reservoir from its cap marking and trace its hoses. Check for leaks, brittle hoses and fluid contamination; do not top up with an assumed fluid.
7. **Strut towers/inner wings:** inspect for corrosion, cracks, previous repairs, distorted seams and loose fasteners. Photograph both towers square-on.
8. **Fuel/LPG:** the photographs do not establish the complete fuel or LPG installation. Inspect petrol hoses, clamps, LPG vapour/liquid lines, reducer, shutoff valves, wiring, tank certification and leak-tightness through a qualified LPG workshop. Do not loosen LPG fittings or perform an improvised leak test.
9. **White patch and unknown modifications:** preserve the as-found state in the digital twin as a separate condition layer; do not represent repairs/modifications as factory-original components.

## 4. CAD work breakdown and gates

| CAD group | Required geometry / relationships | Current status | Release gate |
|---|---|---|---|
| Engine envelope | Block/head/rocker cover, sump, front cover, mounts, crank axis and engine datum | PHOTO ENVELOPE ONLY | Engine code + measured datums + orthogonal photos |
| Carburettor & ignition | Carb body/base, throttle/choke linkage, distributor, coil, leads | PARTLY OCCLUDED | Manufacturer/model marks and close-ups |
| Air cleaner/intake | Canister, lid/clips, inlet snorkel, duct elbows, clamps and patched joint | PHOTO-LOCATED | Diameter/length/centreline measurements; inspect patch |
| Cooling | Radiator, cap/neck, fan/shroud, hoses, thermostat outlet | PHOTO-LOCATED | Core and mounting measurements; hose tracing |
| Accessory drive | Crank/accessory pulleys, belts, brackets, tensioner, pulley planes | PHOTO-LOCATED | Identify each accessory; measure centres, diameters and offsets |
| Hydraulic steering | Reservoir, pump, pressure/return hoses, steering gear | PROVISIONAL | Trace both hoses and read component labels |
| Electrical | Battery, starter/alternator paths, relays, grounds, fan circuit, ignition and loom clips | AS-FOUND ROUTE ONLY | Wiring diagram + conductor-by-conductor trace |
| Fluid containers | Each reservoir, cap, mount and hose connection | UNIDENTIFIED | Read moulded/printed labels and trace hoses |
| Body-in-white bay | Strut towers, inner wings, radiator support, firewall, hood hinge/latch | PHOTO-LOCATED | Datum-based measurements and corrosion survey |

**Coordinate convention for future CAD:** vehicle X positive forward, Y positive vehicle-left, Z positive upward; origin at a clearly selected and physically measured chassis/body datum. This is a proposed project convention, not a factory coordinate system. Record the selected origin and all measurement setups in the master specification before adding coordinates.

## 5. Measurements to capture (mm unless stated)

Do not estimate these from perspective photographs. Use a tape/caliper, plumb references and repeat measurements; record tool accuracy and photo ID.

- Engine: crankshaft centreline height and lateral offset from vehicle centre plane; engine mount bolt centres; block/head maximum envelope; front pulley plane.
- Air cleaner: housing maximum diameter/height; lid and base heights; duct outside diameters; clamp positions; duct centreline stations.
- Radiator: core width/height/thickness; mounting-hole centres; cap-neck position; fan/shroud envelope; hose outside diameters and endpoints.
- Accessory drive: each pulley centre coordinate; pulley OD and groove count/profile; belt path; belt part marking; bracket mounting-hole centres.
- Steering: reservoir/pump label; suction/return/pressure hose IDs and endpoints; pump shaft/pulley plane; steering gear label.
- Electrical: battery L×W×H, terminal orientation and label; ground points; connector IDs; fuse/relay markings; wire colours and measured conductor cross-sections.
- Body: strut-tower stud pattern; tower-centre coordinates; radiator support mounting holes; firewall and inner-wing reference points.

For every measurement, store: value, unit, method, instrument, tolerance/uncertainty, operator, date, evidence reference and verification status. A photograph without a scale is not a dimensional measurement.

## 6. Required follow-up evidence

Priority order:

1. Engine block code/serial stamping, cleaned only gently and photographed square-on; do not grind or abrade the stamp.
2. Carburettor make/model stamp, top and both sides, base flange, throttle/choke linkage.
3. Distributor body/cap and ignition coil labels; clear view of plug-wire routing.
4. Full front view of engine with air-cleaner removed only by a competent person and with engine cold/off; include carburettor and mounting flange. Refit correctly before operation.
5. Radiator label/core dimensions and close-ups of both hose endpoints, cap markings and fan electrical connector.
6. Every belt marking and a clear image of each driven accessory and its hose/connector ports.
7. Battery label square-on and battery hold-down/terminal close-ups.
8. Reservoir cap labels and hose endpoint photos; identify each fluid before service.
9. Both strut towers and inner wings square-on, plus firewall relay/loom close-ups.
10. LPG reducer, valves, line routing and tank identification plate, photographed without loosening fittings.

## 7. Engineering conclusions

- The new photographs materially improve the engine-bay packaging evidence and support creating separate CAD envelopes for the air-cleaner/intake, radiator/fan, accessory drive, battery, reservoirs, strut towers and visible harness.
- They do **not** resolve the carburettor engine's exact family, code, displacement, bore/stroke, cylinder-head architecture or internal dimensions.
- The photographed pulley-driven unit must remain **ACCESSORY-UNKNOWN** until its hose ports and mounting are traced. Do not confuse the water pump, alternator and hydraulic steering pump.
- The label on the battery is not sufficiently legible to publish a verified Ah/CCA value.
- The white intake patch, visible loose wiring and general ageing/contamination require physical inspection before the vehicle is considered serviceable.
- No measured dimensions, manufacturer part numbers, fuse ratings, connector pinouts or verified factory routing are added by this inspection.

**Release decision:** ENGINE-BAY CAD = HOLD / PHOTO-REFERENCE ONLY. The next valid step is measurement and component identification, not detailed parametric modelling from guessed dimensions.
