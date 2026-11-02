#!/usr/bin/env python3
"""Record the owner's tape measurements (codes from docs/OLCUM_REHBERI.md) as evidence.

    python tools/record_measurement.py --state "level ground, half tank, empty" \
        --tol 5 M05=2488 M06=2491 M20=955

For one measurement session this:
  1. writes evidence/measurements/<E-id>.yaml (values only; no photos, no personal data),
  2. appends an E-id row (MEASUREMENT, RECORDED) to EVIDENCE_REGISTER.md,
  3. sets each measured spec parameter to VERIFIED / HIGH with the given tolerance (D-015).
The project must still pass `tools/twin.py validate` afterwards; nothing bypasses the rules.
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import re
import sys
from pathlib import Path

import yaml

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS.parent / "src"))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, TOOLS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def next_evidence_id(register: Path) -> str:
    ids = [int(m) for m in re.findall(r"^\| E-(\d{3}) \|", register.read_text(encoding="utf-8"), re.M)]
    return f"E-{max(ids, default=0) + 1:03d}"


def record(root: Path, values: dict[str, float], tolerance: float, state: str,
           date: str | None = None, note: str = "") -> tuple[str, list[str]]:
    guide, spec_set = _load("measurement_guide"), _load("spec_set")
    code_map = guide.codes()
    unknown = [c for c in values if c not in code_map]
    if unknown:
        raise SystemExit(f"unknown measurement codes: {unknown} (see docs/OLCUM_REHBERI.md)")
    if tolerance <= 0:
        raise SystemExit("tolerance must be > 0 mm")
    date = date or dt.date.today().isoformat()
    register = root / "EVIDENCE_REGISTER.md"
    eid = next_evidence_id(register)
    log = {"id": eid, "date": date, "type": "MEASUREMENT", "method": "owner tape measurement",
           "reference_state": state, "tolerance_mm": tolerance, "note": note,
           "values": [{"code": c, "parameter": code_map[c], "value": v, "unit": "mm"}
                      for c, v in sorted(values.items())]}
    out = root / "evidence" / "measurements" / f"{eid}.yaml"
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        raise SystemExit(f"refusing to overwrite {out}")
    out.write_text(yaml.safe_dump(log, sort_keys=False, allow_unicode=True), encoding="utf-8")
    row = (f"| {eid} | Owner tape measurements ({len(values)} values) | MEASUREMENT | RECORDED | "
           f"evidence/measurements/{eid}.yaml | {date} | Reference state: {state.replace('|', '/')} |\n")
    text = register.read_text(encoding="utf-8")
    register.write_text(text.rstrip("\n") + "\n" + row, encoding="utf-8")
    changed = []
    for code, v in sorted(values.items()):
        pid = code_map[code]
        spec_set.set_param(pid, {"value": v, "status": "VERIFIED", "confidence": "HIGH",
                                 "tolerance": tolerance, "source": [eid],
                                 "notes": f"Owner tape measurement {date} ({code}); reference state in {eid}."},
                           path=root / "specs" / "kartal_s_1997.yaml")
        changed.append(pid)
    return eid, changed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("values", nargs="+", help="CODE=value in mm, e.g. M05=2488")
    ap.add_argument("--tol", type=float, default=5.0, help="measurement tolerance in mm (default 5)")
    ap.add_argument("--state", required=True, help="reference state (fuel, load, ground, tyres)")
    ap.add_argument("--date")
    ap.add_argument("--note", default="")
    ap.add_argument("--root", default=str(TOOLS.parent))
    a = ap.parse_args()
    vals = {}
    for item in a.values:
        code, _, v = item.partition("=")
        vals[code.strip().upper()] = float(v.replace(",", "."))
    eid, changed = record(Path(a.root), vals, a.tol, a.state, a.date, a.note)
    print(f"{eid}: {len(changed)} parameters VERIFIED -> {', '.join(changed)}")
    print("next: python tools/twin.py validate && python tools/twin.py build && "
          "python tools/twin.py sync-inventory && python tools/measurement_guide.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
