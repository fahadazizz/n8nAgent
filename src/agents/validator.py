from src.graph.state import AgentState

def validator_agent(state: AgentState):
    """
    Performs static checks on the generated JSON.
    """
    workflow = state.get("n8n_json")
    if not workflow:
        return {"errors": ["No workflow to validate"]}
        
    errors = []
    nodes = workflow.get("nodes", [])
    connections = workflow.get("connections", {})
    
    # 1. Check for circular dependencies (Basic check)
    # 2. Check for disconnected nodes (except Trigger)
    
    node_names = {n["name"] for n in nodes}
    
    # Check if all connections point to existing nodes
    for source_node, outputs in connections.items():
        if source_node not in node_names:
            errors.append(f"Connection source '{source_node}' does not exist.")
        
        for output_name, routes in outputs.items():
            for route in routes:
                for item in route:
                    target = item.get("node")
                    if target and target not in node_names:
                        errors.append(f"Connection target '{target}' does not exist (from {source_node}).")
                        
    # Check if at least one Trigger exists
    has_trigger = any("trigger" in n.get("type", "").lower() or "webhook" in n.get("type", "").lower() for n in nodes)
    if not has_trigger:
        errors.append("Workflow has no obvious Trigger node (Webhook/Schedule/etc).")
        
    if errors:
        return {"errors": errors, "validation_status": "invalid", "next_step": "end"}
        
    return {"validation_status": "valid", "next_step": "end"}
