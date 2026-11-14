"""Tests for the optional scan profile and the repository structure diagram."""

import io
import json
import os
import re
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from code_atlas.core.profile import ProfileError, load_profile, validate_profile
from code_atlas.core.mermaid_exporter import (
    MermaidExportError,
    generate_repository_structure_mmd,
    generate_repository_structure_page,
)
from code_atlas.scanner import run_scan

# Any Mermaid flowchart link syntax: -->, ---, -.->, ==>, --text-->, ~~~, o--o, x--x
LINK_PATTERN = re.compile(r"(--|==|-\.|~~~)")

PEER_PROFILE = {
    "profile_version": 1,
    "name": "two peers",
    "systems": {
        "Alpha": {"roots": ["sys_a"], "components": {"core": ["sys_a/core"], "gates": ["sys_a/gates"]}},
        "Beta": {"roots": ["sys_b"], "components": {"kernels": ["sys_b/kernels"]}},
    },
    "externals": {"Remote \"Tool\"": {"description": "outside repo", "bridge_files": ["sys_a/core/bridge_*.py"]}},
}


def _write(root, rel, text="x = 1\n"):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


class TestProfileValidation(unittest.TestCase):
    def test_valid_profile_normalizes(self):
        p = validate_profile(PEER_PROFILE)
        self.assertEqual([s["name"] for s in p["systems"]], ["Alpha", "Beta"])
        self.assertEqual(p["externals"][0]["bridge_patterns"], ["sys_a/core/bridge_*.py"])

    def _bad(self, mutate):
        data = json.loads(json.dumps(PEER_PROFILE))
        mutate(data)
        with self.assertRaises(ProfileError):
            validate_profile(data)

    def test_rejects_invalid_profiles(self):
        self._bad(lambda d: d.update(profile_version=2))
        self._bad(lambda d: d.update(typo_key=1))
        self._bad(lambda d: d.update(systems={}))
        self._bad(lambda d: d["systems"]["Alpha"].update(roots=[]))
        self._bad(lambda d: d["systems"]["Alpha"].update(roots=["/abs/path"]))
        self._bad(lambda d: d["systems"]["Alpha"].update(roots=["../escape"]))
        self._bad(lambda d: d["systems"]["Beta"].update(roots=["sys_a/core"]))  # overlap
        self._bad(lambda d: d["systems"]["Alpha"]["components"].update(x=["sys_b"]))  # outside root
        self._bad(lambda d: d["systems"]["Alpha"].update(color="red"))
        self._bad(lambda d: d["externals"].update(Alpha={}))  # duplicate name

    def test_load_profile_errors_and_hash(self):
        tmp = tempfile.mkdtemp()
        try:
            with self.assertRaises(ProfileError):
                load_profile(os.path.join(tmp, "missing.json"))
            bad = os.path.join(tmp, "bad.json")
            with open(bad, "w", encoding="utf-8") as f:
                f.write("{not json")
            with self.assertRaises(ProfileError):
                load_profile(bad)
            good = os.path.join(tmp, "good.json")
            with open(good, "w", encoding="utf-8") as f:
                json.dump(PEER_PROFILE, f)
            _, prov = load_profile(good)
            self.assertEqual(len(prov["sha256"]), 64)
            self.assertEqual(prov["claim_type"], "declared")
        finally:
            shutil.rmtree(tmp)


