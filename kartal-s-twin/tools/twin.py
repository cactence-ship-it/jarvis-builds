#!/usr/bin/env python3
"""Project CLI.

  python tools/twin.py validate          all integrity rules + privacy scan (exit 1 on error)
  python tools/twin.py inventory         regenerate COMPONENT_INVENTORY.md from the YAML
  python tools/twin.py inventory --check fail if COMPONENT_INVENTORY.md is stale
  python tools/twin.py status            evidence-status counts per spec group / assembly
"""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from kartal_twin import INVENTORY_MD_PATH, PROJECT_ROOT, inventory, privacy, spec  # noqa: E402


def _repo_root() -> Path:
    import subprocess
    return Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=PROJECT_ROOT,
                               capture_output=True, text=True, check=True).stdout.strip())


def validate() -> int:
    ev = spec.load_evidence()
    s, m = spec.load_spec(), inventory.load_assembly()
    checks = {
        "evidence register": spec.validate_evidence(ev),
        "master spec": spec.validate_spec(s, ev),
        "component inventory": inventory.validate_assembly(m, ev),
        "inventory markdown in sync": [] if INVENTORY_MD_PATH.exists() and
        INVENTORY_MD_PATH.read_text(encoding="utf-8") == inventory.render_markdown(m)
        else ["COMPONENT_INVENTORY.md is stale - run: python tools/twin.py inventory"],
        "privacy (public repo)": privacy.scan_repository(_repo_root()),
    }
    failed = 0
    for name, errs in checks.items():
        print(f"[{'PASS' if not errs else 'FAIL'}] {name}" + (f" - {len(errs)} issue(s)" if errs else ""))
        for e in errs[:50]:
            print(f"       {e}")
        failed += bool(errs)
    c = spec.status_counts(s)
    n_comp = sum(1 for _ in inventory.iter_components(m))
    print(f"spec: {sum(c.values())} parameters (VERIFIED {c['VERIFIED']}, ESTIMATED {c['ESTIMATED']}, "
          f"UNKNOWN {c['UNKNOWN']}) | inventory: {n_comp} components | evidence: {len(ev)} items")
    return 1 if failed else 0


def write_inventory(check: bool) -> int:
    md = inventory.render_markdown(inventory.load_assembly())
    if check:
        ok = INVENTORY_MD_PATH.exists() and INVENTORY_MD_PATH.read_text(encoding="utf-8") == md
        print("COMPONENT_INVENTORY.md is " + ("up to date" if ok else "STALE"))
        return 0 if ok else 1
    INVENTORY_MD_PATH.write_text(md, encoding="utf-8")
    print(f"wrote {INVENTORY_MD_PATH.relative_to(PROJECT_ROOT)}")
    return 0


def status() -> int:
    s = spec.load_spec()
    for group, params in s["parameters"].items():
        c = Counter(p["status"] for p in params.values())
        print(f"{group:14s} V {c['VERIFIED']:3d}  E {c['ESTIMATED']:3d}  U {c['UNKNOWN']:3d}")
    m = inventory.load_assembly()
    for name, asm in m["assemblies"].items():
        g = sum(1 for c in asm["components"] if any(v != "NONE" for v in c["geometry"].values()))
        print(f"{name:18s} {len(asm['components']):3d} components, {g:3d} with geometry")
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "validate"
    if cmd == "validate":
        sys.exit(validate())
    if cmd == "inventory":
        sys.exit(write_inventory("--check" in sys.argv))
    if cmd == "status":
        sys.exit(status())
    sys.exit(__doc__)
