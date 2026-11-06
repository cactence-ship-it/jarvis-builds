# VEH-01 engine-bay photo engineering audit — 2026-11-06

**Vehicle:** owner-reported 1997 Tofaş Kartal S, carburettor, petrol + LPG  
**Evidence:** seven owner-supplied engine-bay photographs in the current conversation, multiple oblique and close-up views. Original images remain private and are not copied into this public repository.  
**Purpose:** visual configuration audit and evidence-led CAD planning. This is not a physical inspection, a repair instruction, or a production drawing.

## 1. Executive determination

The new photo set materially improves the engine-bay arrangement evidence. It visibly records the air-cleaner assembly and intake duct, radiator/fan package, belt-and-pulley accessory zone, battery, two front strut-tower tops, fluid reservoirs, and portions of the engine-bay wiring.

It does **not** resolve the engine code, OHV/SOHC architecture, carburettor make/model, distributor subtype, exact accessory identity, hose circuit assignments, electrical pinouts, or any production dimensions. The engine and ancillary CAD must therefore remain PLACEHOLDER/envelope geometry. No dimension may be scaled from these perspective photographs because there is no calibrated scale reference.

## 2. Photo-observed register

| Visual ID | Observation | Evidence status | CAD / engineering disposition |
|---|---|---|---|
| EB-PH-01 | Round, top-mounted air-cleaner housing with radial ribs and perimeter retaining clips | OBSERVED | Create separate outer-envelope object only; canister diameter, height, base and fastener locations UNKNOWN |
| EB-PH-02 | Large black intake duct from the air-cleaner area toward the front of the bay; a white textile-like wrap is visible at one joint | OBSERVED | Record duct centreline as schematic; joint condition is a pre-start inspection item. Do not model the wrap as an original component |
| EB-PH-03 | A side opening/branch is visible on the intake duct in one angle | OBSERVED, function UNKNOWN | Do not cap or connect it in CAD until its intended resonator/snorkel/vent function is identified |
| EB-PH-04 | Radiator core, filler neck/cap, upper hose and lower hose region visible | OBSERVED | Radiator/fan package can be positioned schematically; core dimensions, neck OD, pressure-cap rating and mount coordinates UNKNOWN |
| EB-PH-05 | Fan blade/shroud and electric motor area visible behind the radiator | OBSERVED | Model fan, motor and shroud as separate placeholder objects; motor label, blade diameter, rotation, relay/control and clearances UNKNOWN |
| EB-PH-06 | Multiple belt pulleys and a belt-driven cast accessory unit visible at the engine front | OBSERVED; unit identity UNKNOWN | Record pulley axes and belt path only after measurement; do not label the visible unit as alternator, water pump, A/C or steering pump from these images alone |
| EB-PH-07 | Battery installed in the engine bay on a tray/retainer; brand label appears to read İnci Akü | OBSERVED | Battery case and tray may be represented by measured envelope; exact battery model, capacity, terminal standard and hold-down dimensions remain UNKNOWN |
| EB-PH-08 | Both front strut-tower top regions and central mount hardware are visible across the wider views | OBSERVED | Use only as body/underhood landmarks; no suspension pickup coordinates or strut geometry can be extracted from perspective alone |
| EB-PH-09 | More than one translucent fluid container/cap is visible; one cap carries a power-steering legend or similar moulded marking | OBSERVED; circuit assignment pending | Identify each container by tracing its hoses to the terminating component before assigning system IDs or fluid type |
| EB-PH-10 | Loose/untidy wiring, auxiliary relay-like devices and loom sections are visible near the inner wing/firewall/battery region | OBSERVED | Add route corridors as provisional only; conductor colour, gauge, fuse rating, relay function, connector pinout and circuit topology remain UNKNOWN |
| EB-PH-11 | Engine top and ancillary areas are partly obscured by the air cleaner, ducts and hoses | OBSERVED | Carburettor, distributor, ignition coil, engine stamp and starter labels are not sufficiently legible in this batch |

**Evidence boundary:** OBSERVED means visible in the photographs; it does not mean the component is tested, serviceable, original to the factory, or dimensionally verified.

