# Unknown values register

Güncelleme: 2026-11-07. Spec'te UNKNOWN kalan her değer, neden bulunamadığı ve çözüm yolu. Mühendislik belirsizlikleri (çakışmalar vb.) ayrıca `UNCERTAINTY_REGISTER.md` içinde.

| Anahtar | Ad | Sınıf | Neden bulunamadı | Çözüm yolu |
|---|---|---|---|---|
| dimensions.overall_width_mirrors | Overall width incl. mirrors | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Plumb lines at the mirror housings |
| dimensions.overall_height_roof_rails | Overall height incl. roof rails (if fitted) | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Straight-edge across the rails to the ground |
| dimensions.front_overhang | Front overhang (front axle to front extremity) | MEASURE_REQUIRED | Not published. Sum of overhangs = length - wheelbase = 1906 mm (4396) or 1871 mm (4361); the split needs a measurement. | Plumb line at the front extremity to the front hub centre |
| dimensions.rear_overhang | Rear overhang (rear axle to rear extremity) | MEASURE_REQUIRED | See front_overhang: only the sum is derivable from published length and wheelbase. | Plumb line at the rear extremity to the rear hub centre |
| dimensions.wheel_centre_to_arch_fl | Hub centre to wheel-arch lip, front left | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Vertical tape, hub centre to arch edge (records ride height) |
| dimensions.wheel_centre_to_arch_fr | Hub centre to wheel-arch lip, front right | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Vertical tape, hub centre to arch edge |
| dimensions.wheel_centre_to_arch_rl | Hub centre to wheel-arch lip, rear left | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Vertical tape, hub centre to arch edge |
| dimensions.wheel_centre_to_arch_rr | Hub centre to wheel-arch lip, rear right | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Vertical tape, hub centre to arch edge |
| body.body_construction | Body construction (unibody / separate frame) | UNKNOWN | Araştırıldı; birincil kaynak bulunamadı. | Underbody photos |
| body.cargo_floor_length_seat_up | Cargo floor length, rear seat up | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Tape at floor level: tailgate seal to rear-seat backrest |
| body.cargo_floor_length_seat_folded | Cargo floor length, rear seat folded | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Tape at floor level: tailgate seal to front-seat backs |
| body.cargo_width_between_arches | Cargo width between wheel arches | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Tape across the narrowest point |
| body.tailgate_opening_width | Tailgate opening width | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Tape across the opening at its narrowest point |
| body.tailgate_opening_height | Tailgate opening height | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Tape from sill to header at the centre |
| body.load_sill_height | Load sill height | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Ground to top of the rear sill |
| interior.steering_wheel_diameter | Steering wheel outer diameter | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Tape across the rim |
| mass.axle_load_front_measured | Front axle load, measured | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Weighbridge at the reference state |
| mass.axle_load_rear_measured | Rear axle load, measured | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Weighbridge at the reference state |
| engine.engine_code | Engine type code | MEASURE_REQUIRED | Candidates: 131.D1.016 (carburettor, Doğan/Kartal 1.6 S/SL/SLX 1992-2002, wikipedia table E-040) or 131.F3.016 (i.e. cat 1998-2002). VEH-01 is a 1997 carburettor car (air cleaner on a carburettor, E-027), so 131.D1.016 is the only candidate that fits; still UNKNOWN until the block stamping is read. | Engine-number stamping photo / documents |
| suspension.rear_antiroll_bar_fitted | Rear anti-roll bar fitted | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Underbody photo |
| steering.turns_lock_to_lock | Steering-wheel turns, lock to lock | UNKNOWN | Araştırıldı; birincil kaynak bulunamadı. | Count with a tape mark on the wheel rim |
| lpg_system.kit_type | LPG kit type (venturi mixer or vapour injection) | MEASURE_REQUIRED | No mixer or injector rail visible in the engine-bay photos (E-027); the air cleaner covers the carburettor. A round coolant-heated unit near the bulkhead may be the vaporiser (unconfirmed). | Engine-bay photo: mixer in the air intake vs injector rail |
| lpg_system.tank_centre_x | LPG tank centre X (VCS, rearward from front axle) | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Tape from the rear wheel centre to the tank centre, plus wheelbase |
| lpg_system.tank_centre_y | LPG tank centre Y (VCS, right positive) | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Tape from the body centre line |
| lpg_system.tank_base_z | LPG tank underside height above ground | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Tape from the ground to the tank bottom (or floor of the well) |
| lpg_system.filler_location | LPG filler valve location | MEASURE_REQUIRED | Not visible on the exterior photos (E-026): no separate LPG filler on either side or the bumper in those views. Ask the owner or photograph under the fuel flap and the rear bumper. | Exterior photo (bumper / fuel flap / body side) |
| electrical.earth_polarity | Earth polarity | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Battery terminal photo |
| electrical.alternator_rated_current | Alternator rated current | MEASURE_REQUIRED | Listed variants 55 / 65 / 85 A (E-039); read the alternator label. | Alternator label photo |
| electrical.fuse_box_location | Fuse box location | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Photo |
| body_profile.bumper_protrusion | Bumper face beyond the body face (front and rear) | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.bumper_height | Bumper vertical height | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.bumper_bottom_z | Bumper lower edge above ground | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.sill_z | Body-side (sill) lower edge above ground | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.nose_bottom_z | Front panel lower edge above ground | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.nose_top_z | Hood leading edge above ground | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.cowl_x | Windshield base, X behind the front wheel centre | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.belt_z | Side-window sill (beltline) above ground | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.rear_bottom_z | Rear panel lower edge above ground | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.windshield_top_x | Windshield top edge, X behind the front wheel centre | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.roof_rear_inset | Roof end ahead of the rear body face | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.roof_width | Roof width (side to side, at the roof) | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.b_pillar_x | B-pillar centre, X behind the front wheel centre | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.c_pillar_x | Rear-door rear edge, X behind the front wheel centre | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.mirror_protrusion | Mirror housing beyond the body side | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |

### Spec dışında kalan, owner listesindeki maddeler

| Madde | Durum | Not |
|---|---|---|
| Bagaj tabanının iç derinliği | MEASURE_REQUIRED | Spec'te parametre yok; cargo_floor_length ile birlikte ölçülecek. |
| Arka yan gövde çizgisinin konumu | MEASURE_REQUIRED | Spec'te `body_profile.c_pillar_x` ve `roof_rear_inset` var (ESTIMATED/UNKNOWN); ayrı çizgi parametresi yok. |
| Marş motoru gücü | UNKNOWN | Spec'te parametre yok; marş akımı için akü EN değeri (700 A, E-049) marş motorunun çektiği akım değildir. |
