# Component Inventory - VEHICLE_MASTER

<!-- GENERATED from assembly/vehicle_master.yaml by `python tools/twin.py inventory`. Do not edit by hand; edit the YAML and regenerate. -->

Source of truth: `assembly/vehicle_master.yaml` (revision 0.7.0). Components: **157** in **17** assemblies.

Verification status: VERIFIED 2, ESTIMATED 5, UNKNOWN 150.  
Geometry with any content (visual / CAD / mechanical): 35 / 9 / 0.

Legend: fitment = CONFIRMED / UNCONFIRMED / ABSENT on this vehicle; `opt` = may not be fitted; geometry states NONE < PLACEHOLDER < LEGACY_IMPORT < DRAFT < VALIDATED.

| Assembly | Prefix | Phase | Components |
|---|---|---|---|
| BODY_ASSEMBLY | BDY | 4 | 12 |
| EXTERIOR_TRIM | EXT | 4 | 16 |
| GLAZING | GLZ | 4 | 8 |
| LIGHTING | LGT | 4 | 10 |
| INTERIOR | INT | 5 | 21 |
| ENGINE | ENG | 6 | 11 |
| TRANSMISSION | TRN | 6 | 3 |
| DRIVETRAIN | DRV | 6 | 3 |
| CHASSIS | CHS | 7 | 4 |
| FRONT_SUSPENSION | FSU | 8 | 11 |
| REAR_SUSPENSION | RSU | 8 | 9 |
| STEERING | STR | 8 | 5 |
| BRAKING | BRK | 8 | 8 |
| FUEL_SYSTEM | FUL | 7 | 14 |
| EXHAUST | EXH | 7 | 4 |
| ELECTRICAL | ELE | 9 | 9 |
| WHEELS_AND_TIRES | WHL | 4 | 9 |

## BODY_ASSEMBLY

Body-in-white and closures. Construction type (unibody or not) is UNKNOWN until underbody evidence (spec body.body_construction).

| ID | Component | Fitment | Status | Visual | CAD | Mech | Depends on | Sources |
|---|---|---|---|---|---|---|---|---|
| BDY-001 | Body shell (body-in-white) | CONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | - | E-003, E-026 |
| BDY-002 | Roof panel | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-001 | - |
| BDY-003 | Hood (bonnet) | CONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-001 | E-026 |
| BDY-004 | Front fender, LH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-001 | - |
| BDY-005 | Front fender, RH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-001 | - |
| BDY-006 | Rear quarter panel, LH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-001 | - |
| BDY-007 | Rear quarter panel, RH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-001 | - |
| BDY-008 | Front door, LH | CONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-001 | E-026 |
| BDY-009 | Front door, RH | CONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-001 | E-026 |
| BDY-010 | Rear door, LH | CONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-001 | E-026 |
| BDY-011 | Rear door, RH | CONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-001 | E-026 |
| BDY-012 | Tailgate | CONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-001 | E-003, E-026 |

## EXTERIOR_TRIM

Bolt-on exterior parts. The exhaust outlet is EXH-004 (no duplicates across assemblies).

| ID | Component | Fitment | Status | Visual | CAD | Mech | Depends on | Sources |
|---|---|---|---|---|---|---|---|---|
| EXT-001 | Front bumper | CONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-001 | E-026 |
| EXT-002 | Rear bumper | CONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-001 | E-026 |
| EXT-003 | Radiator grille | CONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-001 | E-026 |
| EXT-004 | Exterior mirror, LH | CONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-008 | E-026 |
| EXT-005 | Exterior mirror, RH | CONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-009 | E-026 |
| EXT-006 | Outer door handle, front LH | UNCONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-008 | - |
| EXT-007 | Outer door handle, front RH | UNCONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-009 | - |
| EXT-008 | Outer door handle, rear LH | UNCONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-010 | - |
| EXT-009 | Outer door handle, rear RH | UNCONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-011 | - |
| EXT-010 | Tailgate handle / release | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-012 | - |
| EXT-011 | Side protective mouldings (set) (opt) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-001 | - |
| EXT-012 | Roof rail, LH (opt) | CONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-002 | E-026 |
| EXT-013 | Roof rail, RH (opt) | CONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-002 | E-026 |
| EXT-014 | Door and tailgate seals (set) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-008, BDY-009, BDY-010, BDY-011, BDY-012 | - |
| EXT-015 | Front wiper system (arms, blades, linkage, motor) | CONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-001, ELE-007 | E-026 |
| EXT-016 | Rear (tailgate) wiper (opt) | CONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-012, ELE-007 | E-026 |

