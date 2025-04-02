from langgraph.graph import END, StateGraph
from core.nodes import decide_route, use_wikipedia_tool, generate_response, direct_answer

# Define the ChatState class
class ChatState(dict):  # Can be extended for typing if needed
    pass

# Create the workflow graph
workflow = StateGraph(ChatState)

# Add nodes to the workflow
workflow.add_node("decision", decide_route)
workflow.add_node("use_tool", use_wikipedia_tool)
workflow.add_node("generate_response", generate_response)
workflow.add_node("direct_answer", direct_answer)

# Add conditional edges for decision-making
workflow.add_conditional_edges("decision", lambda s: s["next"], {
    "use_tool": "use_tool",
    "direct_answer": "direct_answer"
})

# Add direct edges between nodes
workflow.add_edge("use_tool", "generate_response")
workflow.add_edge("generate_response", END)
workflow.add_edge("direct_answer", END)

# Set the entry point for the workflow
workflow.set_entry_point("decision")

# Compile the workflow into an executable app
app = workflow.compile()