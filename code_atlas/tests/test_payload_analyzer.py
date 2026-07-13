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

    def _run_diagnostics(self, file_contents, local_dependencies=None):
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
            
        return analyze_payload_handoffs(
            files_data,
            candidates_by_file,
            self.test_dir,
            local_dependencies=local_dependencies,
        )

    def test_ambiguous_exported_function_is_not_guessed(self):
        files = {
            "tier2/producer.py": """
def build_scene():
    return {"wrong": True}
""",
            "producer.py": """
def build_scene():
    return {"scene_id": 1}
""",
            "consumer.py": """
def consume_scene(payload):
    print(payload["scene_id"])
""",
            "main.py": """
from consumer import consume_scene
payload = build_scene()
consume_scene(payload)
""",
        }

        result = self._run_diagnostics(files)

        self.assertFalse(
            any(
                handoff["payload_candidate_id"]
                == "flow_build_scene_to_consume_scene"
                for handoff in result["payload_handoffs"]
            )
        )

    def test_reporter_dependency_selects_payload_defining_file(self):
        files = {
            "tier2/producer.py": """
def build_scene():
    return {"wrong": True}
""",
            "tier1/producer.py": """
def build_scene():
    return {"scene_id": 1}
""",
            "consumer.py": """
def consume_scene(payload):
    print(payload["scene_id"])
""",
            "main.py": """
payload = build_scene()
consume_scene(payload)
""",
        }
        local_dependencies = [
            {"source": "main.py", "target": "tier1/producer.py", "type": "import"},
            {"source": "main.py", "target": "consumer.py", "type": "import"},
        ]

        result = self._run_diagnostics(files, local_dependencies)

        flow = next(
            handoff
            for handoff in result["payload_handoffs"]
            if handoff["payload_candidate_id"] == "flow_build_scene_to_consume_scene"
        )
        self.assertEqual(flow["producer"]["file"], "tier1/producer.py")

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
        verdicts = {claim["field"]: claim for claim in flow["effect_claims"]}
        self.assertEqual(verdicts["grid_size"]["verdict"], "EFFECTIVE")
        self.assertEqual(verdicts["grid_size"]["sink_type"], "FILE_WRITE")
        self.assertEqual(verdicts["tiles"]["verdict"], "DROPPED")
        self.assertEqual(verdicts["version"]["verdict"], "DROPPED")
        self.assertFalse(any(
            u.get("artifact_paths") == ["trixelcomposer_recipe.json"]
            for u in res["unresolved_payload_routes"]
        ))

    def test_effect_fixture_d_whole_parameter_to_serializer(self):
        files = {
            "producer.py": """
def produce():
    return {
        "book_count": 1,
        "books": [],
        "chapter_count": 4,
        "contract": "chapter_index.v1",
        "vault_root": "/vault",
    }
""",
            "consumer.py": """
import json

def consume(index, path):
    with open("chapter_index.json", "w") as handle:
        json.dump(index, handle)
""",
            "main.py": """
from producer import produce
from consumer import consume
consume(produce(), "chapter_index.json")
""",
        }

        flow = next(
            handoff for handoff in self._run_diagnostics(files)["payload_handoffs"]
            if handoff["payload_candidate_id"] == "flow_produce_to_consume"
        )
        claims = {claim["field"]: claim for claim in flow["effect_claims"]}

        self.assertEqual(flow["consumers"][0]["matched_parameter"], "index")
        self.assertTrue(flow["whole_parameter_forwarded"])
        self.assertEqual(flow["observed_shape"]["utilized_keys"], [
            "book_count", "books", "chapter_count", "contract", "vault_root",
        ])
        self.assertTrue(all(claim["verdict"] == "EFFECTIVE" for claim in claims.values()))
        self.assertTrue(all(claim["sink_type"] == "FILE_WRITE" for claim in claims.values()))

    def test_effect_fixture_b_stranded_denylist_only(self):
        files = {
            "producer.py": """
def build_payload():
    return {"tiles": [1], "grid_size": 3}
""",
            "consumer.py": """
import logging
logger = logging.getLogger(__name__)
def consume(payload):
    tiles = payload["tiles"]
    logger.debug(f"tiles={len(tiles)}")
""",
            "main.py": """
from producer import build_payload
from consumer import consume
consume(build_payload())
""",
        }
        flow = next(h for h in self._run_diagnostics(files)["payload_handoffs"] if h["payload_candidate_id"] == "flow_build_payload_to_consume")
        verdicts = {claim["field"]: claim["verdict"] for claim in flow["effect_claims"]}
        self.assertEqual(verdicts["tiles"], "STRANDED")
        self.assertEqual(verdicts["grid_size"], "DROPPED")

    def test_effect_fixture_c_unknown_call_is_unclassified(self):
        files = {
            "producer.py": """
def build_payload():
    return {"size": 3}
""",
            "consumer.py": """
def consume(payload, atlas_service):
    size = payload["size"]
    atlas_service.register(size)
""",
            "main.py": """
from producer import build_payload
from consumer import consume
consume(build_payload(), service)
""",
        }
        flow = next(h for h in self._run_diagnostics(files)["payload_handoffs"] if h["payload_candidate_id"] == "flow_build_payload_to_consume")
        claim = flow["effect_claims"][0]
        self.assertEqual(claim["verdict"], "UNCLASSIFIED_TERMINUS")
        self.assertEqual(claim["confidence"], "low")

    def test_route_qualified_argument_position_selects_consumer_parameter(self):
        files = {
            "producer.py": """
def build_body():
    return {"value": 1}
def build_surface():
    return {"value": 2}
""",
            "consumer.py": """
def consume(body_lane, surface_lane):
    return {"body": body_lane["value"], "surface": surface_lane["value"]}
""",
            "main.py": """
from producer import build_body, build_surface
from consumer import consume
consume(build_body(), build_surface())
""",
        }
        result = self._run_diagnostics(files)
        body = next(h for h in result["payload_handoffs"] if h["payload_candidate_id"] == "flow_build_body_to_consume")
        surface = next(h for h in result["payload_handoffs"] if h["payload_candidate_id"] == "flow_build_surface_to_consume")
        self.assertEqual(body["consumers"][0]["matched_parameter"], "body_lane")
        self.assertEqual(surface["consumers"][0]["matched_parameter"], "surface_lane")
        self.assertEqual(body["access_modes"], {"value": "REQUIRED"})
        self.assertEqual(surface["access_modes"], {"value": "REQUIRED"})
        self.assertEqual(
            surface["construction_observations"],
            [{
                "output_field": "surface",
                "expression": "surface_lane['value']",
                "source_parameter": "surface_lane",
                "source_parameter_keys": ["value"],
            }],
        )

    def test_returned_call_syntax_is_preserved(self):
        path = os.path.join(self.test_dir, "smooth.py")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(
                "import numpy as np\n"
                "def _smooth(arr, k=3):\n"
                "    return np.pad(arr, k // 2, mode='edge')\n"
            )

        candidates = extract_payload_candidates(path)
        smooth = next(item for item in candidates["producers"] if item["function"] == "_smooth")

        self.assertEqual(smooth["returned_call"], "np.pad(arr, k // 2, mode='edge')")

    def test_access_modes_and_build_influence(self):
        files = {
            "producer.py": """
def build_payload():
    return {"required": 1, "defaulted": 2, "implicit": 3, "guarded": 4}
""",
            "consumer.py": """
def consume(payload):
    output = []
    output.append(payload["required"])
    payload.get("defaulted", 0)
    payload.get("implicit")
    if "guarded" in payload:
        output.append(payload["guarded"])
    return output
""",
            "main.py": """
from producer import build_payload
from consumer import consume
consume(build_payload())
""",
        }
        flow = next(h for h in self._run_diagnostics(files)["payload_handoffs"] if h["payload_candidate_id"] == "flow_build_payload_to_consume")
        self.assertEqual(flow["access_modes"], {
            "defaulted": "DEFAULTED",
            "guarded": "GUARDED",
            "implicit": "OPTIONAL_IMPLICIT_NONE",
            "required": "REQUIRED",
        })
        claims = {claim["field"]: claim for claim in flow["effect_claims"]}
        self.assertEqual(claims["required"]["sink_type"], "BUILD_INFLUENCE")
        self.assertEqual(claims["guarded"]["sink_type"], "BUILD_INFLUENCE")
