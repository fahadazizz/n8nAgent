#!/usr/bin/env python3
"""Direct test of n8n API integration."""

from src.utils.n8n_api import N8nAPI
import json

# Sample workflow JSON
sample_workflow = {
    "name": "Test Webhook to Slack",
    "nodes": [
        {
            "id": "webhook-1",
            "name": "Webhook",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 1.0,
            "position": [250, 300],
            "parameters": {
                "httpMethod": "POST",
                "path": "test-webhook"
            },
            "credentials": {}
        },
        {
            "id": "slack-1",
            "name": "Slack",
            "type": "n8n-nodes-base.slack",
            "typeVersion": 1.0,
            "position": [450, 300],
            "parameters": {
                "resource": "message",
                "operation": "post",
                "channel": "#general",
                "text": "Test message from automated workflow"
            },
            "credentials": {}
        }
    ],
    "connections": {
        "Webhook": {
            "main": [[{"node": "Slack", "type": "main", "index": 0}]]
        }
    },
    "pinData": {},
    "settings": {"executionOrder": "v1"},
    "active": False
}

def main():
    print("Testing n8n API Integration...")
    print(f"Workflow: {sample_workflow['name']}")
    
    # Initialize API client
    n8n = N8nAPI()
    
    # Test: Import workflow
    print("\n1. Importing workflow...")
    result = n8n.import_workflow(sample_workflow)
    
    if result.get("success"):
        print(f"✓ Success: {result.get('message')}")
        workflow_id = result.get('data', {}).get('id')
        print(f"  Workflow ID: {workflow_id}")
        print(f"  Access at: http://localhost:5678/workflow/{workflow_id}")
        
        # Test: List workflows
        print("\n2. Listing workflows...")
        list_result = n8n.list_workflows()
        if list_result.get("success"):
            workflows = list_result.get('data', {}).get('data', [])
            print(f"✓ Found {len(workflows)} workflow(s)")
            for wf in workflows[:3]:  # Show first 3
                print(f"  - {wf.get('name')} (ID: {wf.get('id')})")
        else:
            print(f"✗ Failed: {list_result.get('error')}")
    else:
        print(f"✗ Failed: {result.get('message')}")
        print(f"  Error details: {result.get('error')}")

if __name__ == "__main__":
    main()
