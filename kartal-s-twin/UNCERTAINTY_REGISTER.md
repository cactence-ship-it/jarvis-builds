# Uncertainty Register

Open questions that limit fidelity. A hypothesis here is **not evidence** and must not be
used for geometry until it is resolved. Priority: P1 blocks a phase; P2 degrades accuracy;
P3 cosmetic.

| ID | Topic | What is uncertain | Impact | Resolution path | Priority | Status |
|---|---|---|---|---|---|---|
| U-001 | Engine variant | Literature (E-011..E-013) points to a carburettor SOHC 1.6 (1581 cm3, ~61 kW) for the Kartal S; all ESTIMATED and LOW-MEDIUM confidence. Engine code, actual fitted engine and any LPG kit on VEH-01 are unknown. | Blocks Phase 6, ENG-* | Ruhsat fields 'Silindir hacmi', 'Motor gücü', 'Yakıt cinsi' (redact owner data); engine-bay photos; engine-number stamping | P1 | OPEN |
| U-002 | Vehicle dimensions | No dimension is verified: main dimensions and tracks are literature estimates; body-profile values are placeholders (see PROJECT_STATUS for counts). | Blocks accurate Phase 4 onward | Owner tape measurements against the spec's verify_by fields (guide in Phase 3); documents | P1 | OPEN |
| U-003 | Legacy archive | Kartal_S_Studyo.zip not received. Its about 47 objects, their geometry type and their quality are unverified. | Reuse decision for Phase 2 and 4 | Owner attaches the ZIP; ingest; inspect index.html and kartal.json | P1 | OPEN |
| U-004 | Photo set | The 9 photographs have not been received. Expected coverage gaps: engine bay, underbody, wheel close-ups, VIN plate. | Blocks Phase 2 | Owner attaches the photos; later targeted extra photos | P1 | OPEN |
| U-005 | Trim and equipment content | Which "S" features are fitted: roof rails, rear wiper, side repeaters, mouldings, booster and similar (inventory items marked optional). | Component fitment | Photos | P2 | OPEN |
| U-006 | Drive layout and rear axle | Hypothesis (unverified): front-engine RWD with a live rear axle, by model-family lineage. | DRV-*, RSU-*, CHS-* | Underbody photo of the propeller shaft and differential housing | P1 for Phase 6-8 | OPEN |
| U-007 | Steering side | Expected LHD for the market; not yet observed. | INT-*, STR-* | Dashboard photo | P2 | OPEN |
| U-008 | Reference state for Z=0 | Fuel level, load and tyre pressures for the ground plane are not defined. | All Z values, ride height | Define at the first measurement session and record it in the spec | P2 | OPEN |
| U-009 | Private storage of originals | The repository is public, so originals cannot be committed (D-012) and they survive only on the owner's phone. | Long-term preservation of evidence | **Owner decision:** make the repository private, or name a private repository or store, and authorise it | P1 | OPEN - needs owner |
| U-010 | Modifications and repairs | Non-original parts, repaint, LPG kit, aftermarket wheels and similar on this specific car. | Faithfulness to THIS vehicle | Owner statement plus photos | P2 | OPEN |
| U-011 | Series and facelift features | Which design generation the 1997 model year carries (bumpers, lamps, dashboard). | Phase 4 and 5 styling | Photos plus documents; no assumption from generic references | P2 | OPEN |
