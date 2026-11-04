#!/usr/bin/env python3
"""Set fields of one parameter in specs/kartal_s_1997.yaml, preserving comments and layout.

    python tools/spec_set.py dimensions.wheelbase_lh value=2490 status=ESTIMATED \
        confidence=MEDIUM tolerance=10 source=E-009,E-008 notes="..."

Values are parsed as YAML scalars (numbers stay numbers). The result must still pass
`tools/twin.py validate`; this tool does not bypass any rule.
"""
import re
import sys
from pathlib import Path

import yaml

SPEC = Path(__file__).resolve().parents[1] / "specs" / "kartal_s_1997.yaml"
ORDER = ("name", "value", "unit", "status", "confidence", "tolerance", "source", "verify_by", "notes")


def _dump(v) -> str:
    return yaml.safe_dump(v, allow_unicode=True, default_flow_style=True, width=10**6).strip().removesuffix("...").strip()


def set_param(pid: str, updates: dict, path: Path = SPEC) -> None:
    group, key = pid.split(".")
    text = path.read_text(encoding="utf-8")
    g = re.search(rf"^  {re.escape(group)}:\n", text, re.M)
    if not g:
        raise SystemExit(f"group {group} not found")
    k = re.compile(rf"^    {re.escape(key)}:\n((?:      .*\n)+)", re.M).search(text, g.end())
    if not k:
        raise SystemExit(f"parameter {pid} not found")
    rec = yaml.safe_load(k.group(1).replace("\n      ", "\n").lstrip())
    for f in updates:
        if f not in ORDER:
            raise SystemExit(f"unknown field {f}")
    rec.update(updates)
    body = "".join(f"      {f}: {_dump(rec[f])}\n" for f in ORDER)
    path.write_text(text[:k.start(1)] + body + text[k.end(1):], encoding="utf-8")


def main(argv):
    pid, updates = argv[0], {}
    for a in argv[1:]:
        f, _, v = a.partition("=")
        updates[f] = [s for s in v.split(",") if s] if f == "source" else yaml.safe_load(v) if f not in ("notes", "verify_by", "name") else v
    set_param(pid, updates)
    print(f"updated {pid}: {updates}")


if __name__ == "__main__":
    main(sys.argv[1:])
