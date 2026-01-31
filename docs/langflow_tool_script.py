from langflow.io import Output
from langflow.custom import CustomComponent
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

    def build(self, api_url: str) -> Output:
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
            
            # 3. Return as a clean string for the LLM
            return Output(value=str(summary))
            
        except Exception as e:
            return Output(value=f"Error fetching data: {str(e)}")
