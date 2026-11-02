# Engineering roadmap - dependency order

The live, machine-checked queue is [TASKS.md](TASKS.md) (from `tasks/*.yaml`). This page is the
phase-level order. No phase is "done" without recorded tests and an independent review.

| Order | Work package | Depends on | Unblocked by | Current state |
|---|---|---|---|---|
| 1 | Evidence intake: measurements M01-M31, ruhsat fields, 9 photos, legacy ZIP | - | Owner | Waiting (T-003, T-004) |
| 2 | Reference geometry: wheel centres, ride height, Z=0 state | 1 | Measurements M05-M16 | Tire envelopes DRAFT from literature |
| 3 | Wheels: rim + hub interface (PCD, ET, centre bore) | 1, 2 | Rim photo / stamping | T-007 blocked |
| 4 | Body side profile, greenhouse, glazing (DRAFT CAD) | 1, 2 | Side photo + M17-M31 | T-006 blocked; visual placeholder only |
| 5 | Closures, bumpers, lamps, trim (CAD) | 4 | Photos | Visual placeholders only |
| 6 | Packaging clearances: tire-arch, steering lock, ground clearance | 2, 4 | Steering lock angle, arch geometry | Framework done (T-001), rules blocked (T-008) |
| 7 | Interior (dashboard, seats, trim) | 1 | Interior photos | Not started |
| 8 | Underbody, chassis members, mounting points | 1 | Underbody photos / measurements | Not started - no evidence |
| 9 | Powertrain (engine, gearbox, propshaft, axle, exhaust) | 1, 8 | Engine bay photos, ruhsat, manuals | Not started - no evidence |
| 10 | Suspension, steering, brakes | 8 | Underbody photos, measurements | Not started - no evidence |
| 11 | Electrical (harness, connectors, lamps, instruments) | 5, 7, 9 | Photos, service documentation | Not started - no evidence |
| 12 | Integration, mechanical assembly, full clearance set, documentation | all | - | CI and validation framework in place |