class TestProfileScan(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.project = os.path.join(self.tmp, "proj")
        _write(self.project, "sys_a/core/engine.py", "import sys_b.kernels.k\n")
        _write(self.project, "sys_a/core/bridge_tool.py")
        _write(self.project, "sys_a/gates/gate.py")
        _write(self.project, "sys_a/loose.py")
        _write(self.project, "sys_b/kernels/k.py")
        _write(self.project, "sys_b/kernels/__init__.py", "")
        _write(self.project, "sys_b/__init__.py", "")
        _write(self.project, "misc/tool.py")
        self.profile_path = os.path.join(self.tmp, "profile.json")
        with open(self.profile_path, "w", encoding="utf-8") as f:
            json.dump(PEER_PROFILE, f)
        self.out = os.path.join(self.tmp, "out", "report.json")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _scan(self, **kw):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            run_scan(self.project, self.out, **kw)
        with open(self.out, encoding="utf-8") as f:
            return json.load(f)

    def test_no_profile_adds_no_sections(self):
        report = self._scan()
        for key in ("profile", "systems", "externals", "coverage"):
            self.assertNotIn(key, report)

    def test_profile_sections(self):
        report = self._scan(profile_path=self.profile_path)
        systems = {s["name"]: s for s in report["systems"]}
        self.assertEqual(set(systems), {"Alpha", "Beta"})
        alpha = systems["Alpha"]
        self.assertEqual(alpha["claim_type"], "declared")
        comps = {c["name"]: c["files"] for c in alpha["components"]}
        self.assertEqual(comps["core"], ["sys_a/core/bridge_tool.py", "sys_a/core/engine.py"])
        self.assertEqual(comps["gates"], ["sys_a/gates/gate.py"])
        self.assertEqual(alpha["unassigned_files"], ["sys_a/loose.py"])
        self.assertEqual(report["coverage"]["files_outside_declared_systems"], ["misc/tool.py"])
        ext = report["externals"][0]
        self.assertFalse(ext["scanned"])
        self.assertEqual(ext["bridge_files_in_scan"], ["sys_a/core/bridge_tool.py"])
        self.assertFalse(report["coverage"]["mechanisms"]["http"]["scanned"])
        self.assertEqual(len(report["profile"]["sha256"]), 64)
        # The profile must not alter scan relationships.
        baseline = self._scan()
        self.assertEqual(report["local_dependencies"], baseline["local_dependencies"])
        self.assertEqual(report["payload_handoffs"], baseline["payload_handoffs"])

    def test_invalid_profile_stops_before_output(self):
        with open(self.profile_path, "w", encoding="utf-8") as f:
            json.dump({"profile_version": 1, "systems": {}}, f)
        with self.assertRaises(SystemExit):
            self._scan(profile_path=self.profile_path)
        self.assertFalse(os.path.exists(self.out))

    def test_mermaid_requires_profile(self):
        with self.assertRaises(SystemExit):
            self._scan(mermaid_dir=os.path.join(self.tmp, "mmd"))
        self.assertFalse(os.path.exists(self.out))

    def test_structure_diagram(self):
        mdir = os.path.join(self.tmp, "mmd")
        report = self._scan(profile_path=self.profile_path, mermaid_dir=mdir)
        with open(os.path.join(mdir, "repository_structure.mmd"), encoding="utf-8") as f:
            mmd = f.read()
        body = [l for l in mmd.splitlines() if not l.lstrip().startswith("%%")]
        # Containment only: no link syntax anywhere in the diagram body.
        for line in body:
            self.assertIsNone(LINK_PATTERN.search(line), line)
        # Peers: both systems are subgraphs directly inside the repository subgraph.
        depth, peers = 0, []
        for line in body:
            s = line.strip()
            if s.startswith("subgraph "):
                depth += 1
                if depth == 2:
                    peers.append(s)
            elif s == "end":
                depth -= 1
        self.assertEqual(len(peers), 2)
        self.assertTrue(any("Alpha · system" in p for p in peers))
        self.assertTrue(any("Beta · system" in p for p in peers))
        # External sits outside the repository subgraph, with its quote escaped.
        ext_lines = [l for l in body if "external · not scanned" in l]
        self.assertEqual(len(ext_lines), 1)
        self.assertTrue(ext_lines[0].startswith("  x_"))
        self.assertIn("Remote #quot;Tool#quot;", ext_lines[0])
        self.assertIn("Source-level architectural map", mmd)
        # Deterministic for the same report.
        self.assertEqual(mmd, generate_repository_structure_mmd(report))
        page = generate_repository_structure_page(report, mmd)
        self.assertIn("```mermaid", page)
        self.assertIn(report["profile"]["sha256"], page)

    def test_diagram_requires_profile_sections(self):
        with self.assertRaises(MermaidExportError):
            generate_repository_structure_mmd({"project_name": "x", "files": {}})


if __name__ == "__main__":
    unittest.main()
