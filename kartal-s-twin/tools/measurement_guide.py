#!/usr/bin/env python3
"""Generate docs/OLCUM_REHBERI.md - the owner's measurement and evidence guide (Turkish).

    python tools/measurement_guide.py          write the guide
    python tools/measurement_guide.py --check  fail if the guide is stale

Generated from specs/kartal_s_1997.yaml and specs/placeholder_assumptions.yaml, so it always
lists exactly what is still UNKNOWN, ESTIMATED or a PLACEHOLDER.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from kartal_twin import PROJECT_ROOT  # noqa: E402
from kartal_twin.params import load_assumptions  # noqa: E402
from kartal_twin.spec import iter_parameters, load_spec  # noqa: E402

OUT = PROJECT_ROOT / "docs" / "OLCUM_REHBERI.md"

# P1 - tape measurements that drive the body geometry (Turkish instructions).
TAPE = {
    "dimensions.overall_length": "Ön ve arka tamponun en uç noktasından yere çekül (ip + ağırlık) sarkıtın, iki işaret arasını ölçün.",
    "dimensions.overall_width_body": "Aynalar hariç, gövdenin en geniş noktasından iki yana çekül; aradaki mesafe.",
    "dimensions.overall_width_mirrors": "Aynalar dahil en geniş nokta, iki yandan çekül.",
    "dimensions.overall_height": "Tavana düz bir çıta koyun (tavan rayı varsa rayların arasından), çıtadan yere dik mesafe.",
    "dimensions.overall_height_roof_rails": "Tavan rayı varsa: rayların üstüne çıta, çıtadan yere.",
    "dimensions.wheelbase_lh": "Sol taraf: ön jant göbeği merkezinden arka jant göbeği merkezine (tekerlekler düz).",
    "dimensions.wheelbase_rh": "Sağ taraf: aynı ölçü.",
    "dimensions.front_track": "Ön iki lastiğin diş ortasından ortasına, yere yakın (tekerlekler düz).",
    "dimensions.rear_track": "Arka iki lastiğin diş ortasından ortasına.",
    "dimensions.front_overhang": "Ön jant merkezinden tamponun en ön noktasına (yatay, yerde çekülle).",
    "dimensions.rear_overhang": "Arka jant merkezinden tamponun en arka noktasına.",
    "dimensions.ground_clearance_min": "Gövdenin en alçak noktasından yere; hangi parça olduğunu yazın.",
    "dimensions.wheel_centre_to_arch_fl": "Sol ön: jant merkezinden çamurluk kemerinin kenarına dik mesafe.",
    "dimensions.wheel_centre_to_arch_fr": "Sağ ön: aynı ölçü.",
    "dimensions.wheel_centre_to_arch_rl": "Sol arka: aynı ölçü.",
    "dimensions.wheel_centre_to_arch_rr": "Sağ arka: aynı ölçü.",
}
# P1b - placeholder shape assumptions, measured in the vehicle coordinate system.
SHAPE = {
    "front_track": "Yukarıdaki ön iz genişliği ölçüsü bunu da değiştirir.",
    "rear_track": "Yukarıdaki arka iz genişliği ölçüsü bunu da değiştirir.",
    "front_overhang": "Yukarıdaki ön çıkıntı ölçüsü bunu da değiştirir.",
    "nose_top_z": "Kaputun ön kenarının yerden yüksekliği.",
    "nose_bottom_z": "Ön panelin (tampon arkası) alt kenarının yerden yüksekliği.",
    "bumper_bottom_z": "Ön tamponun alt kenarının yerden yüksekliği.",
    "bumper_height": "Tamponun dikey yüksekliği.",
    "bumper_protrusion": "Tamponun kaportadan ne kadar dışarı çıktığı.",
    "sill_z": "Kapı altı marşpiyelin alt kenarının yerden yüksekliği.",
    "belt_z": "Yan camların alt kenarının (kapı üst çizgisi) yerden yüksekliği.",
    "cowl_x": "Ön jant merkezinden ön camın alt kenarına yatay mesafe.",
    "windshield_top_x": "Ön jant merkezinden ön camın üst kenarına yatay mesafe (çekülle).",
    "b_pillar_x": "Ön jant merkezinden orta direğin (ön/arka kapı arası) ortasına.",
    "c_pillar_x": "Ön jant merkezinden arka kapının arka kenarına.",
    "roof_rear_inset": "Tavanın arka bitişi ile arka tampon dışındaki gövde arasındaki yatay fark.",
    "rear_bottom_z": "Bagaj kapağı altındaki arka panelin alt kenarının yerden yüksekliği.",
    "greenhouse_inset_roof": "Tavanın genişliği (yandan yana), ölçülen değeri yazın.",
    "mirror_protrusion": "Aynanın gövde yanından dışarı taşma mesafesi.",
}
# P2 - registration certificate (ruhsat) fields. Owner data must be covered before photographing.
RUHSAT = [
    ("Markası / Tipi / Ticari adı", "identity.make, identity.model, identity.variant"),
    ("Model yılı", "identity.model_year"),
    ("Rengi", "identity.exterior_colour"),
    ("Silindir hacmi", "engine.displacement"),
    ("Motor gücü", "engine.max_power"),
    ("Yakıt cinsi", "engine.fuel_type"),
    ("Net ağırlığı", "mass.curb_mass"),
    ("Azami yüklü ağırlığı", "mass.gross_vehicle_mass"),
    ("Koltuk sayısı", "interior.seating_capacity"),
]
PHOTOS = [
    "Motor bölmesi: kaput açık, üstten ve iki yandan (motor tipi, karbüratör/enjeksiyon, servo fren).",
    "Alt gövde: arka aksın ve şaftın göründüğü açı (arkadan itişli mi, arka süspansiyon tipi).",
    "Ön tekerlek: direksiyon tam kırık, tekerlek arkasından süspansiyon ve fren.",
    "Lastik yanağı yakın çekim: ebat ve DOT kodu okunacak şekilde (4 lastik).",
    "Jant: ET/offset ve ebat damgası varsa yakın çekim.",
    "Akü etiketi (V, Ah, CCA) ve sigorta kutusu.",
    "Tam yan profil: aracın tam ortasından, 6-8 m uzaktan, telefon yere paralel (lens distorsiyonu az).",
    "Tam önden ve tam arkadan: aynı şekilde, aracın orta ekseninde.",
]


def render() -> str:
    spec = load_spec()
    params = dict(iter_parameters(spec))
    asm = load_assumptions()
    st = lambda pid: params[pid]["status"] + (f" ({params[pid]['value']})" if params[pid]["value"] is not None else "")
    lines = [
        "# Ölçüm ve Kanıt Rehberi - Kartal S (VEH-01)",
        "",
        "<!-- GENERATED by `python tools/measurement_guide.py`. Elle düzenlemeyin. -->",
        "",
        "Bu rehber, dijital ikizdeki **tahminleri (ESTIMATED)** ve **varsayımları (PLACEHOLDER)** "
        "gerçek ölçülerle değiştirmek için gereken bilgileri listeler. Sizin ölçtüğünüz değerler "
        "MEASUREMENT kanıtı olarak kaydedilir ve parametre **VERIFIED** olabilir.",
        "",
        "**Nasıl gönderilir:** Ölçüleri mesaja `KOD = değer` şeklinde yazın (örnek: `M05 = 2488`), "
        "milimetre cinsinden. Mümkünse şerit metrenin göründüğü bir fotoğraf ekleyin. "
        "Fotoğraflar public GitHub'a yüklenmez; sadece değerler ve dosya özetleri (SHA-256) kaydedilir.",
        "",
        "**Referans durumu:** Araç düz zeminde, yakıt deposu yaklaşık yarım, bagaj boş, lastik basınçları "
        "normal. Bu durumu bir kez not edin (U-008).",
        "",
        "## 1. Şerit metre ölçüleri (gövde geometrisini belirler)",
        "",
        "| Kod | Ölçü | Nasıl ölçülür | Şu anki durum |",
        "|---|---|---|---|",
    ]
    n = 0
    for pid, how in TAPE.items():
        n += 1
        lines.append(f"| M{n:02d} | {params[pid]['name']} (`{pid}`) | {how} | {st(pid)} |")
    lines += ["", "## 2. Biçim ölçüleri (şu an PLACEHOLDER varsayım)", "",
              "Koordinat: X = ön jant merkezinden **geriye** doğru yatay mesafe, Z = **yerden** yükseklik.", "",
              "| Kod | Ölçü | Nasıl ölçülür | Şu anki varsayım |", "|---|---|---|---|"]
    for key, how in SHAPE.items():
        n += 1
        a = asm[key]
        lines.append(f"| M{n:02d} | `{key}` | {how} | {a['value']} {a['unit'] or ''} (PLACEHOLDER) |")
    lines += ["", "## 3. Ruhsat bilgileri", "",
              "Ruhsatın fotoğrafını çekmeden önce **ad-soyad, TC kimlik no, adres ve plaka** alanlarını kapatın. "
              "Sadece aşağıdaki teknik alanlar gerekli; yazıyla göndermeniz de yeterli.", "",
              "| Kod | Ruhsat alanı | Spec parametresi |", "|---|---|---|"]
    for i, (field, pids) in enumerate(RUHSAT, 1):
        lines.append(f"| R{i:02d} | {field} | `{pids}` |")
    lines += ["", "## 4. İstenen fotoğraflar", ""]
    lines += [f"{i}. {t}" for i, t in enumerate(PHOTOS, 1)]
    unknown = sum(1 for p in params.values() if p["status"] == "UNKNOWN")
    est = sum(1 for p in params.values() if p["status"] == "ESTIMATED")
    lines += ["", "## Özet", "",
              f"Spec: {len(params)} parametre: {est} ESTIMATED, {unknown} UNKNOWN, 0 VERIFIED. "
              f"Varsayım dosyası: {len(asm)} PLACEHOLDER değer. "
              "Bu rehberdeki ölçüler geldikçe ilgili parçalar PLACEHOLDER'dan DRAFT'a geçer.", ""]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        ok = OUT.exists() and OUT.read_text(encoding="utf-8") == text
        print("OLCUM_REHBERI.md is " + ("up to date" if ok else "STALE"))
        return 0 if ok else 1
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
