# VEH-01 Mechanical + Electrical Harness Modelling Plan

**Vehicle:** 1997 Tofaş Kartal S  
**Scope:** mechanical assembly and electrical harness digital twin  
**Representation:** visual envelope / engineering CAD / mechanical assembly remain separate.

## 1. What is established

The project evidence register and owner photo handoff describe a longitudinal front engine, carburettor configuration, manual transmission, rear-wheel drive, MacPherson front suspension, rigid rear axle, hydraulic steering, battery in the engine bay, electric radiator fan, and a toroidal LPG tank in the rear spare-wheel-well region. These are arrangement/configuration observations, not dimensional drawings. The private photo originals remain outside the public repository.

The carburettor variant is mandatory. Do not import 1.6 i.e. fuel-injection ECU, injector, fuel-pump relay or injection-only sender geometry. Trim/year-specific secondary evidence makes a 1.6 SOHC 8-valve Tempra-family carburettor architecture the leading provisional candidate for a 1997 Kartal S. The exact engine code is UNKNOWN: 131.D2.016 is directly listed for Şahin S, not conclusively for this Kartal; D1/D2 mappings vary among secondary sources. S-specific sources report ~86 hp DIN, while 1997 marketplace records show 83 hp / 131 Nm / 1,581 cc, D2 cross-model records 92 hp SAE / 123 Nm, and generic Kartal 81 bhp. Keep all outputs and internals unverified. See `docs/SECONDARY_SOURCE_RESEARCH_2026-11-06.md` for variant evidence and source conflicts.

## 2. Mechanical CAD work breakdown

Use the register in `specs/mechanical_subassembly_register.yaml`. Model each part as a separate stable-ID component, not one fused mesh.

| Work package | Components to detail | Current modelling state | Evidence needed to move beyond placeholder |
|---|---|---|---|
| ENG-01 | block, head, crank, rods, pistons, timing, valve train | neutral envelope / internals not modelled | engine code/stamp, casting marks, workshop manual matching that engine, bore/stroke and bearing measurements |
| ENG-02 | carburettor, throttle/choke, intake/exhaust manifolds | envelope only | carburettor make/model, flange pattern, linkage photos and measurements |
| ENG-03 | distributor, coil, HT leads, starter, alternator | envelope only | labels, terminal views, bracket and pulley measurements |
| COOL-01 | radiator, fan, shroud, water pump, thermostat and hoses | envelope only | core dimensions, hose OD/ID, neck positions, fan label |
| TRN-01 | flywheel, clutch, gearbox, selector, mounts | envelope only | gearbox code, spline counts, clutch friction OD/ID, mount coordinates |
| DRV-01 | propeller shaft, U-joints, centre bearing if fitted, differential, axle | envelope only | shaft length at ride height, flange PCD, joint series, differential tag/ratio, axle dimensions |
| FSU-01 | struts, top mounts, springs, lower arms, knuckles, hubs, anti-roll bar | envelope only | pickup coordinates, strut length, spring dimensions, hub PCD/centre bore |
| STE-01 | steering wheel, column, joints, hydraulic pump, steering gear and hoses | envelope only | steering gear ID, shaft spline, column joints, pump label and hose fittings |
| RSU-01 | rear springs, dampers, axle links and brackets | envelope only | actual spring type, seat centres, damper eye lengths, link topology |
| BRK-01 | master cylinder, booster if fitted, front discs/calipers, rear drums/shoes, hard lines | neutral envelope | actual front hardware, disc stamp/MIN TH, drum ID, cylinder and hose labels |
| FUL-01 | petrol tank, sender, mechanical pump, filter, carburettor feed | envelope only | tank label/capacity, sender resistance, pump model, pipe routing |
| LPG-01 | toroidal tank, multivalve, reducer, shutoff valves, filler and approved lines | tank local-frame CAD only; installation geometry blocked | tank maker/serial/dimensions, reducer and multivalve labels, certified installer inspection |
| EXH-01 | manifold, downpipe, intermediate pipe, silencer, heat shields | envelope only | pipe OD, silencer shell dimensions, hanger coordinates and underbody photos |

### Mechanical CAD acceptance

