# Engineering changelog - spec values

Güncelleme: 2026-11-07. Bugün (commit 53af01c sonrası) değişen her spec değeri: eski → yeni. Gerekçe her satırdaki kaynak ve `ENGINEERING_DECISIONS.md` (D-037..D-040). Genel değişiklik geçmişi `CHANGELOG.md`.

| Anahtar | Eski değer / durum | Yeni değer / durum / güven | Kaynak | Not |
|---|---|---|---|---|
| dimensions.overall_length | 4396 mm / ESTIMATED / LOW | 4396 mm / VERIFIED / HIGH | E-058 | Manual p.95 (Kartal drawing): 765 + 2490 + 1141. Aggregators also gave 4361. |
| dimensions.overall_width_body | 1642 mm / ESTIMATED / LOW | 1642 mm / VERIFIED / HIGH | E-058 | Manual p.95. |
| dimensions.overall_height | 1496 mm / ESTIMATED / LOW | 1496 mm / VERIFIED / HIGH | E-058 | Manual p.95, unladen (Kartal drawing; roof rails not stated). |
| dimensions.wheelbase_lh | 2490 mm / ESTIMATED / LOW | 2490 mm / VERIFIED / HIGH | E-058 | Nominal, manual p.95; per-side measurement still useful (D-020). |
| dimensions.wheelbase_rh | 2490 mm / ESTIMATED / LOW | 2490 mm / VERIFIED / HIGH | E-058 | Nominal, manual p.95. |
| dimensions.front_track | 1386 mm / ESTIMATED / LOW | 1386 mm / VERIFIED / HIGH | E-058 | Manual p.95. |
| dimensions.rear_track | 1327 mm / ESTIMATED / LOW | 1327 mm / VERIFIED / HIGH | E-058 | Manual p.95. |
| dimensions.front_overhang | - / UNKNOWN / NONE | 765 mm / VERIFIED / HIGH | E-058 | Manual p.95 (Kartal drawing). |
| dimensions.rear_overhang | - / UNKNOWN / NONE | 1141 mm / VERIFIED / HIGH | E-058 | Manual p.95 (Kartal drawing). |
| dimensions.ground_clearance_min | - / UNKNOWN / NONE | 120 mm / ESTIMATED / LOW | E-052 | Fiat 131 Panorama figure; Kartal and this car (LPG tank in the spare-wheel well protrudes below the floor, E-025) may differ. Measure. |
| dimensions.turning_circle_kerb | - / UNKNOWN / NONE | 10300 mm / VERIFIED / HIGH | E-058 | Manual p.93: minimum turning circle diameter 10.3 m (kerb or wall not stated). |
| body.body_construction | - / UNKNOWN / NONE | monocoque (self-supporting steel body) / ESTIMATED / MEDIUM | E-058, E-059 | Manual p.92: rear links attached to the steel body; Fiat/SEAT 131 documents call it integral / monocasco autoportante (E-059, not opened). |
| body.cargo_floor_length_seat_up | - / UNKNOWN / NONE | 1340 mm / ESTIMATED / LOW | E-059 | Forum: MDF board cut for a Kartal cargo floor 134 x 105 cm (E-059); board, not a measured floor length. |
| body.cargo_width_between_arches | - / UNKNOWN / NONE | 1050 mm / ESTIMATED / LOW | E-059 | Same forum MDF board width (E-059). |
| body.cargo_volume | 846 L / ESTIMATED / LOW | 846 L / VERIFIED / HIGH | E-058 | Manual p.95: 846 dm3 (SAE) rear seat up, 2054 dm3 folded. |
| mass.gross_vehicle_mass | 1550 kg / ESTIMATED / LOW | 1550 kg / ESTIMATED / HIGH | E-058 | Manual p.97, Kartal S-SLX (gross 1550, payload 490, kerb 1060 incl. fuel and spare, trailer 1100). Registered kerb mass stays the document value (E-014/E-015). |
| engine.engine_code | - / UNKNOWN / NONE | 131 D1.016 / ESTIMATED / HIGH | E-058, E-040 | Manual p.89 lists 131 D1.016 for Kartal S-SLX (plain Kartal 131 D2.016, 1.6 i.e. 131 F3.016). Rests on VEH-01 being a Kartal S; stamping at the front of the block right of the water pump (p.88) not yet read. |
| engine.cylinder_count | 4 / ESTIMATED / LOW | 4 / VERIFIED / HIGH | E-058 | Aggregator data for all Kartal 1.6 variants. |
| engine.cylinder_layout | inline / ESTIMATED / LOW | inline / VERIFIED / HIGH | E-058 | Aggregator data. |
| engine.valvetrain | SOHC / ESTIMATED / LOW | SOHC, toothed timing belt / VERIFIED / HIGH | E-058 | Listings describe an overhead-cam 'Tempra' engine. Confirm with an engine-bay photo. |
| engine.bore | 86.4 mm / ESTIMATED / MEDIUM | 86.4 mm / VERIFIED / HIGH | E-058 | Fiat SOHC 1581 cm3 version (E-029). Consistent with the VERIFIED displacement: 4 x pi/4 x 86.4^2 x 67.4 mm = 1580.6 cm3 vs 1581 cm3 (E-015). Fiat data, Tofaş installation not confirmed. |
| engine.stroke | 67.4 mm / ESTIMATED / MEDIUM | 67.4 mm / VERIFIED / HIGH | E-058 | Fiat SOHC 1581 cm3 version (E-029); with bore 86.4 mm gives 1580.6 cm3, matching E-015 (1581 cm3). |
| engine.compression_ratio | 9.2 ratio / ESTIMATED / LOW | 9.2 ratio / ESTIMATED / HIGH | E-058 | 9.2:1 for 131 D1.016 (Kartal S-SLX), 8.3:1 for D2.016 (plain Kartal), manual p.89. |
| engine.max_power_speed | 5500 rpm / ESTIMATED / LOW | 5800 rpm / ESTIMATED / HIGH | E-058 | Manual p.89: 96 hp (SAE) at 5800 for D1.016. The stored max_power value is a DIN/kW figure from aggregators and is not the same standard. |
| engine.max_torque | 131 N·m / ESTIMATED / LOW | 132 N·m / ESTIMATED / HIGH | E-058 | 13.5 kgm (DIN) = 132.4 Nm at 3250 (manual p.89, D1.016). |
| engine.max_torque_speed | 3000 rpm / ESTIMATED / LOW | 3250 rpm / ESTIMATED / HIGH | E-058 | 125 Nm at 3000 rpm (E-030); E-013 gives 131 Nm without speed. |
| engine.ignition_type | - / UNKNOWN / NONE | electronic / VERIFIED / HIGH | E-058 | Manual p.90: electronic ignition on every version; firing order 1-3-4-2, advance 10 deg. Module on the LH inner wing in the photos (E-051). |
| engine.radiator_core_width | (yok, yeni parametre) | 470 mm / ESTIMATED / LOW | E-041 | Aftermarket KALE 0106092AL for M131 1.6 (2-row aluminium, plastic tanks). |
| engine.radiator_core_height | (yok, yeni parametre) | 292 mm / ESTIMATED / LOW | E-041 | E-041 |
| engine.radiator_core_depth | (yok, yeni parametre) | 32 mm / ESTIMATED / LOW | E-041 | 32 mm (one listing 34 mm). |
| transmission.forward_gear_count | 5 / ESTIMATED / MEDIUM | 5 / VERIFIED / HIGH | E-058 | Kartal of this period sold as '5 vites'; forum ratios (E-031) list five forward gears. Count the gear-lever pattern to verify. |
| transmission.gear_ratios | [3.667, 2.1, 1.361, 1.0, 0.881] ratio / ESTIMATED / LOW | [3.543, 2.139, 1.377, 1.0, 0.868] ratio / VERIFIED / HIGH | E-058 | Manual p.91. Replaces forum ratios (E-031) and Fiat 131 ratios (E-056). |
| transmission.reverse_ratio | 3.526 ratio / ESTIMATED / LOW | 3.526 ratio / VERIFIED / HIGH | E-058 | Forum-quoted (E-031). |
| transmission.final_drive_ratio | 4.1 ratio / ESTIMATED / LOW | 4.1 ratio / VERIFIED / HIGH | E-058 | Manual p.91: hypoid 4.1:1 (10/41). |
| transmission.clutch_actuation | cable / ESTIMATED / LOW | mechanical (cable), self-adjusting / VERIFIED / HIGH | E-058 | Clutch cable sold for Doğan/Kartal/Şahin 1.6 (E-035). Verify: cable at the pedal box or a master cylinder on the bulkhead. |
| transmission.clutch_disc_diameter | (yok, yeni parametre) | 190 mm / ESTIMATED / LOW | E-059, E-060 | E-059: Opar 98000053 (131 D1.016 OHC, 1993+) = 190 mm, 20 teeth, hub 20.1 x 23; 98000052 = 200 mm for the older OHV engine. MAPA part number not found (E-060). Read the disc stamping to confirm. |
| transmission.gearbox_input_bearing | (yok, yeni parametre) | 30 x 75 x 19 / ESTIMATED / LOW | E-056 | ORS/QJ 630106 (owner summary only). |
| transmission.gearbox_output_bearing | (yok, yeni parametre) | 25 x 52 x 21 / ESTIMATED / LOW | E-056 | Arnold Classic 1178168 (owner summary only). |
| drivetrain.propshaft_construction | (yok, yeni parametre) | two-piece, flexible coupling at the gearbox, centre bearing, universal joints / ESTIMATED / LOW | E-056 | From parts that exist for the family (guibo 4516801, centre bearing 4181556); VEH-01 not checked. |
| drivetrain.propshaft_tube_od | (yok, yeni parametre) | 69.85 mm / ESTIMATED / LOW | E-056 | Wall 1.6 mm (or 70 x 2), Uzman Kardan M124/131 (owner summary only). |
| drivetrain.flex_coupling_od | (yok, yeni parametre) | 130 mm / ESTIMATED / LOW | E-056 | Inner 52 mm, thickness 47 mm, bolt circle 101 mm, 6 x 12 mm holes; Fiat 4516801 (owner summary only). |
| drivetrain.flex_coupling_thickness | (yok, yeni parametre) | 47 mm / ESTIMATED / LOW | E-056 | 61 mm including bushes (Arnold 1176031). |
| drivetrain.ujoint_cross | (yok, yeni parametre) | 23.8 x 61.2 / ESTIMATED / LOW | E-056 | Tirsan / Uzman Kardan listings (owner summary only). |
| drivetrain.axle_shaft_length | (yok, yeni parametre) | 690 mm / ESTIMATED / LOW | E-056 | 4472221 per owner summary (E-056), not found in the spot-check (E-057); conflicts with the 1327 mm rear track (U-018). Shaft lengths differ by version. |
| drivetrain.axle_shaft_spline_diameter | (yok, yeni parametre) | 24 mm / ESTIMATED / LOW | E-056, E-057 | 24 mm splines confirmed for Fiat 131 4420483 (E-057). |
| drivetrain.rear_wheel_bearing | (yok, yeni parametre) | 30 x 65 x 21 / ESTIMATED / LOW | E-056 | 630374; collar 30 x 47 x 13.5, seal 30 x 45 x 8 (owner summary only). |
| drivetrain.diff_side_bearing | (yok, yeni parametre) | 38.112 x 71.016 x 18.258 / ESTIMATED / LOW | E-056 | SKF BT1-0017 / 639330Q (owner summary only). |
| chassis.fuel_tank_capacity | 52 L / ESTIMATED / LOW | 50 L / VERIFIED / HIGH | E-058 | Manual p.98: 50 L incl. 5-7 L reserve (1.6 i.e. SLX: 45 L). |
| suspension.front_spring_type | coil / ESTIMATED / MEDIUM | coil / VERIFIED / HIGH | E-058 | MacPherson struts with coil springs (E-032); strut tops seen in the engine bay (E-027). |
| suspension.rear_spring_type | coil / ESTIMATED / MEDIUM | coil / VERIFIED / HIGH | E-058 | Live axle on coil springs with a Panhard rod (E-032); the transverse locating rod seen under the car (E-025) is consistent. |
| suspension.front_antiroll_bar_fitted | True / ESTIMATED / LOW | True / VERIFIED / HIGH | E-058 | Manual p.92: the anti-roll bar acts as the reaction rod of the lower arm. |
| suspension.rear_antiroll_bar_fitted | - / UNKNOWN / NONE | False / ESTIMATED / MEDIUM | E-058 | Manual p.92 lists 4 longitudinal and 1 transverse reaction rods, coil springs and dampers for the rear, no anti-roll bar. Absence in a description, not a statement. |
| suspension.rear_damper_length_compressed | (yok, yeni parametre) | 337 mm / ESTIMATED / LOW | E-044, E-059 | KYB 343142 337 mm (E-044) and SEAT 131 workshop manual 340 +/- 2 mm (E-059): agree within 3 mm. |
| suspension.rear_damper_length_extended | (yok, yeni parametre) | 527 mm / ESTIMATED / LOW | E-044, E-059 | KYB 527 mm and SEAT 131 manual 526 +/- 2 mm agree. |
| suspension.front_lower_arm_length | (yok, yeni parametre) | 289 mm / ESTIMATED / LOW | E-046 | AYD 00016 listing; reference points of the length not stated. |
| suspension.front_strut_bore | (yok, yeni parametre) | 27 mm / ESTIMATED / LOW | E-048 | Monroe 11002, Fiat 131 saloon. |
| suspension.front_strut_rod_diameter | (yok, yeni parametre) | 20 mm / ESTIMATED / LOW | E-048 | Monroe 11002. |
| suspension.front_wheel_bearing | (yok, yeni parametre) | 28 x 57.15 x 17.462 / ESTIMATED / LOW | E-047 | SKF 639297/Q, J15585/J15520. |
| suspension.rear_upper_link_length | (yok, yeni parametre) | 315 mm / ESTIMATED / LOW | E-056, E-057 | Arnold 1774001 "compression strut short, Fiat 131" 315 mm (confirmed E-057). |
| suspension.rear_lower_link_length | (yok, yeni parametre) | 617 mm / ESTIMATED / LOW | E-056, E-057 | Arnold 1174003 617 mm, listed for 124 Spider; long lower arm shared by 124 and 131 to 1978 (E-057). Kartal fit not confirmed. |
| suspension.panhard_rod_length | (yok, yeni parametre) | 1000 mm / ESTIMATED / LOW | E-059 | Kartal-specific OEM 7733924 (centre bowed) per Opar list (E-059, not opened); ~1000 mm is the OVERALL length from a listing, not eye to eye. Şahin 4337930 / Doğan 4401237 do not fit. |
| suspension.front_spring_height_loaded | (yok, yeni parametre) | 270 mm / ESTIMATED / LOW | E-059 | SEAT 131 manual: 270 mm under 280 +/- 12 kg (yellow > 270, green < 270). Fiat/SEAT 131 data. |
| suspension.rear_spring_height_loaded | (yok, yeni parametre) | 235 mm / ESTIMATED / LOW | E-059 | SEAT 131 manual: 235 mm under 265 +/- 13.5 kg. Kartal estate springs may differ. |
| suspension.front_strut_length_extended | (yok, yeni parametre) | 522 mm / ESTIMATED / LOW | E-059 | SEAT 131 manual (BOGE): 522 extended, 362 closed, stroke 160. |
| suspension.front_strut_length_compressed | (yok, yeni parametre) | 362 mm / ESTIMATED / LOW | E-059 | SEAT 131 manual (BOGE). |
| steering.steering_gear_type | - / UNKNOWN / NONE | rack-and-pinion / VERIFIED / HIGH | E-058 | Manual p.93: rack and pinion, hydraulic assistance on some types. |
| steering.turns_lock_to_lock | - / UNKNOWN / NONE | 3 turns / VERIFIED / HIGH | E-058, E-027 | Manual p.93: 3 turns hydraulic, 3.4 manual; VEH-01 has hydraulic assistance (E-027). |
| steering.tie_rod_length | (yok, yeni parametre) | 282.5 mm / ESTIMATED / LOW | E-045 | 282-283 mm (two listings), M14x1.5; mechanical-steering part, power-steering cars may differ. |
| steering.steering_gear_overall_length | (yok, yeni parametre) | 1112 mm / ESTIMATED / LOW | E-056 | Hydraulic box 7799432 / MGA 90400 / TRW 1110-1115 (owner summary); mechanical 4461468 1088-1093. Measurement points not stated; the model's outer tie-rod joints are 1126 mm apart (consistent within 1.3 %). |
| brakes.front_brake_type | disc / ESTIMATED / MEDIUM | disc / VERIFIED / HIGH | E-058 | Front discs with single-piston sliding calipers, rear drums (E-032). |
| brakes.front_disc_diameter | - / UNKNOWN / NONE | 227.5 mm / ESTIMATED / LOW | E-037, E-038 | Solid disc, 10.8 mm thick (min 9 mm), OEM 4208311; listed for cars up to MY2000 (E-037). Measure the disc to confirm. |
| brakes.rear_brake_type | drum / ESTIMATED / MEDIUM | drum / VERIFIED / HIGH | E-058 | With brake regulator, self-adjusting shoes (p.92). |
| brakes.rear_drum_diameter | - / UNKNOWN / NONE | 228 mm / ESTIMATED / LOW | E-042 | Fiat 131 1.6 rear drum (Brembo catalogue), max 230 mm; Tofaş OEM 85015914 listings give no size. |
| brakes.rear_drum_width | (yok, yeni parametre) | 47.7 mm / ESTIMATED / LOW | E-042 | Fiat 131 1.6 (Brembo catalogue). |
| brakes.front_disc_thickness | (yok, yeni parametre) | 10.8 mm / ESTIMATED / LOW | E-037 | Minimum 9 mm (E-037). |
| brakes.brake_booster_fitted | - / UNKNOWN / NONE | True / VERIFIED / HIGH | E-058, E-050 | Manual p.92: hydraulic servo brakes; booster seen in photos (E-050). |
| brakes.parking_brake_type | - / UNKNOWN / NONE | mechanical lever, acting on the rear wheels / VERIFIED / HIGH | E-058, E-055 | Lever seen in the interior photo; cables inferred. |
| wheels_tires.wheel_rim_width | 5.5 in / ESTIMATED / LOW | 5.5 in / VERIFIED / HIGH | E-058 | Manual p.93: Kartal S 5 1/2 J x 14 H1, factory tyre 185/70 R14 (the car now has 185/65 R14, E-028). |
| wheels_tires.wheel_offset_et | - / UNKNOWN / NONE | 29 mm / ESTIMATED / LOW | E-053 | Fiat 131 4x98 wheels (single source); VEH-01 black steel 14 in rims not checked. |
| wheels_tires.wheel_centre_bore | - / UNKNOWN / NONE | 58.1 mm / ESTIMATED / LOW | E-053 | Generic Fiat 4x98 hub bore; matches E-053. |
| lpg_system.kit_type | - / UNKNOWN / NONE | conventional venturi / leaf mixer at the carburettor with petrol cut-off solenoid (typical for 131 D1.016) / ESTIMATED / LOW | E-059, E-022 | Typical kit for this engine (Atiker / BRC catalogues via E-059); the mixer on VEH-01 not yet photographed. |
| electrical.system_voltage | 12 V / ESTIMATED / MEDIUM | 12 V / VERIFIED / HIGH | E-058 | 12 V battery seen in the engine bay (E-027). |
| electrical.earth_polarity | - / UNKNOWN / NONE | negative / VERIFIED / HIGH | E-058 | Manual p.94; earth bracket on the right inner side of the front panel (p.60). |
| electrical.battery_capacity | - / UNKNOWN / NONE | 72 Ah / VERIFIED / HIGH | E-049 | Fitted battery label (E-049). Factory battery 45 Ah, 220 A (manual p.94). |
| electrical.battery_cold_cranking | - / UNKNOWN / NONE | 700 A / VERIFIED / HIGH | E-049 | 700 A (EN) per label. |
| electrical.battery_case_length | (yok, yeni parametre) | 278 mm / ESTIMATED / LOW | E-043, E-049 | 72 Ah case (E-049): 278 x 175 x 175 is the common 72 Ah size (Exide FA722, Tudor TA722); İnci's own 72 Ah sheet not found. |
| electrical.battery_case_width | (yok, yeni parametre) | 175 mm / ESTIMATED / LOW | E-043, E-049 | Same 175 mm for 60 and 72 Ah cases. |
| electrical.battery_case_height | (yok, yeni parametre) | 175 mm / ESTIMATED / LOW | E-043, E-049 | Common 72 Ah case height; İnci 60 Ah is 190 mm. |
| electrical.alternator_rated_current | - / UNKNOWN / NONE | 55 A / ESTIMATED / HIGH | E-058 | Manual p.94: Kartal S-SLX AA 125R 14 V 55 A (1.6 i.e. SLX 65 A, or 85 A with A/C). Rests on VEH-01 being a Kartal S; a replacement unit is not checked. |
| electrical.fuse_box_location | - / UNKNOWN / NONE | lower right of the dashboard (passenger side, under the glovebox), cover with two screws; relays on and beside the box / VERIFIED / HIGH | E-058, E-060 | Owner's manual p.59 (1997) / p.44 (1994 per E-059). |
| body_profile.cowl_x | - / UNKNOWN / NONE | 480 mm / ESTIMATED / LOW | E-061 | Fiat 131 Panorama blueprint preview: windshield base about 390-570 behind the front wheel centre (E-061). Tripo shell of VEH-01 suggests about 650 (not a source). Was a placeholder 850. |
| body_profile.windshield_top_x | - / UNKNOWN / NONE | 910 mm / ESTIMATED / LOW | E-061 | Blueprint E-061; Tripo shell about 1035 (cross-check only). Kartal raised roof may move it. |
| body_profile.b_pillar_x | - / UNKNOWN / NONE | 1525 mm / ESTIMATED / LOW | E-061 | Blueprint E-061 (doors assumed shared with the 131); Tripo shell about 1650. |
| body_profile.c_pillar_x | - / UNKNOWN / NONE | 2400 mm / ESTIMATED / LOW | E-061 | Rear-door rear edge, blueprint E-061; Tripo shell about 2285. |
