"""Tests for Code Atlas parser, entrypoint detection, status classification, capability grouping, ranking, routing, and reporting."""

import json
import os
import shutil
import tempfile
import unittest

from code_atlas.core.parser import parse_file, get_module_path
from code_atlas.core.reporter import generate_report, resolve_import_to_local_file, generate_markdown_report
from code_atlas.core.entrypoint_detector import detect_entrypoint
from code_atlas.core.status_classifier import classify_statuses
from code_atlas.core.capability_grouper import infer_subsystem_groups, get_role_hint
from code_atlas.core.ranking import calculate_inspection_rankings

class TestParserAndMetadata(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_module_path(self):
        self.assertEqual(get_module_path("foo/bar.py"), "foo.bar")
        self.assertEqual(get_module_path("foo/__init__.py"), "foo")

    def test_parse_signals(self):
        code = """
import argparse

@app.route('/api')
def handle():
    pass

if __name__ == '__main__':
    pass
"""
        file_path = os.path.join(self.test_dir, "app.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

        result = parse_file(file_path, self.test_dir)
        self.assertTrue(result["_has_main_block"])
        self.assertTrue(result["_has_route_decorators"])
        self.assertFalse(result["_is_stub"])

    def test_parse_stub(self):
        code = """
def my_func():
    raise NotImplementedError
"""
        file_path = os.path.join(self.test_dir, "stub.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

        result = parse_file(file_path, self.test_dir)
        self.assertTrue(result["_is_stub"])


class TestEntrypointAndStatus(unittest.TestCase):
    def test_detect_entrypoint(self):
        # 1. Main block
        info1 = {"_has_main_block": True, "raw_imports": []}
        is_entry, evidence = detect_entrypoint("some_file.py", info1)
        self.assertTrue(is_entry)

        # 2. Flask route
        info2 = {"_has_route_decorators": True, "raw_imports": []}
        is_entry, evidence = detect_entrypoint("some_file.py", info2)
        self.assertTrue(is_entry)

        # 3. Argparse import
        info3 = {"raw_imports": ["argparse"]}
        is_entry, evidence = detect_entrypoint("some_file.py", info3)
        self.assertTrue(is_entry)

        # 4. Standard name alone is NOT an entrypoint (Audit requirement)
        info4 = {"raw_imports": []}
        is_entry, evidence = detect_entrypoint("main.py", info4)
        self.assertFalse(is_entry)

    def test_status_classification(self):
        files_data = {
            "main.py": {
                "_has_main_block": True,
                "raw_imports": ["helper"]
            },
            "helper.py": {
                "raw_imports": []
            },
            "unimported.py": {
                "raw_imports": []
            },
            "stub.py": {
                "_is_stub": True,
                "raw_imports": []
            }
        }
        local_deps = [
            {"source": "main.py", "target": "helper.py", "type": "import"}
        ]
        
        statuses = classify_statuses(files_data, local_deps)
        
        self.assertEqual(statuses["main.py"]["status"], "likely_active")
        self.assertEqual(statuses["helper.py"]["status"], "likely_active")
        self.assertEqual(statuses["unimported.py"]["status"], "orphaned")
        self.assertEqual(statuses["stub.py"]["status"], "stubbed")


class TestReporterAndGrouping(unittest.TestCase):
    def test_get_role_hint(self):
        self.assertEqual(get_role_hint("models/user.py", {}), "model")
        self.assertEqual(get_role_hint("utils/helpers.py", {}), "utility")
        self.assertEqual(get_role_hint("tests/test_parser.py", {}), "test")
        self.assertEqual(get_role_hint("cli.py", {}), "cli")

    def test_infer_subsystem_groups(self):
        files_data = {
            "main.py": {
                "role_hint": "cli",
                "raw_imports": ["core.parser", "utils.helper"]
            },
            "core/parser.py": {
                "role_hint": "utility",
                "raw_imports": ["utils.helper"]
            },
            "utils/helper.py": {
                "role_hint": "utility",
                "raw_imports": []
            },
            "tests/test_main.py": {
                "role_hint": "test",
                "raw_imports": ["main"]
            }
        }
        
        local_deps = [
            {"source": "main.py", "target": "core/parser.py", "type": "import"},
            {"source": "main.py", "target": "utils/helper.py", "type": "import"},
            {"source": "core/parser.py", "target": "utils/helper.py", "type": "import"},
            {"source": "tests/test_main.py", "target": "main.py", "type": "import"}
        ]
        
        groups = infer_subsystem_groups(files_data, local_deps)
        group_names = {g["name"]: g for g in groups}
        
        self.assertIn("Root Components", group_names)
        self.assertIn("Core Subsystem", group_names)
        self.assertIn("Testing Suite", group_names)
        self.assertIn("Utilities Subsystem", group_names)

        self.assertEqual(group_names["Root Components"]["member_files"], ["main.py"])
        self.assertEqual(group_names["Utilities Subsystem"]["member_files"], ["utils/helper.py"])

        self.assertEqual(group_names["Root Components"]["internal_edge_count"], 0)
        self.assertEqual(group_names["Root Components"]["external_edge_count"], 3)

        self.assertEqual(
            group_names["Testing Suite"]["grouping_basis"],
            ["seed: test_role_hint", "refined_by: role_consolidation"]
        )

        self.assertEqual(group_names["Testing Suite"]["outbound_interface_files"], ["main.py"])
        self.assertEqual(group_names["Root Components"]["inbound_interface_files"], ["tests/test_main.py"])

    def test_structural_ambiguity(self):
        files_data = {
            "main.py": {
                "role_hint": "cli",
                "raw_imports": []
            },
            "core/file_a.py": {
                "role_hint": "unknown",
                "raw_imports": ["main"]
            },
            "core/file_b.py": {
                "role_hint": "unknown",
                "raw_imports": ["main"]
            }
        }
        local_deps = [
            {"source": "core/file_a.py", "target": "main.py", "type": "import"},
            {"source": "core/file_b.py", "target": "main.py", "type": "import"}
        ]

        groups = infer_subsystem_groups(files_data, local_deps)
        group_names = {g["name"]: g for g in groups}

        core_group = group_names["Core Subsystem"]
        self.assertTrue(core_group["structurally_ambiguous"])
        self.assertEqual(core_group["confidence"], "low")

    def test_named_control_center_with_concentrated_outbound_edges_is_cohesive(self):
        files_data = {
            "engainos/__init__.py": {"role_hint": "package_init", "raw_imports": []},
            "engainos/engainos_control_center.py": {"role_hint": "unknown", "raw_imports": []},
            "engainos/server.py": {"role_hint": "unknown", "raw_imports": []},
            "engainos/gates/a.py": {"role_hint": "unknown", "raw_imports": []},
            "engainos/gates/b.py": {"role_hint": "unknown", "raw_imports": []},
            "engainos/gates/c.py": {"role_hint": "unknown", "raw_imports": []},
        }
        local_deps = [
            {"source": "engainos/engainos_control_center.py", "target": "engainos/gates/a.py", "type": "import"},
            {"source": "engainos/engainos_control_center.py", "target": "engainos/gates/b.py", "type": "import"},
            {"source": "engainos/engainos_control_center.py", "target": "engainos/gates/c.py", "type": "import"},
        ]

        groups = infer_subsystem_groups(files_data, local_deps)
        engainos = next(group for group in groups if group["name"] == "Engainos Subsystem")

        self.assertFalse(engainos["structurally_ambiguous"])
        self.assertEqual(engainos["confidence"], "medium")
        self.assertTrue(any("Coordinator cohesion" in item for item in engainos["evidence"]))
        self.assertIn("refined_by: coordinator_outbound_concentration", engainos["grouping_basis"])

    def test_outbound_concentration_without_named_coordinator_remains_ambiguous(self):
        files_data = {
            "runner/a.py": {"role_hint": "unknown", "raw_imports": []},
            "runner/b.py": {"role_hint": "unknown", "raw_imports": []},
            "gates/x.py": {"role_hint": "unknown", "raw_imports": []},
            "gates/y.py": {"role_hint": "unknown", "raw_imports": []},
            "gates/z.py": {"role_hint": "unknown", "raw_imports": []},
        }
        local_deps = [
            {"source": "runner/a.py", "target": "gates/x.py", "type": "import"},
            {"source": "runner/a.py", "target": "gates/y.py", "type": "import"},
            {"source": "runner/a.py", "target": "gates/z.py", "type": "import"},
        ]

        groups = infer_subsystem_groups(files_data, local_deps)
        runner = next(group for group in groups if group["name"] == "Runner Subsystem")

        self.assertTrue(runner["structurally_ambiguous"])

    def test_single_qualifying_utility_stays_in_source_directory(self):
        files_data = {
            "shared/common.py": {"role_hint": "utility", "raw_imports": []},
            "alpha/use_common.py": {"role_hint": "unknown", "raw_imports": []},
            "beta/use_common.py": {"role_hint": "unknown", "raw_imports": []},
        }
        local_deps = [
            {"source": "alpha/use_common.py", "target": "shared/common.py", "type": "import"},
            {"source": "beta/use_common.py", "target": "shared/common.py", "type": "import"},
        ]

        groups = infer_subsystem_groups(files_data, local_deps)
        group_names = {group["name"]: group for group in groups}

        self.assertNotIn("Shared Utility Subsystem", group_names)
        self.assertEqual(
            group_names["Shared Subsystem"]["member_files"],
            ["shared/common.py"],
        )

    def test_multiple_qualifying_utilities_can_form_shared_group(self):
        files_data = {
            "alpha/common.py": {"role_hint": "utility", "raw_imports": []},
            "beta/helper.py": {"role_hint": "utility", "raw_imports": []},
            "one/use.py": {"role_hint": "unknown", "raw_imports": []},
            "two/use.py": {"role_hint": "unknown", "raw_imports": []},
        }
        local_deps = [
            {"source": "one/use.py", "target": "alpha/common.py", "type": "import"},
            {"source": "two/use.py", "target": "alpha/common.py", "type": "import"},
            {"source": "one/use.py", "target": "beta/helper.py", "type": "import"},
            {"source": "two/use.py", "target": "beta/helper.py", "type": "import"},
        ]

        groups = infer_subsystem_groups(files_data, local_deps)
        shared = next(group for group in groups if group["name"] == "Shared Utility Subsystem")

        self.assertEqual(shared["member_files"], ["alpha/common.py", "beta/helper.py"])

    def test_utility_toolbox_uses_external_consumer_cohesion(self):
        files_data = {
            "brushes/alpha.py": {"role_hint": "utility", "raw_imports": []},
            "brushes/beta.py": {"role_hint": "utility", "raw_imports": []},
            "brushes/__init__.py": {"role_hint": "package_init", "raw_imports": []},
            "editor/tool_a.py": {"role_hint": "unknown", "raw_imports": []},
            "runtime/tool_b.py": {"role_hint": "unknown", "raw_imports": []},
        }
        local_deps = [
            {"source": "editor/tool_a.py", "target": "brushes/alpha.py", "type": "import"},
            {"source": "editor/tool_a.py", "target": "brushes/beta.py", "type": "import"},
            {"source": "runtime/tool_b.py", "target": "brushes/alpha.py", "type": "import"},
            {"source": "runtime/tool_b.py", "target": "brushes/beta.py", "type": "import"},
        ]

        groups = infer_subsystem_groups(files_data, local_deps)
        brushes = next(g for g in groups if "brushes/alpha.py" in g["member_files"])

        self.assertEqual(brushes["internal_edge_count"], 0)
        self.assertEqual(brushes["inbound_interface_files"], ["editor/tool_a.py", "runtime/tool_b.py"])
        self.assertFalse(brushes["structurally_ambiguous"])
        self.assertEqual(brushes["confidence"], "medium")
        self.assertTrue(any("Toolbox cohesion" in item for item in brushes["evidence"]))

    def test_directory_toolbox_members_are_not_extracted_by_cross_boundary_consolidation(self):
        files_data = {
            "shared/__init__.py": {"role_hint": "package_init", "raw_imports": []},
            "shared/case_tool.py": {"role_hint": "utility", "raw_imports": []},
            "shared/separator_tool.py": {"role_hint": "utility", "raw_imports": []},
            "hello/hello_builder.py": {"role_hint": "unknown", "raw_imports": []},
            "world/world_builder.py": {"role_hint": "unknown", "raw_imports": []},
            "assembly/message_assembler.py": {"role_hint": "unknown", "raw_imports": []},
            "formatting/message_formatter.py": {"role_hint": "unknown", "raw_imports": []},
        }
        local_deps = [
            {"source": "hello/hello_builder.py", "target": "shared/case_tool.py", "type": "import"},
            {"source": "world/world_builder.py", "target": "shared/case_tool.py", "type": "import"},
            {"source": "assembly/message_assembler.py", "target": "shared/separator_tool.py", "type": "import"},
            {"source": "formatting/message_formatter.py", "target": "shared/separator_tool.py", "type": "import"},
        ]

        groups = infer_subsystem_groups(files_data, local_deps)
        shared = next(group for group in groups if group["name"] == "Shared Subsystem")

        self.assertEqual(
            shared["member_files"],
            [
                "shared/__init__.py",
                "shared/case_tool.py",
                "shared/separator_tool.py",
            ],
        )
        self.assertEqual(shared["internal_edge_count"], 0)
        self.assertEqual(shared["external_edge_count"], 4)
        self.assertEqual(len(shared["inbound_interface_files"]), 4)
        self.assertFalse(shared["structurally_ambiguous"])
        self.assertEqual(shared["confidence"], "medium")
        self.assertIn("refined_by: toolbox_external_consumers", shared["grouping_basis"])
        self.assertFalse(
            any(group["name"] == "Shared Utility Subsystem" for group in groups)
        )


class TestRankingEngine(unittest.TestCase):
    def test_calculate_inspection_rankings(self):
        files_data = {
            "helper.py": {
                "inbound_count": 5,
                "outbound_count": 0,
                "status": {"status": "likely_active"},
                "classes": [],
                "functions": []
            },
            "stub.py": {
                "inbound_count": 0,
                "outbound_count": 0,
                "status": {"status": "stubbed"},
                "classes": [],
                "functions": []
            },
            "orphaned_code.py": {
                "inbound_count": 0,
                "outbound_count": 0,
                "status": {"status": "orphaned"},
                "classes": [{"name": "MyClass"}],
                "functions": []
            }
        }
        parse_errors = [
            {"filepath": "broken.py", "error": "SyntaxError"}
        ]
        candidate_groups = [
            {
                "name": "Core Subsystem",
                "structurally_ambiguous": True,
                "member_files": ["helper.py"]
            },
            {
                "name": "Other Subsystem",
                "structurally_ambiguous": False,
                "member_files": ["stub.py", "orphaned_code.py"]
            }
        ]

        rankings = calculate_inspection_rankings(files_data, parse_errors, candidate_groups)
        rank_map = {r["filepath"]: r for r in rankings}

        self.assertEqual(rank_map["broken.py"]["score"], 100)
        self.assertIn("parse_error", rank_map["broken.py"]["reasons"])

        self.assertEqual(rank_map["helper.py"]["score"], 75)
        self.assertIn("structurally_ambiguous_subsystem", rank_map["helper.py"]["reasons"])
        self.assertIn("high_inbound_coupling", rank_map["helper.py"]["reasons"])

        self.assertEqual(rank_map["stub.py"]["score"], 30)

        self.assertEqual(rank_map["orphaned_code.py"]["score"], 20)

        filepath_order = [r["filepath"] for r in rankings]
        self.assertEqual(filepath_order, ["broken.py", "helper.py", "stub.py", "orphaned_code.py"])


class TestMarkdownReport(unittest.TestCase):
    def test_generate_markdown_report(self):
        report = {
            "project_name": "test_project",
            "scanned_at": "2026-07-09T00:00:00Z",
            "files": {
                "main.py": {
                    "is_entrypoint": True,
                    "role_hint": "cli",
                    "status": {
                        "status": "likely_active",
                        "evidence": ["Filename matches standard entrypoint naming"]
                    }
                }
            },
            "candidate_subsystem_groups": [
                {
                    "name": "Root Components",
                    "confidence": "high",
                    "claim_type": "inferred",
                    "structurally_ambiguous": False,
                    "grouping_basis": ["seed: directory_structure"],
                    "evidence": ["Directory layout check"],
                    "member_files": ["main.py"],
                    "inbound_interface_files": [],
                    "outbound_interface_files": []
                }
            ],
            "next_files_to_inspect": [
                {
                    "filepath": "main.py",
                    "score": 90,
                    "reasons": ["some_reason"],
                    "evidence": ["some_evidence"]
                }
            ],
            "routes": [
                {
                    "entrypoint": "main.py",
                    "claim_type": "inferred",
                    "confidence": "high",
                    "evidence": ["DFS traversal"],
                    "route_files": ["main.py"],
                    "boundary_crossings": [],
                    "stubbed_files": [],
                    "unresolved_files": [],
                    "parse_error_files": [],
                    "next_file_to_inspect_in_route": "main.py"
                }
            ],
            "parse_errors": []
        }
        
        md_report = generate_markdown_report(report)
        self.assertIn("# Code Atlas Component Relationship Report: test_project", md_report)
        self.assertIn("Total Files Scanned:** 1", md_report)
        self.assertIn("Root Components", md_report)
        self.assertIn("main.py", md_report)
        self.assertIn("Score: **90**", md_report)
        self.assertIn("Likely_active", md_report)
        self.assertIn("Active (Runtime Confirmed):** 0", md_report)
        self.assertIn("## 4. Path and Dependency Routes", md_report)
        self.assertIn("Static Route from entrypoint: `main.py`", md_report)


class TestRouting(unittest.TestCase):
    def test_calculate_dependency_routes(self):
        from code_atlas.core.router import calculate_dependency_routes
        
        files_data = {
            "main.py": {
                "is_entrypoint": True,
                "status": {"status": "likely_active"},
                "inspection_score": 60
            },
            "core/helper.py": {
                "is_entrypoint": False,
                "status": {"status": "likely_active"},
                "inspection_score": 50
            },
            "utils/util.py": {
                "is_entrypoint": False,
                "status": {"status": "stubbed"},
                "inspection_score": 30
            }
        }
        parse_errors = [
            {"filepath": "broken.py", "error": "SyntaxError"}
        ]
        local_dependencies = [
            {"source": "main.py", "target": "core/helper.py", "type": "import"},
            {"source": "core/helper.py", "target": "utils/util.py", "type": "import"},
            {"source": "core/helper.py", "target": "broken.py", "type": "import"}
        ]
        candidate_groups = [
            {
                "name": "Root Components",
                "member_files": ["main.py"],
                "structurally_ambiguous": False
            },
            {
                "name": "Core Subsystem",
                "member_files": ["core/helper.py"],
                "structurally_ambiguous": False
            },
            {
                "name": "Shared Utility Subsystem",
                "member_files": ["utils/util.py"],
                "structurally_ambiguous": False
            }
        ]

        routes = calculate_dependency_routes(files_data, parse_errors, local_dependencies, candidate_groups)
        
        self.assertEqual(len(routes), 1)
        r = routes[0]
        self.assertEqual(r["entrypoint"], "main.py")
        self.assertEqual(r["claim_type"], "inferred")
        
        self.assertEqual(r["route_files"], ["main.py", "core/helper.py", "broken.py", "utils/util.py"])
        
        self.assertEqual(len(r["boundary_crossings"]), 3)
        self.assertEqual(r["boundary_crossings"][0], {"from": "Root Components", "to": "Core Subsystem", "file": "core/helper.py"})
        
        self.assertEqual(r["stubbed_files"], ["utils/util.py"])
        self.assertEqual(r["parse_error_files"], ["broken.py"])
        
        self.assertEqual(r["next_file_to_inspect_in_route"], "broken.py")

    def test_single_node_route_has_no_self_referential_advisory(self):
        from code_atlas.core.router import calculate_dependency_routes

        files_data = {
            "main.py": {
                "is_entrypoint": True,
                "status": {"status": "likely_active"},
                "inspection_score": 60,
            }
        }

        routes = calculate_dependency_routes(files_data, [], [], [])

        self.assertEqual(routes[0]["route_files"], ["main.py"])
        self.assertIsNone(routes[0]["next_file_to_inspect_in_route"])

    def test_routing_cycles(self):
        from code_atlas.core.router import calculate_dependency_routes
        
        files_data = {
            "a.py": {
                "is_entrypoint": True,
                "status": {"status": "likely_active"},
                "inspection_score": 60
            },
            "b.py": {
                "is_entrypoint": False,
                "status": {"status": "likely_active"},
                "inspection_score": 40
            }
        }
        local_dependencies = [
            {"source": "a.py", "target": "b.py", "type": "import"},
            {"source": "b.py", "target": "a.py", "type": "import"}
        ]
        
        routes = calculate_dependency_routes(files_data, [], local_dependencies, [])
        self.assertEqual(len(routes), 1)
        self.assertEqual(routes[0]["route_files"], ["a.py", "b.py"])
        self.assertEqual(routes[0]["next_file_to_inspect_in_route"], "b.py")


class TestPilotCorrections(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_stub_detection_logic_substring(self):
        # 1. Code containing the string "TODO" inside logic, not comments/docstrings, should NOT be marked stubbed
        code = """
def check_logic():
    my_var = "this has a TODO substring"
    return my_var
"""
        file_path = os.path.join(self.test_dir, "logic.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
            
        res = parse_file(file_path, self.test_dir)
        self.assertFalse(res["_is_stub"])

    def test_stub_detection_genuine_comment(self):
        # 2. Genuine # TODO comment -> should be marked stubbed
        code = """
def active_code():
    # TODO: implement this function
    pass
"""
        file_path = os.path.join(self.test_dir, "comment.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
            
        res = parse_file(file_path, self.test_dir)
        self.assertTrue(res["_is_stub"])

    def test_stub_detection_not_implemented(self):
        # 3. raise NotImplementedError -> should be marked stubbed
        code = """
def empty_logic():
    raise NotImplementedError
"""
        file_path = os.path.join(self.test_dir, "raise_stub.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
            
        res = parse_file(file_path, self.test_dir)
        self.assertTrue(res["_is_stub"])

    def test_stub_detection_pass_only(self):
        # 3b. pass-only bodies -> should be marked stubbed
        code = """
def empty_logic():
    pass
"""
        file_path = os.path.join(self.test_dir, "pass_stub.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
            
        res = parse_file(file_path, self.test_dir)
        self.assertTrue(res["_is_stub"])

    def test_stub_detection_ellipsis_only(self):
        # 3c. ellipsis-only bodies -> should be marked stubbed
        code = """
def empty_logic():
    ...
"""
        file_path = os.path.join(self.test_dir, "ellipsis_stub.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
            
        res = parse_file(file_path, self.test_dir)
        self.assertTrue(res["_is_stub"])

    def test_namespace_package_resolution(self):
        # 4. Namespace package without __init__.py -> resolved correctly or recorded as gap
        os.makedirs(os.path.join(self.test_dir, "namespace_pkg"), exist_ok=True)
        with open(os.path.join(self.test_dir, "namespace_pkg", "module.py"), "w", encoding="utf-8") as f:
            f.write("def func(): pass\n")
            
        scanned_files = {"namespace_pkg/module.py"}
        
        # Clean resolution should work for a single candidate matching the path
        resolved = resolve_import_to_local_file("namespace_pkg.module", scanned_files)
        self.assertEqual(resolved, "namespace_pkg/module.py")
        
        # Ambiguous resolution should return "AMBIGUOUS"
        scanned_files_ambiguous = {"my_project/module.py", "module.py"}
        resolved_ambig = resolve_import_to_local_file("my_project.module", scanned_files_ambiguous, "my_project")
        self.assertEqual(resolved_ambig, "AMBIGUOUS")


if __name__ == "__main__":
    unittest.main()
