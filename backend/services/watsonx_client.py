"""
Silent Bottleneck Detector - watsonx.ai Client

Integrates with IBM watsonx.ai for intelligent pattern analysis.
"""

import os
import json
from typing import Dict, List, Any
from datetime import datetime


class WatsonxClient:
    """Client for watsonx.ai integration."""
    
    def __init__(self):
        self.api_key = os.getenv("WATSONX_API_KEY")
        self.project_id = os.getenv("WATSONX_PROJECT_ID")
        self.url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        self.use_mock = os.getenv("USE_MOCK_AI", "true").lower() == "true"
        
        if not self.use_mock and self.api_key and self.project_id:
            self._init_real_client()
    
    def _init_real_client(self):
        """Initialize the real watsonx.ai client."""
        try:
            from ibm_watsonx_ai import APIClient
            from ibm_watsonx_ai import Credentials
            
            credentials = Credentials(
                url=self.url,
                api_key=self.api_key,
            )
            self.client = APIClient(credentials)
            self.use_mock = False
            print("✅ Connected to watsonx.ai")
        except Exception as e:
            print(f"⚠️ Could not connect to watsonx.ai: {e}")
            print("📌 Falling back to mock mode")
            self.use_mock = True
    
    def analyze_bottlenecks(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze workflow data to detect bottlenecks."""
        if self.use_mock:
            return self._mock_analysis(data)
        else:
            return self._real_analysis(data)
    
    def _real_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform real analysis using watsonx.ai."""
        try:
            from ibm_watsonx_ai.foundation_models import Model
            
            model = Model(
                model_id="ibm/granite-13b-instruct-v2",
                credentials={
                    "url": self.url,
                    "apikey": self.api_key,
                },
                project_id=self.project_id,
            )
            
            prompt = self._create_analysis_prompt(data)
            
            response = model.generate_text(
                prompt=prompt,
                params={
                    "max_new_tokens": 2000,
                    "temperature": 0.3,
                    "top_p": 0.9,
                }
            )
            
            return self._parse_ai_response(response, data)
            
        except Exception as e:
            print(f"⚠️ watsonx.ai analysis failed: {e}")
            return self._mock_analysis(data)
    
    def _create_analysis_prompt(self, data: Dict[str, Any]) -> str:
        """Create a prompt for watsonx.ai analysis."""
        github_summary = data.get("github", {}).get("summary", {})
        jira_summary = data.get("jira", {}).get("summary", {})
        slack_summary = data.get("slack", {}).get("summary", {})
        cicd_summary = data.get("cicd", {}).get("summary", {})
        
        return f"""Analyze the following team workflow data and identify bottlenecks:

## GitHub Data
- Total PRs: {github_summary.get('total_prs', 'N/A')}
- Average review time: {github_summary.get('avg_review_time_hours', 'N/A')} hours
- Pending reviews: {github_summary.get('pending_reviews', 'N/A')}

## Jira Data
- Total tickets: {jira_summary.get('total_tickets', 'N/A')}
- Blocked tickets: {jira_summary.get('blocked_count', 'N/A')}

## Slack Data
- Meeting time: {slack_summary.get('meeting_percentage', 'N/A')}% of work hours

## CI/CD Data
- Success rate: {cicd_summary.get('success_rate', 'N/A')}%
- Most failing stage: {cicd_summary.get('flaky_stage', 'N/A')}

Identify the top 5 bottlenecks and provide actionable recommendations.
Format as JSON with bottlenecks array, health_score (0-100), and summary."""
    
    def _parse_ai_response(self, response: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse the AI response into structured format."""
        try:
            import re
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                result = json.loads(json_match.group())
                result["analysis_id"] = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                result["timestamp"] = datetime.now().isoformat()
                return result
        except:
            pass
        return self._mock_analysis(data)
    
    def _mock_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock analysis results based on the data patterns."""
        bottlenecks = []
        
        # Analyze GitHub data for PR review bottleneck
        github = data.get("github", {})
        reviewer_stats = github.get("reviewer_stats", {})
        if reviewer_stats:
            top_reviewer = max(reviewer_stats.items(), key=lambda x: x[1].get("percentage", 0))
            reviewer_id, stats = top_reviewer
            if stats.get("percentage", 0) > 50:
                bottlenecks.append({
                    "type": "single_point_of_failure",
                    "severity": "high",
                    "title": "PR Review Concentration",
                    "description": f"{stats['member']['name']} approved {stats['percentage']}% of all PRs last month",
                    "impact": "Team velocity is at risk if this person is unavailable.",
                    "recommendation": "Train 2 more developers on code review best practices",
                    "icon": "🚨",
                    "metric_value": f"{stats['percentage']}%",
                    "metric_label": "PRs reviewed by one person",
                })
        
        # Analyze deploy delays
        github_summary = github.get("summary", {})
        avg_merge_delay = github_summary.get("avg_merge_delay_hours", 0)
        if avg_merge_delay > 8:
            bottlenecks.append({
                "type": "hidden_delay",
                "severity": "medium",
                "title": "Deploy Queue Bottleneck",
                "description": f"Average time from PR-approved to deployed: {avg_merge_delay} hours",
                "impact": "Features sit idle waiting for deployment",
                "recommendation": "Automate deploy pipeline to run immediately after approval",
                "icon": "⏰",
                "metric_value": f"{avg_merge_delay}h",
                "metric_label": "avg deploy delay",
            })
        
        # Analyze CI/CD flakiness
        cicd = data.get("cicd", {})
        cicd_summary = cicd.get("summary", {})
        failure_rate = cicd_summary.get("failure_rate", 0)
        flaky_stage = cicd_summary.get("flaky_stage")
        if failure_rate > 25 and flaky_stage:
            bottlenecks.append({
                "type": "flaky_process",
                "severity": "high",
                "title": "Flaky CI/CD Pipeline",
                "description": f"'{flaky_stage}' stage fails {failure_rate}% of the time",
                "impact": "Developers waste time re-running builds",
                "recommendation": f"Investigate and fix flaky tests in {flaky_stage}",
                "icon": "🔄",
                "metric_value": f"{failure_rate}%",
                "metric_label": "pipeline failure rate",
            })
        
        # Analyze knowledge silos
        knowledge_silos = github.get("knowledge_silos", [])
        critical_silos = [s for s in knowledge_silos if s.get("is_silo") and s.get("area") in ["auth", "payments", "database"]]
        if critical_silos:
            silo = critical_silos[0]
            bottlenecks.append({
                "type": "knowledge_silo",
                "severity": "medium",
                "title": f"Knowledge Silo: {silo['area'].title()}",
                "description": f"Only {silo['contributor_count']} people have touched {silo['area']} code",
                "impact": f"Critical system at risk if these people leave",
                "recommendation": f"Schedule knowledge-sharing sessions for {silo['area']}",
                "icon": "🔐",
                "metric_value": str(silo['contributor_count']),
                "metric_label": "contributors (bus factor)",
            })
        
        # Analyze meeting overload
        slack = data.get("slack", {})
        slack_summary = slack.get("summary", {})
        meeting_pct = slack_summary.get("meeting_percentage", 0)
        if meeting_pct > 25:
            bottlenecks.append({
                "type": "meeting_overload",
                "severity": "medium" if meeting_pct < 35 else "high",
                "title": "Excessive Meeting Time",
                "description": f"Team spent {meeting_pct}% of time in meetings (healthy target: <20%)",
                "impact": "Reduced focus time for deep work",
                "recommendation": "Audit recurring meetings, implement 'No Meeting Wednesdays'",
                "icon": "💬",
                "metric_value": f"{meeting_pct}%",
                "metric_label": "time in meetings",
            })
        
        # Analyze blocked tickets
        jira = data.get("jira", {})
        jira_summary = jira.get("summary", {})
        blocked_count = jira_summary.get("blocked_count", 0)
        if blocked_count > 5:
            bottlenecks.append({
                "type": "blocked_work",
                "severity": "medium",
                "title": "Stalled Tickets in Review",
                "description": f"{blocked_count} tickets blocked waiting for review",
                "impact": "Sprint velocity impacted",
                "recommendation": "Set up daily review rotation and max 24-hour review SLA",
                "icon": "🚫",
                "metric_value": str(blocked_count),
                "metric_label": "blocked tickets",
            })
        
        # Calculate health score
        severity_weights = {"high": 15, "medium": 8, "low": 3}
        penalty = sum(severity_weights.get(b["severity"], 5) for b in bottlenecks)
        health_score = max(0, min(100, 100 - penalty))
        
        import random
        trend_change = random.choice([-8, -5, -3, 2, 5])
        
        return {
            "analysis_id": f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "health_score": health_score,
            "health_status": "healthy" if health_score >= 80 else ("warning" if health_score >= 60 else "critical"),
            "bottlenecks": sorted(bottlenecks, key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x["severity"], 3)),
            "trends": {
                "health_score_change": trend_change,
                "new_bottlenecks": len([b for b in bottlenecks if b["severity"] == "high"]),
                "resolved_bottlenecks": random.randint(0, 2),
            },
            "summary": f"Detected {len(bottlenecks)} bottlenecks. Health score: {health_score}/100.",
        }
    
    def generate_recommendations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actionable recommendations based on the analysis."""
        recommendations = []
        
        for bottleneck in analysis.get("bottlenecks", []):
            action = {
                "id": f"rec_{len(recommendations) + 1}",
                "title": bottleneck.get("recommendation", "Take action"),
                "related_bottleneck": bottleneck.get("title"),
                "priority": bottleneck.get("severity"),
                "status": "pending",
                "actions": [],
            }
            
            btype = bottleneck.get("type")
            
            if btype == "single_point_of_failure":
                action["actions"] = [
                    {"type": "create_jira_ticket", "description": "Create training ticket for code review best practices"},
                    {"type": "slack_message", "description": "Notify team about review load distribution"},
                ]
            elif btype == "hidden_delay":
                action["actions"] = [
                    {"type": "create_jira_ticket", "description": "Automate deployment pipeline"},
                ]
            elif btype == "flaky_process":
                action["actions"] = [
                    {"type": "create_jira_ticket", "description": "Investigate and fix flaky tests"},
                    {"type": "slack_message", "description": "Alert team about pipeline reliability issues"},
                ]
            elif btype == "knowledge_silo":
                action["actions"] = [
                    {"type": "schedule_meeting", "description": "Schedule knowledge-sharing session"},
                ]
            elif btype == "meeting_overload":
                action["actions"] = [
                    {"type": "slack_message", "description": "Propose 'No Meeting Wednesday' policy"},
                ]
            elif btype == "blocked_work":
                action["actions"] = [
                    {"type": "create_jira_ticket", "description": "Define review SLA policy"},
                ]
            
            recommendations.append(action)
        
        return recommendations


_client = None

def get_watsonx_client() -> WatsonxClient:
    """Get the singleton watsonx client instance."""
    global _client
    if _client is None:
        _client = WatsonxClient()
    return _client
