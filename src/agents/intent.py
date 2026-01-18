from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from src.graph.state import AgentState, IntentSpec
from src.utils.llm import get_llm

def intent_agent(state: AgentState):
    """
    Analyzes the user request to determine the intent, trigger, and constraints.
    """
    user_request = state["user_request"]
    
    # Load prompt
    with open("src/prompts/intent.md", "r") as f:
        prompt_text = f.read()
        
    prompt = ChatPromptTemplate.from_template(prompt_text)
    
    # Initialize LLM (Ollama or OpenAI based on config)
    llm = get_llm().with_structured_output(IntentSpec)
    
    chain = prompt | llm
    
    try:
        result = chain.invoke({"user_request": user_request})
        return {
            "intent": result,
            "next_step": "planner",
            "errors": []
        }
    except Exception as e:
        return {
            "errors": [f"Intent Extraction Failed: {str(e)}"],
            "next_step": "end" # Or repair
        }
