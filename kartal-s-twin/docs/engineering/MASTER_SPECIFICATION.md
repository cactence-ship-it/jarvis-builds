# Master specification - Tofaş Kartal S 1997 (VEH-01)

Güncelleme: 2026-11-07. Bu dosya `specs/kartal_s_1997.yaml` dosyasından üretildi (tek doğru kaynak odur; değerler orada değiştirilir). Durumlar: proje şeması VERIFIED / ESTIMATED / UNKNOWN (D-005). Bu belgedeki sınıflar: VERIFIED = birincil kanıt (araç belgesi, aracın kendi etiketinin fotoğrafı veya ölçüm); PROVISIONAL = ESTIMATED, kaynağı var ama varyant/ölçü noktası kesin değil; UNKNOWN = araştırıldı, güvenilir veri yok, belge araştırmasıyla hâlâ bulunabilir; MEASURE_REQUIRED = yalnızca gerçek araç üzerinde ölçüm/inceleme ile bulunabilir. Güven puanı: A birincil belge/etiket; B birden fazla bağımsız teknik kaynak; C tek katalog/üretici kaydı veya net fotoğraf yorumu; D ilan/topluluk/arama özeti; E mühendislik tahmini. E sınıfı değerler üretim CAD'inde kesin ölçü olarak kullanılmaz; proje kuralı D-016 zaten mühendislik CAD'inde PLACEHOLDER'ı reddeder.

## Bugünkü başlangıçta bilinmeyen 52 değerin durumu

**VERIFIED**: 2 · **PROVISIONAL**: 6 · **UNKNOWN**: 2 · **MEASURE_REQUIRED**: 42

