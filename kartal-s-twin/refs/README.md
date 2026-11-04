# Reference files - preservation rules (D-008, D-012)

* `MANIFEST.csv` - append-only record of every original received: SHA-256, size, original
  name, time, storage. **Committed**, so integrity can be proven in every future session.
* `original/` - byte-identical, read-only copies, written only by `tools/ingest_refs.py`.
  **Git-ignored while the repository is public**: photos, the legacy ZIP and document scans
  are private and are not published without the owner's explicit authorisation.
* `derived/` - generated material (ZIP member listings, extractions, crops). Never edited
  by hand; git-ignored for the same reason, since it can contain private content.

Ingest (stdlib only, works before setup):

    python3 tools/ingest_refs.py --note "front view" /mnt/user-data/uploads/IMG_1234.jpg

Re-uploading the same file in a later session is recognised by its hash and restores the
local copy under its original `R-nnnn` id. Nothing is ever overwritten.
