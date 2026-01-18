from datetime import datetime
import json
from src.graph.state import AgentState

def compiler_agent(state: AgentState):
    """
    Assembles the final n8n JSON workflow.
    This is a deterministic node, not using an LLM.
    """
    n8n_partial = state.get("n8n_json") # From Data Flow agent
    intent = state.get("intent")
    
    if not n8n_partial:
        return {"errors": ["No partial workflow found for compilation"]}
        
    nodes = n8n_partial.get("nodes", [])
    connections = n8n_partial.get("connections", {})
    
    # Basic envelope
    final_workflow = {
        "name": f"Auto-Generated: {intent.get('raw_intent', 'Workflow')[:50]}",
        "nodes": nodes,
        "connections": connections,
        "pinData": {},
        "settings": {
            "executionOrder": "v1"
        },
        "versionId": "auto-generated-version", # specific to n8n import
        "meta": {
            "templateCredsSetupCompleted": True,
            "instanceId": "local-agent"
        }
    }
    
    return {
        "n8n_json": final_workflow,
        "next_step": "validator",
        "errors": []
    }
