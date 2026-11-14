import unittest

from code_atlas.core.blast_radius import blast_radius
from code_atlas.core.profile import ProfileError, build_profile_sections, lifecycle_of, validate_profile
from code_atlas.core.reporter import generate_report

FILES = {
    "os/a.py": {"raw_imports": ["sim.core", "sim.util"]},
    "os/b.py": {"raw_imports": ["sim.core"]},
    "os/old/c.py": {"raw_imports": ["sim.core"]},
    "os/d.py": {"raw_imports": ["shared"]},        # ambiguous: sim/shared.py or legacy/shared.py
    "sim/core.py": {"raw_imports": ["sim.util"]},  # intra-system edge: not a coupling pair
    "sim/util.py": {"raw_imports": []},
    "sim/shared.py": {"raw_imports": []},
    "legacy/shared.py": {"raw_imports": ["sim.core"]},
}
PROFILE = {
    "profile_version": 1, "name": "t",
    "systems": {"OS": {"roots": ["os"]}, "Sim": {"roots": ["sim"]}},
    "lifecycle": {"active": ["os", "sim"], "archived": ["os/old", "legacy"]},
}


def _report():
    report = generate_report("/nonexistent/project", dict(FILES), [])
    report.update(build_profile_sections(report, validate_profile(PROFILE), {"name": "t"}, set()))
    return report


class TestLifecycle(unittest.TestCase):
    def test_longest_declared_prefix_wins_and_rest_is_undeclared(self):
        decl = validate_profile(PROFILE)["lifecycle"]
        self.assertEqual(lifecycle_of("os/old/c.py", decl), "archived")
        self.assertEqual(lifecycle_of("os/a.py", decl), "active")
        self.assertEqual(lifecycle_of("tools/x.py", decl), "undeclared")

    def test_invalid_lifecycle_rejected(self):
        for bad in ({"dormant": ["os"]}, {"active": ["os"], "archived": ["os"]}, {"active": "os"}):
            with self.assertRaises(ProfileError):
                validate_profile({**PROFILE, "lifecycle": bad})

    def test_lifecycle_section_counts(self):
        life = _report()["lifecycle"]
        self.assertEqual(life["claim_type"], "declared")
        self.assertEqual(life["file_counts"], {"active": 6, "retired": 0, "archived": 2, "undeclared": 0})


class TestSystemCoupling(unittest.TestCase):
    def test_pair_edges_shares_and_lifecycle(self):
        pairs = {(p["from"], p["to"]): p for p in _report()["system_coupling"]["pairs"]}
        os_sim = pairs[("OS", "Sim")]
        self.assertEqual(os_sim["edges"], 4)  # a->core, a->util, b->core, old/c->core
        self.assertEqual(os_sim["edges_by_source_lifecycle"], {"active": 3, "archived": 1})
        self.assertEqual([(r["file"], r["share_percent"]) for r in os_sim["source_files"]],
                         [("os/a.py", 50.0), ("os/b.py", 25.0), ("os/old/c.py", 25.0)])
        self.assertEqual(os_sim["target_files"][0], {"file": "sim/core.py", "lifecycle": "active",
                                                     "edges": 3, "share_percent": 75.0})
        self.assertNotIn(("Sim", "Sim"), pairs)

    def test_possible_edges_kept_apart(self):
        pairs = {(p["from"], p["to"]): p for p in _report()["system_coupling"]["pairs"]}
        self.assertEqual(pairs[("OS", "Sim")]["possible_edges"], 1)
        self.assertEqual(pairs[("OS", "Sim")]["possible"][0]["candidates"], ["sim/shared.py"])
        outside = pairs[("OS", "(outside declared systems)")]
        self.assertEqual((outside["edges"], outside["possible_edges"]), (0, 1))
        self.assertEqual(outside["source_files"], [])

    def test_blast_radius_reports_dependent_lifecycle(self):
        r = blast_radius(_report(), "sim/core.py")
        self.assertEqual(r["confirmed"]["os/old/c.py"], {"system": "OS", "lifecycle": "archived"})
        self.assertEqual(r["confirmed"]["legacy/shared.py"]["system"], "(outside declared systems)")
        self.assertEqual(r["confirmed_by_lifecycle"], {"active": 2, "archived": 2})


if __name__ == "__main__":
    unittest.main()
