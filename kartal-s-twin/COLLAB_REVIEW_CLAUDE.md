# COLLAB_REVIEW_CLAUDE — Bağımsız mühendislik denetimi (Claude)

**Tarih:** 2026-11-02 · **Proje:** Tofaş Kartal S (1997) dijital ikizi, VEH-01 · **Depo:** `cactence-ship-it/jarvis-builds` (PUBLIC)
**Branch:** `ccr-b5d82c24-huyj0b` · **Denetim öncesi HEAD:** `f44a5c9` · **Bu raporu içeren commit:** HANDOFF.md'deki AUTO-CHECKPOINT kaydı / `git log -1`

Bu belgedeki her sayının yanında kaynağı (dosya veya komut) yazılıdır. Doğrulanmamış hiçbir şey "doğrulandı" diye yazılmamıştır.

---

## A. Mevcut durum (kanıtlı)

| # | Soru | Değer | Kaynak / komut |
|---|---|---|---|
| 1 | Toplam bileşen | **143** (17 montaj) | `assembly/vehicle_master.yaml`; `kartal_twin.inventory.iter_components` |
| 2 | Görsel modeli olan | **35**, hepsi `visual: PLACEHOLDER` | aynı YAML, `geometry.visual` sayımı |
| 3 | Gerçek CAD geometrisi olan | **4** (WHL-001..004 lastik tasarım zarfı), `cad: DRAFT` | `geometry.cad` sayımı; `build/manifest.json` → `checks.cad` |
| 4 | Mekanik modellenmiş | **0** | `geometry.mechanical` = NONE (143/143) |
| 5 | Parametre durumu | 111 parametre: **0 VERIFIED / 27 ESTIMATED / 84 UNKNOWN** | `python tools/twin.py validate` |
| 6 | Testler | **55/55 geçti**, başarısız 0 | `bash scripts/run_tests.sh` → `test-results/latest.txt` |
| 7 | Yeniden açılıp doğrulanan dosyalar | Bkz. bölüm D (STEP, STL, GLB, 5 CAD STEP) | `src/kartal_twin/pipeline.py` (`export_all`, `export_cad`) |
| 8 | Son commit / testin koştuğu commit | Denetim öncesi `f44a5c9`; bu turun testleri `f44a5c9` tabanındaki çalışma kopyasında koştu. Kesin değer `test-results/latest.txt` başlığında yazar. | `git rev-parse HEAD`, `head -1 test-results/latest.txt` |
| 9 | PR #1 | **Açık, merge edilmedi.** Base `main` = `d63aa68`. İnceleme yorumu yok, CI check run yok, çakışma yok. | GitHub API `pull_request_read` (get / get_review_comments / get_check_runs) |
| 10 | Faz 2 engelleri | Sahip fotoğrafları (9 adet) ve `Kartal_S_Studyo.zip` **bu ortamda yok**: `/mnt/user-data/uploads` boş. `/tmp` altında bulunan 24 adet `Kartal_S_Studyo.zip`, `tests/test_legacy.py`'nin ürettiği **sentetik test dosyalarıydı** (638 ve 62 bayt). Bunlar gerçek arşiv değil; sızıntı bu turda giderildi. | `ls /mnt/user-data/uploads`, `find / -name Kartal_S_Studyo.zip` |

**Kaynak 3D model (bölüm 3 isteği):** `Kartal_S_Studyo.zip` / `kartal.json` **incelenemedi**, çünkü dosya bu ortama hiç yüklenmedi. Bu yüzden mesh/node sayısı, vertex/üçgen sayısı, parça adları, indeks bütünlüğü, ölçek ve iç parça varlığı hakkında **hiçbir iddiada bulunmuyorum**. Daha önce konuşmada geçen "~47 nesne" bilgisi sahibin aktardığı ve doğrulanmamış bir bilgidir (E-002, NOT_RECEIVED). Arşiv geldiğinde `python3 tools/analyze_legacy.py <zip>` bu soruların tamamını tek komutla raporlayacak. Araç yalnızca sentetik arşivlerde test edildi.

**Görsel model ne değildir:** 35 görsel parça, yayınlanmış ana ölçülere (ESTIMATED) oturtulmuş bir *yer tutucu zarftır*. Kaporta profili, kapı biçimleri, lamba konumları ve renk `specs/placeholder_assumptions.yaml` içindeki varsayımlardan gelir; gerçek araçtan değil.

---

## B. Tespit edilen hatalar, riskler ve tutarsızlıklar

