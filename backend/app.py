"""
Silent Bottleneck Detector - Flask Backend API

Main application entry point with all API endpoints for:
- Mock data retrieval (GitHub, Jira, Slack, CI/CD)
- Bottleneck analysis using watsonx.ai
- Recommendations and metrics
- Orchestration webhooks
"""

import os
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our modules
from mock_data import (
    generate_github_data,
    generate_jira_data,
    generate_slack_data,
    generate_cicd_data,
    generate_all_mock_data,
)
from services import get_watsonx_client, get_cloudant_client

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
CORS(app, origins=[frontend_url, "http://localhost:3000", "http://localhost:5173", "*"])

# Cache for mock data (regenerated on demand)
_cached_data = None
_cache_timestamp = None


def get_mock_data(days: int = 30, force_refresh: bool = False):
    """Get cached mock data or generate fresh data."""
    global _cached_data, _cache_timestamp
    
    # Refresh cache if older than 5 minutes or forced
    if (force_refresh or _cached_data is None or _cache_timestamp is None or
        (datetime.now() - _cache_timestamp).seconds > 300):
        _cached_data = generate_all_mock_data(days)
        _cache_timestamp = datetime.now()
    
    return _cached_data


# =============================================================================
# Health Check
# =============================================================================

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Silent Bottleneck Detector",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
    })


# =============================================================================
# Data Endpoints (Mock Data)
# =============================================================================

@app.route("/api/data/github", methods=["GET"])
def get_github_data():
    """Get GitHub PR and review data."""
    days = request.args.get("days", 30, type=int)
    data = get_mock_data(days)
    return jsonify(data["github"])


@app.route("/api/data/jira", methods=["GET"])
def get_jira_data():
    """Get Jira ticket and flow data."""
    days = request.args.get("days", 30, type=int)
    data = get_mock_data(days)
    return jsonify(data["jira"])


@app.route("/api/data/slack", methods=["GET"])
def get_slack_data():
    """Get Slack activity and meeting data."""
    days = request.args.get("days", 30, type=int)
    data = get_mock_data(days)
    return jsonify(data["slack"])


@app.route("/api/data/cicd", methods=["GET"])
def get_cicd_data():
    """Get CI/CD pipeline data."""
    days = request.args.get("days", 30, type=int)
    data = get_mock_data(days)
    return jsonify(data["cicd"])


@app.route("/api/data/all", methods=["GET"])
def get_all_data():
    """Get all mock data combined."""
    days = request.args.get("days", 30, type=int)
    refresh = request.args.get("refresh", "false").lower() == "true"
    data = get_mock_data(days, force_refresh=refresh)
    return jsonify(data)


# =============================================================================
# Analysis Endpoints
# =============================================================================

@app.route("/api/analyze", methods=["POST"])
def analyze_bottlenecks():
    """
    Trigger bottleneck analysis using watsonx.ai.
    
    Request body (optional):
        {
            "days": 30,  // Number of days to analyze
            "save": true  // Whether to save to Cloudant
        }
    
    Returns:
        Analysis results with detected bottlenecks and recommendations
    """
    # Get request parameters
    body = request.get_json() or {}
    days = body.get("days", 30)
    save_results = body.get("save", True)
    
    # Get the data
    data = get_mock_data(days, force_refresh=True)
    
    # Run analysis
    watsonx = get_watsonx_client()
    analysis = watsonx.analyze_bottlenecks(data)
    
    # Generate recommendations
    recommendations = watsonx.generate_recommendations(analysis)
    analysis["recommendations"] = recommendations
    
    # Save to Cloudant if requested
    if save_results:
        cloudant = get_cloudant_client()
        cloudant.store_analysis(analysis)
        
        # Store recommendations
        for rec in recommendations:
            cloudant.store_recommendation(rec)
    
    return jsonify(analysis)


@app.route("/api/analyze/quick", methods=["GET"])
def quick_analysis():
    """Quick analysis endpoint for demos - uses cached data."""
    data = get_mock_data(30)
    watsonx = get_watsonx_client()
    analysis = watsonx.analyze_bottlenecks(data)
    return jsonify(analysis)


# =============================================================================
# Metrics Endpoints
# =============================================================================

@app.route("/api/metrics", methods=["GET"])
def get_metrics():
    """Get current metrics summary."""
    data = get_mock_data(30)
    
    # Combine summaries from all data sources
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
    
    # Get historical stats from Cloudant
    cloudant = get_cloudant_client()
    metrics["historical"] = cloudant.get_summary_stats()
    
    return jsonify(metrics)


@app.route("/api/metrics/health-score", methods=["GET"])
def get_health_score():
    """Get just the health score for quick dashboard updates."""
    data = get_mock_data(30)
    watsonx = get_watsonx_client()
    analysis = watsonx.analyze_bottlenecks(data)
    
    return jsonify({
        "health_score": analysis["health_score"],
        "health_status": analysis["health_status"],
        "bottleneck_count": len(analysis["bottlenecks"]),
        "timestamp": datetime.now().isoformat(),
    })


# =============================================================================
# Recommendations Endpoints
# =============================================================================

