"""SHA-256 integrity verification (T-018) for audit snapshots and the reference manifest.

Checks every `audit/<date>/SHA256SUMS` and every row of `refs/MANIFEST.csv` whose file must be
present. Each entry gets one status: OK, MISMATCH (content changed), MISSING (file absent),
MALFORMED (unparseable line or manifest header), UNSAFE_PATH (absolute or escaping the snapshot
directory), EMPTY (a SHA256SUMS file without entries). A missing integrity file itself (no
refs/MANIFEST.csv, no audit/<date>/SHA256SUMS at all) is MISSING too: absence never reads as
clean (ChatGPT T-018 review, bf31d4d). Anything other than OK is a failure, except
NOT_PRESENT_LOCAL_ONLY for private originals (D-012).
"""
from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path, PurePosixPath

from . import PROJECT_ROOT

_LINE = re.compile(r"^([0-9a-f]{64})\s+\*?(.+)$")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _safe(rel: str) -> bool:
    pp = PurePosixPath(rel)
    return not pp.is_absolute() and ".." not in pp.parts and rel.strip() == rel and rel != ""


MANIFEST_COLUMNS = {"ref_id", "stored_name", "sha256", "storage"}


def verify_sums(sums_file: Path) -> list[dict]:
    if not sums_file.is_file():
        return [{"file": sums_file.name, "status": "MISSING"}]
    base = sums_file.parent
    out = []
    for n, line in enumerate(sums_file.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        m = _LINE.match(line)
        if not m:
            out.append({"file": f"{sums_file.name}:{n}", "status": "MALFORMED"})
            continue
        expected, rel = m.group(1), m.group(2)
        if not _safe(rel):
            out.append({"file": rel, "status": "UNSAFE_PATH"})
            continue
        p = base / rel
        if not p.is_file():
            out.append({"file": rel, "status": "MISSING"})
        else:
            got = sha256(p)
            out.append({"file": rel, "status": "OK" if got == expected else "MISMATCH",
                        "expected": expected, "actual": got})
    if not out:
        out.append({"file": sums_file.name, "status": "EMPTY"})
    return out


def verify_manifest(manifest: Path, originals: Path) -> list[dict]:
    """refs/MANIFEST.csv: rows stored in git must exist; any present file must match."""
    out = []
    if not manifest.is_file():
        return [{"file": manifest.name, "status": "MISSING"}]
    with open(manifest, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not MANIFEST_COLUMNS <= set(reader.fieldnames or []):
            return [{"file": manifest.name, "status": "MALFORMED"}]
        for row in reader:
            p = originals / row["stored_name"]
            if not _safe(row["stored_name"]):
                out.append({"file": row["stored_name"], "status": "UNSAFE_PATH"})
            elif not p.is_file():
                status = "MISSING" if row["storage"] == "git" else "NOT_PRESENT_LOCAL_ONLY"
                out.append({"file": row["stored_name"], "status": status})
            else:
                got = sha256(p)
                out.append({"file": row["stored_name"], "status": "OK" if got == row["sha256"] else "MISMATCH",
                            "expected": row["sha256"], "actual": got})
    return out


def verify_project(root: Path = PROJECT_ROOT) -> dict[str, list[dict]]:
    res = {}
    snapshots = sorted((root / "audit").glob("*/SHA256SUMS"))
    if not snapshots:                                  # at least one dated snapshot is expected (D-017)
        res["audit"] = [{"file": "audit/<date>/SHA256SUMS", "status": "MISSING"}]
    for sums in snapshots:
        res[str(sums.relative_to(root))] = verify_sums(sums)
    res["refs/MANIFEST.csv"] = verify_manifest(root / "refs" / "MANIFEST.csv", root / "refs" / "original")
    return res


def failures(results: dict[str, list[dict]]) -> list[str]:
    ok = {"OK", "NOT_PRESENT_LOCAL_ONLY"}            # local-only originals are private by design (D-012)
    return [f"{src}: {e['file']} {e['status']}" for src, entries in results.items() for e in entries
            if e["status"] not in ok]
