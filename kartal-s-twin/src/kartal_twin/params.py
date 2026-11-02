"""Parameter resolution with provenance tracking (D-013).

Builders never read the YAML directly; they ask a Resolver. The Resolver returns the
spec value when it is ESTIMATED/VERIFIED, otherwise a placeholder assumption if one
exists, otherwise raises UnknownParameter - and records which provenance every value
had, so the geometry status of each part is derived mechanically, not claimed.
"""
from __future__ import annotations

from pathlib import Path

import yaml

from . import PROJECT_ROOT
from .spec import iter_parameters, load_spec

ASSUMPTIONS_PATH = PROJECT_ROOT / "specs" / "placeholder_assumptions.yaml"
# Best achievable geometry status for each provenance. VALIDATED is never automatic.
_STATUS_FOR = {"VERIFIED": "DRAFT", "ESTIMATED": "DRAFT", "PLACEHOLDER": "PLACEHOLDER"}


class UnknownParameter(KeyError):
    """Raised when geometry needs a value that is UNKNOWN and has no placeholder."""


def load_assumptions(path: Path = ASSUMPTIONS_PATH) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["assumptions"]


class Resolver:
    def __init__(self, spec: dict | None = None, assumptions: dict | None = None):
        self.spec = spec if spec is not None else load_spec()
        self.assumptions = assumptions if assumptions is not None else load_assumptions()
        self._params = dict(iter_parameters(self.spec))
        self._replacing = {a["replaces"]: k for k, a in self.assumptions.items() if a.get("replaces")}
        self.used: dict[str, str] = {}

    def fork(self) -> "Resolver":
        """Fresh usage record sharing the same data (one per component)."""
        r = Resolver.__new__(Resolver)
        r.spec, r.assumptions, r._params, r._replacing = self.spec, self.assumptions, self._params, self._replacing
        r.used = {}
        return r

    def get(self, key: str):
        p = self._params.get(key)
        if p is not None and p["status"] != "UNKNOWN":
            self.used[key] = p["status"]
            return p["value"]
        alt = self._replacing.get(key)
        if p is not None and alt is not None:
            self.used[key] = "PLACEHOLDER"
            return self.assumptions[alt]["value"]
        if p is None and key in self.assumptions:
            if self.assumptions[key].get("replaces"):
                raise KeyError(f"{key} stands in for {self.assumptions[key]['replaces']} - read that spec key")
            self.used[key] = "PLACEHOLDER"
            return self.assumptions[key]["value"]
        raise UnknownParameter(f"{key} is UNKNOWN and has no placeholder - geometry cannot be built")

    def absorb(self, other: "Resolver") -> None:
        """Inherit another resolver's usage (for values derived from shared layout)."""
        self.used.update(other.used)

    @property
    def geometry_status(self) -> str:
        if not self.used:
            return "PLACEHOLDER"
        return "PLACEHOLDER" if "PLACEHOLDER" in self.used.values() else _STATUS_FOR["ESTIMATED"]