## GLAZING

All glass. Rear-door fixed vent glass will be added only if the photos show it.

| ID | Component | Fitment | Status | Visual | CAD | Mech | Depends on | Sources |
|---|---|---|---|---|---|---|---|---|
| GLZ-001 | Windshield | CONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-001 | E-026 |
| GLZ-002 | Tailgate (rear) glass | CONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-012 | E-003, E-026 |
| GLZ-003 | Front door glass, LH | UNCONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-008 | - |
| GLZ-004 | Front door glass, RH | UNCONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-009 | - |
| GLZ-005 | Rear door glass, LH | UNCONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-010 | - |
| GLZ-006 | Rear door glass, RH | UNCONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-011 | - |
| GLZ-007 | Rear quarter (side) glass, LH | UNCONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-006 | - |
| GLZ-008 | Rear quarter (side) glass, RH | UNCONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-007 | - |

## LIGHTING

Lamps as physical parts; their circuits are ELE-005.

| ID | Component | Fitment | Status | Visual | CAD | Mech | Depends on | Sources |
|---|---|---|---|---|---|---|---|---|
| LGT-001 | Headlamp, LH | CONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-001, ELE-005 | E-026 |
| LGT-002 | Headlamp, RH | CONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-001, ELE-005 | E-026 |
| LGT-003 | Front indicator, LH | UNCONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-001, ELE-005 | - |
| LGT-004 | Front indicator, RH | UNCONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-001, ELE-005 | - |
| LGT-005 | Side repeater, LH (opt) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-004, ELE-005 | - |
| LGT-006 | Side repeater, RH (opt) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-005, ELE-005 | - |
| LGT-007 | Tail lamp, LH | CONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-006, ELE-005 | E-026 |
| LGT-008 | Tail lamp, RH | CONFIRMED | UNKNOWN | PLACEHOLDER | NONE | NONE | BDY-007, ELE-005 | E-026 |
| LGT-009 | Licence-plate lamp | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | ELE-005 | - |
| LGT-010 | Interior lamp(s) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | INT-018, ELE-005 | - |

## INTERIOR

Cabin and cargo-area parts. Steering wheel and column are kept here per the master directive; the steering gear is STR-001.

| ID | Component | Fitment | Status | Visual | CAD | Mech | Depends on | Sources |
|---|---|---|---|---|---|---|---|---|
| INT-001 | Dashboard (instrument panel) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-001 | E-003 |
| INT-002 | Instrument cluster | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | INT-001, ELE-006 | - |
| INT-003 | Steering wheel | CONFIRMED | UNKNOWN | NONE | NONE | NONE | INT-004 | E-003, E-024 |
| INT-004 | Steering column | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | STR-001, BDY-001 | - |
| INT-005 | Pedal box (clutch, brake, accelerator) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-001 | - |
| INT-006 | Gear lever | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | TRN-003 | - |
| INT-007 | Handbrake lever | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BRK-008 | - |
| INT-008 | Centre console | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | CHS-001 | - |
| INT-009 | Front seat, LH | CONFIRMED | UNKNOWN | NONE | NONE | NONE | INT-012, CHS-001 | E-003, E-024 |
| INT-010 | Front seat, RH | CONFIRMED | UNKNOWN | NONE | NONE | NONE | INT-012, CHS-001 | E-003, E-024 |
| INT-011 | Rear seat (cushion and backrest) | CONFIRMED | UNKNOWN | NONE | NONE | NONE | CHS-001 | E-024 |
| INT-012 | Seat frames and runners (set) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | CHS-001 | - |
| INT-013 | Door card, front LH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-008 | - |
| INT-014 | Door card, front RH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-009 | - |
| INT-015 | Door card, rear LH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-010 | - |
| INT-016 | Door card, rear RH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-011 | - |
| INT-017 | Door controls (window winders or switches, inner handles, lock buttons - set) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | INT-013, INT-014, INT-015, INT-016 | - |
| INT-018 | Headliner | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-002 | - |
| INT-019 | Carpets (set) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | CHS-001 | - |
| INT-020 | Interior trim panels (pillars, quarters - set) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-001 | - |
| INT-021 | Cargo compartment trim and floor covering | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | CHS-001, BDY-012 | E-003 |

