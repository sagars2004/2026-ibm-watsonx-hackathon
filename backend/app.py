"""
Silent Bottleneck Detector - Flask Backend API
"""

import os
import uuid
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from mock_data import generate_github_data, generate_jira_data, generate_slack_data, generate_cicd_data, generate_all_mock_data
from services import get_watsonx_client, get_cloudant_client

app = Flask(__name__)

# A2A Protocol API Key (for watsonx Orchestrate authentication)
A2A_API_KEY = os.getenv("A2A_API_KEY", "bottleneck-detector-key-2026")

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
CORS(app, origins=[frontend_url, "http://localhost:3000", "http://localhost:5173", "*"])

_cached_data = None
_cache_timestamp = None


def get_mock_data(days: int = 30, force_refresh: bool = False):
    global _cached_data, _cache_timestamp
    
    if (force_refresh or _cached_data is None or _cache_timestamp is None or
        (datetime.now() - _cache_timestamp).seconds > 300):
        _cached_data = generate_all_mock_data(days)
        _cache_timestamp = datetime.now()
    
    return _cached_data


# ============================================
# A2A Protocol Endpoints (for watsonx Orchestrate)
# ============================================

@app.route("/.well-known/agent.json", methods=["GET"])
def a2a_agent_card():
    """A2A Agent Card - describes this agent's capabilities"""
    base_url = request.host_url.rstrip('/')
    
    return jsonify({
        "name": "Bottleneck Detector",
        "description": "AI-powered agent that analyzes team workflows to detect hidden bottlenecks in code reviews, deployments, meetings, and CI/CD pipelines. Provides health scores and actionable recommendations.",
        "url": base_url,
        "version": "1.0.0",
        "capabilities": {
            "streaming": False,
            "pushNotifications": False
        },
        "skills": [
            {
                "id": "analyze_bottlenecks",
                "name": "Analyze Team Bottlenecks",
                "description": "Run a comprehensive analysis to detect hidden workflow bottlenecks",
                "tags": ["analysis", "bottlenecks", "workflow"]
            },
            {
                "id": "get_health_score",
                "name": "Get Health Score",
                "description": "Get the current team health score (0-100)",
                "tags": ["metrics", "health"]
            },
            {
                "id": "get_recommendations",
                "name": "Get Recommendations",
                "description": "Get AI-generated recommendations to fix bottlenecks",
                "tags": ["recommendations", "actions"]
            },
            {
                "id": "get_github_data",
                "name": "Get GitHub Data",
                "description": "Retrieve GitHub PR and code review metrics",
                "tags": ["github", "data"]
            },
            {
                "id": "get_jira_data",
                "name": "Get Jira Data",
                "description": "Retrieve Jira ticket flow data",
                "tags": ["jira", "data"]
            }
        ],
        "defaultInputModes": ["text"],
        "defaultOutputModes": ["text"],
        "authentication": {
            "type": "apiKey",
            "header": "X-API-Key"
        }
    })


@app.route("/", methods=["POST"])
def root_post():
    """Handle POST to root - Orchestrate sends A2A requests here"""
    return a2a_task_send()


