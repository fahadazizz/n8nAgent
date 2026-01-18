from langchain_core.prompts import ChatPromptTemplate
from src.graph.state import AgentState
from src.utils.llm import get_llm
from src.utils.schemas import AbstractDAGResponse

def planner_agent(state: AgentState):
    """
    Generates an abstract DAG based on the intent.
    """
    intent = state.get("intent")
    if not intent:
        return {"errors": ["No intent found for planning"]}
        
    # Load prompt
    with open("src/prompts/planner.md", "r") as f:
        prompt_text = f.read()
        
    prompt = ChatPromptTemplate.from_template(prompt_text)
    
    llm = get_llm().with_structured_output(AbstractDAGResponse)
    
    chain = prompt | llm
    
    try:
        result = chain.invoke({"intent": str(intent)})
        # Convert Pydantic models to dicts for state
        abstract_dag = [n.model_dump() for n in result.steps]
        return {
            "abstract_dag": abstract_dag,
            "next_step": "node_design",
            "errors": []
        }
    except Exception as e:
        return {
            "errors": [f"Planning Failed: {str(e)}"],
            "next_step": "end"
        }
