"""Hook scripts fed real tool-input JSON. Run: python3 -m unittest discover tests"""

import json
import subprocess
import unittest
from pathlib import Path

HOOKS = Path(__file__).resolve().parent.parent / "hooks"


def run_hook(name, tool_input, tool="Bash"):
    payload = json.dumps({"tool_name": tool, "tool_input": tool_input, "cwd": "/nonexistent"})
    return subprocess.run(["bash", str(HOOKS / name)], input=payload, capture_output=True, text=True).returncode


class KnownFailingChecksTest(unittest.TestCase):
    def test_bash_write_to_allowlist_is_blocked(self):
        for cmd in [
            "echo AssertionError >> .claude/known-failing-checks",
            "sed -i 's/x/y/' proj/.claude/known-failing-checks",
            "printf 'Error\\n' | tee -a .claude/known-failing-checks",
        ]:
            self.assertEqual(run_hook("git-guard.sh", {"command": cmd}), 2, cmd)

    def test_unrelated_bash_is_allowed(self):
        self.assertEqual(run_hook("git-guard.sh", {"command": "make check"}), 0)

    def test_edit_to_allowlist_still_blocked(self):
        self.assertEqual(run_hook("no-skipped-tests.sh", {"file_path": "/p/.claude/known-failing-checks", "content": "x"}, "Write"), 2)


if __name__ == "__main__":
    unittest.main()