@app.route("/a2a/tasks/send", methods=["POST"])
def a2a_task_send():
    """A2A Task Endpoint - receives and processes tasks from Orchestrate"""
    # Verify API key
    api_key = request.headers.get("X-API-Key")
    if api_key != A2A_API_KEY:
        return jsonify({"error": "Invalid API key"}), 401
    
    body = request.get_json() or {}
    
    # Log incoming request for debugging
    print(f"📨 A2A Request received: {body}")
    
    task_id = body.get("id", str(uuid.uuid4()))
    user_content = ""
    
    # Try multiple ways to extract the user message
    # Method 1: A2A standard format
    message = body.get("message", {})
    if "parts" in message:
        for part in message.get("parts", []):
            if part.get("type") == "text":
                user_content = part.get("text", "")
                break
    
    # Method 2: Direct content field
    if not user_content:
        user_content = body.get("content", "")
    
    # Method 3: Input field
    if not user_content:
        user_content = body.get("input", "")
    
    # Method 4: Query field
    if not user_content:
        user_content = body.get("query", "")
    
    # Method 5: Text field
    if not user_content:
        user_content = body.get("text", "")
    
    print(f"📝 Extracted user content: {user_content}")
    user_content = user_content.lower()
    
    # Process the request based on content
    watsonx = get_watsonx_client()
    data = get_mock_data(30)
    
    response_text = ""
    
    if "health" in user_content or "score" in user_content:
        analysis = watsonx.analyze_bottlenecks(data)
        response_text = f"📊 **Team Health Score: {analysis['health_score']}/100**\n\n"
        response_text += f"Status: {'✅ Healthy' if analysis['health_status'] == 'healthy' else '⚠️ ' + analysis['health_status'].title()}\n"
        response_text += f"Bottlenecks detected: {len(analysis['bottlenecks'])}"
        
    elif "bottleneck" in user_content or "analyze" in user_content or "analysis" in user_content:
        analysis = watsonx.analyze_bottlenecks(data)
        response_text = f"🔍 **Bottleneck Analysis Results**\n\n"
        response_text += f"Health Score: {analysis['health_score']}/100\n\n"
        response_text += "**Detected Bottlenecks:**\n"
        for b in analysis['bottlenecks'][:5]:
            response_text += f"- {b['icon']} **{b['title']}** ({b['severity']}): {b['description']}\n"
            
    elif "recommend" in user_content:
        analysis = watsonx.analyze_bottlenecks(data)
        recommendations = watsonx.generate_recommendations(analysis)
        response_text = "💡 **Recommendations**\n\n"
        for rec in recommendations[:5]:
            response_text += f"- **{rec['title']}** (Priority: {rec['priority']})\n"
            
    elif "github" in user_content:
        github = data["github"]["summary"]
        response_text = f"📊 **GitHub Metrics**\n\n"
        response_text += f"- Total PRs: {github['total_prs']}\n"
        response_text += f"- Avg Review Time: {github['avg_review_time_hours']} hours\n"
        response_text += f"- Pending Reviews: {github['pending_reviews']}"
        
    elif "jira" in user_content:
        jira = data["jira"]["summary"]
        response_text = f"📋 **Jira Metrics**\n\n"
        response_text += f"- Total Tickets: {jira['total_tickets']}\n"
        response_text += f"- Blocked: {jira['blocked_count']}\n"
        response_text += f"- Velocity: {jira['velocity']} points"
        
    else:
        response_text = "👋 I'm the Bottleneck Detector! I can help you with:\n\n"
        response_text += "- **Analyze bottlenecks** - Run a full workflow analysis\n"
        response_text += "- **Get health score** - Check team health (0-100)\n"
        response_text += "- **Get recommendations** - AI-suggested improvements\n"
        response_text += "- **GitHub/Jira data** - View specific metrics\n\n"
        response_text += "What would you like to know?"
    
    # Return response in multiple formats for compatibility
    return jsonify({
        "id": task_id,
        "status": "completed",
        # A2A standard format
        "result": {
            "parts": [
                {
                    "type": "text",
                    "text": response_text
                }
            ]
        },
        # Alternative formats Orchestrate might expect
        "output": response_text,
        "message": {
            "role": "assistant",
            "content": response_text,
            "parts": [
                {
                    "type": "text", 
                    "text": response_text
                }
            ]
        },
        "response": response_text
    })


# ============================================
# Standard API Endpoints
# ============================================

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Silent Bottleneck Detector",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
    })


@app.route("/api/data/github", methods=["GET"])
def get_github_data_endpoint():
    days = request.args.get("days", 30, type=int)
    data = get_mock_data(days)
    return jsonify(data["github"])


@app.route("/api/data/jira", methods=["GET"])
def get_jira_data_endpoint():
    days = request.args.get("days", 30, type=int)
    data = get_mock_data(days)
    return jsonify(data["jira"])


@app.route("/api/data/slack", methods=["GET"])
def get_slack_data_endpoint():
    days = request.args.get("days", 30, type=int)
    data = get_mock_data(days)
    return jsonify(data["slack"])


@app.route("/api/data/cicd", methods=["GET"])
def get_cicd_data_endpoint():
    days = request.args.get("days", 30, type=int)
    data = get_mock_data(days)
    return jsonify(data["cicd"])


@app.route("/api/data/all", methods=["GET"])
def get_all_data():
    days = request.args.get("days", 30, type=int)
    refresh = request.args.get("refresh", "false").lower() == "true"
    data = get_mock_data(days, force_refresh=refresh)
    return jsonify(data)


