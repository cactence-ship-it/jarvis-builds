"""Task registry rules (D-019): no self-approval, blockers named, acyclic, board in sync."""
import copy
import unittest

from kartal_twin import tasks


class TaskRegistry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.t = tasks.load_tasks()

    def test_registry_valid_and_board_in_sync(self):
        self.assertEqual(tasks.validate(self.t), [])
        self.assertEqual(tasks.BOARD_PATH.read_text(encoding="utf-8"), tasks.render_board(self.t))

    def _accepted(self, reviewer, same_commit=True):
        t = copy.deepcopy(self.t)
        r = t["T-001"]["results"][0]
        t["T-001"]["status"] = "accepted"
        t["T-001"]["finished_at"] = "2026-11-02T00:00:00Z"
        t["T-001"]["reviews"] = [{"reviewer": reviewer, "commit": r["commit"] if same_commit else "other",
                                  "verdict": "ACCEPT", "findings": []}]
        return tasks.validate(t)

    def test_self_approval_is_rejected(self):
        self.assertTrue(any("different agent" in e for e in self._accepted("claude")))

    def test_review_of_other_commit_is_rejected(self):
        self.assertTrue(any("different agent" in e for e in self._accepted("chatgpt", same_commit=False)))

    def test_independent_review_is_accepted(self):
        self.assertEqual(self._accepted("chatgpt"), [])

    def test_later_changes_request_blocks_acceptance(self):
        t = copy.deepcopy(self.t)
        r = t["T-001"]["results"][0]
        t["T-001"]["status"] = "accepted"
        t["T-001"]["finished_at"] = "2026-11-02T00:00:00Z"
        t["T-001"]["reviews"] = [
            {"reviewer": "chatgpt", "commit": r["commit"], "verdict": "ACCEPT", "findings": []},
            {"reviewer": "chatgpt", "commit": r["commit"], "verdict": "CHANGES_REQUESTED", "findings": ["x"]}]
        self.assertTrue(any("supersedes" in e for e in tasks.validate(t)))

    def test_accepted_requires_finished_at(self):
        t = copy.deepcopy(self.t)
        t["T-005"]["finished_at"] = None
        self.assertTrue(any("finished_at" in e for e in tasks.validate(t)))

    def test_json_export_maps_statuses(self):
        # Independent of the current registry content: set each status explicitly on a copy.
        import json
        t = copy.deepcopy(self.t)
        for tid, st in (("T-001", "submitted"), ("T-005", "accepted"), ("T-009", "blocked"),
                        ("T-003", "open"), ("T-013", "changes_requested")):
            t[tid]["status"] = st
        rows = {r["task_id"]: r for r in json.loads(tasks.export_json(t))["tasks"]}
        expect = {"T-001": "NEEDS_REVIEW", "T-005": "PASS", "T-009": "BLOCKED", "T-003": "TODO", "T-013": "FAILED"}
        for tid, ext in expect.items():
            self.assertEqual(rows[tid]["status"], ext, tid)

    def test_blocked_requires_named_blocker(self):
        t = copy.deepcopy(self.t)
        t["T-009"]["blocker"] = None
        self.assertTrue(any("blocker" in e for e in tasks.validate(t)))

    def test_dependency_cycle_detected(self):
        t = copy.deepcopy(self.t)
        t["T-001"]["depends_on"] = ["T-005"]                     # T-005 already depends on T-001
        self.assertTrue(any("cycle" in e for e in tasks.validate(t)))


if __name__ == "__main__":
    unittest.main()
