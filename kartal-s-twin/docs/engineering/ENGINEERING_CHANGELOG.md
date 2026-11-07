# Engineering changelog - spec values

Güncelleme: 2026-11-07. Bugün (commit 53af01c sonrası) değişen her spec değeri: eski → yeni. Gerekçe her satırdaki kaynak ve `ENGINEERING_DECISIONS.md` (D-037..D-040). Genel değişiklik geçmişi `CHANGELOG.md`.

| Anahtar | Eski değer / durum | Yeni değer / durum / güven | Kaynak | Not |
|---|---|---|---|---|
| dimensions.ground_clearance_min | - / UNKNOWN / NONE | 120 mm / ESTIMATED / LOW | E-052 | Fiat 131 Panorama figure; Kartal and this car (LPG tank in the spare-wheel well protrudes below the floor, E-025) may differ. Measure. |
| dimensions.turning_circle_kerb | - / UNKNOWN / NONE | 10300 mm / ESTIMATED / LOW | E-038 | Fiat 131 Panorama figure; kerb/wall definition not stated. |
| engine.ignition_type | - / UNKNOWN / NONE | electronic (breakerless) module / ESTIMATED / LOW | E-051 | Module-like unit on the LH inner wing (photo). Listings sell both breaker-point and module distributors for the family; distributor not visible. |
| engine.radiator_core_width | (yok, yeni parametre) | 470 mm / ESTIMATED / LOW | E-041 | Aftermarket KALE 0106092AL for M131 1.6 (2-row aluminium, plastic tanks). |
| engine.radiator_core_height | (yok, yeni parametre) | 292 mm / ESTIMATED / LOW | E-041 | E-041 |
| engine.radiator_core_depth | (yok, yeni parametre) | 32 mm / ESTIMATED / LOW | E-041 | 32 mm (one listing 34 mm). |
| suspension.rear_damper_length_compressed | (yok, yeni parametre) | 337 mm / ESTIMATED / LOW | E-044 | KYB 343142, Fiat 131 saloon application; estate may differ. |
| suspension.rear_damper_length_extended | (yok, yeni parametre) | 527 mm / ESTIMATED / LOW | E-044 | KYB 343142 (stroke 190 mm). |
| suspension.front_lower_arm_length | (yok, yeni parametre) | 289 mm / ESTIMATED / LOW | E-046 | AYD 00016 listing; reference points of the length not stated. |
| suspension.front_strut_bore | (yok, yeni parametre) | 27 mm / ESTIMATED / LOW | E-048 | Monroe 11002, Fiat 131 saloon. |
| suspension.front_strut_rod_diameter | (yok, yeni parametre) | 20 mm / ESTIMATED / LOW | E-048 | Monroe 11002. |
| suspension.front_wheel_bearing | (yok, yeni parametre) | 28 x 57.15 x 17.462 / ESTIMATED / LOW | E-047 | SKF 639297/Q, J15585/J15520. |
| steering.steering_gear_type | - / UNKNOWN / NONE | rack-and-pinion / ESTIMATED / LOW | E-039, E-038 | Mechanical rack for the family (E-039); VEH-01 has a belt-driven power-steering pump (E-027), so assisted rack likely on this car. |
| steering.tie_rod_length | (yok, yeni parametre) | 282.5 mm / ESTIMATED / LOW | E-045 | 282-283 mm (two listings), M14x1.5; mechanical-steering part, power-steering cars may differ. |
| brakes.front_disc_diameter | - / UNKNOWN / NONE | 227.5 mm / ESTIMATED / LOW | E-037, E-038 | Solid disc, 10.8 mm thick (min 9 mm), OEM 4208311; listed for cars up to MY2000 (E-037). Measure the disc to confirm. |
| brakes.rear_drum_diameter | - / UNKNOWN / NONE | 228 mm / ESTIMATED / LOW | E-042 | Fiat 131 1.6 rear drum (Brembo catalogue), max 230 mm; Tofaş OEM 85015914 listings give no size. |
| brakes.rear_drum_width | (yok, yeni parametre) | 47.7 mm / ESTIMATED / LOW | E-042 | Fiat 131 1.6 (Brembo catalogue). |
| brakes.front_disc_thickness | (yok, yeni parametre) | 10.8 mm / ESTIMATED / LOW | E-037 | Minimum 9 mm (E-037). |
| brakes.brake_booster_fitted | - / UNKNOWN / NONE | True / ESTIMATED / MEDIUM | E-050 | Round unit behind the master cylinder at the LH bulkhead (photo interpretation). |
| brakes.parking_brake_type | - / UNKNOWN / NONE | centre lever, cables to rear drums / ESTIMATED / MEDIUM | E-055, E-042 | Lever seen in the interior photo; cables inferred. |
| wheels_tires.wheel_offset_et | - / UNKNOWN / NONE | 29 mm / ESTIMATED / LOW | E-053 | Fiat 131 4x98 wheels (single source); VEH-01 black steel 14 in rims not checked. |
| wheels_tires.wheel_centre_bore | - / UNKNOWN / NONE | 58.1 mm / ESTIMATED / LOW | E-053 | Generic Fiat 4x98 hub bore; matches E-053. |
| electrical.battery_capacity | - / UNKNOWN / NONE | 72 Ah / VERIFIED / HIGH | E-049 | Label of the fitted battery (İnci Formul A Taurus). The original factory battery is not known. |
| electrical.battery_cold_cranking | - / UNKNOWN / NONE | 700 A / VERIFIED / HIGH | E-049 | 700 A (EN) per label. |
| electrical.battery_case_length | (yok, yeni parametre) | 278 mm / ESTIMATED / LOW | E-043, E-049 | 72 Ah case (E-049): 278 x 175 x 175 is the common 72 Ah size (Exide FA722, Tudor TA722); İnci's own 72 Ah sheet not found. |
| electrical.battery_case_width | (yok, yeni parametre) | 175 mm / ESTIMATED / LOW | E-043, E-049 | Same 175 mm for 60 and 72 Ah cases. |
| electrical.battery_case_height | (yok, yeni parametre) | 175 mm / ESTIMATED / LOW | E-043, E-049 | Common 72 Ah case height; İnci 60 Ah is 190 mm. |
