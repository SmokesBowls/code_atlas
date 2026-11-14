"""Tests for the HTTP boundary inventory and matcher (separate from the import scanner)."""

import io
import json
import os
import shutil
import tempfile
import textwrap
import unittest
from contextlib import redirect_stderr, redirect_stdout

from code_atlas.core.boundary_matcher import match_boundaries
from code_atlas.core.http_boundaries import build_http_inventory, pattern_regex
from code_atlas.scanner import run_scan

SERVER = '''
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        base = urlparse(self.path).path.rstrip("/")
        if base in ("", "/health"):
            return self.ok()
        elif base == "/snapshot":
            return self.ok()

    def do_POST(self):
        if self.path == "/command":
            return self.ok()

def main():
    ThreadingHTTPServer(("127.0.0.1", 8080), Handler).serve_forever()
'''

CLIENT = '''
import os
import urllib.request

class RuntimeClient:
    def __init__(self, base_url=None):
        self.base_url = (base_url or os.environ.get("RT_URL", "http://127.0.0.1:8080")).rstrip("/")

    def _request(self, method, path, payload=None):
        req = urllib.request.Request(self.base_url + path, data=payload, method=method.upper())
        with urllib.request.urlopen(req) as resp:
            return resp.read()

    def snapshot(self):
        return self._request("GET", "/snapshot")

    def command(self, cmd):
        return self._request("POST", "/command", cmd)

    def say(self, cmd):
        return self._request("POST", "/dialogue/say", cmd)
'''

OTHER_PORT = '''
import urllib.request
PORT = 8768

def ping():
    return urllib.request.urlopen(f"http://127.0.0.1:{PORT}/health")
'''

PORTLESS_SERVER = '''
from fastapi import FastAPI
app = FastAPI()

@app.get("/health")
def health():
    return {}
'''

HUB = '''
class Hub:
    def __init__(self, http):
        self.http = http

    def http_api(self, method, url, data=None):
        return self.http.request(method, url, data=data)
'''

HUB_USER = '''
def show(hub, url):
    return hub.http_api("get", url)
'''

GAPS = '''
import requests

class Mirror:
    def fetch(self, url):
        requests.get("http://example.invalid/simple")
        return self.http.async_get(url=url)

    def lookup(self):
        return self.client.get("cache-key")

def with_client():
    import httpx
    c = httpx.Client()
    return c.post("http://127.0.0.1:9000/upload")
'''

IMPORTS_ONLY = '''
from pyramid.httpexceptions import HTTPNotFound
import requests.exceptions

def missing():
    raise HTTPNotFound()
'''

PYRAMID_ROUTES = '''
def includeme(config):
    config.add_route("/{user}/{index}", "/{user:[^+/]+}/{index:[^+/]+}")
'''

PYRAMID_VIEWS = '''
from pyramid.view import view_config

class Views:
    @view_config(route_name="/{user}/{index}", request_method="PATCH")
    def modify(self):
        return {}
'''

FACTORY = '''
from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route("/items", methods=["GET", "POST"])
    def items():
        return ""

    app.add_url_rule("/legacy", view_func=items)
    return app
'''


def _write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(text))


class BoundaryTestBase(unittest.TestCase):
    files = {}

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        for rel, text in self.files.items():
            _write(self.tmp, rel, text)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def inventory(self):
        return build_http_inventory(self.tmp, sorted(self.files), lambda rel: rel.split("/")[0])


class TestClientServerMatching(BoundaryTestBase):
    files = {"sim/server.py": SERVER, "os_/client.py": CLIENT, "os_/tools.py": OTHER_PORT,
             "facade/app.py": PORTLESS_SERVER}

    def test_outcomes(self):
        inv = self.inventory()
        res = match_boundaries([inv])["results"]
        by = {(r["call"]["file"], r["call"]["method"], r["destination"]["path"]): r for r in res}
        snap = by[("os_/client.py", "GET", "/snapshot")]
        self.assertEqual(snap["outcome"], "matched")
        self.assertEqual(snap["servers"][0]["file"], "sim/server.py")
        self.assertIn("caveat", snap)  # destination came from an environment default
        self.assertEqual(by[("os_/client.py", "POST", "/command")]["outcome"], "matched")
        self.assertEqual(by[("os_/client.py", "POST", "/dialogue/say")]["outcome"], "unmatched")
        # /health exists on the 8080 server, but this call targets 8768: never matched to it.
        ping = by[("os_/tools.py", "GET", "/health")]
        self.assertEqual(ping["outcome"], "candidate")
        self.assertEqual([s["file"] for s in ping["servers"]], ["facade/app.py"])

    def test_wrapper_call_sites_and_direction(self):
        inv = self.inventory()
        out = [o for o in inv["outgoing"] if o["file"] == "os_/client.py"]
        self.assertEqual(sorted(o["function"] for o in out), ["command", "say", "snapshot"])
        self.assertTrue(all(o["direction"] == "outgoing" and o["via"] for o in out))
        self.assertTrue(all(r["direction"] if "direction" in r else True for r in inv["incoming"]))
        self.assertEqual(inv["bindings"][0]["port"], 8080)

    def test_deterministic(self):
        a = json.dumps(self.inventory(), sort_keys=True)
        b = json.dumps(self.inventory(), sort_keys=True)
        self.assertEqual(a, b)


