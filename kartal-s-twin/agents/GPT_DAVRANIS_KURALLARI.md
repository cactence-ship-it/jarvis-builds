# Yapay zekâ ortakları davranış kuralları: baş mühendis, yalakalık yok, sahte başarı yok

Projede üç ortak çalışır: **GPT (OpenAI)**, **Claude (Anthropic)**, **Gemini (Google)**.
Hepsi aynı talimata ve aynı denetime tabidir.

## Üç ortak nasıl çalışır

- Görevleri sırayla biri yazar: GPT → Claude → Gemini → GPT …
- Yazanın değişikliğini **diğer ikisi** aynı commit üzerinde bağımsız inceler.
- Onay için ikisinin de kabul etmesi gerekir. Biri reddederse değişiklik durur. Biri kabul
  edip öteki reddederse karar senindir.
- Kimse kendi işini onaylayamaz. Yeni bir commit gelince eski onaylar geçersiz olur.
- Onay merge değildir: merge her zaman senin kararın.

## Talimat nasıl verilir

Talimat metninin tek kaynağı
[`orchestrator/prompts/engineer_tr.txt`](../../orchestrator/prompts/engineer_tr.txt) dosyasıdır.
Orkestratör ileride API çağrısı yaparken de aynı metni kullanacak (`ENGINEER_SYSTEM_PROMPT`).

1. Dosyayı GitHub'da aç ve tamamını kopyala. Terminalden almak için:
   `cargo run -q --manifest-path orchestrator/Cargo.toml -- prompt`
2. Yapıştır:
   - **ChatGPT:** Ayarlar → Kişiselleştirme → Özel talimatlar.
   - **Gemini:** yeni bir Gem oluştur ve metni Talimatlar alanına koy.
   - **Claude:** bir Proje oluştur ve metni Proje talimatlarına koy.

   Alan küçükse metni her görevin başına yapıştır. Görevle birlikte almak için:
   `... -- prompt "görev metni"`

Talimat her ortaktan şunları ister:
- **Yöntem:** sorun tanımı, mevcut durumu gerçekten okuma, kök neden, en az iki seçenek ve
  aralarındaki ödünleşim, arıza modları, en küçük doğru değişiklik, kanıtlı doğrulama.
- **Disiplin:** her sayının birimi; her değerin durumu (VERIFIED / ESTIMATED ± / UNKNOWN);
  tolerans; tekrarlanabilir hesap.
- **Yasaklar:** övgü, kanıtsız "bitti" iddiası, kontrolü bozarak yeşil göstermek, tekrar
  commit, sahibin onayı gereken işler.
- **Rapor biçimi:** Sorun / Kök neden / Seçenekler / Değişiklik / Doğrulama / Riskler.

## Mekanik denetim

Bir ortak kurala uymasa da yakalanır:
- Her PR'da CI'daki `PR guard` işi diff'i ve commit'leri denetler.
- Elle denetim için komutlar:

```sh
cargo build --manifest-path orchestrator/Cargo.toml
B=orchestrator/target/debug/kartal-orchestrator

$B check-report rapor.txt          # mühendislik raporu: bölümler, kanıt, birimler
$B check-response cevap.txt        # serbest cevap: övgü, kanıtsız başarı iddiası
git show <sha> | $B check-diff -   # kontrol zayıflatma, test silme, sahip onayı gerekenler
git log --format=%s origin/<taban>..HEAD | $B check-commits -
```

Çıkış kodu: `0` ACCEPT, `1` NEEDS_OWNER (senin onayın gerekli), `2` REJECT.

| Kural | Sonuç |
|---|---|
| Rapor bölümü eksik (ör. kök neden yok, seçenek yok) | REJECT |
| Doğrulama bölümünde kanıt yok, "çalıştırmadım" da denmemiş | REJECT |
| "Testler geçti", "push ettim", "tamamlandı" + SHA ve CI linki/çıkış kodu yok | REJECT |
| `cargo fmt` (`--check` yok), `\|\| true`, `continue-on-error`, `--no-verify`, `pull_request_target` | REJECT |
| Test silmek, `#[ignore]`, `@pytest.mark.skip`/`xfail` | REJECT |
| Yeni `.py` dosyası (Blender betikleri ve mevcut Python testleri hariç), D-029: yeni kod Rust | REJECT |
| Ücretli API açmak, VERIFIED/VALIDATED yapmak, force push | NEEDS_OWNER |
| Övgü cümlesi, birimsiz fiziksel değer, tekrarlanan commit | uyarı |

Gerçek örnek: `git show 14e0e9f | $B check-diff -` → `verdict=REJECT`. O commit CI'daki
`cargo fmt --check` adımını düz `cargo fmt` yapmıştı.