@app.route("/api/recommendations", methods=["GET"])
def get_recommendations():
    """Get current recommendations."""
    # Get latest analysis
    data = get_mock_data(30)
    watsonx = get_watsonx_client()
    analysis = watsonx.analyze_bottlenecks(data)
    recommendations = watsonx.generate_recommendations(analysis)
    
    return jsonify({
        "recommendations": recommendations,
        "count": len(recommendations),
        "generated_at": datetime.now().isoformat(),
    })


@app.route("/api/recommendations/<rec_id>/status", methods=["PUT"])
def update_recommendation_status(rec_id: str):
    """Update the status of a recommendation."""
    body = request.get_json() or {}
    new_status = body.get("status", "in_progress")
    
    cloudant = get_cloudant_client()
    
    # This is simplified for the demo
    return jsonify({
        "id": rec_id,
        "status": new_status,
        "updated_at": datetime.now().isoformat(),
    })


# =============================================================================
# Orchestration Endpoints (for watsonx Orchestrate webhooks)
# =============================================================================

@app.route("/api/orchestrate/trigger", methods=["POST"])
def orchestrate_trigger():
    """
    Webhook endpoint for watsonx Orchestrate to trigger actions.
    
    Request body:
        {
            "action": "weekly_analysis" | "balance_workload" | "create_tickets",
            "params": { ... }
        }
    """
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
        # Run full analysis
        days = params.get("days", 30)
        data = get_mock_data(days, force_refresh=True)
        watsonx = get_watsonx_client()
        analysis = watsonx.analyze_bottlenecks(data)
        
        result["outputs"] = {
            "health_score": analysis["health_score"],
            "bottleneck_count": len(analysis["bottlenecks"]),
            "summary": analysis["summary"],
            "top_bottleneck": analysis["bottlenecks"][0] if analysis["bottlenecks"] else None,
        }
        
    elif action == "balance_workload":
        # Return workload distribution recommendation
        data = get_mock_data(30)
        reviewer_stats = data["github"]["reviewer_stats"]
        
        # Find overloaded reviewers
        overloaded = [
            {"reviewer": stats["member"]["name"], "load": stats["percentage"]}
            for reviewer_id, stats in reviewer_stats.items()
            if stats["percentage"] > 30
        ]
        
        result["outputs"] = {
            "overloaded_reviewers": overloaded,
            "recommendation": "Redistribute PR reviews to balance workload",
            "suggested_assignees": ["Mike Johnson", "Alex Rivera"],
        }
        
    elif action == "create_tickets":
        # Simulate creating Jira tickets for recommendations
        data = get_mock_data(30)
        watsonx = get_watsonx_client()
        analysis = watsonx.analyze_bottlenecks(data)
        
        tickets_created = []
        for i, bottleneck in enumerate(analysis["bottlenecks"][:3]):  # Top 3
            tickets_created.append({
                "ticket_id": f"BOTTLENECK-{1000 + i}",
                "title": f"Address: {bottleneck['title']}",
                "priority": bottleneck["severity"].upper(),
                "assignee": "Team Lead",
            })
        
        result["outputs"] = {
            "tickets_created": tickets_created,
            "count": len(tickets_created),
        }
        
    elif action == "send_slack_summary":
        # Generate Slack-formatted summary
        data = get_mock_data(30)
        watsonx = get_watsonx_client()
        analysis = watsonx.analyze_bottlenecks(data)
        
        slack_message = {
            "blocks": [
                {
                    "type": "header",
                    "text": {"type": "plain_text", "text": "🔍 Weekly Bottleneck Report"}
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Health Score:* {analysis['health_score']}/100\n*Bottlenecks Detected:* {len(analysis['bottlenecks'])}"
                    }
                }
            ]
        }
        
        # Add bottleneck summaries
        for b in analysis["bottlenecks"][:3]:
            slack_message["blocks"].append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{b.get('icon', '⚠️')} *{b['title']}*\n{b['description']}"
                }
            })
        
        result["outputs"] = {
            "slack_message": slack_message,
            "channel": "#engineering",
        }
    
    return jsonify(result)