**Bu turda bulunup düzeltilenler (testle kanıtlı):**
1. **Manifestte bayat dosyalar:** `manifest.json`, `build/` altını tarayıp eski teslim paketi kopyalarını (`delivery/stage/*`) ve önceki başarısız çalıştırmadan kalan bir CAD STEP'i güncel çıktı gibi listeliyordu. Aynı dosya için iki farklı SHA görünüyordu. Düzeltme: her çalıştırmada eski çıktılar temizleniyor, manifest yalnızca o çalıştırmanın yazdığı dosyaları listeliyor. Test: `Reproducibility.test_manifest_lists_only_this_runs_outputs`.
2. **STEP SHA'ları tekrarlanamıyordu:** STEP başlığına derleme saati yazılıyordu. Artık sabit zaman damgası kullanılıyor. Kalan sınırlama:
   - renkli görsel `vehicle.step`, OCCT renk/stil kayıtlarını değişken sırayla yazdığı için bayt bayt aynı değil; geometrik olarak (katı sayısı, hacim) aynı;
   - CAD STEP'ler ve GLB ayrı süreçlerde bayt bayt aynı;
   - aynı süreç içinde OCCT montaj sayaçları (`NEXT_ASSEMBLY_USAGE_OCCURRENCE`) artıyor.
3. **Test geçici dosya sızıntısı:** `test_legacy.py` geçici dizinlerini silmiyordu (24 dosya). Düzeltildi; test sonrası 0 dosya kalıyor.
4. **Revizyon tutarsızlığı:** spec ve envanterdeki `revision` alanları 0.1.0'da kalmıştı (CHANGELOG 0.4.0). İkisi de 0.5.0 yapıldı.
5. **Bayat durum belgesi:** `PROJECT_STATUS.md` 48/48 test ve spec 0.3.0 yazıyordu; güncellendi.

**Daha önce bulunup düzeltilenler (kayıtlı):**
6. Commit `183c608`, 2 başarısız testle push edildi; `9b76991`'de düzeltildi. Artık `checkpoint.sh` test geçmezse commit yapmıyor.
7. Görüntüleyici tarayıcı testi bir süre eski bir sunucuya karşı çalıştı; artık rastgele port kullanıyor.

**Açık riskler (düzeltilmedi):**
8. **Kanıt kalitesi zayıf:** 27 ESTIMATED değerin hepsi toplayıcı siteler ve sahibin girdiği ilanlardan, **arama motoru özetleri** üzerinden alındı. Kaynak sayfaların kendisi bu ortamdan okunamadı: auto-data.net DNS seviyesinde engelli; bu turda denendi ve başarısız oldu. Çelişkiler kayıtlı:
   - uzunluk 4396 ve 4360 mm;
   - lastik 175/70 R14 ve 185/70 R14.
9. **CAD lastik zarfı düşük güvenli girdiye bağlı:** lastik ebadı LOW güvenle girilmiş. 185/70 R14 çıkarsa dış çap 614,6 mm olur (+14,0); jant R13 çıkarsa 575,2 mm olur (−25,4). CAD zarfı DRAFT, VALIDATED değil.
10. **Görsel ve CAD temsilleri Z'de 12 mm farklı:** görsel tekerlek, varsayım olan 12 mm statik çökme ile yere batık; CAD zarfı yüksüz konumda. Bu bilinçli bir ayrım (D-006/D-016), ama karıştırılmamalı.
11. **Girişim/boşluk kontrolü yok:** direktifteki "assembly interference" doğrulaması henüz uygulanmadı. Lastik zarfı ile çamurluk boşluğu ölçülmüyor, çünkü kaporta zaten yer tutucu.
12. **CI yok:** testler yalnızca oturum içinde koşuyor; GitHub'da bağımsız bir CI çalıştırması yok.
13. **Gizlilik taraması kalıp tabanlı:** plaka regex'i büyük harf ve standart formatı arıyor; küçük harf veya ayraçsız yazımları kaçırabilir. Fotoğraflar ve arşivler dosya uzantısından engelleniyor.
14. **Görsel gövde kaba:** kapılar 45 mm'lik dilimler, alt gövdede yan eğim (tumblehome) yok, camlar düz. Gerçekçilik sınırlı.
15. **Küçük kod kusuru:** `twin.py` çıktısı `| head` ile kesilince `BrokenPipeError` veriyor. Kozmetik; dosyalar önceden yazıldığı için veri kaybı yok.

---

## C. Bağımsız mühendislik çözümü

**Mimari (mevcut, kodda):** Python + build123d 0.13 / OpenCascade (OCP 8.0.1.1), hash'lenmiş bağımlılıklar. Tek doğruluk kaynakları:
- değerler: `specs/kartal_s_1997.yaml`;
- yapı: `assembly/vehicle_master.yaml`.

