"""Vehicle configuration rules (D-026): keep the carburettor engine variant separate from
fuel-injected variants. Rules live in specs/configuration_rules.yaml; values in the spec."""
from __future__ import annotations

from pathlib import Path

import yaml

from . import PROJECT_ROOT
from .spec import iter_parameters

RULES_PATH = PROJECT_ROOT / "specs" / "configuration_rules.yaml"


def load_rules(path: Path = RULES_PATH) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def check(spec: dict, rules: dict | None = None) -> list[str]:
    rules = rules if rules is not None else load_rules()
    params = dict(iter_parameters(spec))
    fs = params.get("engine.fuel_system_type") or {}
    if fs.get("status") == "UNKNOWN" or fs.get("value") is None:
        return []                                   # variant not known: nothing to separate yet
    excluded = (rules.get("engine_variant_exclusions") or {}).get(fs["value"], {})
    errs = []
    for pid, p in params.items():
        if not pid.startswith("engine.") or p.get("status") == "UNKNOWN":
            continue
        bad = [s for s in p.get("source") or [] if s in excluded]
        if bad:
            errs.append(f"{pid}: cites {bad} ({'; '.join(excluded[b] for b in bad)}), "
                        f"but the engine is '{fs['value']}'")
    return errs
