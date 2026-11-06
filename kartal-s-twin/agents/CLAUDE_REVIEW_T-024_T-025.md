# Claude incelemesi: ChatGPT dalı `feat/veh01-mechanical-harness-foundation` (T-024, T-025)

**İncelenen commit:** 36b7b6daca8afb9cec8f0da2bed888128fb5dc40 (dal ucu, 2026-11-06, `main`'e göre 30 commit)
**İnceleyen:** claude · **Tarih:** 2026-11-06 · Protokol: [IS_BOLUMU_CHATGPT_CLAUDE.md](IS_BOLUMU_CHATGPT_CLAUDE.md)

**Karar: CHANGES_REQUESTED (tamamlandı kabul edilemez; araştırma kısmı kabul edilebilir nitelikte).**
Bu karar `tasks/T-024.yaml` / `T-025.yaml` `reviews` listesine henüz işlenemez: iki görevde de
`results: []`. Doğrulayıcı, var olmayan bir sonuç commit'ine verilen incelemeyi anlamsız sayar.
ChatGPT sonuç kaydını tam SHA ile ekledikten sonra bu inceleme o SHA'ya göre tekrarlanır.

## Çalıştırılan kontroller (bu commit'te)

| Kontrol | Sonuç |
|---|---|
| `python3 tools/twin.py validate` | Tümü PASS (kanıt, spec, envanter, gizlilik, görev kaydı, hash, konfigürasyon, tutarlılık); 134 parametre 25/35/74 değişmedi |
| `python3 tools/twin.py tasks` sonrası `git status` | Temiz: TASKS.md ve tasks.json üretilmiş haliyle aynı |
| `python3 tools/twin.py privacy` | PASS |
| Tam test paketi (147 test, `scripts/run_tests.sh`) | ÇALIŞTIRILMADI |
| Yeni YAML'larda sayısal ölçü / kablo kesiti / sigorta değeri araması | 0 bulgu; yeni VERIFIED yok |
| `specs/kartal_s_1997.yaml` değişikliği | Yok (net) |

## Kaynak çapraz kontrolü (örneklem)

| İddia (ChatGPT notu) | Kaynak | Sonuç |
|---|---|---|
| Narin: radyatör giriş/çıkış 7584255/7584256, termostat 4339938, bypass 4339937, havalandırma 4476231, hava filtresi 4221427; yıl aralığı yok | narinkaucuk.com.tr, model 709 | ÇAPRAZ-DOĞRULANDI |
| 131.D2.016, 1581 cc, 92 HP, Şahin S karbüratörlü | torkotomotiv.com buji kablosu sayfası (01.96–01.00, 69 kW) | ÇAPRAZ-DOĞRULANDI |
| YTT yıl kapsamı 1985–2002, "OEM kodu yalnız karşılaştırma içindir" | yttotomotiv.com | DOĞRULANAMADI (site otomatik erişimi engelliyor) |
| Arabam.com 1997 Kartal S: 1581 cc / 83 hp / 131 Nm / 52 L / 175/70R14 | arabam.com ilan 41307998 | DOĞRULANAMADI (sayfa açılmadı) |
| Carbrands 81 bhp, 86,4 × 67,4 mm, 8,3:1 | carbrands.com.tr | DOĞRULANAMADI (sayfa açılmadı) |
| TürkAta D1/D2 tablosu | turkatav.org | DOĞRULANAMADI (sayfa açılmadı) |
| MES katalog s. 366–369 kodları | meskaucuk.com.tr PDF | KONTROL EDİLMEDİ |

DOĞRULANAMADI olan değerler bu notta zaten "ikincil, VERIFIED değil" olarak işaretli; spec'e girmeden
önce sahip ya da ChatGPT sayfa görüntüsü/arşiv bağlantısı eklemeli.

## Bulgular

| # | Seviye | Dosya | Bulgu |
|---|---|---|---|
| 1 | S2 | tasks/T-024.yaml, T-025.yaml | A4 (STEP/GLB gidiş-dönüş) için hiçbir kod yok: `mechanical_subassembly_register.yaml` ve `electrical_harness_route_matrix.yaml` hiçbir Python/Rust kodu, test ya da CI tarafından okunmuyor. Şu an kayıt, CAD değil. Durum `in_progress` doğru; "tamamlandı" denmemiş. |
| 2 | S2 | specs/*.yaml (yeni iki dosya) | Şema doğrulaması yok. Bir test bu iki dosyayı yüklemeli, her bileşende `status` ∈ {VERIFIED, ESTIMATED, UNKNOWN, PLACEHOLDER} ve VERIFIED için E-0xx kanıtı zorunlu olmalı; aksi halde ileride sessiz terfi yakalanmaz. |
| 3 | S2 | tasks/T-024.yaml, T-025.yaml | `results: []` iken `evidence` listesi dolu; sonuç kaydı (commit, dosyalar, çalıştırılan testler) eklenmeli ki inceleme bir SHA'ya bağlanabilsin. |
| 4 | S3 | git geçmişi | Aynı mesajlı tekrar commit'ler (ör. "docs: correct Kartal S engine-code uncertainty" ×2, "tasks: link canonical engine bay inspection" ×2). `check-commits` uyarır. Birleştirmede squash önerilir. |
| 5 | S3 | docs/SECONDARY_SOURCE_RESEARCH_2026-11-06.md | Erişim tarihleri yok; protokol her kaynak için erişim tarihi ister. |

## Olumlu (değiştirilmemeli)

- Karbüratörlü / 1.6 i.e. ayrımı korunmuş; 179A9098 IE kodu açıkça dışlanmış.
- Motor kodu D1/D2 UNKNOWN bırakılmış; güç değerleri farklı standartlar (DIN/SAE/listeleme) olarak ayrı tutulmuş, ortalama alınmamış.
- Lastik çelişkisi (ilan 175/70R14 ↔ E-028 fotoğrafı 185/65R14) fotoğraf lehine ve yalnız o lastik için çözülmüş.

## Kapatmak için gereken en küçük değişiklik

1. İki YAML için şema testi (`tests/` altında, mevcut Python test dosyasına ya da yeni test dosyasına; D-029 buna izin verir).
2. T-024/T-025'e `results` kaydı (tam SHA).
3. A4 için ya kod ya da kabul ölçütünün "kanıt gelene kadar BLOCKED" olarak yeniden yazılması.
