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
        
        # Simple Cache for Demo Performance
        self._cache = None
        self._last_analysis_time = 0
        
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
        
        # ⚡️ Check Cache (60s)
        import time
        now = time.time()
        if self._cache and (now - self._last_analysis_time < 60):
            print(f"⚡️ [WatsonxClient] Serving cached analysis ({int(now - self._last_analysis_time)}s old)")
            return self._cache

        result = None
        if self.use_mock:
            result = self._mock_analysis(data)
        else:
            result = self._real_analysis(data)
            
        # Store Cache
        self._cache = result
        self._last_analysis_time = now
        return result
    
    def _real_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform real analysis using watsonx.ai."""
        try:
            from ibm_watsonx_ai.foundation_models import ModelInference
            
            model = ModelInference(
                model_id="ibm/granite-4-h-small",
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
                    "temperature": 0.1, # Deterministic behavior
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

Identify the top 5 bottlenecks.
Format as JSON with a 'bottlenecks' array. Each item must have: type, severity (high/medium/low), title, description, recommendation, metric_value.
Output raw JSON only. Do not use Markdown code blocks."""
    
    def _parse_ai_response(self, response: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse the AI response and apply deterministic scoring."""
        try:
            import re
            # Strip markdown code blocks if present
            clean_response = response.replace("```json", "").replace("```", "").strip()
            
            json_match = re.search(r'\{[\s\S]*\}', clean_response)
            if json_match:
                result = json.loads(json_match.group())
                bottlenecks = result.get("bottlenecks", [])
                
                # Apply deterministic scoring logic
                return self._calculate_metrics(bottlenecks, data)
        except Exception as e:
            print(f"Error parsing AI response: {e}")
        return self._mock_analysis(data)
    
    def _calculate_metrics(self, bottlenecks: List[Dict[str, Any]], data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply deterministic scoring and predictions to bottlenecks."""
        
        # Calculate health score
        # For Demo Drama: Make Blockers the dominant factor
        penalty = 0
        for b in bottlenecks:
            title = b.get("title", "").lower()
            b_type = b.get("type", "").lower()
            
            if b_type == "blocked_work" or "blocked" in title:
                # Linear penalty: 2.5 points per blocked ticket
                try:
                    val = str(b.get("metric_value", "0")).replace("%", "").replace("h", "")
                    count = float(val) if val.replace(".", "").isdigit() else 0
                    if count == 0: count = data.get("jira", {}).get("summary", {}).get("blocked_count", 0)
                except:
                    count = data.get("jira", {}).get("summary", {}).get("blocked_count", 0)
                
                b["type"] = "blocked_work" # Standardize
                b["metric_value"] = str(int(count))
                penalty += count * 2.5
            else:
                penalty += 5
                
        health_score = int(max(30, min(100, 100 - penalty)))
        
        # Trends
        if health_score < 60: trend_change = -5
        elif health_score > 85: trend_change = 5
        else: trend_change = 0

        # Predictions
        jira = data.get("jira", {})
        velocity = jira.get("summary", {}).get("velocity", 20)
        total_points = jira.get("summary", {}).get("total_tickets", 50) * 3
        
        efficiency_factor = health_score / 100.0
        projected_velocity = velocity * efficiency_factor
        
        remaining_points = max(0, total_points - velocity)
        if projected_velocity > 0:
            days = int((remaining_points / projected_velocity) * 14)
        else:
            days = 999
            
        risk = "low"
        if days > 30: risk = "high"
        elif days > 14: risk = "medium"

        return {
            "analysis_id": f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "health_score": health_score,
            "health_status": "healthy" if health_score >= 50 else ("warning" if health_score >= 40 else "critical"),
            "bottlenecks": sorted(bottlenecks, key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x.get("severity"), 3)),
            "trends": { "health_score_change": trend_change },
            "predictions": {
                "projected_velocity": round(projected_velocity, 1),
                "original_velocity": velocity,
                "days_to_completion": days,
                "risk_level": risk,
                "forecast": f"Projected to finish in {days} days ({'On Track' if risk == 'low' else 'Delay Risk'})"
            },
            "summary": f"Detected {len(bottlenecks)} bottlenecks. Health score: {health_score}/100.",
        }

    def _mock_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock analysis results with Specific Narratives for Demo."""
        bottlenecks = []
        
        # 1. PR Bottleneck: Emma Wilson is overloaded
        bottlenecks.append({
            "type": "single_point_of_failure",
            "severity": "high",
            "title": "Review Bottleneck: Emma Wilson",
            "description": "Emma Wilson is reviewing 68% of all PRs. This is a critical velocity risk.",
            "impact": "Team merges are blocked when Emma is unavailable.",
            "recommendation": "Distribute review load to Alex and Sarah immediately.",
            "icon": "🚨",
            "metric_value": "68%",
            "metric_label": "review share",
        })
        
        # 2. Deployment Delay
        bottlenecks.append({
            "type": "hidden_delay",
            "severity": "medium",
            "title": "Stagnant Deploys",
            "description": "Features sit in 'Approved' state for avg 14 hours before merge.",
            "impact": "Slow feedback loop from QA.",
            "recommendation": "Enable auto-merge for approved low-risk PRs.",
            "icon": "⏰",
            "metric_value": "14h",
            "metric_label": "avg merge delay",
        })
        
        # 3. Flaky Tests
        bottlenecks.append({
            "type": "flaky_process",
            "severity": "high",
            "title": "Flaky CI: E2E Payments",
            "description": "'e2e-payment-tests' stage failed 12 times today (35% rate).",
            "impact": "Developers are re-running builds constantly.",
            "recommendation": "Quarantine 'TestPaymentFlow.spec.js' and fix race condition.",
            "icon": "🔄",
            "metric_value": "35%",
            "metric_label": "failure rate",
        })
        
        # 4. Knowledge Silo
        bottlenecks.append({
            "type": "knowledge_silo",
            "severity": "medium",
            "title": "Risk: Auth Service",
            "description": "Alex Rivera is the only contributor to 'auth-service' in 6 months.",
            "impact": "Bus factor of 1 on critical security component.",
            "recommendation": "Schedule Deep Dive session with Alex for the team.",
            "icon": "🔐",
            "metric_value": "1",
            "metric_label": "contributor",
        })

        # 5. Meeting Overload
        bottlenecks.append({
            "type": "meeting_overload",
            "severity": "low",
            "title": "Meeting Heavy: David Kim",
            "description": "David Kim spent 24 hours in meetings this week (60% load).",
            "impact": "Zero coding time availble for Tech Lead.",
            "recommendation": "Decline non-critical syncs.",
            "icon": "💬",
            "metric_value": "60%",
            "metric_label": "meeting load",
        })
        
        # Dynamic Scoring for Demo (Responsive to Actions)
        # Base: 58 (Warning)
        # If blockers cleared -> +27 points -> 85 (Healthy)
        jira_summary = data.get("jira", {}).get("summary", {})
        blocked = jira_summary.get("blocked_count", 0)
        
        health_score = 58
        trend_change = -12
        
        if blocked == 0:
            health_score = 85 # Healthy!
            trend_change = 27
            bottlenecks = [b for b in bottlenecks if b["type"] != "blocked_work"] # Remove blocker card
            
        elif blocked < 5:
            health_score = 72
            trend_change = 14
        
        # Predictions
        projected_velocity = 14.5
        velocity = 20
        days_to_complete = 42
        risk_level = "high"

        return {
            "analysis_id": f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "health_score": health_score,
            "health_status": "warning",
            "bottlenecks": sorted(bottlenecks, key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x["severity"], 3)),
            "trends": {
                "health_score_change": trend_change,
                "new_bottlenecks": 2,
                "resolved_bottlenecks": 0,
            },
            "predictions": {
                "projected_velocity": projected_velocity,
                "original_velocity": velocity,
                "days_to_completion": days_to_complete,
                "risk_level": risk_level,
                "forecast": f"Projected to finish in {days_to_complete} days (Delay Risk)"
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
