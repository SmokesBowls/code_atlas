"""Unit tests for Payload Handoff Diagnostics (Milestone 9)."""

import unittest
import tempfile
import os
import shutil
from code_atlas.core.payload_extractor import extract_payload_candidates
from code_atlas.core.payload_analyzer import analyze_payload_handoffs

from code_atlas.core import parser

class TestPayloadAnalyzerRestructured(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def _write_file(self, rel_path, content):
        full_path = os.path.join(self.test_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return full_path

    def _run_diagnostics(self, file_contents):
        files_data = {}
        candidates_by_file = {}
        
        # First write all files
        full_paths = {}
        for rel_path, content in file_contents.items():
            full_paths[rel_path] = self._write_file(rel_path, content)
            
        # Use real parser and candidates extractor
        for rel_path, full_path in full_paths.items():
            files_data[rel_path] = parser.parse_file(full_path, self.test_dir)
            candidates_by_file[rel_path] = extract_payload_candidates(full_path)
            
        return analyze_payload_handoffs(files_data, candidates_by_file, self.test_dir)

    def test_a_direct_connected_handoff(self):
        # Test A: Direct connected handoff
        # payload = build_scene()
        # consume_scene(payload)
        files = {
            "producer.py": """
def build_scene():
    return {"scene_id": 1, "metadata": {}}
""",
            "consumer.py": """
def consume_scene(payload):
    print(payload["scene_id"])
""",
            "main.py": """
from producer import build_scene
from consumer import consume_scene
payload = build_scene()
consume_scene(payload)
"""
        }
        res = self._run_diagnostics(files)
        handoffs = res["payload_handoffs"]
        
        self.assertTrue(any(h["payload_candidate_id"] == "flow_build_scene_to_consume_scene" for h in handoffs))
        flow = next(h for h in handoffs if h["payload_candidate_id"] == "flow_build_scene_to_consume_scene")
        self.assertEqual(flow["route_status"], "connected_partial")
        self.assertEqual(flow["claim_type"], "confirmed")
        self.assertIn("scene_id", flow["observed_shape"]["utilized_keys"])

    def test_b_nested_connected_handoff(self):
        # Test B: Nested connected handoff
        # consume_scene(build_scene())
        files = {
            "producer.py": """
def build_scene():
    return {"scene_id": 1}
""",
            "consumer.py": """
def consume_scene(payload):
    print(payload["scene_id"])
""",
            "main.py": """
from producer import build_scene
from consumer import consume_scene
consume_scene(build_scene())
"""
        }
        res = self._run_diagnostics(files)
        handoffs = res["payload_handoffs"]
        
        self.assertTrue(any(h["payload_candidate_id"] == "flow_build_scene_to_consume_scene" for h in handoffs))
        flow = next(h for h in handoffs if h["payload_candidate_id"] == "flow_build_scene_to_consume_scene")
        self.assertEqual(flow["route_status"], "connected")

    def test_c_file_connected_handoff(self):
        # Test C: File connected handoff
        # writer and reader use the same explicit path.
        files = {
            "writer.py": """
def export():
    open("scene.json", "w").write("data")
""",
            "reader.py": """
def import_scene():
    open("scene.json", "r").read()
"""
        }
        res = self._run_diagnostics(files)
        handoffs = res["payload_handoffs"]
        
        self.assertTrue(any(h["payload_candidate_id"] == "file_scene.json" for h in handoffs))
        flow = next(h for h in handoffs if h["payload_candidate_id"] == "file_scene.json")
        self.assertEqual(flow["route_status"], "connected_unused")

    def test_d_ambiguous_file_handoff(self):
        # Test D: Ambiguous file handoff
        # two possible readers match the same basename.
        files = {
            "writer.py": """
def export():
    open("scene.json", "w").write("data")
""",
            "reader1.py": """
def read1():
    open("scene.json", "r").read()
""",
            "reader2.py": """
def read2():
    open("scene.json", "r").read()
"""
        }
        res = self._run_diagnostics(files)
        handoffs = res["payload_handoffs"]
        
        self.assertTrue(any(h["route_status"] == "ambiguous_consumer" for h in handoffs))

    def test_e_producer_only_boundary(self):
        # Test E: Producer-only boundary
        # writer exists, but no reader exists in the scanned fixture.
        files = {
            "writer.py": """
def export():
    open("trixelcomposer_recipe.json", "w").write("data")
"""
        }
        res = self._run_diagnostics(files)
        unresolved = res["unresolved_payload_routes"]
        
        self.assertTrue(any(u["status"] == "producer_only" for u in unresolved))
        u = next(x for x in unresolved if x["status"] == "producer_only")
        self.assertEqual(u["reason"], "consumer outside scan boundary")
        self.assertEqual(u["claim_type"], "gap")

    def test_f_non_payload_dictionary(self):
        # Test F: Non-payload dictionary
        # an internal lookup dictionary must not automatically become a handoff.
        files = {
            "helper.py": """
def _get_lookup():
    return {"_a": 1, "_b": 2}
"""
        }
        res = self._run_diagnostics(files)
        handoffs = res["payload_handoffs"]
        unresolved = res["unresolved_payload_routes"]
        
        # Verify it was ignored
        self.assertEqual(len(handoffs), 0)
        # Should not be in unresolved routes either
        self.assertEqual(len(unresolved), 0)

    def test_g_three_hop_dead_end(self):
        # Test G: 3-hop chain where the leaf is a dead end (does not access keys).
        # Should resolve to connected_unused.
        files = {
            "m1.py": """
def build_scene():
    return {"scene_id": 1, "metadata": {}}
""",
            "m2.py": """
from m1 import build_scene
from m3 import step2
def step1():
    p = build_scene()
    step2(p)
""",
            "m3.py": """
from m4 import step3
def step2(p):
    step3(p)
""",
            "m4.py": """
def step3(p):
    # Dead end: does not access p["scene_id"] or p["metadata"]
    pass
"""
        }
        res = self._run_diagnostics(files)
        handoffs = res["payload_handoffs"]
        
        # Verify the handoff from build_scene is traced to step2
        self.assertTrue(any(h["payload_candidate_id"] == "flow_build_scene_to_step2" for h in handoffs))
        flow = next(h for h in handoffs if h["payload_candidate_id"] == "flow_build_scene_to_step2")
        self.assertEqual(flow["route_status"], "connected_unused")
        self.assertIn("scene_id", flow["observed_shape"]["unutilized_keys"])
        self.assertIn("metadata", flow["observed_shape"]["unutilized_keys"])

    def test_h_three_hop_active_leaf(self):
        # Test H: 3-hop chain where the leaf accesses a key.
        # Should resolve to connected (partial or full depending on accessed keys).
        files = {
            "m1.py": """
def build_scene():
    return {"scene_id": 1, "metadata": {}}
""",
            "m2.py": """
from m1 import build_scene
from m3 import step2
def step1():
    p = build_scene()
    step2(p)
""",
            "m3.py": """
from m4 import step3
def step2(p):
    step3(p)
""",
            "m4.py": """
def step3(p):
    print(p["scene_id"])
"""
        }
        res = self._run_diagnostics(files)
        handoffs = res["payload_handoffs"]
        
        self.assertTrue(any(h["payload_candidate_id"] == "flow_build_scene_to_step2" for h in handoffs))
        flow = next(h for h in handoffs if h["payload_candidate_id"] == "flow_build_scene_to_step2")
        self.assertEqual(flow["route_status"], "connected_partial")
        self.assertIn("scene_id", flow["observed_shape"]["utilized_keys"])
        self.assertIn("metadata", flow["observed_shape"]["unutilized_keys"])

    def test_i_json_dump_sink_value_provenance(self):
        # Prerequisite for EFFECT Fixture A: connect a utilized payload field,
        # through a local alias and dict wrapper, to a literal-path file sink.
        files = {
            "producer.py": """
def build_terrain_field(seed):
    return {
        "grid_size": compute_grid_size(seed),
        "tiles": generate_tiles(seed),
        "version": "1.0",
    }
""",
            "consumer.py": """
import json

def write_recipe_and_atlas(payload):
    size = payload["grid_size"]
    with open("trixelcomposer_recipe.json", "w") as fp:
        json.dump({"size": size}, fp)
""",
            "main.py": """
from producer import build_terrain_field
from consumer import write_recipe_and_atlas
write_recipe_and_atlas(build_terrain_field(1))
""",
        }

        res = self._run_diagnostics(files)
        flow = next(
            h for h in res["payload_handoffs"]
            if h["payload_candidate_id"] == "flow_build_terrain_field_to_write_recipe_and_atlas"
        )

        self.assertEqual(flow["artifact_paths"], ["trixelcomposer_recipe.json"])
        self.assertEqual(flow["observed_shape"]["utilized_keys"], ["grid_size"])
        self.assertEqual(flow["observed_shape"]["unutilized_keys"], ["tiles", "version"])
        self.assertFalse(any(
            u.get("artifact_paths") == ["trixelcomposer_recipe.json"]
            for u in res["unresolved_payload_routes"]
        ))