@app.route("/api/analyze", methods=["POST"])
def analyze_bottlenecks():
    body = request.get_json() or {}
    days = body.get("days", 30)
    save_results = body.get("save", True)
    
    data = get_mock_data(days, force_refresh=True)
    
    watsonx = get_watsonx_client()
    analysis = watsonx.analyze_bottlenecks(data)
    recommendations = watsonx.generate_recommendations(analysis)
    analysis["recommendations"] = recommendations
    
    if save_results:
        cloudant = get_cloudant_client()
        cloudant.store_analysis(analysis)
        for rec in recommendations:
            cloudant.store_recommendation(rec)
    
    return jsonify(analysis)


@app.route("/api/analyze/quick", methods=["GET"])
def quick_analysis():
    data = get_mock_data(30)
    watsonx = get_watsonx_client()
    analysis = watsonx.analyze_bottlenecks(data)
    return jsonify(analysis)


@app.route("/api/metrics", methods=["GET"])
def get_metrics():
    data = get_mock_data(30)
    
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "github": data["github"]["summary"],
        "jira": data["jira"]["summary"],
        "slack": data["slack"]["summary"],
        "cicd": data["cicd"]["summary"],
        "overall": {
            "data_period_days": data["period_days"],
            "generated_at": data["generated_at"],
        }
    }
    
    cloudant = get_cloudant_client()
    metrics["historical"] = cloudant.get_summary_stats()
    
    return jsonify(metrics)


@app.route("/api/metrics/health-score", methods=["GET"])
def get_health_score():
    data = get_mock_data(30)
    watsonx = get_watsonx_client()
    analysis = watsonx.analyze_bottlenecks(data)
    
    return jsonify({
        "health_score": analysis["health_score"],
        "health_status": analysis["health_status"],
        "bottleneck_count": len(analysis["bottlenecks"]),
        "timestamp": datetime.now().isoformat(),
    })


@app.route("/api/recommendations", methods=["GET"])
def get_recommendations():
    data = get_mock_data(30)
    watsonx = get_watsonx_client()
    analysis = watsonx.analyze_bottlenecks(data)
    recommendations = watsonx.generate_recommendations(analysis)
    
    return jsonify({
        "recommendations": recommendations,
        "count": len(recommendations),
        "generated_at": datetime.now().isoformat(),
    })


@app.route("/api/orchestrate/trigger", methods=["POST"])
def orchestrate_trigger():
    body = request.get_json() or {}
    action = body.get("action", "weekly_analysis")
    params = body.get("params", {})
    
    result = {
        "action": action,
        "status": "completed",
        "timestamp": datetime.now().isoformat(),
        "outputs": {},
    }
    
    if action == "weekly_analysis":
        days = params.get("days", 30)
        data = get_mock_data(days, force_refresh=True)
        watsonx = get_watsonx_client()
        analysis = watsonx.analyze_bottlenecks(data)
        
        result["outputs"] = {
            "health_score": analysis["health_score"],
            "bottleneck_count": len(analysis["bottlenecks"]),
            "summary": analysis["summary"],
        }
        
    elif action == "send_slack_summary":
        data = get_mock_data(30)
        watsonx = get_watsonx_client()
        analysis = watsonx.analyze_bottlenecks(data)
        
        slack_message = {
            "blocks": [
                {"type": "header", "text": {"type": "plain_text", "text": "🔍 Weekly Bottleneck Report"}},
                {"type": "section", "text": {"type": "mrkdwn", "text": f"*Health Score:* {analysis['health_score']}/100"}}
            ]
        }
        
        result["outputs"] = {"slack_message": slack_message, "channel": "#engineering"}
    
    return jsonify(result)


@app.route("/api/orchestrate/skills", methods=["GET"])
def get_orchestrate_skills():
    skills = [
        {
            "name": "Analyze Team Bottlenecks",
            "description": "Analyze workflow data to detect hidden bottlenecks",
            "endpoint": "/api/analyze",
            "method": "POST",
        },
        {
            "name": "Get Health Score",
            "description": "Get the current team health score",
            "endpoint": "/api/metrics/health-score",
            "method": "GET",
        },
        {
            "name": "Send Slack Summary",
            "description": "Send a formatted summary to Slack",
            "endpoint": "/api/orchestrate/trigger",
            "method": "POST",
        },
    ]
    
    return jsonify({"service": "Silent Bottleneck Detector", "version": "1.0.0", "skills": skills})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    
    print("\n" + "=" * 60)
    print("🔍 Silent Bottleneck Detector - API Server")
    print("=" * 60)
    print(f"📍 Running on: http://localhost:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"🤖 Mock AI mode: {os.getenv('USE_MOCK_AI', 'true')}")
    print("=" * 60 + "\n")
    
    app.run(host="0.0.0.0", port=port, debug=debug)
