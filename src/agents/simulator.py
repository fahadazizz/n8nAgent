import json
from langchain_core.prompts import ChatPromptTemplate
from src.graph.state import AgentState
from src.utils.llm import get_llm
from pydantic import BaseModel, Field
from typing import List, Literal

class SimulationResponse(BaseModel):
    logs: List[str]
    runtime_errors: List[str]
    status: Literal["success", "failed"]

def simulator_agent(state: AgentState):
    """
    Simulates execution to find runtime errors.
    """
    workflow = state.get("n8n_json")
    
    # Load prompt
    with open("src/prompts/simulator.md", "r") as f:
        prompt_text = f.read()
    
    prompt = ChatPromptTemplate.from_template(prompt_text)
    llm = get_llm().with_structured_output(SimulationResponse)
    
    chain = prompt | llm
    
    try:
        # We invoke the LLM to "think" through the execution
        result = chain.invoke({"workflow": json.dumps(workflow)})
        
        if result.status == "failed":
            return {
                "errors": result.runtime_errors, 
                "next_step": "repair",
                # Append to existing errors
                "validation_status": "runtime_error"
            }
            
        return {
            "validation_status": "verified",
            "next_step": "end",
            "errors": []
        }
    except Exception as e:
        return {"errors": [f"Simulation Failed: {str(e)}"], "next_step": "end"}
