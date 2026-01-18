# LangChain & LangGraph Development Rules

You are an expert in building AI applications with LangChain and LangGraph. Follow these rules for all code generation and planning tasks involving these libraries.

## 1. Core Philosophy & Architecture

- **Prefer LCEL (LangChain Expression Language):** Always use LCEL for constructing chains. It provides automatic parallelization, streaming support, and better composability than legacy `Chain` classes.
  - *Pattern:* `chain = prompt | model | parser`
- **Modularity:** Break down complex logic into small, testable components (Runnables).
- **LangGraph for Agents:** Use LangGraph for *all* agentic workflows, stateful applications, and multi-agent systems. Do not use legacy `AgentExecutor` for new projects.

## 2. LangGraph Best Practices

### State Management
- **Explicit State Schema:** Define the graph state using `TypedDict` or Pydantic models. This is the contract for your system.
  - *Rule:* "Keep state boring." Store only what is necessary (messages, extracted entities, plan status). Avoid dumping large, transient data into the shared state.
- **Immutability & Updates:** Nodes **must not** mutate the state in place. Nodes should return a `dict` of *updates* (keys to modify).
- **Reducers:** Use reducer functions (e.g., `operator.add` for lists of messages) to define how updates are merged into the state.
  - *Example:* `messages: Annotated[list[BaseMessage], operator.add]` ensures new messages are appended, not overwritten.

### Nodes & Edges
- **Single Responsibility Nodes:** Each node should perform one distinct unit of work (e.g., "rewrite_query", "execute_tool", "grade_answer").
- **Conditional Edges:** Use conditional edges for routing logic (e.g., "if not relevant -> end", "if relevant -> generate"). Avoid putting routing logic inside nodes; keep the graph structure visible.
- **Persistence:** Always configure a checkpointer (e.g., `MemorySaver` for dev, Postgres for prod) to enable "time travel," debugging, and human-in-the-loop workflows.

## 3. Tool Calling & Structured Output

### Structured Output
- **Use `with_structured_output()`:** This is the standard method for forcing a model to return data in a specific format.
  - *Input:* Pass a Pydantic model to define the schema.
  - *Mechanism:* It handles the nuance of "tool calling" vs "JSON mode" automatically based on the model provider.
- **Schema Design:** Use Pydantic models with `Field` descriptions. The description is part of the prompt; make it precise.

### Tool Definition
- **Type Hinting:** Strictly type all tool arguments. LangChain uses these types to generate the tool definition for the LLM.
- **Docstrings:** Write comprehensive docstrings for tools. The LLM reads these to understand *when* and *how* to use the tool.
  - *Format:*
    ```python
    @tool
    def my_tool(arg1: int, arg2: str) -> str:
        """Description of what the tool does.
        
        Args:
            arg1: Description of arg1.
            arg2: Description of arg2.
        """
    ```

## 4. Prompts & LLMs

- **Separation of Concerns:** Keep prompts separate from application logic. Do not hardcode strings in Python code.
- **ChatModels over LLMs:** Always use the `ChatModel` interface (e.g., `ChatOpenAI`, `ChatAnthropic`) instead of raw `LLM` interfaces.
- **Message List History:** When managing conversation history, treat it as a list of `BaseMessage` objects.
  
## 5. Testing & Evaluation (LangSmith)

- **Trace Everything:** Enable LangSmith tracing (`LANGCHAIN_TRACING_V2=true`). It is essential for debugging non-deterministic behavior.
- **Unit Testing:** Write unit tests for individual nodes.
- **LLM-as-a-Judge:** Use an LLM to evaluate system outputs for automated grading.

## 6. Project Structure
Follow this structure for LangGraph projects:
```
src/
├── graph/
│   ├── state.py       # State definition (TypedDict)
│   ├── nodes.py       # Node functions (call_model, tool_node)
│   ├── edges.py       # Routing logic (should_continue)
│   └── graph.py       # Graph compilation (StateGraph workflow)
├── tools/             # @tool definitions
├── utils/             # Helper functions
└── main.py            # Entry point
```
