import requests
import json
import os
from typing import Dict, Any

class N8nAPI:
    """Client for n8n REST API."""
    
    def __init__(self, base_url: str = "http://localhost:5678", api_key: str = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key or os.getenv('N8N_API_KEY', '')
        self.headers = {
            'Content-Type': 'application/json'
        }
        if self.api_key:
            self.headers['X-N8N-API-KEY'] = self.api_key
    
    def import_workflow(self, workflow_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Import a workflow into n8n.
        
        Args:
            workflow_json: The complete workflow JSON
            
        Returns:
            Response from n8n API
        """
        # Prepare the payload - n8n API requires specific fields
        payload = {
            "name": workflow_json.get("name", "Imported Workflow"),
            "nodes": workflow_json.get("nodes", []),
            "connections": workflow_json.get("connections", {}),
            "settings": workflow_json.get("settings", {}),
        }
        
        # Add optional fields if present
        if "staticData" in workflow_json:
            payload["staticData"] = workflow_json["staticData"]
        if "tags" in workflow_json:
            payload["tags"] = workflow_json["tags"]
        
        endpoint = f"{self.base_url}/api/v1/workflows"
        
        try:
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            return {
                "success": True,
                "data": response.json(),
                "message": f"Workflow imported successfully. ID: {response.json().get('id')}"
            }
        except requests.exceptions.HTTPError as e:
            # Try to get error details from response
            error_detail = ""
            try:
                error_detail = e.response.json().get("message", str(e))
            except:
                error_detail = str(e)
            return {
                "success": False,
                "error": error_detail,
                "message": f"Failed to import workflow: {error_detail}"
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to import workflow: {str(e)}"
            }
    
    def list_workflows(self) -> Dict[str, Any]:
        """List all workflows in n8n."""
        endpoint = f"{self.base_url}/api/v1/workflows"
        
        try:
            response = requests.get(endpoint, headers=self.headers, timeout=10)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Get a specific workflow by ID."""
        endpoint = f"{self.base_url}/api/v1/workflows/{workflow_id}"
        
        try:
            response = requests.get(endpoint, headers=self.headers, timeout=10)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
