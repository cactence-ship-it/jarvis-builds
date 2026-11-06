# VEH-01 secondary-source research note — 2026-11-06

**Vehicle under study:** 1997 Tofaş Kartal S, owner-reported carburettor + petrol/LPG.
**Purpose:** identify candidate subsystems and variant conflicts before detailed CAD.
**Evidence class:** secondary web/catalogue sources only. This note does not promote any dimension, part number, or architecture to VERIFIED.

## 1. Executive findings

1. Public parts catalogues expose distinct M131/Kartal engine, transmission, steering/suspension, brake, cooling, electrical and ignition product families. They support a parts checklist, not exact geometry or automatic vehicle-specific fitment.
2. The **engine architecture** for the 1997 Kartal S carburettor build is much better supported than its exact engine code: trim/year-specific sources describe Kartal S (1994–1998) with the Tempra-family overhead-cam carburettor engine, and describe the S motor as electronic ignition and approximately 86 hp DIN. This supports a provisional **SOHC 8-valve** CAD architecture.
3. The exact code is still **UNKNOWN**. Code 131.D2.016 is clearly listed for Şahin S in one engine table and supplier listing; the sources do not establish that it is the exact stamped code on a 1997 Kartal S. Other charts place 131.D1.016 with some Kartal/Doğan SL/SLX applications, and source year/trim mappings conflict. Keep D1/D2 as family candidates, not the vehicle's confirmed code.
4. Power and torque values also conflict: the Kartal S community engine post reports about 86 hp DIN; the D2.016 Şahin S record gives 92 hp SAE / 123 Nm SAE; several 1997 Kartal S marketplace records show 1,581 cc, 83 hp and 131 Nm. A generic 1995–2001 Kartal 1.6 carburettor database gives 81 bhp, 1,585 cc, 86.4 × 67.4 mm and 8.3:1. These are not equivalent measurement standards/configurations; do not select a single output or internal geometry as VERIFIED.
5. The owner's carburettor statement and engine-bay photographs remain the vehicle-specific control evidence. For early CAD, use SOHC 8V as the leading provisional architecture but keep block code, bore/stroke, compression, ignition subtype and all internal geometry UNKNOWN.
6. A Valeo catalogue's 179A9098 record is explicitly Kartal 1.6 IE (1997–2002); exclude its ECU, injector/throttle-body and injection-only loom geometry from the default carburettor model.
7. Aftermarket catalogues list both hydraulic- and dry-steering kits. The owner photo shows a power-steering-labelled cap and hoses, supporting hydraulic assist, but pump identity, steering gear, geometry and hose routing remain unverified.
8. Brake catalogues show front disc/pad and rear shoe/adjuster families; this is an inspection checklist only, not proof of the hardware installed on this car. Keep brake geometry PLACEHOLDER.
9. Transmission catalogues expose clutch release bearing, propeller-shaft support, universal-joint, rear-axle bearing and differential product families. They do not establish gearbox code, spline counts, shaft length, flange PCD or differential ratio.

### Trim-specific engine candidate: Kartal S / Tempra-family carburettor

The strongest applicable evidence is the trim/year statement that Kartal S used the Tempra-type overhead-cam carburettor engine during 1994–1998. The same forum post reports electronic ignition and approximately 86 hp DIN. A separate engine table places 131.D2.016 on Şahin S at 1,581 cc / SOHC 8V / 92 hp SAE / 123 Nm SAE; a supplier spark-plug-cable listing similarly ties D2.016 to Şahin S. Other secondary tables associate D1.016 with Kartal/Doğan SL/SLX family applications. These clues support an SOHC 8V family but do not identify the code stamped on VEH-01.

