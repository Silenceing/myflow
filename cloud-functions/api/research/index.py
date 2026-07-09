from http.server import BaseHTTPRequestHandler
import json
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
src_dir = os.path.join(project_root, "src")
sys.path.insert(0, src_dir)

output_dir = os.path.join(project_root, "output")
os.makedirs(output_dir, exist_ok=True)

class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body_bytes = self.rfile.read(content_length)
            body = json.loads(body_bytes.decode('utf-8')) if body_bytes else {}

            topic = body.get("topic", "AI Agents")

            from myflow.main import LatestAiFlow
            flow = LatestAiFlow()
            flow.state.topic = topic
            flow.kickoff()

            report_en = ""
            report_cn = ""

            en_path = os.path.join(output_dir, "report.md")
            cn_path = os.path.join(output_dir, "report_cn.md")

            if os.path.exists(en_path):
                with open(en_path, "r", encoding="utf-8") as f:
                    report_en = f.read()

            if os.path.exists(cn_path):
                with open(cn_path, "r", encoding="utf-8") as f:
                    report_cn = f.read()

            result = json.dumps({
                "success": True,
                "topic": topic,
                "report_en": report_en,
                "report_cn": report_cn,
            }, ensure_ascii=False)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(result.encode('utf-8'))

        except Exception as e:
            import traceback
            result = json.dumps({
                "success": False,
                "error": str(e),
                "trace": traceback.format_exc()
            }, ensure_ascii=False)

            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(result.encode('utf-8'))
