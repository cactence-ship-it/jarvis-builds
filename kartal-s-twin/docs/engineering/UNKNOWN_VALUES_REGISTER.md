# Unknown values register

Güncelleme: 2026-11-07. Spec'te UNKNOWN kalan her değer, neden bulunamadığı ve çözüm yolu. Mühendislik belirsizlikleri (çakışmalar vb.) ayrıca `UNCERTAINTY_REGISTER.md` içinde.

| Anahtar | Ad | Sınıf | Neden bulunamadı | Çözüm yolu |
|---|---|---|---|---|
| dimensions.overall_width_mirrors | Overall width incl. mirrors | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Plumb lines at the mirror housings |
| dimensions.overall_height_roof_rails | Overall height incl. roof rails (if fitted) | MEASURE_REQUIRED | Manual gives 1496 mm unladen without saying whether the rails are included (E-058/E-059). Measure over the rails. | Straight-edge across the rails to the ground |
| dimensions.wheel_centre_to_arch_fl | Hub centre to wheel-arch lip, front left | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Vertical tape, hub centre to arch edge (records ride height) |
| dimensions.wheel_centre_to_arch_fr | Hub centre to wheel-arch lip, front right | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Vertical tape, hub centre to arch edge |
| dimensions.wheel_centre_to_arch_rl | Hub centre to wheel-arch lip, rear left | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Vertical tape, hub centre to arch edge |
| dimensions.wheel_centre_to_arch_rr | Hub centre to wheel-arch lip, rear right | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Vertical tape, hub centre to arch edge |
| body.cargo_floor_length_seat_folded | Cargo floor length, rear seat folded | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Tape at floor level: tailgate seal to front-seat backs |
| body.tailgate_opening_width | Tailgate opening width | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Tape across the opening at its narrowest point |
| body.tailgate_opening_height | Tailgate opening height | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Tape from sill to header at the centre |
| body.load_sill_height | Load sill height | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Ground to top of the rear sill |
| interior.steering_wheel_diameter | Steering wheel outer diameter | MEASURE_REQUIRED | Factory: Fiat/SEAT 131 400 mm, Tofaş new body ~380 mm (listing) per E-059. VEH-01 has an aftermarket three-spoke wheel: measure it. | Tape across the rim |
| mass.axle_load_front_measured | Front axle load, measured | MEASURE_REQUIRED | Reference only: Fiat 131 CL max front axle load 670 kg (KFT sheet via E-059); SEAT 131 weight split 52.5 / 47.5. A weighbridge reading of VEH-01 is needed. | Weighbridge at the reference state |
| mass.axle_load_rear_measured | Rear axle load, measured | MEASURE_REQUIRED | Reference only: Fiat 131 CL max rear axle load 800 kg (E-059). | Weighbridge at the reference state |
| lpg_system.tank_centre_x | LPG tank centre X (VCS, rearward from front axle) | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Tape from the rear wheel centre to the tank centre, plus wheelbase |
| lpg_system.tank_centre_y | LPG tank centre Y (VCS, right positive) | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Tape from the body centre line |
| lpg_system.tank_base_z | LPG tank underside height above ground | MEASURE_REQUIRED | Yayımlanmış kaynakta yok (arandı: üretici özetleri, Fiat 131 sayfaları, yedek parça ilanları); araca özgü değer. | Tape from the ground to the tank bottom (or floor of the well) |
| lpg_system.filler_location | LPG filler valve location | MEASURE_REQUIRED | Typical 1990s-2000s: under the rear bumper (opposite the exhaust) or in the bumper; post-2017 inspection rules require it outside the bumper underside (E-059). VEH-01 not photographed. | Exterior photo (bumper / fuel flap / body side) |
| body_profile.bumper_protrusion | Bumper face beyond the body face (front and rear) | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.bumper_height | Bumper vertical height | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.bumper_bottom_z | Bumper lower edge above ground | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.sill_z | Body-side (sill) lower edge above ground | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.nose_bottom_z | Front panel lower edge above ground | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.nose_top_z | Hood leading edge above ground | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.belt_z | Side-window sill (beltline) above ground | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.rear_bottom_z | Rear panel lower edge above ground | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.roof_rear_inset | Roof end ahead of the rear body face | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.roof_width | Roof width (side to side, at the roof) | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |
| body_profile.mirror_protrusion | Mirror housing beyond the body side | MEASURE_REQUIRED | Placeholder in specs/placeholder_assumptions.yaml until measured | Owner tape measurement per docs/OLCUM_REHBERI.md |

### Spec dışında kalan, owner listesindeki maddeler

| Madde | Durum | Not |
|---|---|---|
| Bagaj tabanının iç derinliği | MEASURE_REQUIRED | Spec'te parametre yok; cargo_floor_length ile birlikte ölçülecek. |
| Arka yan gövde çizgisinin konumu | MEASURE_REQUIRED | Spec'te `body_profile.c_pillar_x` ve `roof_rear_inset` var (ESTIMATED/UNKNOWN); ayrı çizgi parametresi yok. |
| Marş motoru gücü | UNKNOWN | Spec'te parametre yok; marş akımı için akü EN değeri (700 A, E-049) marş motorunun çektiği akım değildir. |
