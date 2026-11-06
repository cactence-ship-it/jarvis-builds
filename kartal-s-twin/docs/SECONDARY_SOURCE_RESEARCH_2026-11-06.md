# VEH-01 secondary-source research note — 2026-11-06

**Vehicle under study:** 1997 Tofaş Kartal S, owner-reported carburettor + petrol/LPG.
**Purpose:** identify candidate subsystems and variant conflicts before detailed CAD.
**Evidence class:** secondary web/catalogue sources only. This note does not promote any dimension, part number, or architecture to VERIFIED.

## 1. Executive findings

1. Public sources agree that the M131/Kartal parts ecosystem has distinct engine, transmission, steering/suspension, brake, cooling, electrical and ignition product families. They are useful for building a parts checklist, not for recovering exact geometry.
2. The engine code on the individual vehicle remains **unverified**, but trim/year-specific evidence now makes a 1.6 SOHC 8-valve Tempra-family carburettor engine the leading working architecture for a 1997 Kartal S. A TofaşTeam community technical post associates Kartal S (1994–1998) with the Tempra-type overhead-cam engine and electronic ignition; a separate engine-family chronology associates the S/Tempra family with SOHC 8V. An engine-code/parts listing identifies 131.D2.016 as 1581 cc, carburettor, 92 hp for Şahin S and other secondary records associate the D2 family with Kartal. Treat 131.D2.016 as the leading code candidate, not a verified identification of VEH-01.
3. This trim-specific evidence is in tension with a generic aggregated Kartal 1.6 carburettor record (1995–2001) listing 81 hp, 1585 cc, 86.4 × 67.4 mm and 8.3:1; that generic record does not identify the S trim or block code. The 1.6 OHV family is described in other secondary sources as an earlier 1988–1994 configuration. A Valeo catalogue entry for Kartal 1.6 IE lists 179A9098 and 1997–2002, but it is explicitly an IE application and must not be assigned to this carburettor-reported vehicle.
4. The owner's carburettor statement and engine-bay photographs remain primary vehicle-specific evidence. For early CAD packaging, use SOHC 8V as the **leading provisional architecture** but keep the exact engine code, bore/stroke, compression ratio, ignition subtype and internals at candidate/UNKNOWN status until vehicle-specific identity evidence exists.
4. Aftermarket categories list both hydraulic- and dry-steering kits. The owner photo evidence indicates a belt-driven steering pump, supporting hydraulic steering on this vehicle, but rack/box code, geometry and hose routing remain unmeasured.
5. Catalogues list front discs/pads and rear brake shoes/adjusters across the Kartal family. This is a useful inspection checklist, not proof of the exact year/trim fitment or dimensions. Keep front/rear hardware geometry PLACEHOLDER until direct photos/measurements confirm it.
6. Transmission listings expose clutch release bearing, propeller-shaft support, universal joints, rear-axle bearing and differential-cover product families. They do not establish gearbox code, spline counts, prop-shaft length, flange PCD or differential ratio.

### Trim-specific engine candidate: Kartal S / Tempra-family carburettor

The 1997 model year alone is not enough to choose the engine architecture because broad database listings mix base Kartal, S/SL/SLX and IE records. The strongest trim-aware secondary clue is the TofaşTeam engine-family record that places the Tempra-type overhead-cam engine in Kartal S during 1994–1998. A parts listing maps code **131.D2.016** to the 1996–2000 Şahin S 1.6 carburettor at 1,581 cc / 92 hp; a separate engine chronology associates the D2 family with Kartal and SOHC 8V. These are supporting cross-model/secondary clues, not proof that this exact code is stamped on VEH-01.

**Provisional CAD decision:** prepare an SOHC 8V carburettor architecture branch as the leading working candidate, while keeping a configurable alternative and retaining all engine-block/head interface dimensions as UNKNOWN. Do not import 1.6 i.e. hardware. Do not set the engine identity to VERIFIED or use the candidate 92 hp / 123 Nm values as certified vehicle output.

Sources:
1. TofaşTeam, *Tofaşın motorları* — reports Kartal S use of Tempra-type overhead-cam engine, 1994–1998: https://www.tofasteam.com/konu-tofasin-motorlari-167?pid=9682
2. DonanımHaber, *Kuş Serisi Kronolojisi* — model/trim chronology and Kartal S distinction from SLX/IE: https://forum.donanimhaber.com/kus-serisi-kronolojisi--130285258
3. Tork Otomotiv, *Tofaş Şahin S carburettor spark-plug cable* — listing maps 131.D2.016 to 1,581 cc, 92 hp, carburettor, 1996–2000 (cross-model catalogue clue): https://torkotomotiv.com/products/tofas-sahin-s-karburatorlu-performans-buji-kablosu
4. TürkAta, *Tofaş Kuş Serisi* — secondary engine-family table associates 131.D2.016 with 1,581 cc SOHC 8V, 92 hp and Kartal family references: https://turkatav.org/ansiklopedi/tofas-kus-serisi
5. Carbrands, generic Kartal 1.6 81 hp carburettor record (not S-specific; public-source disclaimer): https://carbrands.com.tr/motor/tofas/kartal/tofas-kartal/1-6-81-bg-1995-2001

## 2. Engine / variant cross-check

| Candidate record | Secondary source says | Relevance to VEH-01 | CAD treatment |
|---|---|---|---|
| **Kartal S trim: 1.6 SOHC 8V carburettor / Tempra-family; 131.D2.016 leading code candidate** | TofaşTeam reports Kartal S 1994–1998 used the Tempra-type overhead-cam engine; engine chronology and supplier/parts listings associate 131.D2.016 with 1,581 cc SOHC 8V, carburettor, 92 hp and 123 Nm (source standards/trim mappings differ) | Best trim/year-specific working match for the owner's 1997 Kartal S + carburettor report; exact code on VEH-01 is not read | Use SOHC 8V architecture only as a provisional CAD envelope; keep code and internal geometry unverified |
| Kartal 1.6 carburettor, 1995–2001 (generic record) | 81 hp; 1,585 cc; bore 86.4 mm; stroke 67.4 mm; compression 8.3:1 | Generic Kartal listing may represent a different/base configuration; it does not identify the S trim or actual block code | Secondary candidate only; do not override the trim-specific SOHC candidate or dimension internal parts from this record |
| 1.6 OHV 84 hp (131.A1/A2) | Described as carburettor OHV, mainly 1988–1994 | Earlier family; less likely for a 1997 S, but not physically excluded by the available photos | Exclude from detailed CAD unless contrary vehicle-specific evidence identifies it |
| 1.6 SOHC 96 hp (131.D1 family) | Secondary sources associate D1 with some Kartal/Doğan SL/SLX applications; year/trim mappings vary | Alternative SOHC family record; not the leading S-specific D2 candidate | Keep as alternative configuration, not selected |
| 1.6 i.e. (179A9098 / 131.F3 family references) | Valeo lists Kartal 1.6 IE 1997–2002, 1,581 cc, 90 HP, 179A9098; other sources describe the 96 hp IE record | Important exclusion gate: does not match the owner-reported carburettor configuration | Separate injection variant; do not import ECU, injector/throttle-body or IE-only loom geometry |

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
