"""Privacy guard: the public repository must not receive private material (D-012)."""
import subprocess
import unittest
from pathlib import Path

from kartal_twin import PROJECT_ROOT, privacy


class Privacy(unittest.TestCase):
    def test_repository_is_clean(self):
        root = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=PROJECT_ROOT,
                                   capture_output=True, text=True, check=True).stdout.strip())
        self.assertEqual(privacy.scan_repository(root), [])

    def test_policy_blocks_media_while_public(self):
        self.assertFalse(privacy.load_policy()["allow_private_media_in_git"])

    def test_detects_plate_and_email(self):
        # Built at run time so that no plate-like string or address exists in this file.
        plate = "34" + " " + "ABC" + " " + "123"
        mail = "owner" + "@" + "example.com"
        self.assertEqual(len(privacy.scan_text(f"plate {plate}\ncontact {mail}", "x")), 2)

    def test_no_false_positive_on_engineering_text(self):
        text = "12 V 60 Ah battery, ISO 8855, BDY-001, R-0001, E-003, 2026-11-01, 4 x 100 mm"
        self.assertEqual(privacy.scan_text(text, "x"), [])


if __name__ == "__main__":
    unittest.main()