Her geometri değeri `Resolver` üzerinden okunur ve kaynağı kaydedilir. Statü bu kayıttan mekanik olarak türetilir: varsayım varsa PLACEHOLDER; yalnız ESTIMATED veya VERIFIED girdi varsa DRAFT; VALIDATED hiçbir zaman otomatik değildir. CAD temsilinde varsayım okumak kod seviyesinde yasaktır (D-016).

**Koordinat sistemi (D-003):** VCS sağ el kuralı. X boylamsal, pozitif yön geriye; Y yanal, pozitif yön sağa; Z yukarı. Orijin: ön teker merkez çizgisi, araç simetri düzlemi ve referans durumdaki zemin. glTF dönüşümü: (x, y, z) = (−Y, Z, −X)·0,001 m. Bu bir dönmedir (det = +1); test edildi.

**Ölçek kalibrasyonu:** birincil ölçek sahibin şerit metre ölçüleri (D-015, `record_measurement.py`). Fotoğraflarda ölçek dingil mesafesinden alınır, kamera eğimi zemin çizgisiyle giderilir (`photo_scale.py`). Fotoğraftan çıkan değerler en fazla ESTIMATED olur. Tolerans piksel hatası, %2 perspektif payı ve dingil mesafesi toleransının birleşimidir.

**Fotoğraftan ölçü yöntemi:**
1. Aracın orta ekseninden, 6–8 m uzaktan, telefon zemine paralel tutularak çekilmiş yan/ön/arka fotoğraflar.
2. Teker merkezleri ve zemin noktaları işaretlenir.
3. `photo_scale.py` ile mm'ye çevrilir.
4. Şerit metreyle çapraz kontrol yapılır: aynı nokta iki yöntemle ölçülür ve fark tolerans içinde olmalıdır.

**Kaynak mesh'ten CAD'e dönüşüm (arşiv gelince):** üçgen mesh'leri doğrudan B-rep'e çevirmek önerilmiyor; sonuç düzenlenemeyen bir yüzey yığını olur. Yöntem:
1. **Ölçek ve hizalama:** mesh analiz edilir (`analyze_legacy.py`). Teker merkezleri mesh'te bulunursa ölçek dingil mesafesinden kalibre edilir, eksenler VCS'e hizalanır.
2. **Kesit çıkarımı:** X istasyonlarında (ör. her 100 mm) düzlemsel kesitler, ayrıca Y=0 profili ve üstten silüet alınır.
3. **Yüzey kurma:** kesitlere spline uydurulur, loft ile parametrik yüzeyler kurulur.
4. **Sapma kontrolü:** kurulan yüzey ile mesh arasındaki Hausdorff ve RMS sapma raporlanır, kabul sınırı tanımlanır.
5. **Statü:** mesh, kaynak geometri olarak LEGACY_IMPORT olur; ondan üretilen parametrik yüzey kanıt durumuna göre DRAFT olur.
6. **Fotoğrafla karşılaştırma:** fotoğraflarla çelişen bölgeler UNCERTAINTY_REGISTER'a yazılır.

**Modelleme sırası (gerekçesiyle):**
1. Tekerlek/lastik zarfı (yapıldı, DRAFT): ebat tanımı geometriyi tam belirler ve diğer her şeyin referansıdır.
2. Teker merkezleri ve sürüş yüksekliği (M13–M16 ölçüleri).
3. Kaporta yan profili (fotoğraf + M17–M31).
4. Cam evi ve camlar.
5. Kapaklar (kapı, kaput, bagaj kapağı).
6. Tamponlar ve lambalar.
7. İç mekan (fotoğraflardan).
8. Mekanik sistemler, yalnızca kanıt geldikçe (motor bölmesi ve alt gövde fotoğrafları, ruhsat).

**STEP ve GLB doğrulaması (uygulanıyor):**
- **STEP:**
  - yeniden içe aktarma, `is_valid` (BRepCheck) kontrolü;
  - analitik hacim ve sınır kutusu karşılaştırması (lastik zarfında hacim hatası 2·10⁻¹⁴);
  - katı sayısı (yazılan = okunan);
  - ayrı süreçlerde bayt tekrarlanabilirliği.
- **GLB:** CAD çekirdeğinden bağımsız numpy okuyucuyla:
  - başlık ve uzunluk tutarlılığı, accessor min/max kontrolü;
  - su geçirmezlik ve tutarlı sarım (winding), pozitif hacim;
  - eksen ve ölçek kontrolü.
