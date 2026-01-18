from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

# Pydantic versions of our TypedDicts for LLM generation

class AbstractNodeModel(BaseModel):
    id: str = Field(description="Unique identifier for the step")
    label: str = Field(description="Human readable label")
    type: str = Field(description="Abstract type like Trigger, Action, Filter")
    description: str = Field(description="What this step does")
    next_steps: List[str] = Field(description="List of IDs that follow this step")

class AbstractDAGResponse(BaseModel):
    steps: List[AbstractNodeModel]

class ConcreteNodeModel(BaseModel):
    id: str
    name: str = Field(description="Display name")
    type: str = Field(description="n8n node type name, e.g. n8n-nodes-base.slack")
    typeVersion: float = Field(default=1)
    position: List[float] = Field(default=[100, 300])
    parameters: Dict[str, Any] = Field(default_factory=dict)
    credentials: Optional[Dict[str, Any]] = Field(default=None)

class ConcreteNodesResponse(BaseModel):
    nodes: List[ConcreteNodeModel]
