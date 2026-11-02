#!/usr/bin/env python3
"""One-off privacy audit of the WHOLE git history (every blob ever committed on any ref).

    python tools/privacy_history_audit.py      -> prints findings (paths and kinds, never values)

Covers what the per-commit scan cannot: files that were committed and later deleted.
Exit code 1 if anything is found.
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from kartal_twin.privacy import MEDIA_EXT, scan_text  # noqa: E402


def main() -> int:
    root = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                               check=True).stdout.strip())
    objs = subprocess.run(["git", "rev-list", "--all", "--objects"], cwd=root, capture_output=True, text=True,
                          check=True).stdout.splitlines()
    seen, findings, blobs = set(), [], 0
    for line in objs:
        sha, _, path = line.partition(" ")
        if not path or sha in seen:
            continue
        seen.add(sha)
        kind = subprocess.run(["git", "cat-file", "-t", sha], cwd=root, capture_output=True, text=True).stdout.strip()
        if kind != "blob":
            continue
        blobs += 1
        if Path(path).suffix.lower() in MEDIA_EXT:
            findings.append(f"{path} (blob {sha[:10]}): private media type in history")
            continue
        data = subprocess.run(["git", "cat-file", "-p", sha], cwd=root, capture_output=True).stdout
        if len(data) > 2_000_000:
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        findings += [f"{i} (blob {sha[:10]})" for i in scan_text(text, path)]
    print(f"scanned {blobs} blobs across all refs; findings: {len(findings)}")
    for f in findings:
        print("  ", f)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
