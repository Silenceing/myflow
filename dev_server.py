#!/usr/bin/env python3
"""Local dev server for testing the Cloud Function locally.

Usage:
    python dev_server.py          # Start server on port 8080
    python dev_server.py 9000     # Start server on custom port
"""
import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "src"))
sys.path.insert(0, src_dir)


class ResearchHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/research":
            self.send_response(404)
            self.end_headers()
            return

        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)

        try:
            from myflow.main import LatestAiFlow

            body = json.loads(raw_body) if raw_body else {}
            topic = body.get("topic", "AI Agents")

            print(f"\n[Research] Starting flow for topic: {topic}")

            flow = LatestAiFlow()
            flow.state.topic = topic
            flow.kickoff()

            report_en = ""
            report_cn = ""
            en_path = os.path.join("output", "report.md")
            cn_path = os.path.join("output", "report_cn.md")

            if os.path.exists(en_path):
                with open(en_path, "r", encoding="utf-8") as f:
                    report_en = f.read()
            if os.path.exists(cn_path):
                with open(cn_path, "r", encoding="utf-8") as f:
                    report_cn = f.read()

            response = json.dumps(
                {"success": True, "topic": topic, "report_en": report_en, "report_cn": report_cn},
                ensure_ascii=False,
            )
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(response.encode("utf-8"))
            print(f"[Research] Done for topic: {topic}")

        except Exception as e:
            print(f"[Research] Error: {e}")
            response = json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(response.encode("utf-8"))

    def log_message(self, format, *args):
        print(f"[Server] {args[0]}")


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    server = HTTPServer(("127.0.0.1", port), ResearchHandler)
    print(f"Local API server running at http://127.0.0.1:{port}")
    print("API endpoint: POST http://127.0.0.1:8080/api/research")
    print("Press Ctrl+C to stop\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