## ENGINE

Engine variant UNKNOWN (U-001) - no engine geometry until it is identified. Alternator and starter live here (mechanically engine-mounted); ELECTRICAL references them.

| ID | Component | Fitment | Status | Visual | CAD | Mech | Depends on | Sources |
|---|---|---|---|---|---|---|---|---|
| ENG-001 | Engine block | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | - | - |
| ENG-002 | Cylinder head | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | ENG-001 | - |
| ENG-003 | Valve (cam) cover | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | ENG-002 | - |
| ENG-004 | Oil pan (sump) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | ENG-001 | - |
| ENG-005 | Intake system (manifold, air filter) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | ENG-002 | - |
| ENG-006 | Exhaust manifold | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | ENG-002 | - |
| ENG-007 | Carburettor (petrol fuel delivery; fuel-injected variants excluded) | UNCONFIRMED | ESTIMATED | NONE | NONE | NONE | ENG-005, FUL-002 | E-017, E-012, E-013 |
| ENG-008 | Cooling system (radiator, pump, thermostat, hoses, fan) | CONFIRMED | UNKNOWN | NONE | NONE | NONE | ENG-001, BDY-001 | E-027 |
| ENG-009 | Alternator | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | ENG-001, ELE-007 | - |
| ENG-010 | Starter motor | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | ENG-001, ELE-007 | - |
| ENG-011 | Engine mounts | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | ENG-001, CHS-004 | - |

## TRANSMISSION

Gearbox type and gear count UNKNOWN until evidence (spec transmission.*).

| ID | Component | Fitment | Status | Visual | CAD | Mech | Depends on | Sources |
|---|---|---|---|---|---|---|---|---|
| TRN-001 | Gearbox | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | ENG-001 | - |
| TRN-002 | Clutch assembly and actuation | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | ENG-001, TRN-001, INT-005 | - |
| TRN-003 | Gearshift linkage | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | TRN-001 | - |

## DRIVETRAIN

Drive layout UNKNOWN (U-006). The propeller shaft exists only for a front-engine RWD layout.

| ID | Component | Fitment | Status | Visual | CAD | Mech | Depends on | Sources |
|---|---|---|---|---|---|---|---|---|
| DRV-001 | Propeller shaft (opt) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | TRN-001, DRV-002 | - |
| DRV-002 | Differential / final drive | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | CHS-004 | - |
| DRV-003 | Axle shafts / drive shafts | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | DRV-002 | - |

## CHASSIS

Underbody structure. Mapped elsewhere to avoid duplicates: fuel tank FUL-001, fuel lines FUL-002, brake lines BRK-003, exhaust routing EXH-003.

| ID | Component | Fitment | Status | Visual | CAD | Mech | Depends on | Sources |
|---|---|---|---|---|---|---|---|---|
| CHS-001 | Floor pan | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-001 | - |
| CHS-002 | Longitudinal structural members (rails, sills) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-001 | - |
| CHS-003 | Crossmembers | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | CHS-002 | - |
| CHS-004 | Mounting interfaces (engine, suspension, axle - set) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | CHS-002, CHS-003 | - |

## FRONT_SUSPENSION

Front suspension type UNKNOWN; component names are type-neutral until evidence.

| ID | Component | Fitment | Status | Visual | CAD | Mech | Depends on | Sources |
|---|---|---|---|---|---|---|---|---|
| FSU-001 | Front spring, LH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | FSU-011 | - |
| FSU-002 | Front spring, RH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | FSU-011 | - |
| FSU-003 | Front damper, LH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | FSU-011 | - |
| FSU-004 | Front damper, RH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | FSU-011 | - |
| FSU-005 | Front lower control arm, LH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | FSU-011 | - |
| FSU-006 | Front lower control arm, RH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | FSU-011 | - |
| FSU-007 | Front anti-roll bar and links (opt) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | FSU-011 | - |
| FSU-008 | Front suspension bushings (set) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | FSU-005, FSU-006 | - |
| FSU-009 | Front hub / knuckle, LH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | FSU-005 | - |
| FSU-010 | Front hub / knuckle, RH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | FSU-006 | - |
| FSU-011 | Front suspension mounting points (set) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | CHS-004 | - |

