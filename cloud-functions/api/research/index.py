from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"message": "GET works!"}).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body_bytes = self.rfile.read(content_length)
        body = json.loads(body_bytes) if body_bytes else {}

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({
            "success": True,
            "topic": body.get("topic", "test"),
            "report_en": "English report placeholder",
            "report_cn": "中文报告占位符"
        }).encode('utf-8'))
