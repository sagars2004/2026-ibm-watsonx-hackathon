from langflow.io import Output
from langflow.custom import CustomComponent
from langflow.schema import Message
import requests

class SilentBottleneckTool(CustomComponent):
    display_name = "Get Team Bottlenecks"
    description = "Fetches the latest engineering team bottleneck analysis from the local API."
    
    def build_config(self):
        return {
            "api_url": {
                "display_name": "API URL",
                "value": "http://localhost:5001/api/analyze/quick",
                "info": "Endpoint to fetch the bottleneck analysis."
            }
        }

    # Patch for Langflow 1.0+ telemetry bug
    def get_telemetry_input_values(self):
        return {}

    def get_output_logs(self):
        return {}

    def build(self, api_url: str, **kwargs) -> Message:
        try:
            # 1. Call the local Silent Bottleneck Detector API
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            
            # 2. Extract key metrics to minimize token usage
            summary = {
                "health_score": data.get("health_score"),
                "bottleneck_count": len(data.get("bottlenecks", [])),
                "bottlenecks": [
                    f"{b['title']} (Severity: {b['severity']})" 
                    for b in data.get("bottlenecks", [])
                ],
                "predictions": data.get("predictions", {}),
                "recommendations": [
                    r["title"] for r in data.get("recommendations", [])
                ]
            }
            
            # 3. Return as a Message object
            return Message(text=str(summary))
            
        except Exception as e:
            return Message(text=f"Error fetching data: {str(e)}")
