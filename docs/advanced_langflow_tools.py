import requests
from langflow.custom import CustomComponent
from langflow.field_typing import Tool
from langchain.tools import StructuredTool

# ==========================================
# TOOL 1: Bottleneck Analyzer
# ==========================================
class BottleneckAnalyzer(CustomComponent):
    display_name = "Tool: Analyze Bottlenecks"
    description = "Returns a Tool object for analyzing team stats."

    def build_config(self):
        return {
            "api_url": {"display_name": "API URL", "value": "http://host.docker.internal:5001/api/analyze/quick"},
        }
    
    # Patch for telemetry
    def get_telemetry_input_values(self, **kwargs):
        return kwargs

    def get_output_logs(self):
        return {}

    # Patch: accept **kwargs to handle unexpected 'code' arg
    def build(self, api_url: str, **kwargs) -> Tool:
        
        def analyze_logic() -> str:
            try:
                url = api_url.replace("localhost", "host.docker.internal") if "localhost" in api_url else api_url
                res = requests.get(url, timeout=5)
                if res.status_code == 200:
                    d = res.json()
                    summary = f"Health: {d.get('health_score')}, "
                    summary += f"Blocked: {d.get('jira',{}).get('summary',{}).get('blocked_count',0)}\n"
                    if d.get('bottlenecks'):
                        summary += "Top Issue: " + d['bottlenecks'][0]['title']
                    return summary
                return "Error fetching stats."
            except Exception as e:
                return f"Error: {e}"

        return StructuredTool.from_function(
            func=analyze_logic,
            name="analyze_bottlenecks",
            description="Check current team health and blocked tickets."
        )

# ==========================================
# TOOL 2: Blocker Resolver
# ==========================================
class BlockerResolver(CustomComponent):
    display_name = "Tool: Resolve Blockers"
    description = "Returns a Tool object for resolving Jira tickets."

    def build_config(self):
        return {
            "api_url": {"display_name": "API URL", "value": "http://host.docker.internal:5001/api/actions"},
        }

    def get_telemetry_input_values(self, **kwargs):
        return kwargs
    
    def get_output_logs(self):
        return {}

    def build(self, api_url: str, **kwargs) -> Tool:
        
        def resolve_logic(count: int = 5) -> str:
            try:
                url = api_url.replace("localhost", "host.docker.internal") if "localhost" in api_url else api_url
                res = requests.post(url, json={"type": "resolve_blockers", "count": count}, timeout=5)
                return res.json().get("message", "Action failed") if res.status_code == 200 else "Failed"
            except Exception as e:
                return f"Error: {e}"

        return StructuredTool.from_function(
            func=resolve_logic,
            name="resolve_blockers",
            description="Unblock Jira tickets. Input 'count' (int) optional."
        )

# ==========================================
# TOOL 3: Meeting Optimizer
# ==========================================
class MeetingOptimizer(CustomComponent):
    display_name = "Tool: Optimize Meetings"
    description = "Returns a Tool object for optimizing calendar."

    def build_config(self):
        return {
            "api_url": {"display_name": "API URL", "value": "http://host.docker.internal:5001/api/actions"},
        }

    def get_telemetry_input_values(self, **kwargs):
        return kwargs

    def get_output_logs(self):
        return {}

    def build(self, api_url: str, **kwargs) -> Tool:
        
        def meeting_logic() -> str:
            try:
                url = api_url.replace("localhost", "host.docker.internal") if "localhost" in api_url else api_url
                res = requests.post(url, json={"type": "optimize_meetings"}, timeout=5)
                return res.json().get("message", "Action failed") if res.status_code == 200 else "Failed"
            except Exception as e:
                return f"Error: {e}"

        return StructuredTool.from_function(
            func=meeting_logic,
            name="optimize_meetings",
            description="Decline non-critical meetings."
        )
