#!/usr/bin/env python3
"""
n8n Autonomous Agent - Main Entry Point

Usage:
    python main.py "Create a webhook that sends email notifications"
    python main.py --interactive
"""

import sys
import json
from src.graph.supervisor import build_graph

def run_agent(user_request: str, skip_simulation: bool = False):
    """
    Run the autonomous agent with a user request.
    
    Args:
        user_request: Natural language description of the workflow
        skip_simulation: Skip simulation step for faster execution
    """
    print(f"\n{'='*60}")
    print(f"n8n Autonomous Agent")
    print(f"{'='*60}")
    print(f"\nRequest: {user_request}\n")
    
    # Build the graph
    graph = build_graph()
    
    # Prepare initial state
    initial_state = {
        "user_request": user_request,
        "messages": []
    }
    
    # Skip simulation if requested (for speed)
    if skip_simulation:
        initial_state["validation_status"] = "verified"
    
    try:
        print("Processing...\n")
        final_state = graph.invoke(initial_state)
        
        # Display results
        print(f"{'='*60}")
        print("RESULTS")
        print(f"{'='*60}\n")
        
        # Check for errors
        if final_state.get("errors"):
            print("❌ Errors occurred:")
            for error in final_state["errors"]:
                print(f"  - {error}")
            return False
        
        # Show intent
        if final_state.get("intent"):
            print(f"✓ Understood Intent: {final_state['intent'].get('raw_intent')}")
        
        # Show plan
        if final_state.get("abstract_dag"):
            print(f"✓ Generated Plan: {len(final_state['abstract_dag'])} steps")
        
        # Show nodes
        if final_state.get("concrete_nodes"):
            print(f"✓ Created Nodes: {len(final_state['concrete_nodes'])} node(s)")
            for node in final_state['concrete_nodes']:
                print(f"    - {node['name']} ({node['type']})")
        
        # Show import result
        if final_state.get("import_result"):
            import_result = final_state["import_result"]
            if import_result.get("success"):
                workflow_id = import_result.get('data', {}).get('id')
                print(f"\n{'='*60}")
                print("✅ SUCCESS - Workflow Imported to n8n!")
                print(f"{'='*60}")
                print(f"\nWorkflow ID: {workflow_id}")
                print(f"Access URL: http://localhost:5678/workflow/{workflow_id}")
                print(f"\nYou can now:")
                print(f"  1. Open the workflow in n8n")
                print(f"  2. Configure any required credentials")
                print(f"  3. Activate and test the workflow")
                return True
            else:
                print(f"\n❌ Import Failed: {import_result.get('message')}")
                return False
        
        print("\n⚠️  Warning: Workflow generated but not imported")
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def interactive_mode():
    """Run the agent in interactive mode."""
    print(f"\n{'='*60}")
    print("n8n Autonomous Agent - Interactive Mode")
    print(f"{'='*60}")
    print("\nEnter your automation requests (type 'quit' to exit)")
    print("Example: Create a webhook that posts to Slack\n")
    
    while True:
        try:
            request = input("Request: ").strip()
            
            if request.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break
            
            if not request:
                continue
            
            # Ask if they want to skip simulation for speed
            skip = input("Skip simulation for faster execution? (y/n) [n]: ").strip().lower()
            skip_simulation = skip == 'y'
            
            run_agent(request, skip_simulation=skip_simulation)
            print("\n" + "="*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            break

def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--interactive', '-i']:
            interactive_mode()
        elif sys.argv[1] in ['--help', '-h']:
            print(__doc__)
        else:
            # Treat all arguments as the request
            request = ' '.join(sys.argv[1:])
            run_agent(request, skip_simulation=True)
    else:
        # No arguments - show help and enter interactive mode
        print(__doc__)
        print("\nNo request provided. Starting interactive mode...\n")
        interactive_mode()

if __name__ == "__main__":
    main()