@app.route("/api/orchestrate/skills", methods=["GET"])
def get_orchestrate_skills():
    """
    Return available skills for watsonx Orchestrate registration.
    This endpoint describes what actions this API can perform.
    """
    skills = [
        {
            "name": "Analyze Team Bottlenecks",
            "description": "Analyze GitHub, Jira, Slack, and CI/CD data to detect hidden bottlenecks",
            "endpoint": "/api/analyze",
            "method": "POST",
            "parameters": [
                {"name": "days", "type": "integer", "description": "Number of days to analyze", "default": 30}
            ],
            "outputs": ["health_score", "bottlenecks", "recommendations"]
        },
        {
            "name": "Get Health Score",
            "description": "Get the current team health score",
            "endpoint": "/api/metrics/health-score",
            "method": "GET",
            "parameters": [],
            "outputs": ["health_score", "health_status", "bottleneck_count"]
        },
        {
            "name": "Trigger Weekly Analysis",
            "description": "Run weekly analysis and generate recommendations",
            "endpoint": "/api/orchestrate/trigger",
            "method": "POST",
            "parameters": [
                {"name": "action", "type": "string", "value": "weekly_analysis"}
            ],
            "outputs": ["health_score", "bottleneck_count", "summary"]
        },
        {
            "name": "Create Bottleneck Tickets",
            "description": "Create Jira tickets for detected bottlenecks",
            "endpoint": "/api/orchestrate/trigger",
            "method": "POST",
            "parameters": [
                {"name": "action", "type": "string", "value": "create_tickets"}
            ],
            "outputs": ["tickets_created", "count"]
        },
        {
            "name": "Send Slack Summary",
            "description": "Send a formatted summary to Slack",
            "endpoint": "/api/orchestrate/trigger",
            "method": "POST",
            "parameters": [
                {"name": "action", "type": "string", "value": "send_slack_summary"}
            ],
            "outputs": ["slack_message", "channel"]
        },
    ]
    
    return jsonify({
        "service": "Silent Bottleneck Detector",
        "version": "1.0.0",
        "skills": skills,
    })


# =============================================================================
# Demo Endpoints
# =============================================================================

@app.route("/api/demo/scenario/<scenario_name>", methods=["GET"])
def get_demo_scenario(scenario_name: str):
    """
    Get pre-configured demo scenarios.
    
    Scenarios:
        - critical: Team in crisis (health score < 50)
        - warning: Several issues (health score 50-70)
        - healthy: Minor issues only (health score > 80)
        - improvement: Show week-over-week improvement
    """
    scenarios = {
        "critical": {
            "description": "Team in crisis with multiple severe bottlenecks",
            "health_score": 35,
            "bottlenecks": [
                {
                    "type": "single_point_of_failure",
                    "severity": "high",
                    "title": "Critical PR Review Bottleneck",
                    "description": "Sarah approved 92% of all PRs - 18 PRs waiting for her review",
                    "icon": "🚨",
                },
                {
                    "type": "flaky_process",
                    "severity": "high", 
                    "title": "CI/CD Pipeline Broken",
                    "description": "55% failure rate - integration tests failing consistently",
                    "icon": "🔄",
                },
                {
                    "type": "meeting_overload",
                    "severity": "high",
                    "title": "Severe Meeting Overload",
                    "description": "Team spending 48% of time in meetings",
                    "icon": "💬",
                },
            ]
        },
        "warning": {
            "description": "Several issues that need attention",
            "health_score": 62,
            "bottlenecks": [
                {
                    "type": "single_point_of_failure",
                    "severity": "medium",
                    "title": "PR Review Concentration",
                    "description": "Sarah approved 65% of all PRs last month",
                    "icon": "⚠️",
                },
                {
                    "type": "knowledge_silo",
                    "severity": "medium",
                    "title": "Knowledge Silo: Payments",
                    "description": "Only 2 people have touched payments code",
                    "icon": "🔐",
                },
            ]
        },
        "healthy": {
            "description": "Team is performing well with minor issues",
            "health_score": 85,
            "bottlenecks": [
                {
                    "type": "hidden_delay",
                    "severity": "low",
                    "title": "Minor Deploy Delay",
                    "description": "Average deploy time of 4 hours (target: 2 hours)",
                    "icon": "⏰",
                },
            ]
        },
        "improvement": {
            "description": "Showing week-over-week improvement",
            "health_score": 78,
            "previous_health_score": 58,
            "bottlenecks": [
                {
                    "type": "single_point_of_failure",
                    "severity": "medium",
                    "title": "PR Review Distribution (Improving)",
                    "description": "Sarah's review load reduced from 78% to 55%",
                    "icon": "📈",
                },
            ],
            "improvements": [
                "PR review load distributed across 3 more developers",
                "CI/CD failure rate reduced from 40% to 15%",
                "Average deploy time reduced from 18h to 6h",
            ]
        },
    }
    
    if scenario_name not in scenarios:
        return jsonify({"error": f"Unknown scenario: {scenario_name}"}), 404
    
    return jsonify(scenarios[scenario_name])


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    
    print("\n" + "=" * 60)
    print("🔍 Silent Bottleneck Detector - API Server")
    print("=" * 60)
    print(f"📍 Running on: http://localhost:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"🤖 Mock AI mode: {os.getenv('USE_MOCK_AI', 'true')}")
    print("=" * 60)
    print("\nEndpoints:")
    print("  GET  /api/health              - Health check")
    print("  GET  /api/data/github         - GitHub PR data")
    print("  GET  /api/data/jira           - Jira ticket data")
    print("  GET  /api/data/slack          - Slack activity data")
    print("  GET  /api/data/cicd           - CI/CD pipeline data")
    print("  POST /api/analyze             - Run bottleneck analysis")
    print("  GET  /api/metrics             - Get metrics summary")
    print("  GET  /api/recommendations     - Get recommendations")
    print("  POST /api/orchestrate/trigger - Orchestration webhook")
    print("=" * 60 + "\n")
    
    app.run(host="0.0.0.0", port=port, debug=debug)