A pair of 1997 Kartal S marketplace records report 1,581 cc, 83 hp and 131 Nm, and dimensions of 4,396 × 1,642 × 1,496 mm, 2,490 mm wheelbase, 1,060 kg kerb weight and 52 L petrol tank. These are listing/database fields, not factory build records; use as corroborating model-level candidates only. Their tyre field says 175/70R14, while owner photo E-028 shows 185/65R14 86T on one tyre. The vehicle-specific tyre photo takes precedence for that pictured tyre; the other three remain unknown.

**Provisional CAD decision:** create the SOHC 8V carburettor branch as the leading working architecture. Keep exact code D1/D2/other unresolved; do not assign 131.D2.016 to the Kartal merely because it is listed for Şahin S. Preserve the 86 hp DIN / 83 hp listing / 92 hp SAE / 81 bhp generic figures as a conflict set. Do not import 1.6 i.e. hardware or fabricate internal dimensions.

Sources:
1. TofaşTeam, *Tofaşın motorları* — Kartal S Tempra-type OHC carburettor engine, 1994–1998, electronic ignition, approximately 86 hp DIN: https://www.tofasteam.com/konu-tofasin-motorlari-167?pid=9682
2. Doç. Dr. Ömer Aydın, *Tofaş Kartal model özellikleri* — S trim overhead-cam carburettor distinction; forum/blog secondary: https://dromeraydin.blogspot.com/2014/04/
3. Araç Pazarı, *Kartal 1988–2002 engine options* — D1/D2/OHV/IE variant split, secondary: https://aracpazari.com.tr/tofas/kartal/kartal-2-1988-2002
4. TürkAta, *Tofaş Kuş Serisi* — 131.D2.016 for Şahin S; D1.016 family records for Kartal/Doğan lines; model rows and trim associations require care: https://turkatav.org/ansiklopedi/tofas-kus-serisi
5. Tork Otomotiv, *Şahin S carburettor spark-plug cable* — cross-model 131.D2.016 / 1,581 cc record: https://torkotomotiv.com/products/tofas-sahin-s-karburatorlu-performans-buji-kablosu
6. Arabam.com 1997 Kartal S listing records — listing-sourced 1,581 cc / 83 hp / 131 Nm / 52 L and model dimensions; not OEM certification: https://www.arabam.com/ilan/sahibinden-satilik-tofas-kartal-s/sahibinden-tofas-kartal-s-1997-model/41307998
7. Carbrands, generic Kartal 1.6 81 bhp carburettor record (not S-specific; aggregated public-source data): https://carbrands.com.tr/motor/tofas/kartal/tofas-kartal/1-6-81-bg-1995-2001
8. Valeo Service, *Kartal 1.6 IE* — separate injection variant, 179A9098: https://www.valeoservice.com.tr/tr/techassist/vehicle/P-9951

### Engine-specific blockers

- Engine block serial/code and casting marks, photographed square-on and readable.
- Both sides of engine, head/rocker-cover profile, timing cover and distributor.
- Carburettor manufacturer/model stamp, base flange, choke and throttle linkage.
- Distributor body/cap/trigger and ignition coil labels.
- Exact vehicle registration fields for engine capacity/type, cross-checked against physical stamp.

**Important:** the 86.4 × 67.4 mm values above are secondary database data for one 81 hp record. They are not accepted as VEH-01 dimensions without matching engine identification. Do not use the 179A9098 IE code for the owner's carburettor vehicle merely because the model year overlaps.

## 3. Catalogued subsystem families

### Steering and suspension
Otiva's Kartal (1985–2002) category exposes shock absorber mounts, steering boots, steering box/pump, dampers, anti-roll bar, tie rods, coil springs, suspension bushes, axles, ball joints and wheel bearings. Otomehmet's Kartal front-suspension category separately lists complete front kits for hydraulic steering and dry steering. These catalogues support a component checklist and prove that steering variants exist; they do not define exact geometry or fitment for a 1997 S.

### Gearbox and driveline
Otomehmet's Kartal gearbox category lists synchronizer springs, clutch release bearing, propeller-shaft support set, universal joint, rear axle bearing set and differential cover. These categories support separate CAD IDs for clutch, gearbox, shaft support, U-joints, differential and axle. All interfaces, dimensions and ratios remain UNKNOWN.

