# MyFlow - AI Research Agent

An AI research agent built with [CrewAI](https://crewai.com), featuring a React frontend and deployable on [EdgeOne Makers](https://pages.edgeone.ai).

## Project Structure

```
myflow/
├── src/                       React + Vite frontend
│   ├── App.jsx                Main React component
│   ├── main.jsx               Entry point
│   └── index.css              Styling
├── agents/                    CrewAI Agent (EdgeOne Makers)
│   ├── stream.py              Agent handler endpoint
│   ├── requirements.txt       Python dependencies
│   └── _crews/                CrewAI crew definitions
│       └── content_crew/
│           ├── content_crew.py
│           └── config/
│               ├── agents.yaml
│               └── tasks.yaml
├── python_src/                Python source code (for local dev)
│   └── myflow/
├── index.html                 Entry HTML
├── package.json               Frontend dependencies
├── edgeone.json               EdgeOne Makers configuration
└── .env                       Environment variables (not committed)
```

## Features

- AI-powered research on any topic
- Generates both English and Chinese reports
- Web search integration via SerperDevTool
- Clean, responsive React frontend with loading progress
- One-click deployment on EdgeOne Makers

## Prerequisites

- Node.js >= 18
- Python 3.11+
- EdgeOne CLI

## Local Development

### 1. Install EdgeOne CLI

```bash
npm install -g edgeone
edgeone login
```

### 2. Install dependencies

```bash
npm install
```

### 3. Configure environment

Create `.env` file in the project root:

```bash
AI_GATEWAY_API_KEY=your-api-key
AI_GATEWAY_BASE_URL=https://ai-gateway.edgeone.link/v1
AI_GATEWAY_MODEL=openai/gpt-4o
SERPER_API_KEY=your-serper-key
```

### 4. Start local development server

```bash
edgeone makers dev
```

Visit `http://localhost:8080`, enter a topic, and click "Start Research".

> The research typically takes 1-2 minutes. The frontend shows a progress bar and elapsed time.

## Deploy to EdgeOne Makers

### Option 1: Git Integration (Recommended)

1. Push this project to a GitHub repository
2. Log into [EdgeOne Makers Console](https://console.tencentcloud.com/edgeone/makers)
3. Click "Import Git Repository" and select your repository
4. Configure environment variables:

| Variable | Description |
|----------|-------------|
| `AI_GATEWAY_API_KEY` | Model gateway API key |
| `AI_GATEWAY_BASE_URL` | Gateway base URL, e.g. `https://ai-gateway.edgeone.link/v1` |
| `AI_GATEWAY_MODEL` | Model ID, e.g. `openai/gpt-4o` (optional, defaults to `@makers/deepseek-v4-flash`) |
| `SERPER_API_KEY` | SerperDev API key for web search |

5. Click "Deploy"

### Option 2: EdgeOne CLI

```bash
npm install -g edgeone
edgeone login
edgeone makers init
edgeone makers deploy
```

### EdgeOne Makers Free Tier

- 500,000 Tokens/month (via built-in AI Gateway)
- Unlimited static site traffic
- 200,000 Agent executions/month

Use the built-in AI Gateway:
```bash
AI_GATEWAY_API_KEY=<your-api-key>
AI_GATEWAY_BASE_URL=https://ai-gateway.edgeone.link/v1
AI_GATEWAY_MODEL=openai/gpt-4o
```

## API

```
POST /stream
Content-Type: application/json

{"topic": "AI Agents"}
```

Response:
```json
{
  "success": true,
  "topic": "AI Agents",
  "report_en": "...",
  "report_cn": "..."
}
```

## Support

- [CrewAI Documentation](https://docs.crewai.com)
- [EdgeOne Makers Documentation](https://pages.edgeone.ai/document/product-introduction)