## 3. Engine variant and source cross-check

A secondary vehicle database lists a 1995–2001 Kartal 1.6 carburettor record at 1,585 cm³, 81 bhp, 124 Nm, 86.4 mm bore, 67.4 mm stroke and 8.3:1 compression. The same page states that its information is collected from public sources and is not guaranteed. These figures are a **candidate record**, not verified VEH-01 specifications.

Other secondary sources describe multiple Kartal engine families across the period, including earlier 1.6 OHV, later 1.6 SOHC and separate 1.6 i.e. injection variants. Their year/trim descriptions do not agree completely. The new photographs show a round air cleaner and an intake duct but do not expose a legible block stamp or enough of the cylinder-head/timing arrangement to resolve OHV versus SOHC.

**Variant gate remains in force:**
- Retain owner-reported carburettor configuration as the working fuel-system assumption.
- Do not import 1.6 i.e. ECU, injector, throttle-body, injection-only fuel pump relay or injection loom geometry.
- Keep engine family/code, displacement, bore/stroke, compression ratio, cam/timing architecture and distributor subtype UNKNOWN until the physical engine stamp and matching documents are obtained.

Sources:
1. Carbrands, Kartal 1.6 (81 bhp), 1995–2001 (secondary aggregated specification; its own disclaimer says public-source data are not guaranteed): https://carbrands.com.tr/motor/tofas/kartal/tofas-kartal/1-6-81-bg-1995-2001
2. Araç Pazarı, Kartal 1988–2002 engine-option summary (secondary source showing OHV/SOHC/i.e. variant split; year ranges require cross-check): https://aracpazari.com.tr/tofas/kartal/kartal-2-1988-2002
3. TRmotosports, Kartal 1.6 (81 hp) specification summary (corroborating secondary record): https://www.trmotosports.com/tofas-kartal-1-6-81-hp-teknik-ozellikler/
4. Parcacim, M131/SLX parts category catalogue (use for component taxonomy and year/engine filtering only, not exact fitment): https://www.parcacim.tr/tofas/sahin-dogan-kartal
5. Otiva, Kartal parts catalogue (use for system family discovery only): https://otiva.com.tr/yedek-parcalar/tofas/tofas-kartal

## 4. Photo-only condition and safety holds

These are screening observations, not confirmed defects. Have a competent automotive technician inspect the vehicle before running or driving it.

1. **Intake joint / white wrap:** the textile-like wrapping at an intake-duct joint may be a temporary patch. Check the joint for loose material, unmetered/unfiltered air entry, cracks and secure clamps. Do not leave loose cloth or tape where it could be drawn into the intake. Restore the correct duct/joint arrangement after identifying the intended connection.
2. **Intake side opening:** identify whether the visible side port is a designed snorkel/resonator connection or a disconnected branch. Do not blindly plug it; use the correct airbox/duct diagram or trace the original part.
3. **Wiring around battery and firewall:** inspect insulation, terminal security, grounding, abrasion points, heat exposure, added relays and appropriate circuit protection. Do not infer wire size or fuse ratings from appearance.
4. **Belts and rotating equipment:** with engine OFF, inspect belt condition, alignment, pulley runout and specified tension. Keep hands, clothing and tools clear; an electric cooling fan can start unexpectedly.
5. **Cooling circuit:** inspect radiator, cap, hoses, clamps, fan mounting and signs of leakage. Never open a hot/pressurised cooling system. Verify fan control with a qualified technician.
6. **Fluid reservoirs:** positively identify each reservoir and trace every hose before topping up or assigning fluid type. Do not mix or add fluid based only on container appearance.
7. **Battery:** verify label/model, polarity, terminal condition, hold-down and cable routing. The available label view is not sufficient to certify battery capacity or terminal specification.
8. **LPG equipment:** do not adjust, disconnect, pressure-test or re-route LPG components based on these photographs. A certified LPG technician must inspect the reducer, shut-off valves, multivalve, hoses, electrical cut-off and leak integrity.

