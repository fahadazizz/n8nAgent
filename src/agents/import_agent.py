from src.graph.state import AgentState
from src.utils.n8n_api import N8nAPI

def import_agent(state: AgentState):
    """
    Imports the final workflow into n8n.
    """
    workflow = state.get("n8n_json")
    validation_status = state.get("validation_status")
    
    if not workflow:
        return {"errors": ["No workflow to import"]}
    
    if validation_status != "verified" and validation_status != "valid":
        return {"errors": ["Cannot import unverified workflow"]}
    
    # Initialize n8n API client
    n8n = N8nAPI()
    
    # Import the workflow
    result = n8n.import_workflow(workflow)
    
    if result.get("success"):
        return {
            "import_result": result,
            "next_step": "end",
            "errors": []
        }
    else:
        return {
            "errors": [f"Import failed: {result.get('message')}"],
            "next_step": "end"
        }
