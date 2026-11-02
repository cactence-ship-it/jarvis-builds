#!/usr/bin/env python3
"""Project CLI.

  python tools/twin.py validate          all integrity rules + privacy scan (exit 1 on error)
  python tools/twin.py inventory         regenerate COMPONENT_INVENTORY.md from the YAML
  python tools/twin.py inventory --check fail if COMPONENT_INVENTORY.md is stale
  python tools/twin.py status            evidence-status counts per spec group / assembly
  python tools/twin.py build             build + export + validate -> build/ (manifest.json)
  python tools/twin.py sync-inventory    copy built geometry statuses into the inventory
  python tools/twin.py privacy           privacy scan only (also gates WIP checkpoints)
  python tools/twin.py tasks             regenerate TASKS.md from tasks/*.yaml
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


def _manifest_ids() -> set[str]:
    import csv
    path = PROJECT_ROOT / "refs" / "MANIFEST.csv"
    if not path.exists():
        return set()
    with open(path, newline="", encoding="utf-8") as f:
        return {row["ref_id"] for row in csv.DictReader(f)}


def validate() -> int:
    ev = spec.load_evidence()
    s, m = spec.load_spec(), inventory.load_assembly()
    checks = {
        "evidence register": spec.validate_evidence(ev, _manifest_ids()),
        "master spec": spec.validate_spec(s, ev),
        "component inventory": inventory.validate_assembly(m, ev),
        "inventory markdown in sync": [] if INVENTORY_MD_PATH.exists() and
        INVENTORY_MD_PATH.read_text(encoding="utf-8") == inventory.render_markdown(m)
        else ["COMPONENT_INVENTORY.md is stale - run: python tools/twin.py inventory"],
        "privacy (public repo)": privacy.scan_repository(_repo_root()),
        "task registry": _task_errors(),
        "hash integrity (audit snapshots, refs manifest)": __import__("kartal_twin.hashes", fromlist=["x"]).failures(
            __import__("kartal_twin.hashes", fromlist=["x"]).verify_project()),
        "configuration (engine variant separation)": __import__(
            "kartal_twin.configuration", fromlist=["x"]).check(s),
        "dimensional consistency": [f"{r['id']} FAIL: {r['description']} (lhs {r['lhs']:.1f}, rhs {r['rhs']:.1f}, "
                                    f"tolerance {r['combined_tolerance']:.1f})"
                                    for r in __import__("kartal_twin.consistency", fromlist=["x"]).evaluate(s)
                                    if r["status"] == "FAIL"],
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


def _task_errors() -> list:
    from kartal_twin import tasks
    t = tasks.load_tasks()
    errs = tasks.validate(t)
    if tasks.BOARD_PATH.read_text(encoding="utf-8") != tasks.render_board(t) if tasks.BOARD_PATH.exists() else True:
        errs.append("TASKS.md is stale - run: python tools/twin.py tasks")
    if not tasks.JSON_PATH.exists() or tasks.JSON_PATH.read_text(encoding="utf-8") != tasks.export_json(t):
        errs.append("tasks/tasks.json is stale - run: python tools/twin.py tasks")
    return errs


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


def build() -> int:
    from kartal_twin import pipeline
    r = pipeline.run()
    c = r["checks"]
    print(f"parts {len(r['parts'])} | skipped assemblies {len(r['skipped_assemblies'])} | {r['seconds']} s")
    for e in r["errors"]:
        print("  ERROR", e)
    if not r["errors"]:
        print(f"STEP  solids {c['step']['solids_read']}/{c['step']['solids_written']} "
              f"vol err {c['step']['volume_rel_error']:.1e} valid {c['step']['valid']}")
        print(f"STL   triangles {c['stl']['triangles']} normal flips {c['stl']['normal_flips']}")
        print(f"GLB   triangles {c['glb']['triangles']} issues {c['glb']['issues']} bytes {c['glb']['bytes']}")
        print(f"mesh  open/inward bodies: {c['mesh_closed_outward']['failed_bodies']}")
    bad = r["errors"] or c["glb"]["issues"] or c["mesh_closed_outward"]["failed_bodies"] \
        or c["step"]["solids_read"] != c["step"]["solids_written"] or c["stl"]["normal_flips"]
    return 1 if bad else 0


def sync_inventory() -> int:
    import datetime
    import json
    from kartal_twin.pipeline import BUILD_DIR
    r = json.loads((BUILD_DIR / "manifest.json").read_text())
    upd = {p["id"]: (p["representation"], p["geometry_status"]) for p in r["parts"]}
    today = datetime.date.today().isoformat()
    changed = inventory.set_geometry(upd, today, "built by kartal_twin.pipeline from spec + placeholders")
    print(f"inventory updated for {len(changed)} components")
    return write_inventory(False)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "tasks":
        from kartal_twin import tasks as _t
        _tt = _t.load_tasks()
        _t.BOARD_PATH.write_text(_t.render_board(_tt), encoding="utf-8")
        _t.JSON_PATH.write_text(_t.export_json(_tt), encoding="utf-8")
        print("wrote TASKS.md and tasks/tasks.json")
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "privacy":
        issues = privacy.scan_repository(_repo_root())
        for i in issues:
            print("  ", i)
        print("[PASS] privacy" if not issues else f"[FAIL] privacy - {len(issues)} issue(s)")
        sys.exit(1 if issues else 0)
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        sys.exit(build())
    if len(sys.argv) > 1 and sys.argv[1] == "sync-inventory":
        sys.exit(sync_inventory())
    cmd = sys.argv[1] if len(sys.argv) > 1 else "validate"
    if cmd == "validate":
        sys.exit(validate())
    if cmd == "inventory":
        sys.exit(write_inventory("--check" in sys.argv))
    if cmd == "status":
        sys.exit(status())
    sys.exit(__doc__)
