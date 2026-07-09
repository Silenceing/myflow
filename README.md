# MyFlow - AI Research Agent

An AI research agent built with [CrewAI](https://crewai.com), featuring a React frontend and deployable on [EdgeOne Makers](https://pages.edgeone.ai).

## Project Structure

```
myflow/
├── frontend/                  React + Vite frontend
│   ├── src/
│   │   ├── App.jsx            Main React component
│   │   ├── main.jsx           Entry point
│   │   └── index.css          Styling
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── cloud-functions/           Python Cloud Functions (EdgeOne Makers)
│   └── research/
│       ├── index.py           Research API endpoint
│       └── requirements.txt
├── src/myflow/                CrewAI source code
│   ├── main.py                Flow orchestration
│   └── crews/
│       └── content_crew/      Research crew definition
├── dev_server.py              Local development server
├── edgeone.json               EdgeOne Makers configuration
├── pyproject.toml
└── .env                       Environment variables (not committed)
```

## Features

- AI-powered research on any topic
- Generates both English and Chinese reports
- Web search integration via SerperDevTool
- Clean, responsive React frontend with loading progress
- One-click deployment on EdgeOne Makers

## Prerequisites

- Python >= 3.10, < 3.14
- Node.js >= 18

## Local Development

### 1. Install dependencies

```bash
# Python dependencies
pip install uv
uv sync

# Frontend dependencies
cd frontend && npm install && cd ..
```

### 2. Configure environment

Create `.env` file in the project root:

```bash
# Using Ollama (local)
BASE_URL=http://localhost:11434
API_KEY=123456
MODEL=ollama/gemma4:latest
SERPER_API_KEY=your-serper-key

# Using OpenAI
# BASE_URL=
# MODEL=openai/gpt-4o
# API_KEY=sk-your-openai-key
# SERPER_API_KEY=your-serper-key
```

### 3. Start the application

Open two terminals:

**Terminal 1 - Backend API server:**
```bash
python dev_server.py
```

**Terminal 2 - Frontend dev server:**
```bash
cd frontend && npm run dev
```

### 4. Open in browser

Visit `http://localhost:5173`, enter a topic, and click "Start Research".

> The research typically takes 1-2 minutes. The frontend shows a progress bar and elapsed time.

## Deploy to EdgeOne Makers

### Option 1: Git Integration (Recommended)

1. Push this project to a GitHub repository
2. Log into [EdgeOne Makers Console](https://console.tencentcloud.com/edgeone/makers)
3. Click "Import Git Repository" and select your repository
4. Configure environment variables:

| Variable | Description |
|----------|-------------|
| `MODEL` | LLM model name, e.g. `openai/gpt-4o` |
| `API_KEY` | API key for the LLM provider |
| `BASE_URL` | Custom LLM base URL (leave empty for OpenAI) |
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
- 200,000 Cloud Function executions/month

Use the built-in AI Gateway:
```bash
MODEL=openai/gpt-4o
API_KEY=<your-api-key>
BASE_URL=https://ai-gateway.edgeone.link/v1
```

## API

```
POST /api/research
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
