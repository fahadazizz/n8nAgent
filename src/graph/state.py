import operator
from typing import Annotated, Any, Dict, List, Optional, TypedDict, Union
from langchain_core.messages import BaseMessage

class IntentSpec(TypedDict):
    trigger_type: str
    integrations: List[str]
    constraints: List[str]
    raw_intent: str

class AbstractNode(TypedDict):
    id: str
    label: str
    type: str  # Abstract type, e.g., "Webhook", "Slack"
    description: str
    next_steps: List[str]

class ConcreteNode(TypedDict):
    id: str
    name: str
    type: str  # specific n8n node type, e.g., "n8n-nodes-base.slack"
    typeVersion: float
    position: List[float]
    parameters: Dict[str, Any]
    credentials: Optional[Dict[str, Any]]

class N8nWorkflow(TypedDict):
    nodes: List[ConcreteNode]
    connections: Dict[str, Any]
    meta: Dict[str, Any]

class AgentState(TypedDict):
    # Conversation history
    messages: Annotated[List[BaseMessage], operator.add]
    
    # Artifacts produced by agents
    user_request: str
    intent: Optional[IntentSpec]
    abstract_dag: Optional[List[AbstractNode]]
    concrete_nodes: Optional[List[ConcreteNode]]
    n8n_json: Optional[N8nWorkflow]
    
    # Validation & Error tracking
    errors: List[str]
    validation_status: str  # 'pending', 'valid', 'invalid'
    
    # Metadata
    next_step: str
