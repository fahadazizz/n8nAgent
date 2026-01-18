import os
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

def get_llm(model_name="llama3"):
    """
    Factory to get the LLM instance. 
    Defaults to Ollama (llama3) as per project requirements.
    """
    # Updated to match available local model
    return ChatOllama(model="kimi-k2-thinking:cloud", temperature=0, base_url="http://localhost:11434")
