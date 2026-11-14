import unittest

from code_atlas.core.reporter import (
    generate_report,
    resolve_import_to_local_file,
)


class TestUniqueSuffixLocalImportResolution(unittest.TestCase):
    def test_exact_root_relative_match(self):
        scanned_files = {"package/module.py"}

        self.assertEqual(
            resolve_import_to_local_file("package.module.Symbol", scanned_files),
            "package/module.py",
        )

    def test_unique_tier_prefixed_suffix(self):
        scanned_files = {"tier1/engainos/aproom/ap_engine.py"}

        self.assertEqual(
            resolve_import_to_local_file(
                "aproom.ap_engine.StateProvider", scanned_files
            ),
            "tier1/engainos/aproom/ap_engine.py",
        )

    def test_unique_single_module_suffix(self):
        scanned_files = {"tier1/engainos/runtime_client.py"}

        self.assertEqual(
            resolve_import_to_local_file(
                "runtime_client.NGATRTClient", scanned_files
            ),
            "tier1/engainos/runtime_client.py",
        )

    def test_unique_sibling_utility_suffix(self):
        scanned_files = {"interface/interface_common.py"}

        self.assertEqual(
            resolve_import_to_local_file(
                "interface_common.append_ledger", scanned_files
            ),
            "interface/interface_common.py",
        )

    def test_duplicate_suffix_is_ambiguous(self):
        scanned_files = {
            "tier1/alpha/shared/tool.py",
            "tier2/beta/shared/tool.py",
        }

        self.assertEqual(
            resolve_import_to_local_file("shared.tool.run", scanned_files),
            "AMBIGUOUS",
        )

    def test_ambiguous_report_gap_preserves_all_candidates(self):
        scanned_files = {
            "consumer.py": {"raw_imports": ["shared.tool.run"]},
            "tier1/alpha/shared/tool.py": {"raw_imports": []},
            "tier2/beta/shared/tool.py": {"raw_imports": []},
        }

        report = generate_report("/nonexistent/project", scanned_files, [])

        self.assertEqual(report["local_dependencies"], [])
        # A resolver limitation, not a source defect: never in parse_errors, never scored.
        self.assertEqual(report["parse_errors"], [])
        [ambiguity] = report["unresolved_imports"]
        self.assertEqual(ambiguity["source"], "consumer.py")
        self.assertEqual(ambiguity["kind"], "analysis_limitation")
        self.assertEqual(ambiguity["candidates"], ["tier1/alpha/shared/tool.py", "tier2/beta/shared/tool.py"])
        consumer = [r for r in report["next_files_to_inspect"] if r["filepath"] == "consumer.py"]
        self.assertEqual(len(consumer), 1)
        self.assertNotIn("parse_error", consumer[0]["reasons"])

    def test_parse_errors_split_into_defects_and_limitations(self):
        files = {"ok.py": {"raw_imports": []}}
        errors = [{"filepath": "bad.py", "error": "SyntaxError: invalid syntax (bad.py, line 3)"},
                  {"filepath": "binary.py", "error": "UnicodeDecodeError: 'utf-8' codec can't decode"}]
        report = generate_report("/nonexistent/project", files, errors)
        kinds = {e["filepath"]: e["kind"] for e in report["parse_errors"]}
        self.assertEqual(kinds, {"bad.py": "source_defect", "binary.py": "analysis_limitation"})
        scored = {r["filepath"]: r["score"] for r in report["next_files_to_inspect"]}
        self.assertEqual(scored.get("bad.py"), 100)
        self.assertNotIn("binary.py", scored)

    def test_no_target_import_remains_unresolved(self):
        scanned_files = {
            "tier1/engainos/aproom/authority_gate.py",
            "tier1/engainos/core/__init__.py",
        }

        self.assertIsNone(
            resolve_import_to_local_file(
                "core.authority_gate.evaluate", scanned_files
            )
        )

    def test_second_no_target_import_remains_unresolved(self):
        scanned_files = {"tier1/mrlore/gates/review.py"}

        self.assertIsNone(
            resolve_import_to_local_file(
                "engain_control.gate_result.GateResult", scanned_files
            )
        )

    def test_exact_match_precedes_unique_suffix_fallback(self):
        scanned_files = {
            "aproom/ap_engine.py",
            "tier1/engainos/aproom/ap_engine.py",
        }

        self.assertEqual(
            resolve_import_to_local_file(
                "aproom.ap_engine.StateProvider", scanned_files
            ),
            "aproom/ap_engine.py",
        )


if __name__ == "__main__":
    unittest.main()