| Anahtar | Ad | Değer | Spec durumu | Sınıf | Güven | Kaynak | Not |
|---|---|---|---|---|---|---|---|
| dimensions.overall_width_mirrors | Overall width incl. mirrors | - | UNKNOWN | MEASURE_REQUIRED | - | - |  |
| dimensions.overall_height_roof_rails | Overall height incl. roof rails (if fitted) | - | UNKNOWN | MEASURE_REQUIRED | - | - |  |
| dimensions.front_overhang | Front overhang (front axle to front extremity) | - | UNKNOWN | MEASURE_REQUIRED | - | - | Not published. Sum of overhangs = length - wheelbase = 1906 mm (4396) or 1871 mm (4361); the split needs a measurement. |
| dimensions.rear_overhang | Rear overhang (rear axle to rear extremity) | - | UNKNOWN | MEASURE_REQUIRED | - | - | See front_overhang: only the sum is derivable from published length and wheelbase. |
| dimensions.ground_clearance_min | Minimum ground clearance (unladen) | 120 mm | ESTIMATED | PROVISIONAL | D | E-052 | Fiat 131 Panorama figure; Kartal and this car (LPG tank in the spare-wheel well protrudes below the floor, E-025) may differ. Measure. |
| dimensions.wheel_centre_to_arch_fl | Hub centre to wheel-arch lip, front left | - | UNKNOWN | MEASURE_REQUIRED | - | - |  |
| dimensions.wheel_centre_to_arch_fr | Hub centre to wheel-arch lip, front right | - | UNKNOWN | MEASURE_REQUIRED | - | - |  |
| dimensions.wheel_centre_to_arch_rl | Hub centre to wheel-arch lip, rear left | - | UNKNOWN | MEASURE_REQUIRED | - | - |  |
| dimensions.wheel_centre_to_arch_rr | Hub centre to wheel-arch lip, rear right | - | UNKNOWN | MEASURE_REQUIRED | - | - |  |
| body.body_construction | Body construction (unibody / separate frame) | - | UNKNOWN | UNKNOWN | - | - |  |
| body.cargo_floor_length_seat_up | Cargo floor length, rear seat up | - | UNKNOWN | MEASURE_REQUIRED | - | - |  |
| body.cargo_floor_length_seat_folded | Cargo floor length, rear seat folded | - | UNKNOWN | MEASURE_REQUIRED | - | - |  |
| body.cargo_width_between_arches | Cargo width between wheel arches | - | UNKNOWN | MEASURE_REQUIRED | - | - |  |
| body.tailgate_opening_width | Tailgate opening width | - | UNKNOWN | MEASURE_REQUIRED | - | - |  |
| body.tailgate_opening_height | Tailgate opening height | - | UNKNOWN | MEASURE_REQUIRED | - | - |  |
| body.load_sill_height | Load sill height | - | UNKNOWN | MEASURE_REQUIRED | - | - |  |
| interior.steering_wheel_diameter | Steering wheel outer diameter | - | UNKNOWN | MEASURE_REQUIRED | - | - |  |
| mass.axle_load_front_measured | Front axle load, measured | - | UNKNOWN | MEASURE_REQUIRED | - | - |  |
| mass.axle_load_rear_measured | Rear axle load, measured | - | UNKNOWN | MEASURE_REQUIRED | - | - |  |
| engine.engine_code | Engine type code | - | UNKNOWN | MEASURE_REQUIRED | - | - | Candidates: 131.D1.016 (carburettor, Doğan/Kartal 1.6 S/SL/SLX 1992-2002, wikipedia table E-040) or 131.F3.016 (i.e. cat 1998-2002). VEH-01 is a 1997 carburettor car (air cleaner on a carburettor, E-027), so 131.D1.016 is the only candidate that fits; still UNKNOWN until the block stamping is read. |
| engine.ignition_type | Ignition system type | electronic (breakerless) module | ESTIMATED | PROVISIONAL | D | E-051 | Module-like unit on the LH inner wing (photo). Listings sell both breaker-point and module distributors for the family; distributor not visible. |
| suspension.rear_antiroll_bar_fitted | Rear anti-roll bar fitted | - | UNKNOWN | MEASURE_REQUIRED | - | - |  |
| steering.turns_lock_to_lock | Steering-wheel turns, lock to lock | - | UNKNOWN | UNKNOWN | - | - |  |
| brakes.brake_booster_fitted | Brake booster (servo) fitted | True | ESTIMATED | PROVISIONAL | C | E-050 | Round unit behind the master cylinder at the LH bulkhead (photo interpretation). |
| brakes.parking_brake_type | Parking brake type | centre lever, cables to rear drums | ESTIMATED | PROVISIONAL | C | E-055, E-042 | Lever seen in the interior photo; cables inferred. |
| wheels_tires.wheel_offset_et | Wheel offset (ET) | 29 mm | ESTIMATED | PROVISIONAL | D | E-053 | Fiat 131 4x98 wheels (single source); VEH-01 black steel 14 in rims not checked. |
| wheels_tires.wheel_centre_bore | Wheel centre bore | 58.1 mm | ESTIMATED | PROVISIONAL | D | E-053 | Generic Fiat 4x98 hub bore; matches E-053. |
| lpg_system.kit_type | LPG kit type (venturi mixer or vapour injection) | - | UNKNOWN | MEASURE_REQUIRED | - | - | No mixer or injector rail visible in the engine-bay photos (E-027); the air cleaner covers the carburettor. A round coolant-heated unit near the bulkhead may be the vaporiser (unconfirmed). |
| lpg_system.tank_centre_x | LPG tank centre X (VCS, rearward from front axle) | - | UNKNOWN | MEASURE_REQUIRED | - | - |  |
| lpg_system.tank_centre_y | LPG tank centre Y (VCS, right positive) | - | UNKNOWN | MEASURE_REQUIRED | - | - |  |
| lpg_system.tank_base_z | LPG tank underside height above ground | - | UNKNOWN | MEASURE_REQUIRED | - | - |  |
| lpg_system.filler_location | LPG filler valve location | - | UNKNOWN | MEASURE_REQUIRED | - | - | Not visible on the exterior photos (E-026): no separate LPG filler on either side or the bumper in those views. Ask the owner or photograph under the fuel flap and the rear bumper. |
| electrical.earth_polarity | Earth polarity | - | UNKNOWN | MEASURE_REQUIRED | - | - |  |
| electrical.battery_capacity | Battery capacity | 72 Ah | VERIFIED | VERIFIED | A | E-049 | Label of the fitted battery (İnci Formul A Taurus). The original factory battery is not known. |
| electrical.battery_cold_cranking | Battery cold-cranking current | 700 A | VERIFIED | VERIFIED | A | E-049 | 700 A (EN) per label. |
| electrical.alternator_rated_current | Alternator rated current | - | UNKNOWN | MEASURE_REQUIRED | - | - | Listed variants 55 / 65 / 85 A (E-039); read the alternator label. |
| electrical.fuse_box_location | Fuse box location | - | UNKNOWN | MEASURE_REQUIRED | - | - |  |
| body_profile.bumper_protrusion | Bumper face beyond the body face (front and rear) | - | UNKNOWN | MEASURE_REQUIRED | - | - | Placeholder in specs/placeholder_assumptions.yaml until measured |
| body_profile.bumper_height | Bumper vertical height | - | UNKNOWN | MEASURE_REQUIRED | - | - | Placeholder in specs/placeholder_assumptions.yaml until measured |
| body_profile.bumper_bottom_z | Bumper lower edge above ground | - | UNKNOWN | MEASURE_REQUIRED | - | - | Placeholder in specs/placeholder_assumptions.yaml until measured |
| body_profile.sill_z | Body-side (sill) lower edge above ground | - | UNKNOWN | MEASURE_REQUIRED | - | - | Placeholder in specs/placeholder_assumptions.yaml until measured |
| body_profile.nose_bottom_z | Front panel lower edge above ground | - | UNKNOWN | MEASURE_REQUIRED | - | - | Placeholder in specs/placeholder_assumptions.yaml until measured |
| body_profile.nose_top_z | Hood leading edge above ground | - | UNKNOWN | MEASURE_REQUIRED | - | - | Placeholder in specs/placeholder_assumptions.yaml until measured |
| body_profile.cowl_x | Windshield base, X behind the front wheel centre | - | UNKNOWN | MEASURE_REQUIRED | - | - | Placeholder in specs/placeholder_assumptions.yaml until measured |
| body_profile.belt_z | Side-window sill (beltline) above ground | - | UNKNOWN | MEASURE_REQUIRED | - | - | Placeholder in specs/placeholder_assumptions.yaml until measured |
| body_profile.rear_bottom_z | Rear panel lower edge above ground | - | UNKNOWN | MEASURE_REQUIRED | - | - | Placeholder in specs/placeholder_assumptions.yaml until measured |
| body_profile.windshield_top_x | Windshield top edge, X behind the front wheel centre | - | UNKNOWN | MEASURE_REQUIRED | - | - | Placeholder in specs/placeholder_assumptions.yaml until measured |
| body_profile.roof_rear_inset | Roof end ahead of the rear body face | - | UNKNOWN | MEASURE_REQUIRED | - | - | Placeholder in specs/placeholder_assumptions.yaml until measured |
| body_profile.roof_width | Roof width (side to side, at the roof) | - | UNKNOWN | MEASURE_REQUIRED | - | - | Placeholder in specs/placeholder_assumptions.yaml until measured |
| body_profile.b_pillar_x | B-pillar centre, X behind the front wheel centre | - | UNKNOWN | MEASURE_REQUIRED | - | - | Placeholder in specs/placeholder_assumptions.yaml until measured |
| body_profile.c_pillar_x | Rear-door rear edge, X behind the front wheel centre | - | UNKNOWN | MEASURE_REQUIRED | - | - | Placeholder in specs/placeholder_assumptions.yaml until measured |
| body_profile.mirror_protrusion | Mirror housing beyond the body side | - | UNKNOWN | MEASURE_REQUIRED | - | - | Placeholder in specs/placeholder_assumptions.yaml until measured |

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
| dimensions.overall_length | Overall length incl. bumpers | 4396 mm | 40 | ESTIMATED | D (B adayı: birden fazla ilan/özet, bağımsızlık doğrulanmadı) | E-007, E-008, E-009 |
| dimensions.overall_width_body | Overall width excl. mirrors | 1642 mm | 20 | ESTIMATED | D (B adayı: birden fazla ilan/özet, bağımsızlık doğrulanmadı) | E-007, E-010 |
| dimensions.overall_width_mirrors | Overall width incl. mirrors | - | - | UNKNOWN | - | - |
| dimensions.overall_height | Overall height excl. roof rails | 1496 mm | 25 | ESTIMATED | D (B adayı: birden fazla ilan/özet, bağımsızlık doğrulanmadı) | E-007, E-010 |
| dimensions.overall_height_roof_rails | Overall height incl. roof rails (if fitted) | - | - | UNKNOWN | - | - |
| dimensions.wheelbase_lh | Wheelbase, left side | 2490 mm | 10 | ESTIMATED | D (B adayı: birden fazla ilan/özet, bağımsızlık doğrulanmadı) | E-009, E-010 |
| dimensions.wheelbase_rh | Wheelbase, right side | 2490 mm | 10 | ESTIMATED | D (B adayı: birden fazla ilan/özet, bağımsızlık doğrulanmadı) | E-009, E-010 |
| dimensions.front_track | Front track (tyre tread centre to centre) | 1386 mm | 15 | ESTIMATED | D | E-011 |
| dimensions.rear_track | Rear track (tyre tread centre to centre) | 1327 mm | 15 | ESTIMATED | D | E-011 |
| dimensions.front_overhang | Front overhang (front axle to front extremity) | - | - | UNKNOWN | - | - |
| dimensions.rear_overhang | Rear overhang (rear axle to rear extremity) | - | - | UNKNOWN | - | - |
| dimensions.ground_clearance_min | Minimum ground clearance (unladen) | 120 mm | 20 | ESTIMATED | D | E-052 |
| dimensions.wheel_centre_to_arch_fl | Hub centre to wheel-arch lip, front left | - | - | UNKNOWN | - | - |
| dimensions.wheel_centre_to_arch_fr | Hub centre to wheel-arch lip, front right | - | - | UNKNOWN | - | - |
| dimensions.wheel_centre_to_arch_rl | Hub centre to wheel-arch lip, rear left | - | - | UNKNOWN | - | - |
| dimensions.wheel_centre_to_arch_rr | Hub centre to wheel-arch lip, rear right | - | - | UNKNOWN | - | - |
| dimensions.turning_circle_kerb | Turning circle, kerb to kerb | 10300 mm | 300 | ESTIMATED | D | E-038 |
| body.body_construction | Body construction (unibody / separate frame) | - | - | UNKNOWN | - | - |
| body.cargo_floor_length_seat_up | Cargo floor length, rear seat up | - | - | UNKNOWN | - | - |
| body.cargo_floor_length_seat_folded | Cargo floor length, rear seat folded | - | - | UNKNOWN | - | - |
| body.cargo_width_between_arches | Cargo width between wheel arches | - | - | UNKNOWN | - | - |
| body.tailgate_opening_width | Tailgate opening width | - | - | UNKNOWN | - | - |
| body.tailgate_opening_height | Tailgate opening height | - | - | UNKNOWN | - | - |
| body.load_sill_height | Load sill height | - | - | UNKNOWN | - | - |
| body.cargo_volume | Cargo volume (state the method in notes) | 846 L | 50 | ESTIMATED | D | E-034 |
| interior.seating_capacity | Seating capacity | 5 | 1 | ESTIMATED | C | E-014, E-015, E-024 |
| interior.steering_side | Steering side (LHD / RHD) | left-hand drive (LHD) | - | VERIFIED | A | E-024 |
| interior.steering_wheel_diameter | Steering wheel outer diameter | - | - | UNKNOWN | - | - |
| mass.curb_mass | Curb mass (as defined by the source document) | 1125 kg | 1 | VERIFIED | A | E-014, E-015, E-017 |
| mass.gross_vehicle_mass | Gross vehicle mass | 1550 kg | 50 | ESTIMATED | D | E-011 |
| mass.axle_load_front_measured | Front axle load, measured | - | - | UNKNOWN | - | - |
| mass.axle_load_rear_measured | Rear axle load, measured | - | - | UNKNOWN | - | - |
| engine.engine_code | Engine type code | - | - | UNKNOWN | - | - |
| engine.displacement | Displacement | 1581 cm3 | 1 | VERIFIED | A | E-015 |
| engine.cylinder_count | Number of cylinders | 4 | - | ESTIMATED | D | E-011 |
| engine.cylinder_layout | Cylinder layout | inline | - | ESTIMATED | D | E-011 |
| engine.valvetrain | Valvetrain (OHV / SOHC / DOHC) | SOHC | - | ESTIMATED | D | E-012 |
| engine.bore | Bore | 86.4 mm | 0.1 | ESTIMATED | D | E-029 |
| engine.stroke | Stroke | 67.4 mm | 0.1 | ESTIMATED | D | E-029 |
| engine.compression_ratio | Compression ratio | 9.2 ratio | 0.3 | ESTIMATED | D | E-029 |
| engine.max_power | Maximum power | 61 kW | 3 | ESTIMATED | D (B adayı: birden fazla ilan/özet, bağımsızlık doğrulanmadı) | E-011, E-013 |
| engine.max_power_speed | Engine speed at maximum power | 5500 rpm | 250 | ESTIMATED | D | E-030 |
| engine.max_torque | Maximum torque | 131 N·m | 6 | ESTIMATED | D | E-013 |
| engine.max_torque_speed | Engine speed at maximum torque | 3000 rpm | 250 | ESTIMATED | D | E-030 |
| engine.fuel_type | Fuel type as registered (check for LPG conversion) | LPG (registered conversion) | - | VERIFIED | A | E-014, E-015 |
| engine.base_fuel | Base fuel of the engine before the LPG conversion | petrol | - | ESTIMATED | D (B adayı: birden fazla ilan/özet, bağımsızlık doğrulanmadı) | E-017, E-011, E-013 |
| engine.fuel_system_type | Fuel system (carburettor / single-point / multi-point injection) | carburettor | - | ESTIMATED | C | E-017, E-012, E-013, E-027 |
| engine.ignition_type | Ignition system type | electronic (breakerless) module | - | ESTIMATED | D | E-051 |
| engine.cooling_system_type | Cooling system type | liquid-cooled; front radiator with electric fan; separate expansion tank | - | VERIFIED | A | E-027 |
| engine.radiator_core_width | Radiator core width | 470 mm | 5 | ESTIMATED | D | E-041 |
| engine.radiator_core_height | Radiator core height | 292 mm | 5 | ESTIMATED | D | E-041 |
| engine.radiator_core_depth | Radiator core depth | 32 mm | 2 | ESTIMATED | D | E-041 |
| engine.engine_orientation | Engine orientation (longitudinal / transverse) | longitudinal | - | VERIFIED | A | E-027 |
| transmission.transmission_type | Transmission type (manual / automatic) | manual (floor-mounted lever, three pedals) | - | VERIFIED | A | E-024 |
| transmission.forward_gear_count | Number of forward gears | 5 | - | ESTIMATED | D (B adayı: birden fazla ilan/özet, bağımsızlık doğrulanmadı) | E-031, E-012 |
| transmission.gear_ratios | Forward gear ratios (1st..nth) | [3.667, 2.1, 1.361, 1.0, 0.881] ratio | 0.01 | ESTIMATED | D | E-031 |
| transmission.reverse_ratio | Reverse gear ratio | 3.526 ratio | 0.01 | ESTIMATED | D | E-031 |
| transmission.final_drive_ratio | Final drive ratio | 4.1 ratio | 0.05 | ESTIMATED | D | E-031 |
| transmission.clutch_actuation | Clutch actuation (cable / hydraulic) | cable | - | ESTIMATED | D | E-035 |
| drivetrain.drive_layout | Drive layout (e.g. front-engine RWD / FWD) | front-engine, rear-wheel drive | - | ESTIMATED | D | E-009 |
| chassis.fuel_tank_capacity | Fuel tank capacity | 52 L | 3 | ESTIMATED | D | E-010 |
| suspension.front_suspension_type | Front suspension type | MacPherson strut | - | VERIFIED | A | E-027 |
| suspension.rear_suspension_type | Rear suspension type | rigid (live) rear axle | - | VERIFIED | A | E-025 |
| suspension.front_spring_type | Front spring type | coil | - | ESTIMATED | C | E-032, E-027 |
| suspension.rear_spring_type | Rear spring type (coil / leaf) | coil | - | ESTIMATED | C | E-032, E-025 |
| suspension.front_antiroll_bar_fitted | Front anti-roll bar fitted | True | - | ESTIMATED | D | E-032 |
| suspension.rear_antiroll_bar_fitted | Rear anti-roll bar fitted | - | - | UNKNOWN | - | - |
| suspension.rear_damper_length_compressed | Rear damper eye-to-eye length, compressed | 337 mm | 20 | ESTIMATED | D | E-044 |
| suspension.rear_damper_length_extended | Rear damper eye-to-eye length, extended | 527 mm | 20 | ESTIMATED | D | E-044 |
| suspension.front_lower_arm_length | Front lower arm (with ball joint) length | 289 mm | 3 | ESTIMATED | D | E-046 |
| suspension.front_strut_bore | Front strut damper bore | 27 mm | 1 | ESTIMATED | D | E-048 |
| suspension.front_strut_rod_diameter | Front strut piston-rod diameter | 20 mm | 1 | ESTIMATED | D | E-048 |
| suspension.front_wheel_bearing | Front wheel taper bearing (bore x OD x width) | 28 x 57.15 x 17.462 | 0.1 | ESTIMATED | D | E-047 |
| steering.steering_gear_type | Steering gear type (rack-and-pinion / recirculating ball) | rack-and-pinion | - | ESTIMATED | D (B adayı: birden fazla ilan/özet, bağımsızlık doğrulanmadı) | E-039, E-038 |
| steering.power_assisted | Power assisted | yes (hydraulic, belt-driven pump) | - | VERIFIED | A | E-027 |
| steering.turns_lock_to_lock | Steering-wheel turns, lock to lock | - | - | UNKNOWN | - | - |
| steering.tie_rod_length | Tie rod (rot mili) length | 282.5 mm | 1 | ESTIMATED | D | E-045 |
| brakes.front_brake_type | Front brake type (disc / drum) | disc | - | ESTIMATED | D | E-032 |
| brakes.front_disc_diameter | Front disc diameter | 227.5 mm | 1 | ESTIMATED | D (B adayı: birden fazla ilan/özet, bağımsızlık doğrulanmadı) | E-037, E-038 |
| brakes.rear_brake_type | Rear brake type (disc / drum) | drum | - | ESTIMATED | C | E-025 |
| brakes.rear_drum_diameter | Rear drum diameter | 228 mm | 2 | ESTIMATED | D | E-042 |
| brakes.rear_drum_width | Rear drum width | 47.7 mm | 1 | ESTIMATED | D | E-042 |
| brakes.front_disc_thickness | Front disc thickness (new) | 10.8 mm | 0.2 | ESTIMATED | D | E-037 |
| brakes.brake_booster_fitted | Brake booster (servo) fitted | True | - | ESTIMATED | C | E-050 |
| brakes.parking_brake_type | Parking brake type | centre lever, cables to rear drums | - | ESTIMATED | C | E-055, E-042 |
| wheels_tires.tire_size_front | Front tire size and load/speed index | 185/65 R14 | - | ESTIMATED | C | E-028 |
| wheels_tires.tire_size_rear | Rear tire size and load/speed index | 185/65 R14 | - | ESTIMATED | C | E-028 |
| wheels_tires.wheel_rim_diameter | Rim diameter | 14 in | 0.5 | VERIFIED | A | E-017, E-010, E-028 |
| wheels_tires.wheel_rim_width | Rim width | 5.5 in | 0.5 | ESTIMATED | E | E-018 |
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
| lpg_system.kit_type | LPG kit type (venturi mixer or vapour injection) | - | - | UNKNOWN | - | - |
| lpg_system.tank_type | LPG tank type | toroidal (ring) tank in the spare-wheel well | - | VERIFIED | A | E-017, E-022 |
| lpg_system.tank_location | LPG tank location | spare-wheel well at the rear of the luggage floor, near the tailgate sill; underside protrudes below the floor | - | VERIFIED | A | E-017, E-022, E-025 |
| lpg_system.tank_nominal_capacity | LPG tank nominal capacity | 40 L | 1 | ESTIMATED | D | E-017 |
| lpg_system.tank_outer_diameter | LPG tank outer diameter | 600 mm | 30 | ESTIMATED | E | E-018 |
| lpg_system.tank_height | LPG tank height | 180 mm | 20 | ESTIMATED | E | E-018 |
| lpg_system.tank_central_opening_diameter | LPG tank central opening diameter | 130 mm | 40 | ESTIMATED | E | E-019, E-020 |
| lpg_system.tank_wall_thickness | LPG tank wall thickness | 3.0 mm | 1.0 | ESTIMATED | E | E-019 |
| lpg_system.tank_section_shape | LPG tank cross-section model | stadium | - | ESTIMATED | E | E-019 |
| lpg_system.max_fill_fraction | Maximum fill (fill-stop) fraction of water capacity | 80 % | 2 | ESTIMATED | E | E-018, E-020 |
| lpg_system.tank_centre_x | LPG tank centre X (VCS, rearward from front axle) | - | - | UNKNOWN | - | - |
| lpg_system.tank_centre_y | LPG tank centre Y (VCS, right positive) | - | - | UNKNOWN | - | - |
| lpg_system.tank_base_z | LPG tank underside height above ground | - | - | UNKNOWN | - | - |
| lpg_system.multivalve_orientation | Multivalve clock position on the tank | in the central opening, on the inner wall of the tank (ALBIEN multivalve, 12 V solenoid, level gauge) | - | VERIFIED | A | E-022, E-023 |
| lpg_system.filler_location | LPG filler valve location | - | - | UNKNOWN | - | - |
| lpg_system.tank_mounting | Tank mounting (frame, straps, bolts) | bolted through the floor of the spare-wheel well at the tank centre (two brackets in the central opening, two bolt heads visible from below); opening closed by a black cover with two holes | - | VERIFIED | A | E-022, E-025 |
| lpg_system.tank_marking | LPG tank maker and approval marking | maker ATIKER; approval mark 'E7 67R-01 0049401' (UN Regulation No. 67, 01 series) | - | VERIFIED | A | E-022 |
| electrical.system_voltage | System voltage | 12 V | 0.5 | ESTIMATED | C | E-027 |
| electrical.earth_polarity | Earth polarity | - | - | UNKNOWN | - | - |
| electrical.battery_capacity | Battery capacity | 72 Ah | 0 | VERIFIED | A | E-049 |
| electrical.battery_cold_cranking | Battery cold-cranking current | 700 A | 0 | VERIFIED | A | E-049 |
| electrical.battery_case_length | Battery case length | 278 mm | 10 | ESTIMATED | D | E-043, E-049 |
| electrical.battery_case_width | Battery case width | 175 mm | 2 | ESTIMATED | D | E-043, E-049 |
| electrical.battery_case_height | Battery case height | 175 mm | 15 | ESTIMATED | D | E-043, E-049 |
| electrical.alternator_rated_current | Alternator rated current | - | - | UNKNOWN | - | - |
| electrical.headlamp_type | Headlamp type / bulb | H4 halogen | - | ESTIMATED | D | E-036 |
| electrical.fuse_box_location | Fuse box location | - | - | UNKNOWN | - | - |
| body_profile.bumper_protrusion | Bumper face beyond the body face (front and rear) | - | - | UNKNOWN | - | - |
| body_profile.bumper_height | Bumper vertical height | - | - | UNKNOWN | - | - |
| body_profile.bumper_bottom_z | Bumper lower edge above ground | - | - | UNKNOWN | - | - |
| body_profile.sill_z | Body-side (sill) lower edge above ground | - | - | UNKNOWN | - | - |
| body_profile.nose_bottom_z | Front panel lower edge above ground | - | - | UNKNOWN | - | - |
| body_profile.nose_top_z | Hood leading edge above ground | - | - | UNKNOWN | - | - |
| body_profile.cowl_x | Windshield base, X behind the front wheel centre | - | - | UNKNOWN | - | - |
| body_profile.belt_z | Side-window sill (beltline) above ground | - | - | UNKNOWN | - | - |
| body_profile.rear_bottom_z | Rear panel lower edge above ground | - | - | UNKNOWN | - | - |
| body_profile.windshield_top_x | Windshield top edge, X behind the front wheel centre | - | - | UNKNOWN | - | - |
| body_profile.roof_rear_inset | Roof end ahead of the rear body face | - | - | UNKNOWN | - | - |
| body_profile.roof_width | Roof width (side to side, at the roof) | - | - | UNKNOWN | - | - |
| body_profile.b_pillar_x | B-pillar centre, X behind the front wheel centre | - | - | UNKNOWN | - | - |
| body_profile.c_pillar_x | Rear-door rear edge, X behind the front wheel centre | - | - | UNKNOWN | - | - |
| body_profile.mirror_protrusion | Mirror housing beyond the body side | - | - | UNKNOWN | - | - |
