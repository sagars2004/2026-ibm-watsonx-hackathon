"""
Silent Bottleneck Detector - Cloudant Client

Handles data persistence with local JSON fallback.
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import uuid


class CloudantClient:
    """Client for IBM Cloudant with local JSON fallback."""
    
    def __init__(self):
        self.url = os.getenv("CLOUDANT_URL")
        self.api_key = os.getenv("CLOUDANT_API_KEY")
        self.db_name = os.getenv("CLOUDANT_DB_NAME", "bottleneck_detector")
        self.use_local = not (self.url and self.api_key)
        self.local_storage: Dict[str, List[Dict]] = {
            "analyses": [],
            "metrics": [],
            "recommendations": [],
        }
        
        if not self.use_local:
            self._init_cloudant()
        else:
            print("📌 Using local storage (Cloudant not configured)")
            self._load_local_storage()
    
    def _init_cloudant(self):
        """Initialize the Cloudant client."""
        try:
            from ibmcloudant.cloudant_v1 import CloudantV1
            from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
            
            authenticator = IAMAuthenticator(self.api_key)
            self.client = CloudantV1(authenticator=authenticator)
            self.client.set_service_url(self.url)
            
            try:
                self.client.put_database(db=self.db_name)
                print(f"✅ Created Cloudant database: {self.db_name}")
            except:
                print(f"✅ Connected to Cloudant database: {self.db_name}")
            
            self.use_local = False
            
        except Exception as e:
            print(f"⚠️ Could not connect to Cloudant: {e}")
            print("📌 Falling back to local storage")
            self.use_local = True
            self._load_local_storage()
    
    def _get_local_storage_path(self) -> str:
        return os.path.join(os.path.dirname(__file__), "..", "data", "local_storage.json")
    
    def _load_local_storage(self):
        path = self._get_local_storage_path()
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    self.local_storage = json.load(f)
            except:
                pass
    
    def _save_local_storage(self):
        path = self._get_local_storage_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.local_storage, f, indent=2, default=str)
    
    def store_analysis(self, analysis: Dict[str, Any]) -> str:
        doc_id = analysis.get("analysis_id", f"analysis_{uuid.uuid4().hex[:8]}")
        doc = {
            "_id": doc_id,
            "type": "analysis",
            "data": analysis,
            "created_at": datetime.now().isoformat(),
        }
        
        if self.use_local:
            self.local_storage["analyses"].append(doc)
            self._save_local_storage()
        
        return doc_id
    
    def store_recommendation(self, recommendation: Dict[str, Any]) -> str:
        doc_id = recommendation.get("id", f"rec_{uuid.uuid4().hex[:8]}")
        doc = {
            "_id": doc_id,
            "type": "recommendation",
            "data": recommendation,
            "created_at": datetime.now().isoformat(),
        }
        
        if self.use_local:
            self.local_storage["recommendations"].append(doc)
            self._save_local_storage()
        
        return doc_id
    
    def get_summary_stats(self) -> Dict[str, Any]:
        analyses = self.local_storage.get("analyses", [])
        
        if not analyses:
            return {
                "total_analyses": 0,
                "avg_health_score": 0,
                "total_bottlenecks_detected": 0,
            }
        
        health_scores = [a.get("data", {}).get("health_score", 0) for a in analyses[-10:]]
        
        return {
            "total_analyses": len(analyses),
            "avg_health_score": round(sum(health_scores) / len(health_scores), 1) if health_scores else 0,
            "total_bottlenecks_detected": sum(len(a.get("data", {}).get("bottlenecks", [])) for a in analyses),
        }


_client = None

def get_cloudant_client() -> CloudantClient:
    """Get the singleton Cloudant client instance."""
    global _client
    if _client is None:
        _client = CloudantClient()
    return _client
