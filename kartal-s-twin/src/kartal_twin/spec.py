"""Master specification and evidence register: loading and integrity rules (D-005).

The rules are enforced mechanically so that an estimate can never silently become
"verified", and an unknown can never silently acquire a number.
"""
from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import yaml

from . import EVIDENCE_PATH, SPEC_PATH

STATUSES = ("VERIFIED", "ESTIMATED", "UNKNOWN")
CONFIDENCES = ("HIGH", "MEDIUM", "LOW", "NONE")
EVIDENCE_TYPES = ("USER_STATEMENT", "PHOTO", "DOCUMENT", "MEASUREMENT",
                  "LEGACY_MODEL", "LITERATURE", "ENVIRONMENT_TEST")
EVIDENCE_STATES = ("RECEIVED", "RECORDED", "REPORTED", "NOT_RECEIVED", "SUPERSEDED")
# Only these evidence types, once RECEIVED (file checksummed in refs/MANIFEST.csv),
# can make a vehicle value VERIFIED. Owner statements alone give ESTIMATED at most.
PRIMARY_TYPES = ("PHOTO", "DOCUMENT", "MEASUREMENT")
UNITS = {"mm", "kg", "deg", "cm3", "kW", "N·m", "rpm", "L", "V", "Ah", "A", "in",
         "ratio", "turns", "%"}
FIELDS = ("name", "value", "unit", "status", "confidence", "tolerance", "source",
          "verify_by", "notes")
TOP_LEVEL = ("schema_version", "revision", "units", "coordinate_system", "parameters")

_ROW = re.compile(r"^\|\s*(E-\d{3})\s*\|(.*)\|\s*$")


@dataclass(frozen=True)
class Evidence:
    id: str
    title: str
    type: str
    state: str


def load_evidence(path: Path = EVIDENCE_PATH) -> dict[str, Evidence]:
    """Parse the evidence table rows (`| E-nnn | title | TYPE | STATE | ...`)."""
    out: dict[str, Evidence] = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        m = _ROW.match(line)
        if not m:
            continue
        cells = [c.strip().strip("`") for c in m.group(2).split("|")]
        ev = Evidence(m.group(1), cells[0], cells[1], cells[2])
        if ev.id in out:
            raise ValueError(f"duplicate evidence id {ev.id}")
        out[ev.id] = ev
    return out


def validate_evidence(evidence: dict[str, Evidence]) -> list[str]:
    errs = []
    for ev in evidence.values():
        if ev.type not in EVIDENCE_TYPES:
            errs.append(f"{ev.id}: evidence type '{ev.type}' not in {EVIDENCE_TYPES}")
        if ev.state not in EVIDENCE_STATES:
            errs.append(f"{ev.id}: evidence state '{ev.state}' not in {EVIDENCE_STATES}")
    return errs


def primary_sources(sources, evidence: dict[str, Evidence]) -> list[str]:
    """Evidence able to support VERIFIED (D-005, D-015).

    A received photo/document/measurement file, or an owner tape measurement whose values
    are RECORDED in evidence/measurements/ (the committed log is the artifact).
    """
    def ok(e: Evidence) -> bool:
        return (e.type in PRIMARY_TYPES and e.state == "RECEIVED") or \
               (e.type == "MEASUREMENT" and e.state == "RECORDED")
    return [s for s in sources if s in evidence and ok(evidence[s])]


def load_spec(path: Path = SPEC_PATH) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def iter_parameters(spec: dict):
    for group, params in (spec.get("parameters") or {}).items():
        for key, p in (params or {}).items():
            yield f"{group}.{key}", p


def _is_number(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _is_numeric(v) -> bool:
    return _is_number(v) or (isinstance(v, list) and bool(v) and all(map(_is_number, v)))


def validate_spec(spec: dict, evidence: dict[str, Evidence]) -> list[str]:
    errs = [f"spec: missing top-level key '{k}'" for k in TOP_LEVEL if k not in spec]
    for pid, p in iter_parameters(spec):
        def err(msg, pid=pid):
            errs.append(f"{pid}: {msg}")
        if not isinstance(p, dict):
            err("must be a mapping")
            continue
        missing = [f for f in FIELDS if f not in p]
        extra = [f for f in p if f not in FIELDS]
        if extra:
            err(f"unknown fields {extra}")
        if missing:
            err(f"missing fields {missing}")
            continue
        st, conf, val, unit, tol, src = (p[k] for k in
                                         ("status", "confidence", "value", "unit", "tolerance", "source"))
        if not isinstance(p["name"], str) or not p["name"].strip():
            err("name must be a non-empty string")
        if st not in STATUSES:
            err(f"status '{st}' not in {STATUSES}")
        if conf not in CONFIDENCES:
            err(f"confidence '{conf}' not in {CONFIDENCES}")
        if unit is not None and unit not in UNITS:
            err(f"unit '{unit}' not in allowed units")
        if not isinstance(src, list):
            err("source must be a list of evidence IDs")
            src = []
        for s in src:
            if s not in evidence:
                err(f"source {s} is not in EVIDENCE_REGISTER.md")
        if st == "UNKNOWN":
            if val is not None:
                err("UNKNOWN must have value: null (never fabricate a value)")
            if conf != "NONE":
                err("UNKNOWN must have confidence: NONE")
            if tol is not None:
                err("UNKNOWN must have tolerance: null")
            if not (isinstance(p["verify_by"], str) and p["verify_by"].strip()):
                err("UNKNOWN must state how it will be verified (verify_by)")
        elif st in ("ESTIMATED", "VERIFIED"):
            if val is None:
                err(f"{st} requires a value")
            if not src:
                err(f"{st} requires at least one evidence source")
            if conf == "NONE":
                err(f"{st} cannot have confidence NONE")
            if _is_numeric(val) and unit is not None:
                ok = _is_number(tol) and (tol > 0 if st == "ESTIMATED" else tol >= 0)
                if not ok:
                    err(f"{st} numeric value needs a tolerance (± {unit}); "
                        f"{'> 0' if st == 'ESTIMATED' else '>= 0'}")
        if st == "VERIFIED":
            if conf != "HIGH":
                err("VERIFIED requires confidence: HIGH")
            if not primary_sources(src, evidence):
                err("VERIFIED requires a RECEIVED PHOTO/DOCUMENT/MEASUREMENT evidence item "
                    "(owner statements alone are ESTIMATED at most)")
    return errs


def status_counts(spec: dict) -> Counter:
    return Counter(p.get("status") for _, p in iter_parameters(spec) if isinstance(p, dict))
