import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from src.graph.state import AgentState
from src.utils.llm import get_llm
from src.tools.knowledge import search_node_types, get_node_schema
from src.utils.schemas import ConcreteNodesResponse

def node_design_agent(state: AgentState):
    """
    Converts abstract nodes to concrete n8n nodes using knowledge base.
    """
    abstract_dag = state.get("abstract_dag")
    intent = state.get("intent")
    
    if not abstract_dag:
        return {"errors": ["No abstract DAG found for node design"]}
        
    # Load prompt
    with open("src/prompts/node_design.md", "r") as f:
        prompt_text = f.read()
        
    prompt = ChatPromptTemplate.from_template(prompt_text)
    
    # Enable tools for looking up node details
    # tools = [search_node_types, get_node_schema]
    # llm = get_llm().bind_tools(tools)
    
    # Simplified for stability:
    llm = get_llm()
    
    llm_with_output = get_llm().with_structured_output(ConcreteNodesResponse)
    
    chain = prompt | llm_with_output
    
    try:
        # Convert list objects to string for prompt
        result = chain.invoke({
            "abstract_dag": json.dumps(abstract_dag, indent=2),
            "intent": str(intent)
        })
        
        concrete_nodes = [n.model_dump() for n in result.nodes]
        
        return {
            "concrete_nodes": concrete_nodes,
            "next_step": "data_flow",
            "errors": []
        }
    except Exception as e:
        return {
            "errors": [f"Node Design Failed: {str(e)}"],
            "next_step": "end"
        }
