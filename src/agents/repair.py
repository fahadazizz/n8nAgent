import json
from langchain_core.prompts import ChatPromptTemplate
from src.graph.state import AgentState
from src.utils.llm import get_llm
from src.utils.schemas import ConcreteNodesResponse
# Note: Complex repairs might need AbstractDAG response too, but let's focus on node params for now.

def repair_agent(state: AgentState):
    """
    Attempts to fix validation or simulation errors.
    """
    errors = state.get("errors", [])
    concrete_nodes = state.get("concrete_nodes")
    abstract_dag = state.get("abstract_dag")
    
    # Load prompt
    with open("src/prompts/repair.md", "r") as f:
        prompt_text = f.read()
    
    prompt = ChatPromptTemplate.from_template(prompt_text)
    
    # We allow the model to rewrite the concrete nodes.
    # Ideally should handle abstract dag updates too, but that's a cycle back to Planner.
    # For now, we assume most errors are parameter/config errors (Repair -> Compiler).
    
    llm = get_llm().with_structured_output(ConcreteNodesResponse)
    
    chain = prompt | llm
    
    try:
        result = chain.invoke({
            "errors": json.dumps(errors),
            "abstract_dag": json.dumps(abstract_dag),
            "concrete_nodes": json.dumps(concrete_nodes)
        })
        
        updated_nodes = [n.model_dump() for n in result.nodes]
        
        # Clear errors as we have applied a fix
        return {
            "concrete_nodes": updated_nodes,
            "errors": [], 
            "next_step": "data_flow" # Go back to data flow to re-bind connections/expressions
        }
    except Exception as e:
        return {
            "errors": [f"Repair Failed: {str(e)}"],
            "next_step": "end"
        }
