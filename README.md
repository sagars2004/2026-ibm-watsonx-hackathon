# 🔍 Silent Bottleneck Detector

> **IBM watsonx Hackathon 2026** | Theme: AI Demystified — From Idea to Deployment

An AI-powered tool that analyzes workflow patterns to surface hidden inefficiencies in your team. Built with watsonx.ai for intelligent pattern detection and watsonx Orchestrate for automated remediation workflows.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![React](https://img.shields.io/badge/react-19-blue.svg)

## 🎯 The Problem

Teams have invisible bottlenecks that slow everything down but fly under the radar:
- **Sarah reviews 78% of all PRs** - single point of failure
- **Deploy queue takes 18 hours** - hidden delay
- **CI/CD fails 40% of the time** - on the same integration test
- **Only 2 people touch auth code** - knowledge silo
- **34% of time in meetings** - productivity drain

These issues aren't tracked, aren't complained about, and quietly kill productivity.

## 💡 The Solution

An AI agent that:
1. **Monitors** GitHub, Jira, Slack, and CI/CD data
2. **Detects** patterns using watsonx.ai
3. **Surfaces** hidden bottlenecks with actionable insights
4. **Automates** remediation workflows via watsonx Orchestrate

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DATA SOURCES                                 │
│     GitHub PRs    │    Jira Tickets    │    Slack    │   CI/CD     │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        Flask Backend API                            │
│              Pattern Analysis • Metrics • Recommendations           │
└─────────────────────────────────────────────────────────────────────┘
                          │                 │
                          ▼                 ▼
              ┌───────────────────┐  ┌──────────────────────┐
              │    watsonx.ai     │  │  watsonx Orchestrate │
              │  Pattern Detection│  │  Automated Workflows │
              └───────────────────┘  └──────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      React Dashboard                                │
│         Health Score • Bottlenecks • Recommendations • Charts       │
└─────────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- IBM Cloud account with watsonx.ai and watsonx Orchestrate access

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template and add your credentials
cp ../.env.example .env
# Edit .env with your IBM credentials

# Run the server
python app.py
```

The API will be available at `http://localhost:5000`

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The dashboard will be available at `http://localhost:5173`

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/data/github` | GET | Get GitHub PR data |
| `/api/data/jira` | GET | Get Jira ticket data |
| `/api/data/slack` | GET | Get Slack activity data |
| `/api/data/cicd` | GET | Get CI/CD pipeline data |
| `/api/analyze` | POST | Run bottleneck analysis |
| `/api/metrics` | GET | Get summary metrics |
| `/api/recommendations` | GET | Get AI recommendations |
| `/api/orchestrate/trigger` | POST | Webhook for Orchestrate |

## 🔧 Configuration

### Environment Variables

```env
# watsonx.ai
WATSONX_API_KEY=your_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Cloudant
CLOUDANT_URL=your_cloudant_url
CLOUDANT_API_KEY=your_cloudant_api_key

# Mock Mode (for development)
USE_MOCK_AI=true
```

## 🎪 Demo Flow

1. **The Invisible Problem**: Dashboard shows everything looks "fine"
2. **AI Analysis Runs**: "Analyzing 30 days of team activity..."
3. **Bottlenecks Revealed**:
   - 🚨 Sarah is blocking 12 PRs (78% review concentration)
   - ⏰ Deploy process adds 18 hours of delay
   - 🔐 Only 2 people can touch auth code
   - 💬 34% of time spent in meetings
4. **AI Recommendations**: Actionable items for each issue
5. **Orchestration**: Auto-creates Jira tickets, schedules meetings
6. **Next Week**: Shows improvement metrics

## 🧰 Tech Stack

- **Backend**: Python, Flask, flask-cors
- **AI/ML**: IBM watsonx.ai, Granite models
- **Orchestration**: IBM watsonx Orchestrate
- **Database**: IBM Cloudant (with local JSON fallback)
- **Frontend**: React 19, Vite, Recharts
- **Styling**: Custom CSS with dark theme

## 📂 Project Structure

```
silent-bottleneck-detector/
├── backend/
│   ├── app.py                 # Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── mock_data/
│   │   ├── __init__.py
│   │   └── generators.py      # Mock data generators
│   └── services/
│       ├── __init__.py
│       ├── watsonx_client.py  # watsonx.ai integration
│       └── cloudant_client.py # Cloudant integration
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── HealthScoreCard.jsx
│   │   │   ├── BottleneckList.jsx
│   │   │   ├── MetricsGrid.jsx
│   │   │   ├── RecommendationPanel.jsx
│   │   │   └── TrendChart.jsx
│   │   └── index.css
│   └── package.json
├── .env.example
└── README.md
```

## 🏆 Why This Wins

- ✨ **Unique Angle**: Nobody else will build this
- 🎯 **Real Value**: Solves problems teams don't know they have
- 📊 **Data-Driven**: Shows actual metrics and visualizations
- 🤖 **True AI**: Pattern detection, not just automation
- 🔄 **Full Loop**: From detection to automated remediation

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built for the IBM watsonx Hackathon 2026
Theme: AI Demystified — From Idea to Deployment

---

Made with ♥ using watsonx.ai and watsonx Orchestrate
