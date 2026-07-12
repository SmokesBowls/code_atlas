import unittest

from code_atlas.core.capability_grouper import get_role_hint, get_role_signals
from code_atlas.core.reporter import generate_report


class TestRoleClassificationSignals(unittest.TestCase):
    def test_client_filename_does_not_match_bare_cli_substring(self):
        self.assertEqual(
            get_role_hint("tier1/engainos/runtime_client.py", {"raw_imports": []}),
            "unknown",
        )

    def test_cli_filename_token_is_preserved(self):
        info = {"raw_imports": []}

        self.assertEqual(get_role_hint("tools/run_cli.py", info), "cli")
        self.assertEqual(
            get_role_signals("tools/run_cli.py", info)["cli_filename_tokens"],
            ["cli"],
        )

    def test_report_preserves_main_block_role_signal(self):
        files_data = {
            "runner.py": {
                "raw_imports": [],
                "functions": [],
                "_has_main_block": True,
                "_has_route_decorators": False,
                "_is_stub": False,
            }
        }

        report = generate_report("/nonexistent/project", files_data, [])

        self.assertEqual(report["files"]["runner.py"]["role_hint"], "cli")
        self.assertTrue(report["files"]["runner.py"]["role_signals"]["main_block"])
        self.assertNotIn("_has_main_block", report["files"]["runner.py"])

    def test_all_competing_role_signals_are_preserved(self):
        signals = get_role_signals(
            "tools/schema_config_helper.py",
            {"raw_imports": ["argparse"]},
        )

        self.assertTrue(signals["argparse_import"])
        self.assertEqual(signals["config_path_terms"], ["config"])
        self.assertEqual(signals["model_path_terms"], ["schema"])
        self.assertEqual(signals["utility_path_terms"], ["helper", "tool"])


if __name__ == "__main__":
    unittest.main()