class TestUnresolvedAndWrappers(BoundaryTestBase):
    files = {"client/hub.py": HUB, "client/user.py": HUB_USER}

    def test_cross_module_wrapper_records_unresolved_destination(self):
        inv = self.inventory()
        rec = [o for o in inv["outgoing"] if o["file"] == "client/user.py"]
        self.assertEqual(len(rec), 1)
        self.assertEqual(rec[0]["method"], "GET")
        self.assertEqual(rec[0]["destination"]["resolution"], "unresolved")
        self.assertIn("url", rec[0]["destination"]["unresolved_reason"])
        self.assertIn("unique", rec[0]["link_evidence"])
        res = match_boundaries([inv])["results"]
        self.assertEqual({r["outcome"] for r in res}, {"unresolved"})
        sites = {(c["file"], c["status"]) for c in inv["coverage"] if c["side"] == "client"}
        self.assertIn(("client/user.py", "interpreted-unresolved"), sites)
        self.assertIn(("client/hub.py", "interpreted-wrapper"), sites)


class TestCoverage(BoundaryTestBase):
    files = {"svc/mirror.py": GAPS, "svc/errors.py": IMPORTS_ONLY}

    def test_gap_reported_per_call_site_in_interpreted_file(self):
        inv = self.inventory()
        cov = [c for c in inv["coverage"] if c["file"] == "svc/mirror.py"]
        statuses = {c["status"] for c in cov}
        self.assertIn("interpreted", statuses)  # requests.get and httpx client object
        gaps = [c for c in cov if c["status"] == "not-interpreted"]
        self.assertEqual(len(gaps), 1)
        self.assertIn("async_get", gaps[0]["detail"])
        self.assertEqual(inv["coverage_summary"]["not_interpreted"][0]["file"], "svc/mirror.py")

    def test_client_object_recognized_and_dict_get_ignored(self):
        inv = self.inventory()
        out = {(o["method"], o["destination"]["url"]) for o in inv["outgoing"]}
        self.assertIn(("POST", "http://127.0.0.1:9000/upload"), out)
        self.assertNotIn(("GET", "cache-key"), out)
        self.assertEqual(len(inv["outgoing"]), 2)

    def test_imports_alone_are_informational(self):
        inv = self.inventory()
        self.assertNotIn("svc/errors.py", {c["file"] for c in inv["coverage"]})
        self.assertIn("svc/errors.py", inv["files_importing_http_without_operations"])


class TestServerAdapters(BoundaryTestBase):
    files = {"srv/routes.py": PYRAMID_ROUTES, "srv/views.py": PYRAMID_VIEWS, "web/factory.py": FACTORY}

    def test_pyramid_route_joined_to_view(self):
        inv = self.inventory()
        pyr = [r for r in inv["incoming"] if r["recognized_by"].startswith("pyramid")]
        self.assertEqual(len(pyr), 1)
        self.assertEqual(pyr[0]["method"], "PATCH")
        self.assertEqual(pyr[0]["route_declared_at"], "srv/routes.py:3")
        self.assertEqual(pyr[0]["handler"], "Views.modify")

    def test_nested_decorator_routes_and_unsupported_registration(self):
        inv = self.inventory()
        flask = sorted((r["method"], r["path"]) for r in inv["incoming"] if r["file"] == "web/factory.py")
        self.assertEqual(flask, [("GET", "/items"), ("POST", "/items")])
        gaps = [c["detail"] for c in inv["coverage"] if c["status"] == "not-interpreted"]
        self.assertTrue(any("add_url_rule" in g for g in gaps))

    def test_pattern_regex(self):
        import re
        rx = pattern_regex("/{user:[^+/]+}/{index}/+f/{relpath:.*}")
        self.assertTrue(re.fullmatch(rx, "/alice/dev/+f/a/b.tar.gz"))
        self.assertFalse(re.fullmatch(rx, "/alice/+f"))


PREFIX_SERVER = '''
from http.server import BaseHTTPRequestHandler

class ApHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path.startswith("/ap"):
            return self.ok()
'''

OLLAMA_CLIENT = '''
import requests

class Agent:
    def __init__(self):
        self.session = Memory()

    def ask(self):
        self.session.get_history_for_prompt()
        return requests.post("http://localhost:11434/api/generate", json={})
'''


class TestFalseConnectionGuards(BoundaryTestBase):
    files = {"os_/scene_server.py": PREFIX_SERVER, "tools/agent.py": OLLAMA_CLIENT}

    def test_prefix_route_without_port_is_not_a_candidate(self):
        res = match_boundaries([self.inventory()])["results"]
        self.assertEqual([r["outcome"] for r in res], ["unknown"])

    def test_non_verb_method_on_session_is_not_a_gap(self):
        inv = self.inventory()
        self.assertEqual(inv["coverage_summary"]["not_interpreted"], [])


class TestScannerFlag(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.proj = os.path.join(self.tmp, "proj")
        _write(self.proj, "sim/server.py", SERVER)
        _write(self.proj, "os_/client.py", CLIENT)
        self.out = os.path.join(self.tmp, "out", "report.json")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _scan(self, **kw):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            run_scan(self.proj, self.out, **kw)
        with open(self.out, encoding="utf-8") as f:
            return json.load(f)

    def test_flag_is_opt_in_and_leaves_report_alone(self):
        base = self._scan()
        bpath = os.path.join(self.tmp, "out", "boundaries.json")
        with_flag = self._scan(boundaries_output=bpath)
        base.pop("scanned_at")
        with_flag.pop("scanned_at")
        self.assertEqual(base, with_flag)
        with open(bpath, encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["inventory"]["format"], "code_atlas.http_boundary_inventory")
        outcomes = {r["outcome"] for r in data["matching"]["results"]}
        self.assertEqual(outcomes, {"matched", "unmatched"})


if __name__ == "__main__":
    unittest.main()