**No roadworthiness or operational approval is issued by this photo review.** Brakes, steering, suspension, tyres, fuel/LPG system, mounts, cooling and charging systems still require direct physical inspection and tests.

## 5. CAD survey plan — required measurements

Use the project vehicle coordinate system (VCS): X rearward, Y vehicle-right, Z upward. Preserve the existing origin definition (front axle centreline / vehicle centre plane / ground). Record measurements in millimetres, instrument used, date, photo ID and uncertainty. Take orthogonal front/top/side views with a rigid metric scale in the same plane as the measured feature.

| Survey ID | Required measurement / evidence | Intended CAD use |
|---|---|---|
| EB-M01 | Engine code/serial and block/head casting marks, square-on readable photos | Select correct engine family and matching manual |
| EB-M02 | Engine block/head/sump envelope L×W×H and crankshaft centreline coordinates | ENG block/head placement and orientation |
| EB-M03 | Left/right engine mount bolt-centre coordinates, bolt diameters and bracket thickness | Engine mount and chassis interface |
| EB-M04 | Carburettor make/model, throat, base flange hole pattern, height, throttle/choke lever pivots | Carburettor/manifold and controls |
| EB-M05 | Air-cleaner outer diameter/height, inlet/outlet ID/OD, mount points, duct OD and centreline stations | Air-cleaner and intake duct geometry |
| EB-M06 | Radiator core W×H×T, mount centres, cap-neck position, inlet/outlet OD and 3D coordinates | Radiator and hose routing |
| EB-M07 | Fan/shroud outside envelope, motor centre, blade OD, mount coordinates and connector/label | Cooling fan assembly |
| EB-M08 | Every pulley centre coordinate, pulley OD/width/groove profile, belt section and routing; identify unit from label/trace | Accessory drive and belt clearance |
| EB-M09 | Battery case L×W×H, tray envelope, clamp/hold-down positions, terminal polarity and label | Battery/tray and high-current harness |
| EB-M10 | Reservoir labels, body dimensions, outlet positions and hose destination tracing | Correct fluid system assignment |
| EB-M11 | Harness grommet, clips, relay mounting, connector IDs and endpoints; photograph both connector faces | Branch routing and connector objects |

Do not measure near running belts or a running fan. Disconnecting a battery, opening cooling components or handling LPG parts is outside this photo-survey procedure and must be done under the appropriate workshop safety process.

## 6. Harness implications

The photographs add visible engine-bay route corridors around the battery/tray, radiator/fan, air-cleaner/intake area, firewall and inner wings. They do not establish circuit topology. Add route landmarks only as provisional visual references. Keep the following as UNKNOWN until the exact vehicle loom or matching 1997 carburettor wiring diagram is available: wire colours, cross-sections, fuse and relay ratings/terminals, connector pinouts, fan-control logic, ignition feed, ground strap sizes and route cut lengths.

Keep ignition HT leads, battery/starter/alternator high-current conductors, cooling-fan branch, dashboard loom and LPG controls as separate selectable groups. Confirm all endpoints by tracing the physical loom; no wire should be connected based on this photo interpretation.

## 7. Disposition and next acceptance gates

- [x] Record visible engine-bay component groups and their evidence limits.
- [x] Keep ambiguous component identity and all unmeasured dimensions UNKNOWN.
- [x] Add safety screening and measurement protocol.
- [ ] Obtain legible engine code / casting marks and registration engine fields; resolve OHV/SOHC.
- [ ] Identify carburettor, distributor, ignition coil, alternator, starter and every belt-driven accessory by label and hose/wire tracing.
- [ ] Capture radiator/fan/battery/reservoir dimensions and mounting coordinates.
- [ ] Obtain the matching factory wiring diagram and fuse/relay/connector views.
- [ ] Replace all engine-bay envelopes with measured geometry; run STEP/GLB round-trip, clearance and independent review gates.

**Current decision:** photo arrangement evidence improved; mechanical/electrical assemblies remain schematic PLACEHOLDER. No manufacturing dimensions, installation instructions or verified vehicle-specific part numbers are added by this audit.
