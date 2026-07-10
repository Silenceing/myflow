import os
os.environ.setdefault('CREWAI_DISABLE_VERSION_CHECK', 'true')
os.environ.setdefault('OTEL_TRACES_EXPORTER', 'none')
os.environ.setdefault('OTEL_METRICS_EXPORTER', 'none')
os.environ.setdefault('OTEL_LOGS_EXPORTER', 'none')
os.environ.setdefault('CREWAI_DISABLE_TELEMETRY', 'true')

import sys
import json
import traceback

agents_dir = os.path.dirname(os.path.abspath(__file__))
if agents_dir not in sys.path:
    sys.path.insert(0, agents_dir)


async def handler(context):
    """POST /stream — research endpoint."""

    body = context.request.body or {}
    topic = body.get("topic", "AI Agents")

    try:
        env = dict(context.env or {})

        os.environ.setdefault("OPENAI_API_KEY", env.get("AI_GATEWAY_API_KEY", ""))
        os.environ.setdefault("OPENAI_API_BASE", env.get("AI_GATEWAY_BASE_URL", "https://ai-gateway.edgeone.link/v1"))
        os.environ.setdefault("OPENAI_MODEL_NAME", env.get("AI_GATEWAY_MODEL", "gpt-4o"))
        os.environ.setdefault("SERPER_API_KEY", env.get("SERPER_API_KEY", ""))

        # pass context.env directly to the crew module (used by create_llm)
        import _crews.content_crew.content_crew as _cc
        _cc._env = env

        from _crews.content_crew.content_crew import ResearchCrew

        print(f"DEBUG: AI_GATEWAY_API_KEY={'set' if env.get('AI_GATEWAY_API_KEY') else 'MISSING'}", flush=True)
        print(f"DEBUG: AI_GATEWAY_BASE_URL={env.get('AI_GATEWAY_BASE_URL', 'MISSING')}", flush=True)
        print(f"DEBUG: AI_GATEWAY_MODEL={env.get('AI_GATEWAY_MODEL', 'MISSING')}", flush=True)
        print(f"DEBUG: env keys={list(env.keys())}", flush=True)

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