- **STL:** normal–sarım tutarlılığı (ters normal: 0).

**İlk gerçek CAD parçası: lastik tasarım zarfı (WHL-001..004), gerekçe:**
- **Tam belirli geometri:** ebat tanımı (175/70 R14) dış çapı (600,6 mm), oturma çapını (355,6 mm) ve kesit genişliğini (175 mm) standart bir ilişkiyle tanımlar. Hiçbir şekil uydurulmuyor.
- **Varsayımsız konum:** dingil mesafesi ve izler ESTIMATED kanıtlı, PLACEHOLDER kullanılmıyor.
- **Arayüz parçası:** çamurluk boşluğu, süspansiyon, sürüş yüksekliği ve yerden yükseklik buna bağlanır.

Bilinçli olarak modellenmeyenler: omuz yarıçapı, sırt deseni, jant (genişlik/ET/PCD UNKNOWN) ve statik çökme. Bunların hiçbiri için kanıt yok.

---

## D. Üretilen çıktılar

Derleme: `python tools/twin.py build`. Çıktılar `build/` altında (git'e girmez). Denetim için kopyaları ve `SHA256SUMS` dosyası `audit/2026-11-02/` altında commit'li (D-017).

| Dosya | Bayt | SHA-256 | Doğrulama |
|---|---|---|---|
| `build/cad/WHL-001.step` | 10867 | `63b51b1878c9e542913c6cda9aeb614278a7e4bb6644c930a11cc1f93a740c5c` | geçerli; hacim 32 199 027 mm³, analitikle fark 2·10⁻¹⁴; bbox X −300,3…300,3, Y −780,5…−605,5, Z 0…600,6 |
| `build/cad/WHL-002.step` | 10866 | `cbd0f674e85469c8a7af014a85cfdc99d6c3e7cabf52c02c1857ac3b635a1e44` | geçerli; Y merkezi +693,0 (= 1386/2) |
| `build/cad/WHL-003.step` | 10874 | `d19688c1c82a1e20e92ef64754a896ddec06a744d6310ad8bac5516985c8987f` | geçerli; X merkezi 2490 (dingil mesafesi) |
| `build/cad/WHL-004.step` | 10873 | `3c68982d83b5ad5d7d2aedec9447f8eabd100b88806428ac62e43cec06342572` | geçerli; Y merkezi +663,5 (= 1327/2) |
| `build/cad/vehicle_cad.step` | 39313 | `904301ba92846e4f8f7f53840c498bddcee30aa2883f1a2d97cb904115720a6b` | 4 katı yazıldı, 4 okundu, geçerli; ayrı süreçlerde bayt bayt aynı |
| `build/vehicle.step` (görsel) | 1057695 | `d893901d738a762d43f8e73c10d6b891375801f7dc894ba67a61b17421af3025` | 40/40 katı, hacim hatası 2,0·10⁻¹³; **bayt tekrarlanabilir değil** (B-2) |
| `build/vehicle.stl` (görsel) | 620884 | `b1f47b33081d6282f714f854f77fc003fb03d3364b1afaf2d2a8ca4b78bb8c7e` | 12 416 üçgen, ters normal 0 |
| `build/vehicle.glb` (görsel) | 435444 | `8917131321527784263406f80fcae3d61b7e4aabd71aa63594748ba4d95ddcc0` | yapısal sorun 0; tüm gövdeler kapalı ve dışa dönük; ön +Z, yukarı +Y, boy 4,396 m |
| `build/assemblies/*.glb` | 11 900–317 228 | `build/manifest.json` içinde | aynı GLB kontrolleri |

Görsel çıktılar PLACEHOLDER'dır ve gerçek araç geometrisi olarak kullanılamaz.

---

## E. ChatGPT'den beklenen denetim

1. **Lastik zarfı:** OD = d_jant·25,4 + 2·S·(H/S) formülü ve "tasarım zarfı" tanımı (dikdörtgen kesitli halka) bir mühendislik CAD temsili için yeterli mi? ETRTO ölçüm jantı ve şişme etkisi nasıl ele alınmalı?
2. **Kaynak çelişkileri:** 1997 Kartal S için lastik (175 ve 185/70 R14), uzunluk (4396 ve 4360 mm), iz genişlikleri (1386/1327) ve motor (karbüratörlü 1,6, ~61 kW) için daha güvenilir bir kaynağınız var mı (Tofaş kullanım kılavuzu, teknik föy)?
3. **D-015 politikası:** sahibin şerit metre ölçüsünün ±5 mm ile VERIFIED sayılması makul mü? Referans durumu (yakıt, yük, lastik basıncı) yeterince tanımlı mı?
4. **Fotoğraf ölçeği:** %2 perspektif payı ve tek ölçek (dingil mesafesi) yaklaşımı, gövde yan yüzeyinin teker düzleminden farklı derinlikte olmasını yeterince karşılıyor mu?
5. **Mesh'ten CAD'e plan (C bölümü):** kesit, spline, loft ve Hausdorff yaklaşımına alternatifiniz var mı? Kabul eşiği ne olmalı?
6. **Tekrarlanabilirlik:** renkli STEP'in bayt tekrarlanamaması kabul edilebilir mi, yoksa renkleri ayrı bir dosyaya mı taşımalıyız?
7. **Gizlilik:** plaka regex'i ve medya uzantısı engeli public bir depo için yeterli mi?
8. **Eksik doğrulama:** girişim/boşluk kontrolünün kapsamı ne olmalı (statik konum mu, direksiyon ve süspansiyon kursu mu)?

---

## F. Açık sorular (kanıtla çözülemeyenler)

- **Lastik ve jant:** VEH-01'e takılı lastik ebadı ve jant (genişlik, ET, PCD, merkez delik).
- **Motor:** gerçekte takılı motor ve LPG dönüşümü olup olmadığı.
- **Ana ölçüler:** gerçek ölçüler; hiçbiri ölçülmedi, 0 VERIFIED.
- **Kaporta:** profili, renk, kaplama seviyesi ve isteğe bağlı donanımlar (tavan rayı, arka silecek, yan sinyal).
- **Eski arşiv:** `Kartal_S_Studyo.zip` içeriği ve kalitesi.
- **Mekanik:** süspansiyon, direksiyon, fren ve şasi geometrisi; şu an kanıtı yok.
- **Depolama (sahip kararı):** orijinallerin özel depolanması (U-009).

---

## G. Sonraki somut görev (tek ve en önemli)

**Kaporta yan profilini gerçek araçtan DRAFT seviyesine çıkarmak.** Girdi: sahibin M01–M16 şerit metre ölçüleri (`docs/OLCUM_REHBERI.md`) ve bir yan profil fotoğrafı. Akış:
1. Ölçüler: `tools/record_measurement.py`.
2. Fotoğraf noktaları: `tools/photo_scale.py --apply`.
3. Derleme ve doğrulama: `twin.py build` → yeniden açma kontrolleri → `sync-inventory`.
4. Çapraz kontrol: fotoğraf ve şerit metre değerleri tolerans içinde mi?

Bu girdi gelmezse yapılacak iş: **girişim/boşluk kontrol modülü**. CAD lastik zarfı ile çamurluk zarfı arasındaki boşluğu raporlayan, test edilmiş bir kontrol; kaporta ölçüleri geldiğinde hemen anlamlı hâle gelir.

---

## Puanlama (kanıta dayalı)

| Kriter | Ağırlık | Puan | Kanıt |
|---|---|---|---|
| Ölçü ve geometri doğruluğu | %30 | **UNKNOWN** | Gerçek araçta hiçbir ölçü alınmadı (0 VERIFIED). Modelin spec'e iç tutarlılığı test edildi (boy 4396, iz merkezleri ±0,5 mm), ama bu gerçek araca göre doğruluk değildir. |
| CAD kalitesi | %25 | **5 / 25** | 4 geçerli B-rep katı; analitik hacimle 2·10⁻¹⁴ uyum; deterministik STEP. Kapsam: CAD'de 143 bileşenden 4'ü (%2,8); zarf seviyesi, jant yok. |
| Test başarısı | %20 | **15 / 20** | 55/55 geçti; negatif (uydurma veri reddi), tekrarlanabilirlik ve tarayıcı testleri var. Eksik: CI yok, girişim testi yok, eski arşiv aracı gerçek veride denenmedi. |
| Kaynak ve kanıt kalitesi | %15 | **3 / 15** | 13 kanıt kaydı, 0 birincil (fotoğraf/belge/ölçüm). Literatür yalnız arama özetlerinden; kaynak sayfalar okunamadı (DNS engeli). Çelişkiler kayıtlı. |
| Kod kalitesi | %10 | **6 / 10** | Modüler; köken takibi yapan Resolver, test kapısı. Eksikler: YAML'ı metin düzeyinde düzenleme, bu turda bulunan manifest hatası, `BrokenPipeError`. |

**Toplam:** puanlanabilen %70 için 29/70. Ağırlığın %30'u UNKNOWN olduğundan **genel puan hesaplanamaz.**
