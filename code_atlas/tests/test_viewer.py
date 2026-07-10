"""Unit tests for Code Atlas web viewer server and validation checks."""

import json
import os
import socket
import sys
import tempfile
import shutil
import unittest
import urllib.request
import urllib.error
from http.server import HTTPServer
import threading
from unittest.mock import patch

from code_atlas.viewer.server import load_and_validate_report, ViewerHTTPRequestHandler
import code_atlas.viewer.server as server_mod

def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.close()
    return port

class TestViewerServer(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.port = get_free_port()
        self.server = None
        self.server_thread = None

    def tearDown(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        if self.server_thread:
            self.server_thread.join(timeout=1.0)
        shutil.rmtree(self.test_dir)

    def start_mock_server(self, report_path, report_data):
        # Set globals in server module
        server_mod.LOADED_REPORT = report_data
        server_mod.REPORT_FILE_PATH = report_path
        
        server_address = ("127.0.0.1", self.port)
        self.server = HTTPServer(server_address, ViewerHTTPRequestHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()

    def test_missing_report_path(self):
        # 1. Missing report path should exit nonzero
        non_existent = os.path.join(self.test_dir, "does_not_exist.json")
        with self.assertRaises(SystemExit) as cm:
            load_and_validate_report(non_existent)
        self.assertEqual(cm.exception.code, 1)

    def test_unreadable_report(self):
        # 2. Unreadable report should exit nonzero
        path = os.path.join(self.test_dir, "unreadable.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write('{"test": true}')
        
        # Remove all permissions to make it unreadable
        os.chmod(path, 0o000)
        try:
            with self.assertRaises(SystemExit) as cm:
                load_and_validate_report(path)
            self.assertEqual(cm.exception.code, 1)
        finally:
            # Restore permissions so cleanup can delete it
            os.chmod(path, 0o644)

    def test_malformed_json(self):
        # 3. Malformed JSON should exit nonzero
        path = os.path.join(self.test_dir, "malformed.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write('{"broken_json": ')
            
        with self.assertRaises(SystemExit) as cm:
            load_and_validate_report(path)
        self.assertEqual(cm.exception.code, 1)

    def test_non_object_json_root(self):
        # 4. Non-object root should exit nonzero
        path = os.path.join(self.test_dir, "array_root.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write('[1, 2, 3]')
            
        with self.assertRaises(SystemExit) as cm:
            load_and_validate_report(path)
        self.assertEqual(cm.exception.code, 1)

    def test_valid_report_load(self):
        # 5. Valid JSON object should load cleanly
        path = os.path.join(self.test_dir, "valid.json")
        report_payload = {"project_name": "test_proj", "files": {}}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report_payload, f)
            
        data = load_and_validate_report(path)
        self.assertEqual(data["project_name"], "test_proj")

    def test_http_api_report_preservation(self):
        # 6. /api/report must preserve payload and return application/json
        path = os.path.join(self.test_dir, "report.json")
        payload = {"project_name": "test_app", "scanned_at": "2026-07-09T00:00:00Z"}
        self.start_mock_server(path, payload)

        url = f"http://127.0.0.1:{self.port}/api/report"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as res:
            self.assertEqual(res.status, 200)
            self.assertEqual(res.headers.get("Content-Type"), "application/json")
            data = json.loads(res.read().decode('utf-8'))
            
        self.assertEqual(data["project_name"], "test_app")
        self.assertEqual(data["scanned_at"], "2026-07-09T00:00:00Z")
        self.assertIn("viewer_provenance", data)
        self.assertEqual(data["viewer_provenance"]["label"], "Read-only report viewer")

    def test_http_static_routing(self):
        # 7. Static routing must resolve /, /app.js, /styles.css
        path = os.path.join(self.test_dir, "report.json")
        self.start_mock_server(path, {})

        # GET /
        url_root = f"http://127.0.0.1:{self.port}/"
        with urllib.request.urlopen(url_root) as res:
            self.assertEqual(res.status, 200)
            self.assertEqual(res.headers.get("Content-Type"), "text/html")
            self.assertIn(b"Code Atlas Report Viewer", res.read())

        # GET /app.js
        url_js = f"http://127.0.0.1:{self.port}/app.js"
        with urllib.request.urlopen(url_js) as res:
            self.assertEqual(res.status, 200)
            self.assertEqual(res.headers.get("Content-Type"), "application/javascript")

    def test_http_route_404(self):
        # 8. Unknown routes must return 404
        path = os.path.join(self.test_dir, "report.json")
        self.start_mock_server(path, {})

        url = f"http://127.0.0.1:{self.port}/nonexistent_route"
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen(url)
        self.assertEqual(cm.exception.code, 404)

    def test_no_directory_listing_or_arbitrary_file_access(self):
        # 9. Direct directory traversal or arbitrary file access must be blocked
        path = os.path.join(self.test_dir, "report.json")
        self.start_mock_server(path, {})

        # Try to access a file outside the static directory (e.g. /../server.py)
        url = f"http://127.0.0.1:{self.port}/../server.py"
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen(url)
        self.assertIn(cm.exception.code, (404, 403))

    def test_download_endpoints(self):
        # 10. Verify download endpoints resolve companion files
        path = os.path.join(self.test_dir, "report.json")
        md_path = os.path.join(self.test_dir, "report.md")
        ai_json_path = os.path.join(self.test_dir, "report.ai.json")
        ai_md_path = os.path.join(self.test_dir, "report.ai.md")
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("Markdown Report Content")
        with open(ai_json_path, "w", encoding="utf-8") as f:
            f.write('{"ai": true}')
        with open(ai_md_path, "w", encoding="utf-8") as f:
            f.write("AI Markdown Content")
            
        self.start_mock_server(path, {})
        
        # Test GET /api/report/markdown
        url_md = f"http://127.0.0.1:{self.port}/api/report/markdown"
        with urllib.request.urlopen(url_md) as res:
            self.assertEqual(res.status, 200)
            self.assertEqual(res.headers.get("Content-Type"), "text/markdown")
            self.assertIn(b"Markdown Report Content", res.read())
            
        # Test GET /api/report/ai_json
        url_ai_json = f"http://127.0.0.1:{self.port}/api/report/ai_json"
        with urllib.request.urlopen(url_ai_json) as res:
            self.assertEqual(res.status, 200)
            self.assertEqual(res.headers.get("Content-Type"), "application/json")
            
        # Test GET /api/report/ai_markdown
        url_ai_md = f"http://127.0.0.1:{self.port}/api/report/ai_markdown"
        with urllib.request.urlopen(url_ai_md) as res:
            self.assertEqual(res.status, 200)
            self.assertEqual(res.headers.get("Content-Type"), "text/markdown")
            self.assertIn(b"AI Markdown Content", res.read())

    def test_all_payloads_endpoint(self):
        # 11. Verify all_payloads endpoint serves combined reports
        path = os.path.join(self.test_dir, "report.json")
        md_path = os.path.join(self.test_dir, "report.md")
        
        with open(path, "w", encoding="utf-8") as f:
            f.write('{"report": true}')
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("Markdown Report Content")
            
        self.start_mock_server(path, {"report": True})
        
        url_all = f"http://127.0.0.1:{self.port}/api/report/all_payloads"
        with urllib.request.urlopen(url_all) as res:
            self.assertEqual(res.status, 200)
            self.assertEqual(res.headers.get("Content-Type"), "text/plain; charset=utf-8")
            body = res.read()
            self.assertIn(b"FILE: report.json", body)
            self.assertIn(b"FILE: report.md", body)
            self.assertIn(b"Markdown Report Content", body)
