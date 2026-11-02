"""VEHICLE_MASTER component inventory: validation and Markdown rendering."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import yaml

from . import ASSEMBLY_PATH
from .spec import STATUSES, Evidence, primary_sources

ASSEMBLY_ORDER = (
    "BODY_ASSEMBLY", "EXTERIOR_TRIM", "GLAZING", "LIGHTING", "INTERIOR", "ENGINE",
    "TRANSMISSION", "DRIVETRAIN", "CHASSIS", "FRONT_SUSPENSION", "REAR_SUSPENSION",
    "STEERING", "BRAKING", "FUEL_SYSTEM", "EXHAUST", "ELECTRICAL", "WHEELS_AND_TIRES",
)
REPRESENTATIONS = ("visual", "cad", "mechanical")          # D-006: never mixed up
GEOMETRY_STATES = ("NONE", "PLACEHOLDER", "LEGACY_IMPORT", "DRAFT", "VALIDATED")
FITMENTS = ("CONFIRMED", "UNCONFIRMED", "ABSENT")
COMPONENT_FIELDS = ("id", "name", "fitment", "optional", "verification_status",
                    "source_refs", "geometry", "dependencies", "history", "notes")
ASSEMBLY_FIELDS = ("prefix", "phase", "description", "components")
_ID = re.compile(r"^([A-Z]{3})-(\d{3})$")


def load_assembly(path: Path = ASSEMBLY_PATH) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def iter_components(master: dict):
    for name, asm in (master.get("assemblies") or {}).items():
        for comp in asm.get("components") or []:
            yield name, asm, comp


def validate_assembly(master: dict, evidence: dict[str, Evidence]) -> list[str]:
    errs: list[str] = []
    if master.get("root") != "VEHICLE_MASTER":
        errs.append("assembly: root must be VEHICLE_MASTER")
    asms = master.get("assemblies") or {}
    if tuple(asms) != ASSEMBLY_ORDER:
        errs.append(f"assembly: assemblies must be exactly {ASSEMBLY_ORDER} in that order")
    prefixes = Counter(a.get("prefix") for a in asms.values())
    errs += [f"assembly: prefix {p} used {n} times" for p, n in prefixes.items() if n > 1]
    for name, asm in asms.items():
        missing = [f for f in ASSEMBLY_FIELDS if f not in asm]
        if missing:
            errs.append(f"{name}: missing fields {missing}")
    comps: dict[str, dict] = {}
    for name, asm, c in iter_components(master):
        cid = c.get("id", "?")

        def err(msg, cid=cid):
            errs.append(f"{cid}: {msg}")
        missing = [f for f in COMPONENT_FIELDS if f not in c]
        extra = [f for f in c if f not in COMPONENT_FIELDS]
        if missing or extra:
            err(f"missing fields {missing} / unknown fields {extra}")
            continue
        m = _ID.match(cid)
        if not m:
            err("id must look like ABC-001")
        elif m.group(1) != asm.get("prefix"):
            err(f"id prefix does not match assembly {name} ({asm.get('prefix')})")
        if cid in comps:
            err("duplicate component id")
        comps[cid] = c
        if c["fitment"] not in FITMENTS:
            err(f"fitment '{c['fitment']}' not in {FITMENTS}")
        if not isinstance(c["optional"], bool):
            err("optional must be true/false")
        if c["verification_status"] not in STATUSES:
            err(f"verification_status '{c['verification_status']}' not in {STATUSES}")
        for s in c["source_refs"]:
            if s not in evidence:
                err(f"source_ref {s} is not in EVIDENCE_REGISTER.md")
        if c["verification_status"] == "VERIFIED" and not primary_sources(c["source_refs"], evidence):
            err("VERIFIED requires a RECEIVED PHOTO/DOCUMENT/MEASUREMENT evidence item")
        if c["fitment"] == "CONFIRMED" and not primary_sources(c["source_refs"], evidence):
            err("fitment CONFIRMED requires a RECEIVED PHOTO/DOCUMENT/MEASUREMENT evidence item")
        geo = c["geometry"]
        if not isinstance(geo, dict) or tuple(geo) != REPRESENTATIONS:
            err(f"geometry must have exactly {REPRESENTATIONS}")
        else:
            for rep, state in geo.items():
                if state not in GEOMETRY_STATES:
                    err(f"geometry.{rep} '{state}' not in {GEOMETRY_STATES}")
        hist = c["history"]
        if not (isinstance(hist, list) and hist and
                all(isinstance(h, dict) and {"rev", "date", "change"} <= set(h) for h in hist)):
            err("history must be a non-empty list of {rev, date, change}")
    for cid, c in comps.items():
        for d in c.get("dependencies") or []:
            if d == cid:
                errs.append(f"{cid}: depends on itself")
            elif d not in comps:
                errs.append(f"{cid}: unknown dependency {d}")
    errs += _find_cycles(comps)
    return errs


def _find_cycles(comps: dict[str, dict]) -> list[str]:
    state: dict[str, int] = {}          # 1 = on stack, 2 = done
    errs: list[str] = []

    def visit(n: str, path: list[str]):
        state[n] = 1
        for d in comps[n].get("dependencies") or []:
            if d not in comps:
                continue
            if state.get(d) == 1:
                errs.append("dependency cycle: " + " -> ".join(path[path.index(d):] + [d]))
            elif state.get(d) is None:
                visit(d, path + [d])
        state[n] = 2

    for n in comps:
        if n not in state:
            visit(n, [n])
    return errs


def render_markdown(master: dict) -> str:
    rows = list(iter_components(master))
    geo = Counter((rep, c["geometry"][rep]) for _, _, c in rows for rep in REPRESENTATIONS)
    status = Counter(c["verification_status"] for _, _, c in rows)
    out = [
        "# Component Inventory - VEHICLE_MASTER",
        "",
        "<!-- GENERATED from assembly/vehicle_master.yaml by `python tools/twin.py inventory`."
        " Do not edit by hand; edit the YAML and regenerate. -->",
        "",
        f"Source of truth: `assembly/vehicle_master.yaml` (revision {master.get('revision')}). "
        f"Components: **{len(rows)}** in **{len(master['assemblies'])}** assemblies.",
        "",
        "Verification status: " + ", ".join(f"{s} {status.get(s, 0)}" for s in STATUSES) + ".  ",
        "Geometry with any content (visual / CAD / mechanical): "
        + " / ".join(str(sum(n for (r, s), n in geo.items() if r == rep and s != 'NONE'))
                     for rep in REPRESENTATIONS) + ".",
        "",
        "Legend: fitment = CONFIRMED / UNCONFIRMED / ABSENT on this vehicle; `opt` = may not be"
        " fitted; geometry states NONE < PLACEHOLDER < LEGACY_IMPORT < DRAFT < VALIDATED.",
        "",
        "| Assembly | Prefix | Phase | Components |",
        "|---|---|---|---|",
    ]
    for name, asm in master["assemblies"].items():
        out.append(f"| {name} | {asm['prefix']} | {asm['phase']} | {len(asm['components'])} |")
    for name, asm in master["assemblies"].items():
        out += ["", f"## {name}", "", asm["description"].strip(), "",
                "| ID | Component | Fitment | Status | Visual | CAD | Mech | Depends on | Sources |",
                "|---|---|---|---|---|---|---|---|---|"]
        for c in asm["components"]:
            g = c["geometry"]
            out.append(
                f"| {c['id']} | {c['name']}{' (opt)' if c['optional'] else ''} | {c['fitment']} "
                f"| {c['verification_status']} | {g['visual']} | {g['cad']} | {g['mechanical']} "
                f"| {', '.join(c['dependencies']) or '-'} | {', '.join(c['source_refs']) or '-'} |")
    return "\n".join(out) + "\n"


def set_geometry(updates: dict[str, tuple[str, str]], date: str, change: str,
                 path=ASSEMBLY_PATH) -> list[str]:
    """Set geometry[representation] for components and append a history entry.

    updates: {component_id: (representation, new_state)}. Lines are rewritten in place
    (one flow mapping per component), so comments and layout are preserved. Returns the
    IDs actually changed; unchanged states do not add history.
    """
    text = Path(path).read_text(encoding="utf-8").split("\n")
    changed = []
    for i, line in enumerate(text):
        m = re.match(r"^(\s*- )(\{id: ([A-Z]{3}-\d{3}),.*\})$", line)
        if not m or m.group(3) not in updates:
            continue
        comp = yaml.safe_load(m.group(2))
        rep, state = updates[m.group(3)]
        if rep not in REPRESENTATIONS or state not in GEOMETRY_STATES:
            raise ValueError(f"bad update {m.group(3)}: {rep}={state}")
        if comp["geometry"][rep] == state:
            continue
        comp["geometry"][rep] = state
        comp["history"].append({"rev": max(h["rev"] for h in comp["history"]) + 1, "date": date,
                                "change": f"{rep} geometry -> {state}: {change}"})
        dumped = yaml.safe_dump(comp, default_flow_style=True, sort_keys=False, allow_unicode=True,
                                width=10**6).strip()
        text[i] = m.group(1) + dumped
        changed.append(m.group(3))
    Path(path).write_text("\n".join(text), encoding="utf-8")
    return changed