### Brakes
Aktaş's Kartal brake category lists front discs/pads, rear brake shoes and rear adjuster hardware, master cylinder, booster hose, pressure regulator and parking-brake components. Otiva's catalogue also exposes pad, disc, hose and master-cylinder groups. Treat these as parts-family references only; verify actual front caliper/disc and rear drum/backing-plate hardware on the vehicle before detailed solids.

### General parts taxonomy
Parcacim's M131 / SLX catalogue groups engine belts, cooling, alternator, suspension, ignition, brake and clutch/transmission categories, and exposes multiple engine options by year. This reinforces the need to keep model-year and engine-variant filters explicit in any part-number lookup.

### 1997 Kartal S listing cross-check — model dimensions and conflicting tyre / engine values

Several Arabam.com listings have EİDS-confirmed make/model/year metadata for 1997 Tofaş Kartal S and display common technical fields of 1,581 cc, 83 hp, 131 Nm, 4,396 mm length, 1,642 mm width, 1,496 mm height, 2,490 mm wheelbase, 1,060 kg kerb mass, 52 L fuel tank and 175/70R14 tyre size. These records are useful as S-trim-specific corroboration, but engine power, tank capacity, tyre size and dimensions are marketplace/listing fields, not a manufacturer type-approval sheet for VEH-01.

Cross-source comparison:
- The 4,396 mm length is consistent with a separate model-database record, while Carbrands lists 4,361 mm; keep overall length as a candidate conflict until an authoritative body drawing is found.
- The listing's 175/70R14 conflicts with the owner vehicle photo E-028, which visibly reads 185/65R14 86T on one pictured tyre. Use 185/65R14 only for that photographed tyre; do not assume the other three tyres match or that it is the approved homologation size.
- Listing engine values (1,581 cc / 83 hp / 131 Nm) conflict with the Kartal S engine chronology's approximately 86 hp DIN, the 131.D2.016 Şahin S cross-model data (92 hp SAE / 123 Nm SAE), and a generic 1995–2001 Kartal carburettor database entry (81 bhp / 124 Nm / 1,585 cc). Do not convert or average those outputs; keep them as separate source records.
- The listing's 52 L petrol tank capacity differs from a generic model database's 50 L. Neither is verified against VEH-01's tank label.

Sources:
1. Arabam.com, 1997 Kartal S, listing-derived specification record: https://www.arabam.com/ilan/sahibinden-satilik-tofas-kartal-s/sahibinden-tofas-kartal-s-1997-model/41307998
2. Arabam.com, second 1997 Kartal S listing with matching technical fields: https://www.arabam.com/ilan/sahibinden-satilik-tofas-kartal-s/sahibinden-tofas-kartal-s-1997-model/37965928
3. TofaşTeam, *Tofaş Kullanıcı Kılavuzu* — forum post states the 1996–2000 booklet covers Kartal S/SLX/SLX i.e.; the post points to a Fiat PDF. The PDF was not retrieved/read in this research pass, so do not use it for a specification claim: https://www.tofasteam.com/konu-tofas-kullanici-kilavuzu-pdf-formatinda-8468

### Additional hose supplier cross-reference

Narin Kauçuk's Kartal product list shows OEM-reference hose families for a Kartal 1.6: radiator inlet/outlet 7584255/7584256, thermostat 4339938, bypass 4339937, engine-ventilation 4476231 and air-filter hose 4221427. This is a useful third supplier cross-reference alongside MES and YTT. The extracted product list does not show a 1997 year range or explicit S-trim engine-code applicability; it does **not** settle the MES/YTT year-filter conflict or prove individual-vehicle fitment.

Source: Narin Kauçuk, TOFAŞ / KARTAL product list: https://www.narinkaucuk.com.tr/urun_list%26model%3D709