## REAR_SUSPENSION

Rear suspension and spring type UNKNOWN; names are type-neutral until evidence.

| ID | Component | Fitment | Status | Visual | CAD | Mech | Depends on | Sources |
|---|---|---|---|---|---|---|---|---|
| RSU-001 | Rear spring, LH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | RSU-009 | - |
| RSU-002 | Rear spring, RH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | RSU-009 | - |
| RSU-003 | Rear damper, LH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | RSU-009 | - |
| RSU-004 | Rear damper, RH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | RSU-009 | - |
| RSU-005 | Rear axle locating links / arms (set) | CONFIRMED | UNKNOWN | NONE | NONE | NONE | RSU-009 | E-025 |
| RSU-006 | Rear suspension bushings (set) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | RSU-005 | - |
| RSU-007 | Rear hub / axle end, LH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | RSU-005 | - |
| RSU-008 | Rear hub / axle end, RH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | RSU-005 | - |
| RSU-009 | Rear suspension mounting points (set) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | CHS-004 | - |

## STEERING

Steering gear type UNKNOWN (spec steering.steering_gear_type).

| ID | Component | Fitment | Status | Visual | CAD | Mech | Depends on | Sources |
|---|---|---|---|---|---|---|---|---|
| STR-001 | Steering gear | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | STR-005 | - |
| STR-002 | Steering linkage (intermediate / relay, per gear type) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | STR-001 | - |
| STR-003 | Tie rod, LH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | STR-002, FSU-009 | - |
| STR-004 | Tie rod, RH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | STR-002, FSU-010 | - |
| STR-005 | Steering mounting points | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | CHS-004 | - |

## BRAKING

Brake types per axle UNKNOWN (spec brakes.*).

| ID | Component | Fitment | Status | Visual | CAD | Mech | Depends on | Sources |
|---|---|---|---|---|---|---|---|---|
| BRK-001 | Brake master cylinder | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | INT-005, BDY-001 | - |
| BRK-002 | Brake booster (servo) (opt) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BRK-001 | - |
| BRK-003 | Brake lines and routing | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BRK-001, CHS-001 | - |
| BRK-004 | Front brake, LH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | FSU-009, BRK-003 | - |
| BRK-005 | Front brake, RH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | FSU-010, BRK-003 | - |
| BRK-006 | Rear brake, LH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | RSU-007, BRK-003 | - |
| BRK-007 | Rear brake, RH | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | RSU-008, BRK-003 | - |
| BRK-008 | Parking brake mechanism (cables, levers at the brakes) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BRK-006, BRK-007 | - |

## FUEL_SYSTEM

Fuel storage and supply. Petrol system FUL-001..004; LPG system FUL-005..014 kept as separate components (registered LPG conversion E-014/E-015, D-026). Engine-side petrol delivery is ENG-007.

| ID | Component | Fitment | Status | Visual | CAD | Mech | Depends on | Sources |
|---|---|---|---|---|---|---|---|---|
| FUL-001 | Fuel tank | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | CHS-001 | - |
| FUL-002 | Fuel lines and routing | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | FUL-001, CHS-001 | - |
| FUL-003 | Fuel filler neck and cap | CONFIRMED | UNKNOWN | NONE | NONE | NONE | FUL-001 | E-026 |
| FUL-004 | Fuel pump (mechanical or electric - variant UNKNOWN) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | FUL-002 | - |
| FUL-005 | LPG tank, toroidal, luggage compartment (40 L nominal) | CONFIRMED | VERIFIED | NONE | DRAFT | NONE | CHS-001 | E-014, E-015, E-017, E-022, E-025 |
| FUL-006 | LPG multivalve on the tank (fill stop, outlet, gauge, excess-flow) | CONFIRMED | VERIFIED | NONE | NONE | NONE | FUL-005 | E-022, E-023 |
| FUL-007 | LPG filler valve (external filling point) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | FUL-008 | - |
| FUL-008 | LPG high-pressure line, tank to engine bay | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | FUL-006, CHS-001 | - |
| FUL-009 | LPG solenoid shut-off valve with filter | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | FUL-008 | - |
| FUL-010 | LPG vaporiser / pressure regulator (coolant heated) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | FUL-009, ENG-008 | - |
| FUL-011 | LPG gas-air mixer (venturi) at the carburettor intake | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | FUL-010, ENG-005 | - |
| FUL-012 | Petrol cut-off solenoid valve (carburettor feed) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | FUL-002 | - |
| FUL-013 | Petrol / LPG changeover switch | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | FUL-009, FUL-012 | - |
| FUL-014 | LPG tank mounting frame / straps and gas-tight housing or vent | CONFIRMED | UNKNOWN | NONE | NONE | NONE | FUL-005, CHS-001 | E-022, E-025 |

