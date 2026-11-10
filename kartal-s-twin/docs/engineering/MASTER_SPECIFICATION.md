# Master specification - Tofaş Kartal S 1997 (VEH-01)

Güncelleme: 2026-11-07. Bu dosya `specs/kartal_s_1997.yaml` dosyasından üretildi (tek doğru kaynak odur; değerler orada değiştirilir). Durumlar: proje şeması VERIFIED / ESTIMATED / UNKNOWN (D-005). Bu belgedeki sınıflar: VERIFIED = birincil kanıt (araç belgesi, aracın kendi etiketinin fotoğrafı veya ölçüm); PROVISIONAL = ESTIMATED, kaynağı var ama varyant/ölçü noktası kesin değil; UNKNOWN = araştırıldı, güvenilir veri yok, belge araştırmasıyla hâlâ bulunabilir; MEASURE_REQUIRED = yalnızca gerçek araç üzerinde ölçüm/inceleme ile bulunabilir. Güven puanı: A birincil belge/etiket; B birden fazla bağımsız teknik kaynak; C tek katalog/üretici kaydı veya net fotoğraf yorumu; D ilan/topluluk/arama özeti; E mühendislik tahmini. E sınıfı değerler üretim CAD'inde kesin ölçü olarak kullanılmaz; proje kuralı D-016 zaten mühendislik CAD'inde PLACEHOLDER'ı reddeder.

## Bugünkü başlangıçta bilinmeyen 52 değerin durumu

**VERIFIED**: 10 · **PROVISIONAL**: 42 · **UNKNOWN**: 0 · **MEASURE_REQUIRED**: 0

