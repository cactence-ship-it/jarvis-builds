# API'siz iş bölümü: ChatGPT + Claude (sahip kararı, 2026-11-06)

**Kesin şart:** API anahtarı yok, ücretli API yok. Yalnız ücretsiz ChatGPT ve Claude arayüzleri
kullanılır. Bu dosya `GPT_DAVRANIS_KURALLARI.md` içindeki üç ortaklı (Gemini dahil) rotasyonun
yerine geçer; o dosyadaki yöntem, disiplin, yasaklar ve rapor biçimi aynen geçerlidir.

## Ne çalışır, ne çalışmaz (dürüst sınırlar)

| Öğe | Durum |
|---|---|
| GitHub deposu tek gerçek kaynak, CI testleri (sırsız, ücretsiz) | ÇALIŞIYOR |
| `orchestrator` çevrimdışı denetleyici: `check-response`, `check-report`, `check-diff`, `check-commits` | ÇALIŞIYOR (ağsız, API'siz) |
| `tools/twin.py validate`, görev kaydı ve çapraz inceleme kuralı | ÇALIŞIYOR |
| İki modelin birbirine doğrudan mesaj atması | YOK. Köprü sahip ve depodur |
| Görevlerin otomatik dağıtımı (T-009), `agent-panel.yml` (dal `ccr-215f9b0e-pfveg4`) | KAPALI. API anahtarı ister; bu dal birleştirilmez |
| `panel-run --mock` | Yalnız akış testi. GPT ya da Claude görüşü DEĞİLDİR, inceleme yerine sayılmaz |

## Roller

| | ChatGPT | Claude |
|---|---|---|
| Üretir | Kaynak notu (`docs/*_RESEARCH_*.md`): URL, erişim tarihi, değer + birim, kaynak türü, kapsam (yıl/varyant). Parça kodu adayları | Kod, CAD hattı, spec/montaj entegrasyonu, testler, dosya ve proje mimarisi |
| Denetler | Claude'un sonuç commit'leri (tam SHA ile) | ChatGPT'nin iddiaları: spec'e girecek **her** sayının kaynağını açar; diğer notlarda not başına en az 2 rastgele iddia |
| Yazamaz | `specs/kartal_s_1997.yaml` değerleri (yalnız öneri) | Kaynağı açılamayan veriyi kabul edemez |

## Kaynak doğrulama kuralları

1. Her iddia: kaynak URL + erişim tarihi + sayfadaki ifade (15 kelimeyi geçmeyen alıntı ya da özet).
2. İkinci model kaynağı açıp aynı değeri görürse: **ÇAPRAZ-DOĞRULANDI**. Açamazsa: **DOĞRULANAMADI**
   (kabul edilmez, reddedilmez; açık kalır). Farklı değer görürse: **ÇELİŞKİ**.
3. Çapraz doğrulama bir değeri VERIFIED yapmaz. VERIFIED yalnız araca özgü birincil kanıtla
   (sahip ölçüsü, fotoğraf, ruhsat) olur ve sahibin kararıdır (D-005).
4. Katalog uyumluluk yazısı ölçü değildir. Parça kodu bu araca takılı olduğu gösterilmeden BOM'a girmez.

## Döngü (her görev için)

1. **Yazar** işi bir dalda yapar, `tasks/T-nnn.yaml` içine `results` kaydını tam SHA ile ekler.
2. **Yazar** `agents/REVIEW_REQUEST_*.md` dosyasını yazar (SHA, CI linki, neye bakılacağı, cevap biçimi).
3. **Sahip** dosyayı diğer modele verir (GitHub bağlantısı yoksa kopyala-yapıştır).
4. **İnceleyen** kodu yeniden yazmaz; bulguları önem sırasıyla tablo olarak ve cevap biçimiyle döner.
5. **Sahip** cevabı yazara getirir. Yazar cevabı önce denetleyiciden geçirir:
   `kartal-orchestrator check-response cevap.txt` (0 ACCEPT, 1 NEEDS_OWNER, 2 REJECT).
6. Geçerse `reviews` listesine işlenir, `python tools/twin.py tasks` ile pano üretilir, `validate` çalışır.
7. Birleştirme her zaman sahibin kararıdır. Kimse kendi işini onaylayamaz; yeni commit eski onayı düşürür.

## Bulgu önem sırası

| Seviye | Anlamı | Sonuç |
|---|---|---|
| S1 | Uydurma değer, sahte "tamamlandı", gizlilik ihlali, test/kontrol zayıflatma | REJECT |
| S2 | Kabul ölçütü karşılanmamış, test eksik, kaynak çelişkisi gizlenmiş | CHANGES_REQUESTED |
| S3 | Belge/tutarlılık eksiği, tekrar commit, isimlendirme | Not; tek başına engel değil |

## Verimlilik

- İstekler toplu paket olarak gider (ücretsiz arayüzlerin mesaj sınırı var). Bir paket ≤ 5 görev.
- Her paket kendi içinde yeterlidir: SHA, dosya listesi, bakılacak noktalar, cevap biçimi.
- Tekrar okuma yok: değişmeyen dosya için önceki incelemeye atıf yapılır.
