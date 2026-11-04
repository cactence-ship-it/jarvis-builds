#!/usr/bin/env python3
"""Ingest ORIGINAL reference files (photos, the legacy ZIP, document scans) unmodified.

    python3 tools/ingest_refs.py [--note TEXT] [--source TEXT] FILE [FILE ...]

Guarantees (D-008):
  * byte-identical copy into refs/original/<REF>_<name>, verified by SHA-256, set read-only;
  * SHA-256, size and provenance appended to refs/MANIFEST.csv (append-only);
  * never overwrites; a re-upload of an identical file is recognised by its hash and, if
    the local copy is missing (new cloud session), restored under its original REF id;
  * ZIP archives are integrity-tested and their member list written to
    refs/derived/<REF>_zip_listing.json (nothing is extracted here).

Standard library only, so it works before scripts/setup_env.sh has run.
While the repository is public, refs/original/ is git-ignored (privacy policy D-012):
originals then live only in this container and on the owner's phone.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ["ref_id", "stored_name", "original_name", "sha256", "bytes", "media_type",
          "ingested_utc", "storage", "source", "note"]
MEDIA = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".heic": "image/heic",
         ".webp": "image/webp", ".zip": "application/zip", ".pdf": "application/pdf",
         ".json": "application/json", ".html": "text/html"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def read_manifest(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def media_in_git_allowed(root: Path) -> bool:
    text = (root / "project.yaml").read_text(encoding="utf-8")
    m = re.search(r"^\s*allow_private_media_in_git:\s*(true|false)\b", text, re.M)
    return bool(m and m.group(1) == "true")


def _copy_verified(src: Path, dest: Path, digest: str) -> None:
    if dest.exists():
        raise SystemExit(f"refusing to overwrite existing file {dest}")
    shutil.copy2(src, dest)
    if sha256(dest) != digest:
        dest.unlink()
        raise SystemExit(f"copy verification failed for {src}")
    os.chmod(dest, 0o444)


def ingest(paths, root: Path = ROOT, source: str = "owner upload", note: str = "") -> list[dict]:
    refs = root / "refs"
    orig, derived, manifest = refs / "original", refs / "derived", refs / "MANIFEST.csv"
    orig.mkdir(parents=True, exist_ok=True)
    derived.mkdir(parents=True, exist_ok=True)
    rows = read_manifest(manifest)
    by_hash = {r["sha256"]: r for r in rows}
    next_n = max((int(r["ref_id"][2:]) for r in rows), default=0) + 1
    storage = "git" if media_in_git_allowed(root) else "local-only"
    results, new_rows = [], []
    for p in map(Path, paths):
        if not p.is_file():
            raise SystemExit(f"not a file: {p}")
        digest = sha256(p)
        if digest in by_hash:
            row = by_hash[digest]
            dest = orig / row["stored_name"]
            if dest.exists():
                results.append({"status": "duplicate", **row})
            else:
                _copy_verified(p, dest, digest)
                results.append({"status": "restored", **row})
            continue
        ref_id = f"R-{next_n:04d}"
        next_n += 1
        stored = f"{ref_id}_{re.sub(r'[^A-Za-z0-9._-]+', '_', p.name)}"
        dest = orig / stored
        _copy_verified(p, dest, digest)
        media = MEDIA.get(p.suffix.lower(), "application/octet-stream")
        if media == "application/zip":
            with zipfile.ZipFile(dest) as z:
                listing = {"ref_id": ref_id, "first_bad_member": z.testzip(),
                           "members": [{"name": i.filename, "bytes": i.file_size,
                                        "compressed": i.compress_size, "crc32": f"{i.CRC:08x}"}
                                       for i in z.infolist()]}
            (derived / f"{ref_id}_zip_listing.json").write_text(json.dumps(listing, indent=2))
        row = {"ref_id": ref_id, "stored_name": stored, "original_name": p.name,
               "sha256": digest, "bytes": str(p.stat().st_size), "media_type": media,
               "ingested_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               "storage": storage, "source": source, "note": note}
        by_hash[digest] = row
        new_rows.append(row)
        results.append({"status": "ingested", **row})
    if new_rows:
        write_header = not manifest.exists() or manifest.stat().st_size == 0
        with open(manifest, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            if write_header:
                w.writeheader()
            w.writerows(new_rows)
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("files", nargs="+")
    ap.add_argument("--source", default="owner upload via Claude Android")
    ap.add_argument("--note", default="")
    a = ap.parse_args()
    for r in ingest(a.files, source=a.source, note=a.note):
        print(f"{r['status']:9s} {r['ref_id']}  {r['sha256'][:16]}  {r['bytes']:>10s} B  {r['original_name']}")
    if not media_in_git_allowed(ROOT):
        print("NOTE: repository is public -> originals are NOT committed to GitHub (D-012). "
              "Keep the originals on your phone until private storage is decided (U-009).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
