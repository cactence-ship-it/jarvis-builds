# Üç ortağı otomatik çalıştırma: kurulum (sahip için)

Bu sistem, GitHub'daki **Actions → Agent panel** düğmesine bastığında şunu yapar:

1. Seçtiğin ortak (GPT, Claude ya da Gemini) görevi baş mühendis kurallarıyla rapor olarak yazar.
2. Bekçi raporu denetler. Eksik bölüm, kanıtsız "bitti" iddiası ya da yağcılık varsa rapor
   reddedilir ve inceleme parası harcanmaz.
3. Diğer iki ortak raporu bağımsız inceler: `KARAR: KABUL` ya da `KARAR: RET`.
4. Sonuç çalıştırma sayfasında görünür: APPROVED, REJECTED, DISPUTED (karar senin) ya da BLOCKED.

Sistem **kod yazmaz, push etmez, PR açmaz, birleştirmez.** Sadece rapor ve inceleme üretir.

## Bir kerelik kurulum

Hepsi GitHub'da: depo → **Settings → Secrets and variables → Actions**.

### 1. Anahtarlar (Secrets sekmesi → New repository secret)

| Ad | Nereden alınır |
|---|---|
| `ANTHROPIC_API_KEY` | console.anthropic.com → API Keys |
| `OPENAI_API_KEY` | platform.openai.com → API keys |
| `GEMINI_API_KEY` | aistudio.google.com → Get API key |

Anahtarı **sohbete, koda ya da bir dosyaya asla yapıştırma**; yalnız bu ekrana.
Bekçi ve kod anahtarı hiçbir yere yazdırmaz.

### 2. Ayarlar (Variables sekmesi → New repository variable)

| Ad | Değer | Anlamı |
|---|---|---|
| `KARTAL_PAID_DISPATCH` | `on` | Açma/kapama anahtarı. Silersen ya da `off` yaparsan hiçbir ücretli çağrı yapılmaz. |
| `KARTAL_RUN_BUDGET_MICROS` | örn. `2000000` | Bir çalıştırmada harcanabilecek en fazla para, mikro dolar cinsinden. `1000000` = 1 $. |
| `KARTAL_OPENAI_MODEL` | OpenAI model adı | Kullanılacak GPT modeli. |
| `KARTAL_OPENAI_PRICE_IN` / `_PRICE_OUT` | 1 milyon token başına mikro dolar | OpenAI fiyat sayfasındaki güncel fiyat. 2,50 $ → `2500000`. |
| `KARTAL_GEMINI_MODEL` | Gemini model adı | Kullanılacak Gemini modeli. |
| `KARTAL_GEMINI_PRICE_IN` / `_PRICE_OUT` | 1 milyon token başına mikro dolar | Google fiyat sayfasındaki güncel fiyat. |

Claude için ayar gerekmez: varsayılan `claude-opus-5-5`, 4 $ / 20 $ (1 milyon token).
Değiştirmek istersen `KARTAL_ANTHROPIC_MODEL`, `KARTAL_ANTHROPIC_PRICE_IN`, `KARTAL_ANTHROPIC_PRICE_OUT`.

OpenAI ve Gemini için model adı ve fiyatı **senin** girmen gerekiyor; kod bunları tahmin
etmez. Fiyat girilmemiş bir ortak hiç çağrılmaz, çünkü maliyeti hesaplanamayan çağrı yapılmaz.

## Bütçe nasıl korunuyor

- Her çağrıdan **önce** en kötü durum maliyeti hesaplanır (girdi baytı kadar token + en fazla
  16.000 çıktı tokenı). Bu, kalan bütçeyi aşabilecekse çağrı **yapılmaz**, panel BLOCKED ile durur.
- Claude için ek %25 pay ayrılır: Claude bir isteği güvenlik nedeniyle reddederse sunucu
  isteği başka bir Claude modeliyle tekrar dener (fallback); o model farklı fiyatlı olabilir.
- Çağrıdan sonra gerçek token kullanımı kaydedilir ve sayfada tablo olarak gösterilir.
- Aynı anda yalnız bir panel çalışır, iki çalıştırma bütçeyi ikiye katlayamaz.
- Yazarın raporu bekçiden geçemezse inceleme çağrıları hiç yapılmaz. İlk inceleyen
  reddederse ikinci incelemeye para harcanmaz.

Fikir vermesi için: Claude fiyatıyla tek bir çağrının en kötü durumu yaklaşık 0,45 $,
üç çağrılık bir panelin en kötü durumu yaklaşık 1,4 $ (üç çağrı da Claude fiyatıyla
hesaplanırsa; GPT ve Gemini kendi fiyatlarıyla hesaplanır). Gerçek harcama çoğu zaman bunun
altındadır; her çalıştırmanın sayfasında kuruşu kuruşuna yazar. Bütçe en kötü durumun
altındaysa panel ortada durur ve bunu söyler.

## Çalıştırma

1. Depo → **Actions** → soldan **Agent panel** → **Run workflow**.
2. **Görev**: ne istediğini yaz (örn. "Arka süspansiyon için hangi ölçüler eksik, ölçüm planı çıkar").
3. **Yazar**: openai, anthropic ya da gemini. Diğer ikisi otomatik inceler.
4. Bitince çalıştırmaya tıkla: özet sayfasında rapor, iki inceleme ve harcama tablosu var.

Acil durdurma: Variables → `KARTAL_PAID_DISPATCH` değerini `off` yap. Bir sonraki çağrı yapılmaz.


## Seviye 6 ekip lideri (planlama modu)

Bu PR ayrıca `kartal-s-twin/agents/LEVEL6_TEAM_LEADER_PROTOCOL.md` ve
`orchestrator/prompts/team_leader_tr.txt` dosyalarını ekler. Yerel Rust aracıyla
koordinatör talimatını almak için:

```sh
cargo run --manifest-path orchestrator/Cargo.toml -- leader-prompt "Kartal motor bölümü için eksik kanıtları ve paralel işleri planla"
```

Bu komut yalnızca ekip lideri talimatını üretir; kendiliğinden ücretli API çağrısı,
alt ajan çalıştırma, dosya değiştirme veya PR açma yapmaz. Sağlayıcı çağrısı için mevcut
`panel-run` akışı, kill switch ve bütçe korumaları geçerlidir. Gerçek otomatik alt-ajan
dispatch'i ayrı bir sonraki aşamadır; bu PR bunu çalışır gibi göstermemektedir.