### Rubber-hose catalogue cross-check — conflicting year filters (supplier catalogues; fitment not verified)

The MES KAUÇUK *MES Auto Hoses Catalogue*, TOFAŞ section (printed pp. 366–369), and YTT Automotive's online Kartal catalogue share several OEM references but do **not** share the same model-year coverage. This is a supplier-catalogue conflict, not proof of interchangeability or non-fitment.

| Hose family | MES reference / stated Kartal coverage | YTT reference / stated Kartal coverage | VEH-01 decision |
|---|---|---|---|
| Radiator upper | MES 2500; OEM 7584255; Kartal 1.6 1985–1996 | Y30100; OEM 7584255; Tofaş/Kartal 1985–2002 | Candidate for 1997; fitment conflict must be resolved by geometry/OEM confirmation |
| Radiator lower | MES 2501; OEM 7584256; Kartal 1.6 1985–1996 | Y30101; OEM 7584256; Tofaş/Kartal 1985–2002 | Candidate for 1997; fitment conflict must be resolved |
| Thermostat hose | MES 2504; OEM 4339938; Kartal 1.6 1985–1996 | Y30104; OEM 4339938; Tofaş/Kartal 1985–2002 | Candidate for 1997; fitment conflict must be resolved |
| Engine ventilation | MES 2505; OEM 85011144; Kartal 1.6 1985–1996 | Y30108; OEM 85011144; Tofaş/Kartal 1985–2002 | Candidate for 1997; verify shape/end diameters |
| Engine ventilation (alternate) | MES 2512; OEM 4476231; Kartal 1.6 1985–1996 | Y30106; OEM 4476231; Tofaş/Kartal 1985–2002 | Candidate for 1997; verify which branch/component the car uses |
| Carburettor choke hose | MES 2510; 7 mm × 27 cm; OEM 4333269; Kartal 1.6 1985–1996 | Y30112; OEM 4333269 / 7589463; Tofaş/Kartal 1985–2002 | Candidate for 1997; dimensions from MES are supplier-stated, still compare ends/shape |
| Brake-servo vacuum hose | MES 2514 / 2514A; 11 × 17 mm, 80 cm; OEM 14206880; Kartal 1.6 1985–1996 | Y30902; OEM 14206880; Tofaş/Kartal 1985–2002 | Candidate only; confirm servo/pump connections, routing and hose specification |
| Air-filter hose | MES 2511; OEM 4221427; Kartal 1.6 1985–1996 | No matching YTT record captured in this catalogue extract | Candidate only; geometry and 1997 coverage unresolved |
| Vacuum hose | MES 2516; 4 × 9 mm, 71 cm NBR; OEM 7616008; Kartal 1.6 1985–1996 | No matching YTT record captured in this catalogue extract | Candidate only; verify circuit and actual length |

Separate IE entries in MES (for example Doğan 1.6 IE radiator hoses 2550/2551/2552, OEM 7675992/7675991/7765734) are not to be substituted into VEH-01's owner-reported carburettor build. The exact engine subtype must remain unresolved until physical engine identification.

**Correct interpretation:** a YTT year range reaching 2002 is the supplier's declared model-year coverage for its listed OEM-reference family. YTT explicitly states that OEM codes and trademarks are shown for comparison only. The MES filter ending in 1996 is a narrower catalogue coverage statement. Neither database proves that the same hose shape fits every 1997 Kartal S carburettor variation. Do not order or promote a part to VERIFIED solely from either year filter. The best desk-based next action is cross-source OEM matching, followed by comparison with the actual hose routing/terminal shapes and written supplier confirmation.

