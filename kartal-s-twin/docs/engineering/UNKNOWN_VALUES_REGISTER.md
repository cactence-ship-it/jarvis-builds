# Unknown values register

Güncelleme: 2026-11-07. Spec'te UNKNOWN kalan her değer, neden bulunamadığı ve çözüm yolu. Mühendislik belirsizlikleri (çakışmalar vb.) ayrıca `UNCERTAINTY_REGISTER.md` içinde.

| Anahtar | Ad | Sınıf | Neden bulunamadı | Çözüm yolu |
|---|---|---|---|---|

### Spec dışında kalan, owner listesindeki maddeler

| Madde | Durum | Not |
|---|---|---|
| Bagaj tabanının iç derinliği | MEASURE_REQUIRED | Spec'te parametre yok; cargo_floor_length ile birlikte ölçülecek. |
| Arka yan gövde çizgisinin konumu | MEASURE_REQUIRED | Spec'te `body_profile.c_pillar_x` ve `roof_rear_inset` var (ESTIMATED/UNKNOWN); ayrı çizgi parametresi yok. |
| Marş motoru gücü | UNKNOWN | Spec'te parametre yok; marş akımı için akü EN değeri (700 A, E-049) marş motorunun çektiği akım değildir. |
