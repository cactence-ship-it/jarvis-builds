"""Engineering task registry (tasks/T-nnn.yaml): schema, cross-review rule, board rendering (D-019).

The registry is the persistent, idempotent task queue: one file per task, ID = file name,
history append-only. A task can be ACCEPTED only when an agent *other than the one that
produced the result* reviewed that same commit with verdict ACCEPT - self-approval is a
validation error, not a convention.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

from . import PROJECT_ROOT

TASKS_DIR = PROJECT_ROOT / "tasks"
BOARD_PATH = PROJECT_ROOT / "TASKS.md"
AGENTS = ("claude", "chatgpt", "owner")
STATUSES = ("open", "in_progress", "blocked", "submitted", "changes_requested", "accepted", "cancelled")
VERDICTS = ("ACCEPT", "CHANGES_REQUESTED", "REJECT")
CONFIDENCE = ("HIGH", "MEDIUM", "LOW")
FIELDS = ("id", "title", "phase", "owner", "status", "depends_on", "blocker", "acceptance",
          "results", "reviews")
_ID = re.compile(r"^T-\d{3}$")


def load_tasks(d: Path = TASKS_DIR) -> dict[str, dict]:
    out = {}
    for f in sorted(Path(d).glob("T-*.yaml")):
        t = yaml.safe_load(f.read_text(encoding="utf-8"))
        if t.get("id") != f.stem:
            raise ValueError(f"{f.name}: id {t.get('id')} does not match the file name")
        out[t["id"]] = t
    return out


def validate(tasks: dict[str, dict]) -> list[str]:
    errs = []
    for tid, t in tasks.items():
        e = lambda m, tid=tid: errs.append(f"{tid}: {m}")
        missing = [f for f in FIELDS if f not in t]
        if missing:
            e(f"missing fields {missing}")
            continue
        if not _ID.match(tid):
            e("id must look like T-001")
        if t["owner"] not in AGENTS:
            e(f"owner {t['owner']} not in {AGENTS}")
        if t["status"] not in STATUSES:
            e(f"status {t['status']} not in {STATUSES}")
        for d in t["depends_on"]:
            if d not in tasks:
                e(f"unknown dependency {d}")
        if t["status"] == "blocked" and not t["blocker"]:
            e("blocked tasks must name the exact blocker")
        if not t["acceptance"]:
            e("needs at least one acceptance criterion")
        for a in t["acceptance"]:
            if not {"id", "criterion", "check"} <= set(a):
                e("acceptance items need id, criterion and check")
        for r in t["results"]:
            if not {"agent", "commit", "files", "tests", "confidence", "known_defects"} <= set(r):
                e("result entries need agent, commit, files, tests, confidence, known_defects")
            elif r["agent"] not in AGENTS or r["confidence"] not in CONFIDENCE:
                e("result agent/confidence invalid")
        for v in t["reviews"]:
            if not {"reviewer", "commit", "verdict", "findings"} <= set(v):
                e("review entries need reviewer, commit, verdict, findings")
            elif v["verdict"] not in VERDICTS or v["reviewer"] not in AGENTS:
                e("review verdict/reviewer invalid")
        if t["status"] in ("submitted", "accepted") and not t["results"]:
            e(f"{t['status']} requires a recorded result")
        if t["status"] == "accepted":
            producers = {(r["agent"], r["commit"]) for r in t["results"]}
            ok = any(v["verdict"] == "ACCEPT" and (a, v["commit"]) in producers and v["reviewer"] != a
                     for v in t["reviews"] for (a, _) in producers)
            if not ok:
                e("accepted requires an ACCEPT review of the same commit by a different agent")
    # dependency cycles
    state: dict[str, int] = {}

    def visit(n, path):
        state[n] = 1
        for d in tasks[n].get("depends_on", []):
            if d in tasks and state.get(d) == 1:
                errs.append("task dependency cycle: " + " -> ".join(path + [d]))
            elif d in tasks and d not in state:
                visit(d, path + [d])
        state[n] = 2
    for n in tasks:
        if n not in state:
            visit(n, [n])
    return errs


def topo_order(tasks: dict[str, dict]) -> list[str]:
    done, order = set(), []

    def add(n):
        if n in done:
            return
        for d in tasks[n]["depends_on"]:
            add(d)
        done.add(n)
        order.append(n)
    for n in sorted(tasks):
        add(n)
    return order


def render_board(tasks: dict[str, dict]) -> str:
    lines = ["# Task Board - Kartal Jarvis", "",
             "<!-- GENERATED from tasks/*.yaml by `python tools/twin.py tasks`. Do not edit by hand. -->", "",
             "Dependency order. A task is ACCEPTED only after a review of the same commit by a different agent.", "",
             "| ID | Phase | Task | Owner | Status | Depends on | Blocker / last result |", "|---|---|---|---|---|---|---|"]
    for tid in topo_order(tasks):
        t = tasks[tid]
        last = t["results"][-1] if t["results"] else None
        note = t["blocker"] or (f"result {last['agent']}@{last['commit']} ({last['confidence']})" if last else "-")
        lines.append(f"| {tid} | {t['phase']} | {t['title']} | {t['owner']} | **{t['status']}** | "
                     f"{', '.join(t['depends_on']) or '-'} | {note} |")
    return "\n".join(lines) + "\n"