1. Every component has a stable ID, independent object and source/status metadata.
2. VCS coordinate convention is preserved: X rearward, Y right, Z up; origin at front axle centreline / vehicle centre plane / ground.
3. Unknown types are neutral envelopes; unknown dimensions remain null.
4. No estimated dimension is promoted to VERIFIED without received measurement, document or photo evidence.
5. STEP exports are re-opened and checked for units, solid count, invalid topology and assembly placement.
6. Brakes, steering, suspension and LPG remain non-production visual/engineering references until physical measurement and qualified review.

## 3. Electrical harness route matrix

The source-of-truth matrix is `specs/electrical_harness_route_matrix.yaml`. It divides the loom into these separately selectable CAD groups:

- HAR-BAT: battery, starter, alternator and grounds
- HAR-IGN / HAR-HT: ignition primary and high-tension leads (kept separate)
- HAR-LIGHT-F: headlamps, indicators and horn
- HAR-DASH: cluster, switches and cabin controls
- HAR-REAR: rear lamps, tailgate flex section and sender
- HAR-WIPER: wiper motor and washer pump
- HAR-COOL: radiator fan control
- HAR-FUEL: petrol sender and gauge
- HAR-LPG: LPG selector and solenoid control
- HAR-GND: body/engine grounding network

Routes are schematic centre-lines, not wire cut lengths. The exact factory wiring diagram, fuse-box map, wire colours, cross-sections, fuse ratings, relay terminals, connector pinouts and circuit protection values have not been received. They must remain UNKNOWN rather than being fabricated.

### Harness CAD acceptance

1. Each branch is a separate selectable object with branch ID and endpoint labels.
2. Harness routes follow observed clips/grommets where evidence exists; guessed clips remain PLACEHOLDER.
3. Engine-bay, cabin, rear-body, HT ignition and LPG branches have separate layers/groups.
4. Connector shells are modelled only after connector family and pin count are photographed.
5. Wire colours, gauge, fuse rating, pinout and exact route length remain null until source evidence is received.
6. Harness and fuel/LPG routes are checked for heat, abrasion, water, moving-part and service-access conflicts.
7. LPG electrical and fuel-system details are reviewed by a qualified LPG technician; this CAD is not an installation guide.

### New photo audit (2026-11-06)

Seven additional owner-supplied engine-bay views have been reviewed. See `docs/ENGINE_BAY_PHOTO_INSPECTION_2026-11-06.md` for the OBSERVED/UNKNOWN register, photo-only safety holds, engine-variant caveat and metric survey plan. The new photos improve visual arrangement evidence but provide no calibrated dimensions and do not resolve the engine code or OHV/SOHC architecture. Do not promote the accessory-pump identity, reservoir circuit assignments or harness pinouts from visual appearance alone.

## 4. Immediate evidence collection priority

1. Engine block stamping and clear photos of both engine sides, carburettor, distributor, coil, alternator and starter labels.
2. Full fuse/relay panel: cover diagram, fuse values, relay markings, rear connector side.
3. Front loom at headlamps, radiator fan and engine-bay bulkhead grommet.
4. Dashboard cluster rear connectors and LPG selector label.
5. Rear tail lamp connectors, tailgate flexible boot, fuel sender connector and body grounds.
6. Underbody photos along both sills, gearbox tunnel, propeller shaft, rear axle, brake pipes, petrol/LPG lines and exhaust.
7. Mechanical measurements from the existing coded guide; prioritise engine mount centres, gearbox mounts, propeller shaft joint centres, suspension pickup points and brake hardware.

## 5. Research baseline and limitations

- Otiva's Kartal catalogue groups cooling, gearbox/clutch, brakes, lighting, ignition, electrical/charging and suspension/steering components. It is a parts catalogue, not a factory wiring diagram.
- CarBrands lists a 1995–2001 1.6 81 bhp carburettor variant separately from 1997–2001 1.6 i.e. 96 bhp. The latter's ECU/injection architecture must not be used for VEH-01.
- Secondary sources disagree on variant specifications; catalogue fitment is not proof of exact fitment on this individual car.
- No factory 1997 Kartal S carburettor wiring diagram with trustworthy connector/pin detail has been received in this work package.

## 6. Next engineering sequence

A. Confirm engine code and ignition subtype.  
B. Capture fuse/relay box and loom connector evidence.  
C. Replace guessed mechanical envelopes with measured interfaces.  
D. Build per-branch harness geometry and connector objects.  
E. Run interference/clearance checks against engine, exhaust, suspension and LPG groups.  
F. Export/re-open STEP and GLB; attach evidence and test reports to the same commit.
