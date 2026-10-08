"""build-state on throwaway git repos: skipped pipeline steps, built-ness, quickies.

Each state change is tested in both directions. Run: python3 -m unittest discover tests
"""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

BUILD_STATE = Path(__file__).resolve().parent.parent / "bin" / "build-state"
PAGES_WORKFLOW = "jobs:\n  deploy:\n    steps:\n      - uses: actions/deploy-pages@v4\n"


def git(cwd, *args):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


class Repo:
    """A project folder with a bare 'origin' it is pushed to."""

    def __init__(self, base: Path):
        self.dir = base / "proj"
        self.dir.mkdir()
        origin = base / "origin.git"
        git(base, "init", "-q", "--bare", str(origin))
        git(self.dir, "init", "-q", "-b", "main")
        git(self.dir, "config", "user.email", "t@example.com")
        git(self.dir, "config", "user.name", "t")
        git(self.dir, "remote", "add", "origin", str(origin))

    def write(self, name, text):
        p = self.dir / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    def commit(self, push=True):
        git(self.dir, "add", "-A")
        git(self.dir, "commit", "-q", "-m", "x")
        if push:
            git(self.dir, "push", "-q", "-u", "origin", "main")

    def state(self):
        r = subprocess.run(["python3", str(BUILD_STATE), "--json", str(self.dir)],
                           capture_output=True, text=True, check=True)
        return json.loads(r.stdout)


SPEC = "- [{a}] **FR-1 — Thing one.** WHEN x\n- [{b}] **FR-2 — Thing two.** WHEN y\n"


class Pipeline(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.r = Repo(Path(self.tmp.name))

    def tearDown(self):
        self.tmp.cleanup()

    def test_skipped_design_does_not_gate(self):
        # BRIEF and EXPLORE, then straight to SPEC and PLAN: no DESIGN.md.
        self.r.write("BRIEF.md", "# Brief\n")
        self.r.write("EXPLORE.md", "# Explore\n")
        self.r.write("SPEC.md", SPEC.format(a="x", b=" "))
        self.r.write("PLAN.md", "- [x] **Task 1 — a**\n- [ ] **Task 2 — b**\n")
        self.r.write("src/main.py", "")
        self.r.commit()
        s = self.r.state()
        self.assertEqual(s["stage"], "build")
        self.assertEqual(s["skipped"], ["DESIGN.md"])
        # Reverse: add the design doc and nothing is skipped; the stage is unchanged.
        self.r.write("DESIGN.md", "# Design\n")
        s = self.r.state()
        self.assertEqual((s["stage"], s["skipped"]), ("build", []))

    def test_all_frs_ticked_is_built_even_if_plan_lags(self):
        self.r.write("BRIEF.md", "# Brief\n")
        self.r.write("EXPLORE.md", "# Explore\n")
        self.r.write("SPEC.md", SPEC.format(a="x", b="x"))
        self.r.write("PLAN.md", "- [x] **Task 1 — a**\n- [ ] **Task 2 — b**\n")
        self.r.write("src/main.py", "")
        self.r.commit()
        s = self.r.state()
        self.assertEqual(s["stage"], "deploy")  # built, no README, nothing deployed
        self.assertTrue(any("PLAN.md has 1 unticked" in w for w in s["warnings"]))
        # A README with nothing to deploy is the end.
        self.r.write("README.md", "# Proj\n")
        self.assertEqual(self.r.state()["stage"], "done")
        # Reverse: untick an FR and it's back in the build loop.
        self.r.write("SPEC.md", SPEC.format(a="x", b=" "))
        self.assertEqual(self.r.state()["stage"], "build")

    def test_deployed_without_readme_needs_complete(self):
        self.r.write("SPEC.md", SPEC.format(a="x", b="x"))
        self.r.write("PLAN.md", "- [x] **Task 1 — a**\n")
        self.r.write("compose.yml", "services: {}\n")
        self.r.commit()
        s = self.r.state()
        self.assertEqual(s["stage"], "complete")
        self.assertEqual(s["deployments"], ["compose.yml"])

    def test_assumed_gates_until_built_then_warns(self):
        self.r.write("SPEC.md", SPEC.format(a="x", b=" ") + "\n[ASSUMED] retry count\n")
        self.r.write("PLAN.md", "- [x] **Task 1 — a**\n")
        self.r.write("README.md", "# Proj\n")
        self.r.commit()
        self.assertEqual(self.r.state()["stage"], "audit")
        self.r.write("SPEC.md", SPEC.format(a="x", b="x") + "\n[ASSUMED] retry count\n")
        s = self.r.state()
        self.assertEqual(s["stage"], "done")
        self.assertTrue(any("1 [ASSUMED] tag nobody ruled on" in w for w in s["warnings"]))


class Quickie(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.r = Repo(Path(self.tmp.name))

    def tearDown(self):
        self.tmp.cleanup()

    def test_empty_folder_is_not_started(self):
        self.assertEqual(self.r.state()["stage"], "not-started")

    def test_roadmap_only_is_still_pipeline(self):
        self.r.write("ROADMAP.md", "# Roadmap\n")
        self.r.commit()
        s = self.r.state()
        self.assertEqual((s["stage"], s["track"]), ("not-started", "pipeline"))

    def test_shipped_needs_deployed_clean_pushed_and_todo_ticked(self):
        self.r.write("README.md", "# Proj\n\n## To do\n\n- [x] First\n- [ ] Second\n\n## Other\n\n- [ ] not a to-do\n")
        self.r.commit()
        s = self.r.state()
        self.assertEqual((s["stage"], s["track"]), ("quickie", "quickie"))
        self.assertEqual([(t["title"], t["done"]) for t in s["todo"]], [("First", True), ("Second", False)])

        self.r.write(".github/workflows/deploy.yml", PAGES_WORKFLOW)
        self.r.commit()
        self.assertEqual(self.r.state()["stage"], "quickie")  # still a to-do item open

        self.r.write("README.md", "# Proj\n\n## To do\n\n- [x] First\n- [x] Second\n")
        self.r.commit()
        s = self.r.state()
        self.assertEqual((s["stage"], s["track"], s["deployments"]), ("done", "quickie", ["GitHub Pages"]))

        # Reverse, one at a time: uncommitted work, unpushed commit, a new to-do item.
        self.r.write("scratch.txt", "x")
        self.assertEqual(self.r.state()["stage"], "quickie")
        self.r.commit(push=False)
        self.assertEqual(self.r.state()["stage"], "quickie")
        git(self.r.dir, "push", "-q")
        self.assertEqual(self.r.state()["stage"], "done")
        self.r.write("README.md", "# Proj\n\n## To do\n\n- [x] First\n- [x] Second\n- [ ] Third\n")
        self.r.commit()
        self.assertEqual(self.r.state()["stage"], "quickie")

    def test_no_todo_list_ships_on_deploy_alone(self):
        self.r.write("README.md", "# Proj\n")
        self.r.write("docker-compose.yml", "services: {}\n")
        self.r.commit()
        self.assertEqual(self.r.state()["stage"], "done")
        # Reverse: take the deployment away.
        (self.r.dir / "docker-compose.yml").unlink()
        self.r.commit()
        self.assertEqual(self.r.state()["stage"], "quickie")

    def test_never_pushed_is_not_shipped(self):
        self.r.write("README.md", "# Proj\n")
        self.r.write("compose.yml", "services: {}\n")
        self.r.commit(push=False)
        s = self.r.state()
        self.assertEqual(s["stage"], "quickie")
        self.assertTrue(any("no upstream" in d for d in s["detail"]))


if __name__ == "__main__":
    unittest.main()