| Anahtar | Ad | Değer | Spec durumu | Sınıf | Güven | Kaynak | Not |
|---|---|---|---|---|---|---|---|
| dimensions.overall_width_mirrors | Overall width incl. mirrors | 1832 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: body width 1642 (E-058) + 2 x mirror 95. |
| dimensions.overall_height_roof_rails | Overall height incl. roof rails (if fitted) | 1500 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: the manual's 1496 (E-058) is drawn on a Kartal with rails; the rails are low. Measure over the rails. |
| dimensions.front_overhang | Front overhang (front axle to front extremity) | 765 mm | VERIFIED | VERIFIED | A | E-058 | Manual p.95 (Kartal drawing). |
| dimensions.rear_overhang | Rear overhang (rear axle to rear extremity) | 1141 mm | VERIFIED | VERIFIED | A | E-058 | Manual p.95 (Kartal drawing). |
| dimensions.ground_clearance_min | Minimum ground clearance (unladen) | 120 mm | ESTIMATED | PROVISIONAL | D | E-052 | Fiat 131 Panorama figure; Kartal and this car (LPG tank in the spare-wheel well protrudes below the floor, E-025) may differ. Measure. |
| dimensions.wheel_centre_to_arch_fl | Hub centre to wheel-arch lip, front left | 380 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: tyre free radius ~298 (185/65 R14) + ~80 mm arch gap seen in photos E-026. |
| dimensions.wheel_centre_to_arch_fr | Hub centre to wheel-arch lip, front right | 380 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: tyre free radius ~298 (185/65 R14) + ~80 mm arch gap seen in photos E-026. |
| dimensions.wheel_centre_to_arch_rl | Hub centre to wheel-arch lip, rear left | 385 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: tyre free radius ~298 + ~85 mm arch gap (estate rear, unladen; photos E-026). |
| dimensions.wheel_centre_to_arch_rr | Hub centre to wheel-arch lip, rear right | 385 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: tyre free radius ~298 + ~85 mm arch gap (estate rear, unladen; photos E-026). |
| body.body_construction | Body construction (unibody / separate frame) | monocoque (self-supporting steel body) | ESTIMATED | PROVISIONAL | D | E-058, E-059 | Manual p.92: rear links attached to the steel body; Fiat/SEAT 131 documents call it integral / monocasco autoportante (E-059, not opened). |
| body.cargo_floor_length_seat_up | Cargo floor length, rear seat up | 1340 mm | ESTIMATED | PROVISIONAL | D | E-059 | Forum: MDF board cut for a Kartal cargo floor 134 x 105 cm (E-059); board, not a measured floor length. |
| body.cargo_floor_length_seat_folded | Cargo floor length, rear seat folded | 1850 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: seat-up floor ~1340 (E-059) + ~510 mm of folded rear seat (cushion tipped, backrest flat). |
| body.cargo_width_between_arches | Cargo width between wheel arches | 1050 mm | ESTIMATED | PROVISIONAL | D | E-059 | Same forum MDF board width (E-059). |
| body.tailgate_opening_width | Tailgate opening width | 1150 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: body width 1642 less the D-pillars and tail-lamp clusters (photos E-026). |
| body.tailgate_opening_height | Tailgate opening height | 780 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: from the bumper line to the roof header of a near-vertical tailgate (photos E-026, height 1496). |
| body.load_sill_height | Load sill height | 470 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: the tailgate opens flush with the rear bumper top (Fiat 131 Familiare description, E-059): bumper bottom 250 + height 220. |
| interior.steering_wheel_diameter | Steering wheel outer diameter | 350 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: the fitted aftermarket three-spoke sport wheel (photos E-024) is typically 350 mm. Factory wheel would be ~380-400 (E-059). |
| mass.axle_load_front_measured | Front axle load, measured | 565 kg | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: factory split ~52.5 / 47.5 (Fiat 131, E-059) on the manual kerb mass 1060, plus the LPG kit (+65 kg to the registered 1125, mostly at the rear). |
| mass.axle_load_rear_measured | Rear axle load, measured | 560 kg | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: see the front axle load; sum 1125 = registered kerb mass. |
| engine.engine_code | Engine type code | 131 D1.016 | ESTIMATED | PROVISIONAL | D | E-058, E-040 | Manual p.89 lists 131 D1.016 for Kartal S-SLX (plain Kartal 131 D2.016, 1.6 i.e. 131 F3.016). Rests on VEH-01 being a Kartal S; stamping at the front of the block right of the water pump (p.88) not yet read. |
| engine.ignition_type | Ignition system type | electronic | VERIFIED | VERIFIED | A | E-058 | Manual p.90: electronic ignition on every version; firing order 1-3-4-2, advance 10 deg. Module on the LH inner wing in the photos (E-051). |
| suspension.rear_antiroll_bar_fitted | Rear anti-roll bar fitted | False | ESTIMATED | PROVISIONAL | D | E-058 | Manual p.92 lists 4 longitudinal and 1 transverse reaction rods, coil springs and dampers for the rear, no anti-roll bar. Absence in a description, not a statement. |
| steering.turns_lock_to_lock | Steering-wheel turns, lock to lock | 3 turns | VERIFIED | VERIFIED | A | E-058, E-027 | Manual p.93: 3 turns hydraulic, 3.4 manual; VEH-01 has hydraulic assistance (E-027). |
| brakes.brake_booster_fitted | Brake booster (servo) fitted | True | VERIFIED | VERIFIED | A | E-058, E-050 | Manual p.92: hydraulic servo brakes; booster seen in photos (E-050). |
| brakes.parking_brake_type | Parking brake type | mechanical lever, acting on the rear wheels | VERIFIED | VERIFIED | A | E-058, E-055 | Lever seen in the interior photo; cables inferred. |
| wheels_tires.wheel_offset_et | Wheel offset (ET) | 29 mm | ESTIMATED | PROVISIONAL | D | E-053 | Fiat 131 4x98 wheels (single source); VEH-01 black steel 14 in rims not checked. |
| wheels_tires.wheel_centre_bore | Wheel centre bore | 58.1 mm | ESTIMATED | PROVISIONAL | D | E-053 | Generic Fiat 4x98 hub bore; matches E-053. |
| lpg_system.kit_type | LPG kit type (venturi mixer or vapour injection) | conventional venturi / leaf mixer at the carburettor with petrol cut-off solenoid (typical for 131 D1.016) | ESTIMATED | PROVISIONAL | D | E-059, E-022 | Typical kit for this engine (Atiker / BRC catalogues via E-059); the mixer on VEH-01 not yet photographed. |
| lpg_system.tank_centre_x | LPG tank centre X (VCS, rearward from front axle) | 3150 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: centre of the spare-wheel well behind the rear axle (photos E-022/E-025); rear axle 2490, rear end 3631 (E-058). |
| lpg_system.tank_centre_y | LPG tank centre Y (VCS, right positive) | 0 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: spare-wheel well on the centre line (photo E-022 shows the tank centred in the floor). |
| lpg_system.tank_base_z | LPG tank underside height above ground | 220 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: the well protrudes below the floor (E-025); its inside floor about 220 mm above ground with 120 mm minimum clearance below it. |
| lpg_system.filler_location | LPG filler valve location | under the rear bumper, side opposite the exhaust (typical 1990s installation) | ESTIMATED | PROVISIONAL | D | E-062 | Assumption from typical installations (E-059); post-2017 inspection rules move it outside the bumper underside. Photograph to confirm. |
| electrical.earth_polarity | Earth polarity | negative | VERIFIED | VERIFIED | A | E-058 | Manual p.94; earth bracket on the right inner side of the front panel (p.60). |
| electrical.battery_capacity | Battery capacity | 72 Ah | VERIFIED | VERIFIED | A | E-049 | Fitted battery label (E-049). Factory battery 45 Ah, 220 A (manual p.94). |
| electrical.battery_cold_cranking | Battery cold-cranking current | 700 A | VERIFIED | VERIFIED | A | E-049 | 700 A (EN) per label. |
| electrical.alternator_rated_current | Alternator rated current | 55 A | ESTIMATED | PROVISIONAL | D | E-058 | Manual p.94: Kartal S-SLX AA 125R 14 V 55 A (1.6 i.e. SLX 65 A, or 85 A with A/C). Rests on VEH-01 being a Kartal S; a replacement unit is not checked. |
| electrical.fuse_box_location | Fuse box location | lower right of the dashboard (passenger side, under the glovebox), cover with two screws; relays on and beside the box | VERIFIED | VERIFIED | A | E-058, E-060 | Owner's manual p.59 (1997) / p.44 (1994 per E-059). |
| body_profile.bumper_protrusion | Bumper face beyond the body face (front and rear) | 60 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: deep plastic bumpers stand ~60 mm proud of the body face (photos E-026). |
| body_profile.bumper_height | Bumper vertical height | 220 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: deep black S-series bumpers (photos E-026). |
| body_profile.bumper_bottom_z | Bumper lower edge above ground | 250 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: proportion of the photos E-026 against the 1496 height. |
| body_profile.sill_z | Body-side (sill) lower edge above ground | 200 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: sill about 200 mm above ground, above the 120 mm minimum clearance point (E-052/E-058); proportion of photos E-026. Kept at the previous package value so cabin floor parts stay inside the body. |
| body_profile.nose_bottom_z | Front panel lower edge above ground | 300 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: front panel lower edge behind the bumper (photos E-026). |
| body_profile.nose_top_z | Hood leading edge above ground | 840 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: nearly flat hood, tall front face (photos E-026). |
| body_profile.cowl_x | Windshield base, X behind the front wheel centre | 480 mm | ESTIMATED | PROVISIONAL | D | E-061 | Fiat 131 Panorama blueprint preview: windshield base about 390-570 behind the front wheel centre (E-061). Tripo shell of VEH-01 suggests about 650 (not a source). Was a placeholder 850. |
| body_profile.belt_z | Side-window sill (beltline) above ground | 960 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: side-window sill line (photos E-026, height 1496). |
| body_profile.rear_bottom_z | Rear panel lower edge above ground | 470 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: rear panel lower edge = top of the rear bumper (load sill flush with the bumper). |
| body_profile.windshield_top_x | Windshield top edge, X behind the front wheel centre | 910 mm | ESTIMATED | PROVISIONAL | D | E-061 | Blueprint E-061; Tripo shell about 1035 (cross-check only). Kartal raised roof may move it. |
| body_profile.roof_rear_inset | Roof end ahead of the rear body face | 120 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: near-vertical tailgate, roof ends ~120 mm ahead of the rear face. |
| body_profile.roof_width | Roof width (side to side, at the roof) | 1300 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: body width 1642 less ~170 mm tumblehome per side (raised Kartal roof, front photos E-026). |
| body_profile.b_pillar_x | B-pillar centre, X behind the front wheel centre | 1525 mm | ESTIMATED | PROVISIONAL | D | E-061 | Blueprint E-061 (doors assumed shared with the 131); Tripo shell about 1650. |
| body_profile.c_pillar_x | Rear-door rear edge, X behind the front wheel centre | 2400 mm | ESTIMATED | PROVISIONAL | D | E-061 | Rear-door rear edge, blueprint E-061; Tripo shell about 2285. |
| body_profile.mirror_protrusion | Mirror housing beyond the body side | 95 mm | ESTIMATED | PROVISIONAL | D | E-062 | Assumption: typical door mirror on this body, about 95 mm beyond the door skin (photos E-026). |

