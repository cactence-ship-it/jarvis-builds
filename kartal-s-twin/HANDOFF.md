# HANDOFF - Kartal S dijital ikiz (VEH-01)

> Bu dosya her aşamada güncellenir. Oturum yarıda kesilirse buradan devam edin.

**Son güncelleme:** 2026-11-02 · **Branch:** `ccr-b5d82c24-huyj0b` · **PR:** #1 (açık, merge edilmedi)
**Son doğrulanmış commit:** `bash kartal-s-twin/scripts/checkpoint.sh --verify` komutunun çıktısına bakın
(aşağıdaki tabloda her aşamanın SHA'sı var).

## Yeni oturumda devam etmek için
1. `git checkout ccr-b5d82c24-huyj0b` (PR #1 merge edilmediyse)
2. `bash kartal-s-twin/scripts/setup_env.sh`
3. `kartal-s-twin/CLAUDE.md` ve bu dosyayı okuyun, "Sıradaki görevler" listesinden devam edin.

## Aşamalar (2. oturum)
| # | Aşama | Durum | Commit |
|---|---|---|---|
| 1 | Literatür kanıtları (E-007..E-010) + spec ESTIMATED değerleri | TAMAM | 183c608 |
| 1b | Test kapısı: checkpoint testler geçmezse commit etmiyor; sonuçlar test-results/latest.txt | TAMAM | 9b76991 |
| 2 | CAD hattı: Resolver (köken takibi), GLB yazıcı, build/export/doğrulama, 24 PLACEHOLDER parça, önizleme render | TAMAM | e27266d |
| 3 | Android 3D görüntüleyici (tek dosya, GLB gömülü), headless Chromium testi; yayın: https://claude.ai/artifact/7hGubrkeaHVUZSJ4AeGchk | TAMAM | 0877612 |
| 4 | Kapı/kaput/bagaj kapağı ayrı bileşen (panel boşluklu), 30 parça; smoke test port hatası düzeltildi | TAMAM | 8f0119a |
| 5 | Ölçüm rehberi docs/OLCUM_REHBERI.md, senkron testi | TAMAM | 04f0f57 |
| 6 | Ölçüm girişi: tools/record_measurement.py, body_profile spec alanları (15), D-015; 31 ölçü kodu | TAMAM | c2743e3 |
| 7 | Teslim paketi (scripts/package_delivery.sh, ZIP gönderildi) + eski arşiv analiz aracı (tools/analyze_legacy.py) | TAMAM | (bu commit) |

## Sayılar (son durum)
- Spec 111 parametre: 0 VERIFIED / 17 ESTIMATED / 94 UNKNOWN. Kanıt: E-001..E-010.
- 143 bileşenin 30'u modellendi (hepsi görsel PLACEHOLDER). CAD/mekanik temsil yok.
- Testler: 48/48 geçti -> `test-results/latest.txt`; görüntüleyici tarayıcı testi -> `test-results/viewer_smoke.txt`.
- Görüntüleyici: https://claude.ai/artifact/7hGubrkeaHVUZSJ4AeGchk (yeniden yayın: `python tools/package_viewer.py` + aynı dosya yolu ile yayınla).

## Sıradaki görevler (öncelik sırasıyla)
1. **Sahip ölçüleri gelirse:** `python tools/record_measurement.py --state "..." --tol 5 M01=... ` ->
   `tools/twin.py validate` -> `build` -> `sync-inventory` -> `measurement_guide.py` -> testler -> checkpoint -> görüntüleyiciyi yeniden yayınla.
2. **Fotoğraf/ZIP gelirse:** `python3 tools/ingest_refs.py <dosyalar>` (public depo: orijinaller git'e girmez),
   her foto için EVIDENCE_REGISTER'a E-0xx satırı, `python3 tools/analyze_legacy.py refs/original/R-xxxx_Kartal_S_Studyo.zip`,
   sonra Faz 2: fotoğraf-bileşen eşlemesi, kaporta profilini fotoğraftan çıkarma (ölçek: dingil mesafesi 2490 ±10).
3. Kaporta gerçekçiliği (kanıt gelmeden yapılabilecekler, hepsi PLACEHOLDER kalır): tavan/cam kenarı yuvarlatmaları,
   tampon köşe sarması, jant göbeği detayı, kapı kolları (EXT-006..009), sileceği (EXT-015).
4. İç mekan (Faz 5) için sadece fotoğraf geldikten sonra; motor/şasi/süspansiyon kanıt olmadan MODELLENMEZ (kural).
5. PR #1 kullanıcı tarafından merge edilmedi; yeni oturum bu branch'ten devam etmeli.

## Bilinen eksikler / engeller
- Sahip fotoğrafları (9 adet) ve `Kartal_S_Studyo.zip` hâlâ yüklenmedi -> Faz 2 başlayamıyor.
- Depo PUBLIC: orijinaller git'e girmez (D-012). Özel depolama kararı bekleniyor (U-009).
- İz genişlikleri, çıkıntılar, kaporta profil ölçüleri hiçbir kaynakta yok -> sadece PLACEHOLDER.
