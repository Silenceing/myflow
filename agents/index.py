import os
os.environ.setdefault('CREWAI_DISABLE_VERSION_CHECK', 'true')

import sys
import json
import traceback

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
python_src = os.path.join(project_root, "python_src")
if python_src not in sys.path:
    sys.path.insert(0, python_src)


async def handler(context):
    """POST /index — research endpoint."""

    body = context.request.body or {}
    topic = body.get("topic", "AI Agents")

    try:
        os.environ["MODEL"] = context.env.get("MODEL", "openai/gpt-4o")
        os.environ["BASE_URL"] = context.env.get("BASE_URL", "")
        os.environ["API_KEY"] = context.env.get("API_KEY", "")
        os.environ["SERPER_API_KEY"] = context.env.get("SERPER_API_KEY", "")

        from _crews.content_crew.content_crew import ResearchCrew

        crew = ResearchCrew().crew()
        result = crew.kickoff(inputs={"topic": topic})

        report_en = ""
        report_cn = ""

        if result.tasks_output and len(result.tasks_output) >= 1:
            report_en = result.tasks_output[0].raw
        if result.tasks_output and len(result.tasks_output) >= 2:
            report_cn = result.tasks_output[1].raw

        return {
            "status_code": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "success": True,
                "topic": topic,
                "report_en": report_en,
                "report_cn": report_cn,
            }, ensure_ascii=False)
        }

    except Exception as e:
        return {
            "status_code": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "success": False,
                "error": str(e),
                "trace": traceback.format_exc()
            }, ensure_ascii=False)
        }