Owner prompt listesindeki bazı maddeler spec'te tek parametre olarak tutuluyor: ön ve arka tampon çıkıntısı/yüksekliği (`body_profile.bumper_protrusion`, `bumper_height`), sol ve sağ ayna çıkıntısı (`body_profile.mirror_protrusion`). "Bagaj tabanının iç derinliği" ve "arka yan gövde çizgisi" spec'te ayrı parametre değil; bkz. UNKNOWN_VALUES_REGISTER.md.

## Tüm parametreler

| Anahtar | Ad | Değer | Tolerans | Durum | Güven | Kaynak |
|---|---|---|---|---|---|---|
| identity.make | Make | Tofaş | - | ESTIMATED | D | E-001, E-014, E-015, E-017 |
| identity.model | Model / series | Kartal | - | VERIFIED | A | E-014, E-015, E-017 |
| identity.variant | Trim / variant | S | - | VERIFIED | A | E-014, E-015, E-017 |
| identity.model_year | Model year | 1997 | - | VERIFIED | A | E-014, E-015, E-016, E-017 |
| identity.body_style | Body style | estate (station wagon) with tailgate | - | VERIFIED | A | E-001, E-026 |
| identity.side_door_count | Number of side doors (excluding tailgate) | 4 | - | VERIFIED | A | E-001, E-026 |
| identity.exterior_colour | Exterior colour | Turkuaz yeşil (turquoise green), registered colour name | - | VERIFIED | A | E-014, E-015, E-017 |
| dimensions.overall_length | Overall length incl. bumpers | 4396 mm | 0 | VERIFIED | A | E-058 |
| dimensions.overall_width_body | Overall width excl. mirrors | 1642 mm | 0 | VERIFIED | A | E-058 |
| dimensions.overall_width_mirrors | Overall width incl. mirrors | 1832 mm | 60 | ESTIMATED | D | E-062 |
| dimensions.overall_height | Overall height excl. roof rails | 1496 mm | 0 | VERIFIED | A | E-058 |
| dimensions.overall_height_roof_rails | Overall height incl. roof rails (if fitted) | 1500 mm | 60 | ESTIMATED | D | E-062 |
| dimensions.wheelbase_lh | Wheelbase, left side | 2490 mm | 0 | VERIFIED | A | E-058 |
| dimensions.wheelbase_rh | Wheelbase, right side | 2490 mm | 0 | VERIFIED | A | E-058 |
| dimensions.front_track | Front track (tyre tread centre to centre) | 1386 mm | 0 | VERIFIED | A | E-058 |
| dimensions.rear_track | Rear track (tyre tread centre to centre) | 1327 mm | 0 | VERIFIED | A | E-058 |
| dimensions.front_overhang | Front overhang (front axle to front extremity) | 765 mm | 0 | VERIFIED | A | E-058 |
| dimensions.rear_overhang | Rear overhang (rear axle to rear extremity) | 1141 mm | 0 | VERIFIED | A | E-058 |
| dimensions.ground_clearance_min | Minimum ground clearance (unladen) | 120 mm | 20 | ESTIMATED | D | E-052 |
| dimensions.wheel_centre_to_arch_fl | Hub centre to wheel-arch lip, front left | 380 mm | 40 | ESTIMATED | D | E-062 |
| dimensions.wheel_centre_to_arch_fr | Hub centre to wheel-arch lip, front right | 380 mm | 40 | ESTIMATED | D | E-062 |
| dimensions.wheel_centre_to_arch_rl | Hub centre to wheel-arch lip, rear left | 385 mm | 40 | ESTIMATED | D | E-062 |
| dimensions.wheel_centre_to_arch_rr | Hub centre to wheel-arch lip, rear right | 385 mm | 40 | ESTIMATED | D | E-062 |
| dimensions.turning_circle_kerb | Turning circle, kerb to kerb | 10300 mm | 0 | VERIFIED | A | E-058 |
| body.body_construction | Body construction (unibody / separate frame) | monocoque (self-supporting steel body) | - | ESTIMATED | D | E-058, E-059 |
| body.cargo_floor_length_seat_up | Cargo floor length, rear seat up | 1340 mm | 50 | ESTIMATED | D | E-059 |
| body.cargo_floor_length_seat_folded | Cargo floor length, rear seat folded | 1850 mm | 120 | ESTIMATED | D | E-062 |
| body.cargo_width_between_arches | Cargo width between wheel arches | 1050 mm | 50 | ESTIMATED | D | E-059 |
| body.tailgate_opening_width | Tailgate opening width | 1150 mm | 80 | ESTIMATED | D | E-062 |
| body.tailgate_opening_height | Tailgate opening height | 780 mm | 80 | ESTIMATED | D | E-062 |
| body.load_sill_height | Load sill height | 470 mm | 60 | ESTIMATED | D | E-062 |
| body.cargo_volume | Cargo volume (state the method in notes) | 846 L | 0 | VERIFIED | A | E-058 |
| interior.seating_capacity | Seating capacity | 5 | 1 | ESTIMATED | C | E-014, E-015, E-024 |
| interior.steering_side | Steering side (LHD / RHD) | left-hand drive (LHD) | - | VERIFIED | A | E-024 |
| interior.steering_wheel_diameter | Steering wheel outer diameter | 350 mm | 30 | ESTIMATED | D | E-062 |
| mass.curb_mass | Curb mass (as defined by the source document) | 1125 kg | 1 | VERIFIED | A | E-014, E-015, E-017 |
| mass.gross_vehicle_mass | Gross vehicle mass | 1550 kg | 50 | ESTIMATED | D | E-058 |
| mass.axle_load_front_measured | Front axle load, measured | 565 kg | 60 | ESTIMATED | D | E-062 |
| mass.axle_load_rear_measured | Rear axle load, measured | 560 kg | 60 | ESTIMATED | D | E-062 |
| engine.engine_code | Engine type code | 131 D1.016 | - | ESTIMATED | D | E-058, E-040 |
| engine.displacement | Displacement | 1581 cm3 | 1 | VERIFIED | A | E-015 |
| engine.cylinder_count | Number of cylinders | 4 | 0 | VERIFIED | A | E-058 |
| engine.cylinder_layout | Cylinder layout | inline | - | VERIFIED | A | E-058 |
| engine.valvetrain | Valvetrain (OHV / SOHC / DOHC) | SOHC, toothed timing belt | - | VERIFIED | A | E-058 |
| engine.bore | Bore | 86.4 mm | 0 | VERIFIED | A | E-058 |
| engine.stroke | Stroke | 67.4 mm | 0 | VERIFIED | A | E-058 |
| engine.compression_ratio | Compression ratio | 9.2 ratio | 0.1 | ESTIMATED | D | E-058 |
| engine.max_power | Maximum power | 61 kW | 3 | ESTIMATED | D (B adayı: birden fazla ilan/özet, bağımsızlık doğrulanmadı) | E-011, E-013 |
| engine.max_power_speed | Engine speed at maximum power | 5800 rpm | 50 | ESTIMATED | D | E-058 |
| engine.max_torque | Maximum torque | 132 N·m | 1 | ESTIMATED | D | E-058 |
| engine.max_torque_speed | Engine speed at maximum torque | 3250 rpm | 50 | ESTIMATED | D | E-058 |
| engine.fuel_type | Fuel type as registered (check for LPG conversion) | LPG (registered conversion) | - | VERIFIED | A | E-014, E-015 |
| engine.base_fuel | Base fuel of the engine before the LPG conversion | petrol | - | ESTIMATED | D (B adayı: birden fazla ilan/özet, bağımsızlık doğrulanmadı) | E-017, E-011, E-013 |
| engine.fuel_system_type | Fuel system (carburettor / single-point / multi-point injection) | carburettor | - | ESTIMATED | C | E-058, E-027 |
| engine.ignition_type | Ignition system type | electronic | - | VERIFIED | A | E-058 |
| engine.cooling_system_type | Cooling system type | liquid-cooled; front radiator with electric fan; separate expansion tank | - | VERIFIED | A | E-027 |
| engine.radiator_core_width | Radiator core width | 470 mm | 5 | ESTIMATED | D | E-041 |
| engine.radiator_core_height | Radiator core height | 292 mm | 5 | ESTIMATED | D | E-041 |
| engine.radiator_core_depth | Radiator core depth | 32 mm | 2 | ESTIMATED | D | E-041 |
| engine.engine_orientation | Engine orientation (longitudinal / transverse) | longitudinal | - | VERIFIED | A | E-027 |
| transmission.transmission_type | Transmission type (manual / automatic) | manual (floor-mounted lever, three pedals) | - | VERIFIED | A | E-024 |
| transmission.forward_gear_count | Number of forward gears | 5 | 0 | VERIFIED | A | E-058 |
| transmission.gear_ratios | Forward gear ratios (1st..nth) | [3.543, 2.139, 1.377, 1.0, 0.868] ratio | 0.01 | VERIFIED | A | E-058 |
| transmission.reverse_ratio | Reverse gear ratio | 3.526 ratio | 0 | VERIFIED | A | E-058 |
| transmission.final_drive_ratio | Final drive ratio | 4.1 ratio | 0 | VERIFIED | A | E-058 |
| transmission.clutch_actuation | Clutch actuation (cable / hydraulic) | mechanical (cable), self-adjusting | - | VERIFIED | A | E-058 |
| transmission.clutch_disc_diameter | Clutch disc diameter | 190 mm | 10 | ESTIMATED | D (B adayı: birden fazla ilan/özet, bağımsızlık doğrulanmadı) | E-059, E-060 |
| transmission.gearbox_input_bearing | Gearbox input (main) bearing, bore x OD x width | 30 x 75 x 19 | - | ESTIMATED | D | E-056 |
| transmission.gearbox_output_bearing | Gearbox rear output bearing, bore x OD x width | 25 x 52 x 21 | - | ESTIMATED | D | E-056 |
| drivetrain.drive_layout | Drive layout (e.g. front-engine RWD / FWD) | front-engine, rear-wheel drive | - | ESTIMATED | D | E-009 |
| drivetrain.propshaft_construction | Propeller shaft construction | two-piece, flexible coupling at the gearbox, centre bearing, universal joints | - | ESTIMATED | D | E-056 |
| drivetrain.propshaft_tube_od | Propeller shaft tube outer diameter | 69.85 mm | 0.5 | ESTIMATED | D | E-056 |
| drivetrain.flex_coupling_od | Flexible coupling (guibo) outer diameter | 130 mm | 2 | ESTIMATED | D | E-056 |
| drivetrain.flex_coupling_thickness | Flexible coupling thickness | 47 mm | 2 | ESTIMATED | D | E-056 |
| drivetrain.ujoint_cross | Universal-joint cross (cup diameter x span) | 23.8 x 61.2 | - | ESTIMATED | D | E-056 |
| drivetrain.axle_shaft_length | Rear half-shaft overall length | 690 mm | 10 | ESTIMATED | D | E-056 |
| drivetrain.axle_shaft_spline_diameter | Rear half-shaft spline diameter | 24 mm | 0.5 | ESTIMATED | D (B adayı: birden fazla ilan/özet, bağımsızlık doğrulanmadı) | E-056, E-057 |
| drivetrain.rear_wheel_bearing | Rear wheel bearing, bore x OD x width | 30 x 65 x 21 | - | ESTIMATED | D | E-056 |
| drivetrain.diff_side_bearing | Differential side bearing (taper) | 38.112 x 71.016 x 18.258 | - | ESTIMATED | D | E-056 |
| chassis.fuel_tank_capacity | Fuel tank capacity | 50 L | 0 | VERIFIED | A | E-058 |
| suspension.front_suspension_type | Front suspension type | MacPherson strut | - | VERIFIED | A | E-027 |
| suspension.rear_suspension_type | Rear suspension type | rigid (live) rear axle | - | VERIFIED | A | E-025 |
| suspension.front_spring_type | Front spring type | coil | - | VERIFIED | A | E-058 |
| suspension.rear_spring_type | Rear spring type (coil / leaf) | coil | - | VERIFIED | A | E-058 |
| suspension.front_antiroll_bar_fitted | Front anti-roll bar fitted | True | - | VERIFIED | A | E-058 |
| suspension.rear_antiroll_bar_fitted | Rear anti-roll bar fitted | False | - | ESTIMATED | D | E-058 |
| suspension.rear_damper_length_compressed | Rear damper eye-to-eye length, compressed | 337 mm | 20 | ESTIMATED | D (B adayı: birden fazla ilan/özet, bağımsızlık doğrulanmadı) | E-044, E-059 |
| suspension.rear_damper_length_extended | Rear damper eye-to-eye length, extended | 527 mm | 20 | ESTIMATED | D (B adayı: birden fazla ilan/özet, bağımsızlık doğrulanmadı) | E-044, E-059 |
| suspension.front_lower_arm_length | Front lower arm (with ball joint) length | 289 mm | 3 | ESTIMATED | D | E-046 |
| suspension.front_strut_bore | Front strut damper bore | 27 mm | 1 | ESTIMATED | D | E-048 |
| suspension.front_strut_rod_diameter | Front strut piston-rod diameter | 20 mm | 1 | ESTIMATED | D | E-048 |
| suspension.front_wheel_bearing | Front wheel taper bearing (bore x OD x width) | 28 x 57.15 x 17.462 | 0.1 | ESTIMATED | D | E-047 |
| suspension.rear_upper_link_length | Rear upper (short) link, hole to hole | 315 mm | 2 | ESTIMATED | D (B adayı: birden fazla ilan/özet, bağımsızlık doğrulanmadı) | E-056, E-057 |
| suspension.rear_lower_link_length | Rear lower (long) trailing arm, hole to hole | 617 mm | 3 | ESTIMATED | D (B adayı: birden fazla ilan/özet, bağımsızlık doğrulanmadı) | E-056, E-057 |
| suspension.panhard_rod_length | Panhard rod length, hole to hole | 1000 mm | 40 | ESTIMATED | D | E-059 |
| suspension.front_spring_height_loaded | Front spring height under the check load | 270 mm | 5 | ESTIMATED | D | E-059 |
| suspension.rear_spring_height_loaded | Rear spring height under the check load | 235 mm | 5 | ESTIMATED | D | E-059 |
| suspension.front_strut_length_extended | Front strut damper length, extended | 522 mm | 3 | ESTIMATED | D | E-059 |
| suspension.front_strut_length_compressed | Front strut damper length, compressed | 362 mm | 3 | ESTIMATED | D | E-059 |
| steering.steering_gear_type | Steering gear type (rack-and-pinion / recirculating ball) | rack-and-pinion | - | VERIFIED | A | E-058 |
| steering.power_assisted | Power assisted | yes (hydraulic, belt-driven pump) | - | VERIFIED | A | E-027 |
| steering.turns_lock_to_lock | Steering-wheel turns, lock to lock | 3 turns | 0 | VERIFIED | A | E-058, E-027 |
| steering.tie_rod_length | Tie rod (rot mili) length | 282.5 mm | 1 | ESTIMATED | D | E-045 |
| steering.steering_gear_overall_length | Steering gear overall length (catalogue) | 1112 mm | 5 | ESTIMATED | D | E-056 |
| brakes.front_brake_type | Front brake type (disc / drum) | disc | - | VERIFIED | A | E-058 |
| brakes.front_disc_diameter | Front disc diameter | 227.5 mm | 1 | ESTIMATED | D (B adayı: birden fazla ilan/özet, bağımsızlık doğrulanmadı) | E-037, E-038 |
| brakes.rear_brake_type | Rear brake type (disc / drum) | drum | - | VERIFIED | A | E-058 |
| brakes.rear_drum_diameter | Rear drum diameter | 228 mm | 2 | ESTIMATED | D | E-042 |
| brakes.rear_drum_width | Rear drum width | 47.7 mm | 1 | ESTIMATED | D | E-042 |
| brakes.front_disc_thickness | Front disc thickness (new) | 10.8 mm | 0.2 | ESTIMATED | D | E-037 |
| brakes.brake_booster_fitted | Brake booster (servo) fitted | True | - | VERIFIED | A | E-058, E-050 |
| brakes.parking_brake_type | Parking brake type | mechanical lever, acting on the rear wheels | - | VERIFIED | A | E-058, E-055 |
| wheels_tires.tire_size_front | Front tire size and load/speed index | 185/65 R14 | - | ESTIMATED | C | E-028 |
| wheels_tires.tire_size_rear | Rear tire size and load/speed index | 185/65 R14 | - | ESTIMATED | C | E-028 |
| wheels_tires.wheel_rim_diameter | Rim diameter | 14 in | 0.5 | VERIFIED | A | E-017, E-010, E-028 |
| wheels_tires.wheel_rim_width | Rim width | 5.5 in | 0.1 | VERIFIED | A | E-058 |
| wheels_tires.wheel_offset_et | Wheel offset (ET) | 29 mm | 5 | ESTIMATED | D | E-053 |
| wheels_tires.wheel_pcd | Bolt-circle diameter (PCD) | 98 mm | 0.5 | ESTIMATED | C | E-033, E-026 |
| wheels_tires.wheel_fastener_count | Number of wheel bolts or studs | 4 | - | VERIFIED | A | E-026 |
| wheels_tires.wheel_centre_bore | Wheel centre bore | 58.1 mm | 0.5 | ESTIMATED | D | E-053 |
| wheels_tires.wheel_material | Wheel material (steel / alloy) | pressed steel | - | VERIFIED | A | E-017, E-026, E-028 |
| wheels_tires.spare_wheel_location | Spare wheel location | not in the spare-wheel well (the LPG tank occupies it); a wheel stood loose in the luggage compartment in the photos | - | ESTIMATED | C | E-022 |
| wheels_tires.wheel_colour | Wheel finish / colour | black (painted) | - | VERIFIED | A | E-017, E-026 |
| wheels_tires.wheel_rim_flange_contour | Rim flange contour letter | J | - | ESTIMATED | E | E-018 |
| wheels_tires.wheel_rim_flange_height | Rim flange height above the bead seat (contour J) | 17.5 mm | 1.0 | ESTIMATED | D | E-021 |
| wheels_tires.wheel_rim_steel_thickness | Rim barrel and flange steel thickness | 3.0 mm | 1.0 | ESTIMATED | E | E-019 |
| wheels_tires.wheel_disc_thickness | Wheel disc (centre) steel thickness | 4.0 mm | 1.5 | ESTIMATED | E | E-019 |
| lpg_system.kit_type | LPG kit type (venturi mixer or vapour injection) | conventional venturi / leaf mixer at the carburettor with petrol cut-off solenoid (typical for 131 D1.016) | - | ESTIMATED | D | E-059, E-022 |
| lpg_system.tank_type | LPG tank type | toroidal (ring) tank in the spare-wheel well | - | VERIFIED | A | E-017, E-022 |
| lpg_system.tank_location | LPG tank location | spare-wheel well at the rear of the luggage floor, near the tailgate sill; underside protrudes below the floor | - | VERIFIED | A | E-017, E-022, E-025 |
| lpg_system.tank_nominal_capacity | LPG tank nominal capacity | 40 L | 1 | ESTIMATED | D | E-017 |
| lpg_system.tank_outer_diameter | LPG tank outer diameter | 600 mm | 30 | ESTIMATED | E | E-018 |
| lpg_system.tank_height | LPG tank height | 180 mm | 20 | ESTIMATED | E | E-018 |
| lpg_system.tank_central_opening_diameter | LPG tank central opening diameter | 130 mm | 40 | ESTIMATED | E | E-019, E-020 |
| lpg_system.tank_wall_thickness | LPG tank wall thickness | 3.0 mm | 1.0 | ESTIMATED | E | E-019 |
| lpg_system.tank_section_shape | LPG tank cross-section model | stadium | - | ESTIMATED | E | E-019 |
| lpg_system.max_fill_fraction | Maximum fill (fill-stop) fraction of water capacity | 80 % | 2 | ESTIMATED | E | E-018, E-020 |
| lpg_system.tank_centre_x | LPG tank centre X (VCS, rearward from front axle) | 3150 mm | 100 | ESTIMATED | D | E-062 |
| lpg_system.tank_centre_y | LPG tank centre Y (VCS, right positive) | 0 mm | 80 | ESTIMATED | D | E-062 |
| lpg_system.tank_base_z | LPG tank underside height above ground | 220 mm | 60 | ESTIMATED | D | E-062 |
| lpg_system.multivalve_orientation | Multivalve clock position on the tank | in the central opening, on the inner wall of the tank (ALBIEN multivalve, 12 V solenoid, level gauge) | - | VERIFIED | A | E-022, E-023 |
| lpg_system.filler_location | LPG filler valve location | under the rear bumper, side opposite the exhaust (typical 1990s installation) | - | ESTIMATED | D | E-062 |
| lpg_system.tank_mounting | Tank mounting (frame, straps, bolts) | bolted through the floor of the spare-wheel well at the tank centre (two brackets in the central opening, two bolt heads visible from below); opening closed by a black cover with two holes | - | VERIFIED | A | E-022, E-025 |
| lpg_system.tank_marking | LPG tank maker and approval marking | maker ATIKER; approval mark 'E7 67R-01 0049401' (UN Regulation No. 67, 01 series) | - | VERIFIED | A | E-022 |
| electrical.system_voltage | System voltage | 12 V | 0 | VERIFIED | A | E-058 |
| electrical.earth_polarity | Earth polarity | negative | - | VERIFIED | A | E-058 |
| electrical.battery_capacity | Battery capacity | 72 Ah | 0 | VERIFIED | A | E-049 |
| electrical.battery_cold_cranking | Battery cold-cranking current | 700 A | 0 | VERIFIED | A | E-049 |
| electrical.battery_case_length | Battery case length | 278 mm | 10 | ESTIMATED | D | E-043, E-049 |
| electrical.battery_case_width | Battery case width | 175 mm | 2 | ESTIMATED | D | E-043, E-049 |
| electrical.battery_case_height | Battery case height | 175 mm | 15 | ESTIMATED | D | E-043, E-049 |
| electrical.alternator_rated_current | Alternator rated current | 55 A | 1 | ESTIMATED | D | E-058 |
| electrical.headlamp_type | Headlamp type / bulb | H4 halogen | - | ESTIMATED | D | E-036 |
| electrical.fuse_box_location | Fuse box location | lower right of the dashboard (passenger side, under the glovebox), cover with two screws; relays on and beside the box | - | VERIFIED | A | E-058, E-060 |
| body_profile.bumper_protrusion | Bumper face beyond the body face (front and rear) | 60 mm | 30 | ESTIMATED | D | E-062 |
| body_profile.bumper_height | Bumper vertical height | 220 mm | 50 | ESTIMATED | D | E-062 |
| body_profile.bumper_bottom_z | Bumper lower edge above ground | 250 mm | 50 | ESTIMATED | D | E-062 |
| body_profile.sill_z | Body-side (sill) lower edge above ground | 200 mm | 40 | ESTIMATED | D | E-062 |
| body_profile.nose_bottom_z | Front panel lower edge above ground | 300 mm | 50 | ESTIMATED | D | E-062 |
| body_profile.nose_top_z | Hood leading edge above ground | 840 mm | 50 | ESTIMATED | D | E-062 |
| body_profile.cowl_x | Windshield base, X behind the front wheel centre | 480 mm | 100 | ESTIMATED | D | E-061 |
| body_profile.belt_z | Side-window sill (beltline) above ground | 960 mm | 50 | ESTIMATED | D | E-062 |
| body_profile.rear_bottom_z | Rear panel lower edge above ground | 470 mm | 50 | ESTIMATED | D | E-062 |
| body_profile.windshield_top_x | Windshield top edge, X behind the front wheel centre | 910 mm | 80 | ESTIMATED | D | E-061 |
| body_profile.roof_rear_inset | Roof end ahead of the rear body face | 120 mm | 50 | ESTIMATED | D | E-062 |
| body_profile.roof_width | Roof width (side to side, at the roof) | 1300 mm | 80 | ESTIMATED | D | E-062 |
| body_profile.b_pillar_x | B-pillar centre, X behind the front wheel centre | 1525 mm | 80 | ESTIMATED | D | E-061 |
| body_profile.c_pillar_x | Rear-door rear edge, X behind the front wheel centre | 2400 mm | 100 | ESTIMATED | D | E-061 |
| body_profile.mirror_protrusion | Mirror housing beyond the body side | 95 mm | 30 | ESTIMATED | D | E-062 |
