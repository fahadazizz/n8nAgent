from typing import Literal
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from src.graph.state import AgentState
from src.agents.intent import intent_agent
from src.agents.planner import planner_agent
from src.agents.node_design import node_design_agent
from src.agents.data_flow import data_flow_agent
from src.agents.compiler import compiler_agent
from src.agents.validator import validator_agent
from src.agents.error_handler import error_handler_agent
from src.agents.simulator import simulator_agent
from src.agents.repair import repair_agent
from src.agents.import_agent import import_agent

def build_graph():
    """
    Constructs the StateGraph.
    """
    workflow = StateGraph(AgentState)
    
    # Add Nodes
    workflow.add_node("intent", intent_agent)
    workflow.add_node("planner", planner_agent)
    workflow.add_node("node_design", node_design_agent)
    workflow.add_node("data_flow", data_flow_agent)
    workflow.add_node("error_handler", error_handler_agent)
    workflow.add_node("compiler", compiler_agent)
    workflow.add_node("validator", validator_agent)
    workflow.add_node("simulator", simulator_agent)
    workflow.add_node("repair", repair_agent)
    workflow.add_node("import", import_agent)
    
    # Add Edges
    workflow.add_edge(START, "intent")
    
    # Conditional Edges for Linear Flow
    workflow.add_conditional_edges(
        "intent",
        lambda x: "planner" if not x.get("errors") else END
    )
    
    workflow.add_conditional_edges(
        "planner",
        lambda x: "node_design" if not x.get("errors") else END
    )
    
    workflow.add_conditional_edges(
        "node_design",
        lambda x: "data_flow" if not x.get("errors") else END
    )
    
    # Data Flow -> Error Handler -> Compiler
    workflow.add_conditional_edges(
        "data_flow",
        lambda x: "error_handler" if not x.get("errors") else END
    )

    workflow.add_edge("error_handler", "compiler")
    workflow.add_edge("compiler", "validator")
    
    # Validation -> (if invalid) Repair -> Data Flow
    # Validation -> (if valid) Simulator
    def route_validator(state):
        if state.get("errors"):
            return "repair"
        return "simulator"
        
    workflow.add_conditional_edges("validator", route_validator)
    
    # Simulator -> (if failed) Repair -> Data Flow
    # Simulator -> (if success) Import to n8n
    def route_simulator(state):
        if state.get("errors"):
            return "repair"
        return "import"
        
    workflow.add_conditional_edges("simulator", route_simulator)
    
    # Repair -> Data Flow (to re-generate expressions/connections with new nodes)
    workflow.add_edge("repair", "data_flow")
    
    # Import -> End
    workflow.add_edge("import", END)
    
    return workflow.compile()
