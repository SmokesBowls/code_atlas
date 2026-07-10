"""Lightweight HTTP server for viewing Code Atlas reports offline."""

import argparse
import json
import os
import sys
import webbrowser
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

LOADED_REPORT = {}
REPORT_FILE_PATH = ""

class ViewerHTTPRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Silence HTTP logs to keep CLI clean
        pass

    def do_HEAD(self):
        self.handle_request(send_body=False)

    def do_GET(self):
        self.handle_request(send_body=True)

    def handle_request(self, send_body=True):
        if self.command not in ("GET", "HEAD"):
            self.send_error(405, "Method Not Allowed")
            return

        # Normalize URL path to strip query params or fragments
        path = self.path.split('?')[0].split('#')[0]

        if path == "/":
            self.serve_static_file("index.html", "text/html", send_body)
        elif path == "/app.js":
            self.serve_static_file("app.js", "application/javascript", send_body)
        elif path == "/styles.css":
            self.serve_static_file("styles.css", "text/css", send_body)
        elif path == "/api/report":
            self.serve_api_report(send_body)
        elif path == "/api/report/markdown":
            self.serve_companion_file(".md", "text/markdown", send_body)
        elif path == "/api/report/ai_json":
            self.serve_companion_file(".ai.json", "application/json", send_body)
        elif path == "/api/report/ai_markdown":
            self.serve_companion_file(".ai.md", "text/markdown", send_body)
        elif path == "/api/report/all_payloads":
            self.serve_all_payloads(send_body)
        else:
            self.send_error(404, "Not Found")

    def serve_static_file(self, filename, content_type, send_body):
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
        file_path = os.path.join(static_dir, filename)
        
        # Strict directory traversal check
        real_file_path = os.path.realpath(file_path)
        real_static_dir = os.path.realpath(static_dir)
        if not real_file_path.startswith(real_static_dir):
            self.send_error(403, "Forbidden")
            return

        if not os.path.exists(real_file_path) or os.path.isdir(real_file_path):
            self.send_error(404, "Not Found")
            return

        try:
            with open(real_file_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            if send_body:
                self.wfile.write(content)
        except Exception:
            self.send_error(500, "Internal Server Error")

    def serve_api_report(self, send_body):
        report_data = dict(LOADED_REPORT)
        # Provenance metadata required by visual rules
        report_data["viewer_provenance"] = {
            "report_path": os.path.abspath(REPORT_FILE_PATH),
            "label": "Read-only report viewer"
        }
        
        # Check if AI files exist and tell the JS client about them
        base_path = os.path.splitext(REPORT_FILE_PATH)[0]
        report_data["viewer_provenance"]["has_ai_json"] = os.path.exists(base_path + ".ai.json")
        report_data["viewer_provenance"]["has_ai_markdown"] = os.path.exists(base_path + ".ai.md")

        try:
            content = json.dumps(report_data, indent=2).encode('utf-8')
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            if send_body:
                self.wfile.write(content)
        except Exception:
            self.send_error(500, "Internal Server Error")

    def serve_companion_file(self, extension, content_type, send_body):
        base_path = os.path.splitext(REPORT_FILE_PATH)[0]
        target_path = base_path + extension
        
        if not os.path.exists(target_path) or os.path.isdir(target_path):
            self.send_error(404, "Not Found")
            return
            
        try:
            with open(target_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Disposition", f'attachment; filename="{os.path.basename(target_path)}"')
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            if send_body:
                self.wfile.write(content)
        except Exception:
            self.send_error(500, "Internal Server Error")

    def serve_all_payloads(self, send_body):
        base_path = os.path.splitext(REPORT_FILE_PATH)[0]
        paths = [
            (REPORT_FILE_PATH, ".json"),
            (base_path + ".md", ".md"),
            (base_path + ".ai.json", ".ai.json"),
            (base_path + ".ai.md", ".ai.md")
        ]
        
        contents = []
        for file_path, ext in paths:
            if os.path.exists(file_path) and not os.path.isdir(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        text = f.read()
                    contents.append(f"==================================================\n")
                    contents.append(f"FILE: {os.path.basename(file_path)}\n")
                    contents.append(f"==================================================\n\n")
                    contents.append(text)
                    contents.append("\n\n")
                except Exception:
                    pass
                    
        combined_text = "".join(contents)
        content_bytes = combined_text.encode('utf-8')
        
        try:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Disposition", 'attachment; filename="code_atlas_all_payloads.txt"')
            self.send_header("Content-Length", str(len(content_bytes)))
            self.end_headers()
            if send_body:
                self.wfile.write(content_bytes)
        except Exception:
            self.send_error(500, "Internal Server Error")

def load_and_validate_report(report_path):
    """Load the JSON report file and validate structure at startup."""
    if not os.path.exists(report_path):
        print(f"Error: Report path '{report_path}' does not exist.", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error: Unable to read report file. Details: {e}", file=sys.stderr)
        sys.exit(1)
        
    try:
        data = json.loads(content)
    except Exception as e:
        print(f"Error: Report file contains invalid JSON. Details: {e}", file=sys.stderr)
        sys.exit(1)
        
    if not isinstance(data, dict):
        print("Error: Report JSON root must be an object.", file=sys.stderr)
        sys.exit(1)
        
    return data

def main():
    parser = argparse.ArgumentParser(description="Code Atlas Local Web Viewer")
    parser.add_argument("--report", help="Path to the Code Atlas JSON report file")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the HTTP server on")
    
    args = parser.parse_args()
    if not args.report:
        print("Error: The --report argument is required.", file=sys.stderr)
        print("Usage: python3 -m code_atlas.viewer.server --report path/to/report.json [--port 8000]", file=sys.stderr)
        sys.exit(1)
        
    global LOADED_REPORT, REPORT_FILE_PATH
    REPORT_FILE_PATH = args.report
    LOADED_REPORT = load_and_validate_report(args.report)
    
    server_address = ("127.0.0.1", args.port)
    try:
        httpd = HTTPServer(server_address, ViewerHTTPRequestHandler)
    except Exception as e:
        print(f"Error: Failed to bind server to port {args.port}. Details: {e}", file=sys.stderr)
        sys.exit(1)
        
    print(f"Code Atlas Local Web Viewer loaded report successfully.")
    print(f"Server address: http://127.0.0.1:{args.port}/")
    
    def open_browser():
        webbrowser.open(f"http://127.0.0.1:{args.port}/")
        
    threading.Thread(target=open_browser, daemon=True).start()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()
        sys.exit(0)

if __name__ == "__main__":
    main()
