import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from code_atlas.core.blast_radius import blast_radius, blast_radius_counts, main
from code_atlas.core.reporter import generate_report

# c imports b, b imports a, pkg1/x imports a. d's "import x" is ambiguous (pkg1/x.py or pkg2/x.py);
# e imports d. broken.py did not parse.
FILES = {
    "a.py": {"raw_imports": []},
    "b.py": {"raw_imports": ["a"]},
    "c.py": {"raw_imports": ["b"]},
    "pkg1/x.py": {"raw_imports": ["a"]},
    "pkg2/x.py": {"raw_imports": []},
    "d.py": {"raw_imports": ["x"]},
    "e.py": {"raw_imports": ["d"]},
}


def _report():
    return generate_report("/nonexistent/project", dict(FILES),
                           [{"filepath": "broken.py", "error": "SyntaxError: invalid syntax (broken.py, line 1)"}])


class TestBlastRadius(unittest.TestCase):
    def test_direction_is_dependents_not_imports(self):
        r = _report()
        a = blast_radius(r, "a.py")
        self.assertEqual(a["confirmed_direct"], ["b.py", "pkg1/x.py"])
        self.assertEqual(sorted(a["confirmed"]), ["b.py", "c.py", "pkg1/x.py"])
        # c.py imports b and a transitively, but nothing depends on c.py.
        c = blast_radius(r, "c.py")
        self.assertEqual((c["confirmed"], c["possible"]), ({}, {}))

    def test_unresolved_import_is_possible_never_confirmed(self):
        r = _report()
        a = blast_radius(r, "a.py")
        # d.py's import of x may be pkg1/x.py (which imports a); e.py imports d.py.
        self.assertEqual(sorted(a["possible"]), ["d.py", "e.py"])
        self.assertFalse(set(a["possible"]) & set(a["confirmed"]))
        self.assertEqual([u["source"] for u in a["possible_via"]], ["d.py"])
        self.assertEqual(r["files"]["a.py"]["blast_radius"],
                         {"confirmed_direct": 2, "confirmed": 3, "possible": 2})
        self.assertEqual(r["files"]["a.py"]["inbound_count"], 2)

    def test_gaps_explain_incompleteness(self):
        a = blast_radius(_report(), "a.py")
        kinds = {g["kind"]: g for g in a["gaps"]}
        self.assertEqual(kinds["unparsed_files"]["files"], ["broken.py"])
        self.assertEqual(kinds["unresolved_imports"]["count"], 1)
        self.assertIn("untraced_mechanisms", kinds)
        self.assertIn("not a prediction of runtime failure", a["scope"])

    def test_http_gap_named_from_boundaries(self):
        b = {"inventory": {"incoming": [{"file": "a.py"}], "outgoing": []}}
        kinds = {g["kind"]: g for g in blast_radius(_report(), "a.py", b)["gaps"]}
        self.assertEqual(kinds["http_boundary"]["files"], ["a.py (1 routes)"])
        # a route served by a confirmed dependent (b.py) also counts
        b = {"inventory": {"incoming": [{"file": "b.py"}], "outgoing": []}}
        kinds = {g["kind"]: g for g in blast_radius(_report(), "a.py", b)["gaps"]}
        self.assertEqual(kinds["http_boundary"]["files"], ["b.py (1 routes)"])

    def test_counts_cover_every_file_and_cycles_terminate(self):
        r = generate_report("/nonexistent/project",
                            {"p.py": {"raw_imports": ["q"]}, "q.py": {"raw_imports": ["p"]}}, [])
        self.assertEqual(blast_radius_counts(r)["p.py"], {"confirmed_direct": 1, "confirmed": 1, "possible": 0})

    def test_cli_unknown_file_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "r.json")
            with open(path, "w") as fh:
                json.dump(_report(), fh)
            with redirect_stdout(io.StringIO()) as out, redirect_stderr(io.StringIO()):
                self.assertEqual(main(["--report", path, "--file", "missing.py"]), 1)
                self.assertEqual(main(["--report", path, "--file", "a.py"]), 0)
            self.assertIn("Confirmed dependents: 3", out.getvalue())


if __name__ == "__main__":
    unittest.main()
