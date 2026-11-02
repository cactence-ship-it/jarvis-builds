"""Privacy guard for a PUBLIC repository (D-012).

Blocks commits that would publish private material: original photos/archives/scans,
Turkish registration plates, or personal e-mail addresses. Runs inside
`tools/twin.py validate`, which scripts/checkpoint.sh calls before every commit.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

import yaml

from . import PROJECT_CONFIG_PATH

# Turkish plate: province 01-81, then 1 letter + 4-5 digits | 2 letters + 3-4 | 3 letters + 2-3.
PLATE = re.compile(r"\b(?:0[1-9]|[1-7]\d|8[01])[ -]?"
                   r"(?:[A-Z][ -]?\d{4,5}|[A-Z]{2}[ -]?\d{3,4}|[A-Z]{3}[ -]?\d{2,3})\b")
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b")
ALLOWED_EMAILS = {"noreply@anthropic.com"}
MEDIA_EXT = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp", ".gif", ".bmp", ".tif",
             ".tiff", ".zip", ".7z", ".rar", ".tar", ".gz", ".mp4", ".mov", ".pdf"}


def load_policy(path: Path = PROJECT_CONFIG_PATH) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["privacy"]


def candidate_files(repo_root: Path) -> list[str]:
    """Tracked + untracked-but-not-ignored files: exactly what `git add -A` would commit."""
    out = subprocess.run(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                         cwd=repo_root, capture_output=True, check=True).stdout
    return sorted({p for p in out.decode().split("\0") if p})


def scan_text(text: str, where: str) -> list[str]:
    issues = []
    for n, line in enumerate(text.splitlines(), 1):
        for m in PLATE.finditer(line):
            issues.append(f"{where}:{n}: looks like a registration plate ('{m.group(0)}')")
        for m in EMAIL.finditer(line):
            if m.group(0).lower() not in ALLOWED_EMAILS:
                issues.append(f"{where}:{n}: personal e-mail address")
    return issues


def scan_repository(repo_root: Path, policy: dict | None = None) -> list[str]:
    policy = policy or load_policy()
    allow_media = bool(policy.get("allow_private_media_in_git"))
    allowlist = tuple(policy.get("media_allowlist") or ())
    issues = []
    for rel in candidate_files(repo_root):
        p = repo_root / rel
        if not p.is_file():
            continue
        if not allow_media and p.suffix.lower() in MEDIA_EXT and not rel.startswith(allowlist):
            issues.append(f"{rel}: private media type would be published (public repository)")
            continue
        if p.stat().st_size > 2_000_000:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        issues += scan_text(text, rel)
    return issues