## EXHAUST

Exhaust from manifold flange to outlet. Catalyst fitment UNKNOWN.

| ID | Component | Fitment | Status | Visual | CAD | Mech | Depends on | Sources |
|---|---|---|---|---|---|---|---|---|
| EXH-001 | Exhaust front pipe | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | ENG-006 | - |
| EXH-002 | Silencer(s) / catalytic converter | CONFIRMED | UNKNOWN | NONE | NONE | NONE | EXH-001 | E-025 |
| EXH-003 | Exhaust routing and hangers | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | EXH-002, CHS-001 | - |
| EXH-004 | Tailpipe / exhaust outlet | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | EXH-003 | - |

## ELECTRICAL

Electrical system. Alternator = ENG-009, starter = ENG-010. No pinout or wiring data may be assumed.

| ID | Component | Fitment | Status | Visual | CAD | Mech | Depends on | Sources |
|---|---|---|---|---|---|---|---|---|
| ELE-001 | Battery | CONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-001 | E-027 |
| ELE-002 | Fuse box | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | ELE-007 | - |
| ELE-003 | Relays (set) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | ELE-002 | - |
| ELE-004 | Ignition system (coil, distributor or electronic - variant UNKNOWN) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | ENG-002, ELE-007 | - |
| ELE-005 | Lighting circuits | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | ELE-002, ELE-007 | - |
| ELE-006 | Instrumentation circuits and sensors | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | ELE-007 | - |
| ELE-007 | Wiring harnesses (set) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | ELE-001 | - |
| ELE-008 | Connectors (set) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | ELE-007 | - |
| ELE-009 | Ground (earth) points (set) | UNCONFIRMED | UNKNOWN | NONE | NONE | NONE | BDY-001, ELE-007 | - |

## WHEELS_AND_TIRES

Road wheels and tires. Sizes UNKNOWN (spec wheels_tires.*).

| ID | Component | Fitment | Status | Visual | CAD | Mech | Depends on | Sources |
|---|---|---|---|---|---|---|---|---|
| WHL-001 | Wheel and tire, front LH | UNCONFIRMED | UNKNOWN | PLACEHOLDER | DRAFT | NONE | FSU-009 | - |
| WHL-002 | Wheel and tire, front RH | UNCONFIRMED | UNKNOWN | PLACEHOLDER | DRAFT | NONE | FSU-010 | - |
| WHL-003 | Wheel and tire, rear LH | UNCONFIRMED | UNKNOWN | PLACEHOLDER | DRAFT | NONE | RSU-007 | - |
| WHL-004 | Wheel and tire, rear RH | UNCONFIRMED | UNKNOWN | PLACEHOLDER | DRAFT | NONE | RSU-008 | - |
| WHL-005 | Spare wheel (opt) | CONFIRMED | UNKNOWN | NONE | NONE | NONE | - | E-022 |
| WHL-006 | Steel wheel rim, front LH | UNCONFIRMED | ESTIMATED | NONE | DRAFT | NONE | FSU-009 | E-017, E-018 |
| WHL-007 | Steel wheel rim, front RH | UNCONFIRMED | ESTIMATED | NONE | DRAFT | NONE | FSU-010 | E-017, E-018 |
| WHL-008 | Steel wheel rim, rear LH | UNCONFIRMED | ESTIMATED | NONE | DRAFT | NONE | RSU-007 | E-017, E-018 |
| WHL-009 | Steel wheel rim, rear RH | UNCONFIRMED | ESTIMATED | NONE | DRAFT | NONE | RSU-008 | E-017, E-018 |
