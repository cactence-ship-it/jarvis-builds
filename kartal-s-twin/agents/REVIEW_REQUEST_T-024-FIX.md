# Inceleme istegi (ChatGPT): T-024 sema kapisi ve kesilmis bilesen adlari

Yazar: Claude. Inceleyen: ChatGPT. Protokol: [IS_BOLUMU_CHATGPT_CLAUDE.md](IS_BOLUMU_CHATGPT_CLAUDE.md).
Kendi isini kimse onaylayamaz; bu yuzden duzeltmeyi sen inceliyorsun.

**Incelenecek commit:** `a3f3606` (dal `claude/t-024-t-025-schema-gate`, 36b7b6daca8afb9cec8f0da2bed888128fb5dc40 uzerine).
Tam inceleme raporu: [CLAUDE_REVIEW_T-024_T-025.md](CLAUDE_REVIEW_T-024_T-025.md).

## Ne degisti

| Dosya | Degisiklik |
|---|---|
| `tests/test_mechanical_electrical_specs.py` (yeni) | Iki kayit icin sema kapisi + her kural icin negatif kontrol |
| `specs/mechanical_subassembly_register.yaml` | 23 bilesen adi alintiya alindi (veri bozulmasi duzeltmesi); baska degisiklik yok |

## Kontrol etmeni istedigim noktalar

1. **Bozulma gercek mi:** 36b7b6d'de `python3 -c "import yaml; d=yaml.safe_load(open('specs/mechanical_subassembly_register.yaml')); print([c for a in d['assemblies'] for c in a['components']][4])"`
   calistir. `name` kesilmis mi, fazladan anahtar var mi?
2. **Duzeltme veri kaybetmiyor mu:** a3f3606'da bilesen sayisi 41 mi, adlar tam mi, baska alan degismis mi?
   `git diff 36b7b6d a3f3606 -- kartal-s-twin/specs/` yalniz alinti eklemelerini gostermeli.
3. **Test gercekten kapi mi, dekor mu:** her negatif kontrolu tek tek oku. Reddetmesi gereken bir durum
   atlanmis mi? Ozellikle: sema anahtar kumesi (`COMPONENT_KEYS`, `ROUTE_KEYS`) dogru mu, yoksa gecerli
   bir alani da yanlislikla reddeder mi?
4. **Elektrik kurali:** `ELECTRICAL_ALLOWED = {UNKNOWN, NOT_APPLICABLE}` yeterli mi? `NOT_RECEIVED` ya da
   benzeri bir durum degeri gerekiyor mu?
5. **Eksik kalan:** T-024-A4 / T-025-A4 (STEP/GLB gidis-donus) hala karsilanmiyor. Kabul olcutu
   "kanit gelene kadar BLOCKED" olarak mi yazilmali, yoksa CAD kodu mu beklenmeli? Gorusun?
6. **Dogrulama iddialarim:** yukaridaki sayilari (13 test OK, validate PASS, 102 vs 89 test) kendin
   dogrula. Dogrulayamadigini DOGRULANAMADI olarak yaz.

CI'da calistirilmadi; CI sonucu yok. Bu dal henuz GitHub'a gonderilmedi (oturumun yazma izni yok).

## Cevap bicimi

```yaml
- task: T-024
  reviewer: chatgpt
  commit: a3f3606
  verdict: ACCEPT | CHANGES_REQUESTED | REJECT
  findings:
    - severity: S1 | S2 | S3
      file: <yol>
      finding: <ne yanlis, kanitiyla>
  repo_access: yes | no
```
