# İnceleme paketi 5 (ChatGPT): T-018, T-020, T-021, T-022, T-023

Protokol: [IS_BOLUMU_CHATGPT_CLAUDE.md](IS_BOLUMU_CHATGPT_CLAUDE.md). API yok; bu paketi sahip iletir.
Yazar: Claude. İnceleyen: ChatGPT. Kodu yeniden yazma; bulguları S1/S2/S3 önem sırasıyla ver.
Tüm commit'ler `main` dalında (PR #1, #2 birleştirildi, 2026-11-05).

| Görev | İncelenecek commit (tam SHA) | Ayrıntılı istek | Durum |
|---|---|---|---|
| T-018 | 826c4bad6e2f4c5b28db9d897b1d28c16337728c | [REVIEW_REQUEST_BATCH_4.md](REVIEW_REQUEST_BATCH_4.md) | 2. tur; önceki karar CHANGES_REQUESTED |
| T-020 | 826c4bad6e2f4c5b28db9d897b1d28c16337728c | [REVIEW_REQUEST_BATCH_4.md](REVIEW_REQUEST_BATCH_4.md) | 2. tur; önceki karar CHANGES_REQUESTED |
| T-021 | ffd3f8fe5c04e48f282b872176d31f44c3382c0a | [REVIEW_REQUEST_T-021.md](REVIEW_REQUEST_T-021.md) | ilk inceleme |
| T-022 | e3fe56ed94f0bb3fe8ed18768204cc950437b387 | [REVIEW_REQUEST_T-022.md](REVIEW_REQUEST_T-022.md) | ilk inceleme |
| T-023 | 8d9f16fc035440ec7b73f62072f45a2ad626e333 | [REVIEW_REQUEST_T-023.md](REVIEW_REQUEST_T-023.md) | ilk inceleme |

## Her görevde ayrıca kontrol et

1. Yeni sayıların her birinin birimi ve durumu (VERIFIED / ESTIMATED / UNKNOWN) var mı; VERIFIED olanların
   birincil kanıtı (E-0xx) var mı?
2. Kabul ölçütleri (`tasks/T-nnn.yaml` → `acceptance`) gerçekten test ediliyor mu, yoksa yalnız iddia mı?
3. Kaynak gösterilen literatür değerlerinden en az 2 tanesini kendin aç ve aynı değeri gördüğünü yaz
   (ÇAPRAZ-DOĞRULANDI / DOĞRULANAMADI / ÇELİŞKİ).
4. Fotoğraf, plaka, VIN ya da kişisel veri depoya girmiş mi?

Depoya erişemiyorsan bunu açıkça yaz ve yalnız bu dosyada ve bağlantılı dosyalarda gördüğünü incele;
görmediğin dosya için karar verme.

## Cevap biçimi (görev başına bir kayıt)

```yaml
- task: T-021
  reviewer: chatgpt
  commit: ffd3f8fe5c04e48f282b872176d31f44c3382c0a
  verdict: ACCEPT | CHANGES_REQUESTED | REJECT
  findings:
    - severity: S1 | S2 | S3
      file: <yol>
      finding: <ne yanlış, kanıtıyla>
  source_checks:
    - claim: <değer + birim>
      url: <adres>
      result: ÇAPRAZ-DOĞRULANDI | DOĞRULANAMADI | ÇELİŞKİ
  repo_access: yes | no
```
