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
        ambiguity = next(
            error
            for error in report["parse_errors"]
            if "AmbiguousImportError" in error["error"]
        )
        self.assertIn("tier1/alpha/shared/tool.py", ambiguity["error"])
        self.assertIn("tier2/beta/shared/tool.py", ambiguity["error"])

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
