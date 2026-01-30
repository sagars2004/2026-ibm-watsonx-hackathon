"""
Silent Bottleneck Detector - Cloudant Client

Handles data persistence for historical analysis tracking.
Supports both real Cloudant and local mock storage.
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import uuid


class CloudantClient:
    """
    Client for IBM Cloudant database operations.
    Falls back to local JSON storage if Cloudant is not configured.
    """
    
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
            
            # Ensure database exists
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
        """Get path for local storage file."""
        return os.path.join(os.path.dirname(__file__), "..", "data", "local_storage.json")
    
    def _load_local_storage(self):
        """Load local storage from file if it exists."""
        path = self._get_local_storage_path()
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    self.local_storage = json.load(f)
            except:
                pass
    
    def _save_local_storage(self):
        """Save local storage to file."""
        path = self._get_local_storage_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.local_storage, f, indent=2, default=str)
    
    def store_analysis(self, analysis: Dict[str, Any]) -> str:
        """
        Store an analysis result.
        
        Args:
            analysis: The analysis data to store
            
        Returns:
            The ID of the stored document
        """
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
        else:
            try:
                self.client.post_document(db=self.db_name, document=doc)
            except Exception as e:
                print(f"⚠️ Failed to store analysis: {e}")
                self.local_storage["analyses"].append(doc)
        
        return doc_id
    
    def get_analysis(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific analysis by ID."""
        if self.use_local:
            for doc in self.local_storage["analyses"]:
                if doc.get("_id") == analysis_id:
                    return doc.get("data")
            return None
        else:
            try:
                doc = self.client.get_document(db=self.db_name, doc_id=analysis_id).get_result()
                return doc.get("data")
            except:
                return None
    
    def get_historical_analyses(self, days: int = 30, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve historical analyses for trend tracking.
        
        Args:
            days: Number of days to look back
            limit: Maximum number of analyses to return
            
        Returns:
            List of analysis documents
        """
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        
        if self.use_local:
            analyses = [
                doc.get("data") for doc in self.local_storage["analyses"]
                if doc.get("created_at", "") >= cutoff
            ]
            return sorted(analyses, key=lambda x: x.get("timestamp", ""), reverse=True)[:limit]
        else:
            try:
                # Use Cloudant query
                selector = {
                    "type": "analysis",
                    "created_at": {"$gte": cutoff}
                }
                result = self.client.post_find(
                    db=self.db_name,
                    selector=selector,
                    limit=limit,
                    sort=[{"created_at": "desc"}]
                ).get_result()
                return [doc.get("data") for doc in result.get("docs", [])]
            except Exception as e:
                print(f"⚠️ Failed to get historical analyses: {e}")
                return []
    
    def store_metrics(self, metrics: Dict[str, Any]) -> str:
        """Store metrics snapshot."""
        doc_id = f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        doc = {
            "_id": doc_id,
            "type": "metrics",
            "data": metrics,
            "created_at": datetime.now().isoformat(),
        }
        
        if self.use_local:
            self.local_storage["metrics"].append(doc)
            self._save_local_storage()
        else:
            try:
                self.client.post_document(db=self.db_name, document=doc)
            except Exception as e:
                print(f"⚠️ Failed to store metrics: {e}")
                self.local_storage["metrics"].append(doc)
        
        return doc_id
    
    def get_metrics_history(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get metrics history for trend charts."""
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        
        if self.use_local:
            metrics = [
                doc.get("data") for doc in self.local_storage["metrics"]
                if doc.get("created_at", "") >= cutoff
            ]
            return sorted(metrics, key=lambda x: x.get("timestamp", ""))
        else:
            try:
                selector = {
                    "type": "metrics",
                    "created_at": {"$gte": cutoff}
                }
                result = self.client.post_find(
                    db=self.db_name,
                    selector=selector,
                    sort=[{"created_at": "asc"}]
                ).get_result()
                return [doc.get("data") for doc in result.get("docs", [])]
            except:
                return []
    
    def store_recommendation(self, recommendation: Dict[str, Any]) -> str:
        """Store a recommendation with its status."""
        doc_id = recommendation.get("id", f"rec_{uuid.uuid4().hex[:8]}")
        doc = {
            "_id": doc_id,
            "type": "recommendation",
            "data": recommendation,
            "created_at": datetime.now().isoformat(),
        }
        
        if self.use_local:
            # Update if exists, otherwise append
            existing = next((i for i, d in enumerate(self.local_storage["recommendations"]) 
                           if d.get("_id") == doc_id), None)
            if existing is not None:
                self.local_storage["recommendations"][existing] = doc
            else:
                self.local_storage["recommendations"].append(doc)
            self._save_local_storage()
        else:
            try:
                self.client.post_document(db=self.db_name, document=doc)
            except:
                try:
                    self.client.put_document(db=self.db_name, doc_id=doc_id, document=doc)
                except Exception as e:
                    print(f"⚠️ Failed to store recommendation: {e}")
        
        return doc_id
    
    def get_pending_recommendations(self) -> List[Dict[str, Any]]:
        """Get all pending recommendations."""
        if self.use_local:
            return [
                doc.get("data") for doc in self.local_storage["recommendations"]
                if doc.get("data", {}).get("status") == "pending"
            ]
        else:
            try:
                selector = {
                    "type": "recommendation",
                    "data.status": "pending"
                }
                result = self.client.post_find(
                    db=self.db_name,
                    selector=selector
                ).get_result()
                return [doc.get("data") for doc in result.get("docs", [])]
            except:
                return []
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics for the dashboard."""
        analyses = self.get_historical_analyses(days=30, limit=100)
        
        if not analyses:
            return {
                "total_analyses": 0,
                "avg_health_score": 0,
                "total_bottlenecks_detected": 0,
                "most_common_bottleneck": None,
            }
        
        # Calculate stats
        health_scores = [a.get("health_score", 0) for a in analyses]
        all_bottlenecks = []
        for a in analyses:
            all_bottlenecks.extend([b.get("type") for b in a.get("bottlenecks", [])])
        
        # Find most common bottleneck type
        bottleneck_counts = {}
        for b in all_bottlenecks:
            bottleneck_counts[b] = bottleneck_counts.get(b, 0) + 1
        most_common = max(bottleneck_counts.items(), key=lambda x: x[1])[0] if bottleneck_counts else None
        
        return {
            "total_analyses": len(analyses),
            "avg_health_score": round(sum(health_scores) / len(health_scores), 1),
            "total_bottlenecks_detected": len(all_bottlenecks),
            "most_common_bottleneck": most_common,
            "health_trend": health_scores[:7] if len(health_scores) >= 7 else health_scores,
        }


# Singleton instance
_client = None

def get_cloudant_client() -> CloudantClient:
    """Get the singleton Cloudant client instance."""
    global _client
    if _client is None:
        _client = CloudantClient()
    return _client
