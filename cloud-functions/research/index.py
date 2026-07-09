import json
import os
import sys
import tempfile

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
src_dir = os.path.join(project_root, "src")
sys.path.insert(0, src_dir)

output_dir = os.path.join(project_root, "output")
os.makedirs(output_dir, exist_ok=True)

from myflow.crews.content_crew.content_crew import ResearchCrew
from myflow.main import LatestAiFlow


def main(args):
    req = args.get("request", {})
    method = req.get("method", "GET")

    if method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            },
            "body": "",
        }

    if method != "POST":
        return {
            "statusCode": 405,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Method not allowed"}),
        }

    try:
        body = req.get("body", {})
        if isinstance(body, str):
            body = json.loads(body)

        topic = body.get("topic", "AI Agents")

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

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(
                {
                    "success": True,
                    "topic": topic,
                    "report_en": report_en,
                    "report_cn": report_cn,
                },
                ensure_ascii=False,
            ),
        }
    except Exception as e:
        import traceback
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(
                {"success": False, "error": str(e), "trace": traceback.format_exc()},
                ensure_ascii=False,
            ),
        }