Sources:
1. MES KAUÇUK, *MES Auto Hoses Catalogue*, TOFAŞ section, printed pp. 366–369 (PDF content lines record MES codes, OEM references and model-year filters): https://www.meskaucuk.com.tr/uploads/catalogue/MES%20AUTO%20HOSES%20Catalogue.pdf
2. YTT Automotive, Tofaş/Kartal hose catalogue; entries Y30100, Y30101, Y30104, Y30106, Y30108, Y30109, Y30110, Y30112, Y30113 and Y30902: https://www.yttotomotiv.com/tr/katalog/tofas/kartal

## 4. Evidence ranking and limits

- **Vehicle-specific evidence remains primary:** E-017 owner configuration; E-022 LPG label/tank photo; E-024 cabin; E-025 rear underbody; E-027 engine bay; E-028 tyre sidewall.
- **Manufacturer/supplier catalogue:** Valeo Service is useful for catalogue-scoped variant metadata, but the cited page is specifically the Kartal 1.6 IE listing.
- **Aftermarket catalogue:** Otiva, Otomehmet, Aktaş and Parcacim can identify saleable component families and compatibility filters. A product title such as "Doğan Şahin Kartal" is not a guaranteed 1997 S fitment or dimensional drawing.
- **Aggregated vehicle database / community sources:** Carbrands, Aracpazari and TofasTeam are corroborative clues only. Their year, power, engine-family and trim descriptions are not fully consistent; never resolve a conflict by choosing the most convenient source.

## 5. Source register

1. Carbrands, *Tofaş Kartal 1.6 (81 bg), 1995–2001* — secondary engine figures and carburettor label: https://carbrands.com.tr/motor/tofas/kartal/tofas-kartal/1-6-81-bg-1995-2001
2. Araç Pazarı, *Tofaş Kartal (1988–2002) motor seçenekleri* — OHV/SOHC/i.e. variant separation: https://aracpazari.com.tr/tofas/kartal/kartal-2-1988-2002
3. Valeo Service, *TOFAS KARTAL 1.6 IE* — 1997–2002, 1581 cc, code 179A9098; IE-specific record: https://www.valeoservice.com.tr/tr/techassist/vehicle/P-9951
4. Otiva, *Kartal suspension and steering catalogue* — product-family taxonomy: https://otiva.com.tr/yedek-parcalar/tofas/tofas-kartal/kategori/suspansiyon-direksiyon
5. Otomehmet, *Kartal front-suspension catalogue* — hydraulic/dry steering kits and front-end parts: https://www.otomehmetyedekparca.com/kategori/on-takim-44
6. Otomehmet, *Kartal gearbox catalogue* — clutch, shaft support, U-joint, axle bearing and differential categories: https://www.otomehmetyedekparca.com/kategori/sanziman-36
7. Aktaş Oto, *Kartal brake-system catalogue* — front discs/pads, rear shoes/adjusters and hydraulic parts: https://www.aktasotoyedekparca.com/kategori/fren-sistemi-7
8. Parcacim, *Şahin / Doğan / Kartal parts catalogue* — M131 family filters and category taxonomy: https://www.parcacim.tr/tofas/sahin-dogan-kartal
9. Tofaş Team forum, *Tofaş'ın motorları* — community account of S/SLX/IE engine-family years; low-confidence corroboration only: https://www.tofasteam.com/konu-tofasin-motorlari-167?pid=9682

## 6. Next engineering actions

1. Resolve the exact engine family from block stamp and component photos before modelling internals.
2. Photograph the front brake hardware, rear drum/backing plate, rear spring type, axle-link pickups, steering gear label and gearbox casting.
3. Capture gearbox code, clutch cover/disc markings, output flange and propeller-shaft joint/support arrangement.
4. For each candidate catalogue part, record manufacturer, full part number, model-year filter and engine/steering variant before adding it to the parts BOM.
5. Keep all exact dimensions UNKNOWN until physical measurement, matching workshop documentation or an unambiguous manufacturer drawing is captured.

**CAD gate:** this research note adds no VERIFIED geometry. Continue using neutral PLACEHOLDER envelopes for unmeasured systems; do not convert catalogue compatibility text into manufacturing dimensions.
