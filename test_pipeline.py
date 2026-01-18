from src.graph.supervisor import build_graph
from pprint import pprint
import json

def run_test():
    print("Building Graph...")
    graph = build_graph()
    
    user_request = "Create a webhook that sends a message to Slack channel #general saying 'Hello World'"
    
    print(f"Invoking graph with request: {user_request}")
    initial_state = {"user_request": user_request, "messages": []}
    
    try:
        final_state = graph.invoke(initial_state)
        
        print("\n--- Final State Summary ---")
        if final_state.get("errors"):
            print("Errors:", final_state["errors"])
        
        if final_state.get("intent"):
            print("\n[Intent]:", final_state["intent"]["raw_intent"])
            
        if final_state.get("abstract_dag"):
            print(f"\n[Plan]: Generated {len(final_state['abstract_dag'])} abstract steps.")
            
        if final_state.get("concrete_nodes"):
            print(f"\n[Node Design]: Generated {len(final_state['concrete_nodes'])} concrete nodes.")
            for node in final_state['concrete_nodes']:
                print(f" - {node['name']} ({node['type']})")
                
        if final_state.get("n8n_json"):
            print("\n[Data Flow Output]:")
            print(json.dumps(final_state["n8n_json"], indent=2))
        
        if final_state.get("import_result"):
            print("\n[Import to n8n]:")
            import_result = final_state["import_result"]
            if import_result.get("success"):
                print(f"✓ {import_result.get('message')}")
                print(f"  Workflow ID: {import_result.get('data', {}).get('id')}")
            else:
                print(f"✗ {import_result.get('message')}")
            
    except Exception as e:
        print(f"Execution failed: {e}")

if __name__ == "__main__":
    run_test()
