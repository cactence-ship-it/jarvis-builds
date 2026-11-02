"""Tofaş Kartal S (1997) digital twin - project package.

Only infrastructure lives here in Phase 1: integrity rules for the master spec and
registers, the component inventory, export re-open checks and the privacy guard.
Geometry builders live in kartal_twin.assemblies (one module per master assembly).
"""
from pathlib import Path

__version__ = "0.1.0"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = PROJECT_ROOT / "specs" / "kartal_s_1997.yaml"
ASSEMBLY_PATH = PROJECT_ROOT / "assembly" / "vehicle_master.yaml"
EVIDENCE_PATH = PROJECT_ROOT / "EVIDENCE_REGISTER.md"
INVENTORY_MD_PATH = PROJECT_ROOT / "COMPONENT_INVENTORY.md"
PROJECT_CONFIG_PATH = PROJECT_ROOT / "project.yaml"
REFS_DIR = PROJECT_ROOT / "refs"
