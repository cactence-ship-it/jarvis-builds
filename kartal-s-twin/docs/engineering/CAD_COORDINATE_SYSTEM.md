# CAD coordinate system and datums

Güncelleme: 2026-11-08 (fabrika kullanım kılavuzu E-058 ile). Tanım karar **D-003**'tür (değişmedi); bu belge datum tablosunu toplar.

## Eksenler (Vehicle Coordinate System, VCS)
- **X**: boyuna eksen, **arkaya doğru pozitif**. X = 0 ön aks (ön teker merkezi) çizgisi.
- **Y**: enine eksen, **sağa doğru pozitif** (LH = -Y). Y = 0 aracın simetri düzlemi.
- **Z**: dikey, yukarı pozitif. Z = 0 referans durumda zemin.
- Birim mm. glTF/telefon görüntüleyicisine dönüşüm: (x, y, z)_glTF = (-Y, Z, -X) / 1000 (metre); glTF'te +Z aracın önü.

Owner prompt'undaki eksen tanımı (X boyuna, Y enine, Z dikey, X=0 ön aks, Y=0 simetri, Z=0 zemin) bununla aynıdır; tek fark
X'in yönüdür (arkaya pozitif) ve proje başından beri böyle olduğu için değiştirilmedi.

## Datum tablosu

| Datum | X | Y | Z | Durum | Kaynak |
|---|---|---|---|---|---|
| Araç ön ucu | -765 | 0 | - | VERIFIED (ön çıkıntı 765, kılavuz s.95) | E-058 |
| Ön aks merkezi (FL/FR teker merkezi) | 0 | ∓693 | ≈286 | X tanım; Y VERIFIED (iz 1386, kılavuz); Z PLACEHOLDER (lastik yarıçapı, yük altında değil) | E-058, E-028 |
| Arka aks merkezi (RL/RR) | 2490 | ∓663,5 | ≈286 | X VERIFIED nominal (dingil 2490, kılavuz); Y VERIFIED (iz 1327) | E-058 |
| Araç arka ucu | 3631 | 0 | - | VERIFIED (arka çıkıntı 1141; toplam boy 4396) | E-058 |
| Motor bloğu ön yüzü | -150 | 0 | - | PLACEHOLDER (`pkg_engine_x0`) | tahmin |
| Motor bloğu arka yüzü / volan | 320 | 0 | - | PLACEHOLDER (blok 470 mm) | tahmin |
| Krank mili ekseni | -150…320 | 0 | 300 | PLACEHOLDER (`pkg_crank_z`); **U-017**: karter zemine ~70 mm, gerçekçi değil | tahmin |
| Şanzıman (çan + kutu) | 320…980 | 0 | ≈300 | PLACEHOLDER (`pkg_gearbox_len` 660); 5 vites ESTIMATED (E-031) | tahmin |
| Şanzıman çıkışı / kardan başlangıcı | ≈980 | 0 | ≈300 | PLACEHOLDER | tahmin |
| Diferansiyel (arka aks ortası) | 2490 | 0 | ≈286 | X ESTIMATED; konum yapısal (sabit arka aks, E-025/E-032) | E-025, E-032 |
| Radyatör çekirdeği | -640 | 0 | 304…596 | X PLACEHOLDER; çekirdek boyu ESTIMATED LOW (470 × 292 × 32) | E-041 |
| Ön bölme (motor bölmesi arka duvarı) | 790 | - | - | PLACEHOLDER | tahmin |
| LPG simit tank merkezi | ≈3150 | ≈0 | taban ≈350 | PLACEHOLDER (stepne yuvası, fotoğraf R-0007); `lpg_system.tank_centre_*` UNKNOWN | E-022, E-025 |

## Bilinmeyenler
- Motor ve şanzıman eğim açısı: UNKNOWN (veri yok); model yatay çiziliyor.
- Kardan açısı, diferansiyel pinyon yüksekliği: UNKNOWN.
- Teker merkezi yüksekliği yük altında: UNKNOWN (statik çökme kanıtı yok).
Bu değerler kesinmiş gibi kaydedilmedi; mühendislik CAD'i (D-016) PLACEHOLDER değerleri reddeder.
