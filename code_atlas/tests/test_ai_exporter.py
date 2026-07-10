"""Unit and integration tests for Code Atlas AI-oriented architectural exporter."""

import json
import os
import shutil
import tempfile
import unittest

from code_atlas.scanner import run_scan
from code_atlas.core.ai_exporter import generate_ai_json, generate_ai_markdown

class TestAIExporter(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_existing_scanner_output_unchanged_with_no_flags(self):
        # 1. Verify no AI flags produces only normal reports and doesn't generate AI files
        project_dir = os.path.join(self.test_dir, "project")
        os.makedirs(project_dir, exist_ok=True)
        with open(os.path.join(project_dir, "main.py"), "w", encoding="utf-8") as f:
            f.write("if __name__ == '__main__': pass\n")
            
        output_json = os.path.join(self.test_dir, "report.json")
        run_scan(project_dir, output_json)
        
        # Verify standard outputs exist
        self.assertTrue(os.path.exists(output_json))
        self.assertTrue(os.path.exists(output_json.replace(".json", ".md")))
        
        # Verify AI outputs do NOT exist
        self.assertFalse(os.path.exists(output_json.replace(".json", ".ai.json")))
        self.assertFalse(os.path.exists(output_json.replace(".json", ".ai.md")))

    def test_independent_output_modes(self):
        # 2. Verify JSON-only and Markdown-only work independently
        project_dir = os.path.join(self.test_dir, "project")
        os.makedirs(project_dir, exist_ok=True)
        with open(os.path.join(project_dir, "main.py"), "w", encoding="utf-8") as f:
            f.write("if __name__ == '__main__': pass\n")
            
        output_json = os.path.join(self.test_dir, "report.json")
        
        # Markdown-only
        ai_md = os.path.join(self.test_dir, "report.ai.md")
        run_scan(project_dir, output_json, ai_output=ai_md)
        self.assertTrue(os.path.exists(ai_md))
        self.assertFalse(os.path.exists(ai_md.replace(".md", ".json")))
        
        # Cleanup
        os.remove(ai_md)
        
        # JSON-only
        ai_json = os.path.join(self.test_dir, "report.ai.json")
        run_scan(project_dir, output_json, ai_json_output=ai_json)
        self.assertTrue(os.path.exists(ai_json))
        self.assertFalse(os.path.exists(ai_json.replace(".json", ".md")))

    def test_byte_identical_stability_determinism(self):
        # 3. Repeated runs must produce byte-identical output (stable key sorting)
        source_report = {
            "project_name": "stable_project",
            "scanned_at": "2026-07-09T00:00:00Z",
            "limitations": [
                {"reason": "Z", "claim_type": "gap", "confidence": "high"},
                {"reason": "A", "claim_type": "gap", "confidence": "low"}
            ],
            "candidate_subsystem_groups": [
                {"name": "SubB", "claim_type": "inferred", "confidence": "medium", "member_files": ["b.py"], "grouping_basis": ["y", "x"]},
                {"name": "SubA", "claim_type": "inferred", "confidence": "high", "member_files": ["a.py"], "grouping_basis": ["w"]}
            ],
            "next_files_to_inspect": [
                {"filepath": "b.py", "score": 80, "reasons": ["R2", "R1"], "claim_type": "inferred"},
                {"filepath": "a.py", "score": 80, "reasons": ["R3"], "claim_type": "inferred"}
            ]
        }
        
        out1 = generate_ai_json(source_report, "standard")
        out2 = generate_ai_json(source_report, "standard")
        
        str1 = json.dumps(out1, sort_keys=True)
        str2 = json.dumps(out2, sort_keys=True)
        self.assertEqual(str1, str2)
        
        # Assert keys are sorted deterministically in list contents
        self.assertEqual(out1["limitations"][0]["reason"], "A")
        self.assertEqual(out1["limitations"][1]["reason"], "Z")
        self.assertEqual(out1["candidate_subsystems"][0]["name"], "SubA")
        self.assertEqual(out1["candidate_subsystems"][0]["grouping_basis"], ["w"])
        self.assertEqual(out1["candidate_subsystems"][1]["grouping_basis"], ["x", "y"])
        # Same score: sorted by path: a.py, then b.py
        self.assertEqual(out1["top_inspection_targets"][0]["filepath"], "a.py")
        self.assertEqual(out1["top_inspection_targets"][1]["filepath"], "b.py")

    def test_claim_type_isolation_and_route_groups(self):
        # 4. Check that different claim types are never merged, and grouped routes retain paths
        source_report = {
            "routes": [
                {
                    "entrypoint": "a.py",
                    "claim_type": "confirmed",
                    "route_files": ["a.py"],
                    "boundary_crossings": []
                },
                {
                    "entrypoint": "b.py",
                    "claim_type": "inferred",
                    "route_files": ["b.py"],
                    "boundary_crossings": []
                }
            ]
        }
        
        out = generate_ai_json(source_report, "standard")
        warnings = out["route_summaries"]["grouped_warnings"]
        
        # Should create 2 separate warning blocks, one for confirmed, one for inferred
        self.assertEqual(len(warnings), 2)
        self.assertEqual(warnings[0]["claim_type"], "confirmed")
        self.assertEqual(warnings[0]["affected_paths"], ["a.py"])
        self.assertEqual(warnings[1]["claim_type"], "inferred")
        self.assertEqual(warnings[1]["affected_paths"], ["b.py"])

    def test_schema_stability(self):
        # 5. Verify compact, standard, and full schemas are explicit and stable
        source_report = {
            "project_name": "schema_test",
            "files": {
                "main.py": {
                    "language": "python",
                    "role_hint": "cli",
                    "inbound_count": 0,
                    "outbound_count": 0,
                    "status": {"status": "likely_active", "claim_type": "confirmed"},
                    "inspection_score": 10
                }
            },
            "local_dependencies": [
                {"source": "main.py", "target": "helper.py", "claim_type": "inferred"}
            ],
            "routes": [
                {
                    "entrypoint": "main.py",
                    "claim_type": "inferred",
                    "route_files": ["main.py", "helper.py"],
                    "boundary_crossings": [{"from": "A", "to": "B", "file": "helper.py", "claim_type": "inferred"}],
                    "stubbed_files": [],
                    "unresolved_files": [],
                    "parse_error_files": [],
                    "next_file_to_inspect_in_route": "helper.py"
                }
            ]
        }
        
        # Test Compact
        compact = generate_ai_json(source_report, "compact")
        self.assertIn("contract", compact)
        self.assertIn("top_inspection_targets", compact)
        self.assertNotIn("boundary_crossings", compact)
        self.assertNotIn("route_summaries", compact)
        self.assertNotIn("files", compact)
        self.assertNotIn("local_dependencies", compact)
        
        # Test Standard
        standard = generate_ai_json(source_report, "standard")
        self.assertIn("boundary_crossings", standard)
        self.assertIn("route_summaries", standard)
        self.assertNotIn("files", standard)
        self.assertNotIn("local_dependencies", standard)
        
        # Test Full
        full = generate_ai_json(source_report, "full")
        self.assertIn("boundary_crossings", full)
        self.assertIn("route_summaries", full)
        self.assertIn("files", full)
        self.assertIn("local_dependencies", full)
        self.assertEqual(full["files"][0]["filepath"], "main.py")
        self.assertEqual(full["local_dependencies"][0]["target"], "helper.py")
