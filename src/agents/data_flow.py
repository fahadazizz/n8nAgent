import json
from langchain_core.prompts import ChatPromptTemplate
from src.graph.state import AgentState, N8nWorkflow
from src.utils.llm import get_llm

def data_flow_agent(state: AgentState):
    """
    Connects nodes and adds expressions.
    """
    concrete_nodes = state.get("concrete_nodes")
    
    if not concrete_nodes:
        return {"errors": ["No concrete nodes found for data flow"]}
        
    # Load prompt
    with open("src/prompts/data_flow.md", "r") as f:
        prompt_text = f.read()
        
    prompt = ChatPromptTemplate.from_template(prompt_text)
    
    llm = get_llm().with_structured_output(N8nWorkflow)
    
    chain = prompt | llm
    
    try:
        result = chain.invoke({
            "concrete_nodes": json.dumps(concrete_nodes, indent=2)
        })
        
        return {
            "n8n_json": result,
            "next_step": "end", # Moving to validation later
            "errors": []
        }
    except Exception as e:
        return {
            "errors": [f"Data Flow Failed: {str(e)}"],
            "next_step": "end"
        }
