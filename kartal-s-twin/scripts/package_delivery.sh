#!/usr/bin/env bash
# Build, validate, render and package everything the owner can open on Android into one ZIP.
#   bash scripts/package_delivery.sh   -> build/delivery/kartal_twin_<commit>.zip
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$ROOT"
PY=.venv/bin/python
$PY tools/twin.py build
$PY tools/render_preview.py
$PY tools/package_viewer.py
SHA="$(git rev-parse --short HEAD)"
D=build/delivery; rm -rf "$D/stage"; mkdir -p "$D/stage"
cp build/vehicle.step build/vehicle.stl build/vehicle.glb build/manifest.json "$D/stage/"
cp -r build/assemblies build/previews "$D/stage/"
cp build/viewer/kartal_viewer.html docs/OLCUM_REHBERI.md "$D/stage/"
cat > "$D/stage/BENIOKU.txt" <<TXT
Tofaş Kartal S (1997) dijital ikiz - teslim paketi (commit $SHA)

DURUM: Tüm parçalar PLACEHOLDER (varsayım). Ana ölçüler yayınlanmış kaynaklardan
TAHMİN (ESTIMATED); kaporta biçimi, renk ve detaylar gerçek araçtan DEĞİL.

kartal_viewer.html  Telefonda tarayıcıyla açın: döndür, yakınlaştır, patlatma, parça bilgisi
                    (internet gerekir: three.js CDN'den yüklenir)
vehicle.glb         Android 3D görüntüleyicilerde açılır (metre, Y yukarı, ön +Z)
assemblies/*.glb    Alt sistem önizlemeleri
vehicle.step        Mühendislik CAD (mm, araç koordinatları: X geri, Y sağ, Z yukarı)
vehicle.stl         Mesh (mm)
previews/*.png      Hazır görüntüler
manifest.json       Her parçanın kanıt durumu ve doğrulama sonuçları
OLCUM_REHBERI.md    Gerçek ölçüleri göndermek için rehber (M01..M31 kodları)
TXT
OUT="$D/kartal_twin_${SHA}.zip"; rm -f "$OUT"
(cd "$D/stage" && zip -qr "../$(basename "$OUT")" .)
unzip -tq "$OUT" && echo "packaged $OUT ($(du -h "$OUT" | cut -f1))"
