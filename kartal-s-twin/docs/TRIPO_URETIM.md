# Tripo AI ile gerçekçi Kartal S modeli (telefondan)

Tripo'nun ürettiği modeli `tools/meshfit` aracı dijital ikizin gerçek ölçülerine oturtur:
- uzunluk, dingil mesafesi, iz genişliği ve lastik çapı ruhsattan ve kaynaklardan gelir;
- model yönüne çevrilir, ölçeklenir ve yerine konur;
- oranları kontrol edilir.

Sonuç telefonda döndürülebilen sayfada görünür (`viewer/tripo.html`).

**Bilmen gereken:** Tripo'nun şekli fotoğraftan tahmin edilir. Bu model görsel olarak CAD'in
yerine geçer, ama ölçüm değildir (D-030). Mühendislik CAD'i olan parçalar (lastik, jant, LPG
tankı) CAD olarak kalır.

## Plan A (önerilen): bütün araç tek parça

En tutarlı sonucu verir, çünkü gövde ve tekerler aynı modelden gelir.

1. Telefonda **tripo3d.ai** sitesini aç ve giriş yap.
2. **Image to 3D** bölümünde, varsa **Multiview** (çoklu görünüm) seçeneğini aç.
3. Fotoğrafları yükle:
   - Ön: aracın tam önünden, 6–8 m uzaktan.
   - Yan: sol yandan, aracın ortasının hizasından, telefon yere paralel.
   - Arka: tam arkadan.
   - Arka çapraz görünüm de eklenebiliyorsa ekle.
   - **Önce plakayı kapat:** fotoğraf düzenleyicide plakanın üstünü karala. Tripo
     fotoğrafı kendi sunucusuna yükler; dokuda plaka görünmemeli.
4. Ayarlar: **Texture açık**, mümkünse **PBR** ve en yüksek kalite. **Quad/low-poly kapalı**.
5. Üretilen modeli **GLB** olarak indir.
6. Dosya adını `car.glb` yap ve bu sohbete ek olarak gönder.

## Plan B: parça parça

Tekerleri tam ölçüde ve dört gerçek teker merkezinde istersen bu planı kullan.

| Dosya adı | Tripo'da ne üret | Nasıl birleştirilir |
|---|---|---|
| `body.glb` | Gövde, **tekersiz**. Image to 3D'ye yan, ön ve arka fotoğrafları ver. Text kutusu varsa: "car body only, no wheels, empty wheel arches". | Boyu gerçek uzunluğa ölçeklenir, tavan çizgisi gerçek yüksekliğe hizalanır. |
| `wheel.glb` | **Tek** teker + lastik. Tekerin dik ve yakından çekilmiş fotoğrafından üret. | Lastik dış çapına (yaklaşık 596 mm) ölçeklenir ve dört teker merkezine kopyalanır. Sağdakiler aynalanır. |

İkisini birden kullanma: Plan A'da tekerler zaten modelin içinde. Plan B için iki dosyayı da gönder.

## Tutarlılık kontrolü

Her parça için şu rapor çıkar:

```
part VIS-TRIPO-CAR (car): CONSISTENT
  width   fitted 1.862 m, target 1.862 m, deviation +0.0 %
  height  fitted 1.581 m, target 1.570 m, deviation +0.7 %
```

- **CONSISTENT (tutarlı):** sapma %3'ün altında.
- **WARN (sınırda):** sapma %3 ile %8 arasında. Kullanılabilir, ama göze batabilir.
- **INCONSISTENT (tutarsız):** sapma %8'in üstünde. Model başka bir şekil olmuş; Tripo'da
  yeniden üret. Kredin varsa birkaç aday üretip en tutarlısını seçeriz.

Kontrolün dayandığı ölçüler raporda yazar. Şu an genişlikteki ayna payı ve tavan rayı
yüksekliği tahmindir (PLACEHOLDER). Şerit metreyle ölçülürse (M-kodları, `OLCUM_REHBERI.md`)
kontrol de kesinleşir.

**Yön:** boyut kontrolü aracın önünün hangi yöne baktığını göremez, çünkü kutu simetriktir.
Görüntüleyicideki turkuaz **ÖN oku** kaputu göstermiyorsa parçanın `front` ayarını çeviririm.

## Teknik (Claude için)

```sh
bash tools/viewer_smoke/tripo.sh              # refs/derived/tripo/*.glb: yerleştir + tarayıcıda kontrol et
bash tools/viewer_smoke/tripo.sh --self-test  # ikizin kendi GLB'si ile uçtan uca sınama
tools/meshfit/target/release/meshfit inspect refs/derived/tripo/car.glb
```

GLB dosyaları `refs/derived/tripo/` altında durur ve git'e girmez (D-012).
