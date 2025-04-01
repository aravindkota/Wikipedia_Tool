# core/graph.py

from langgraph.graph import END, StateGraph
from core.nodes import decide_route, use_wikipedia_tool, generate_response, direct_answer

class ChatState(dict):  # Can be extended for typing if needed
    pass

workflow = StateGraph(ChatState)

# Add nodes
workflow.add_node("decision", decide_route)
workflow.add_node("use_tool", use_wikipedia_tool)
workflow.add_node("generate_response", generate_response)
workflow.add_node("direct_answer", direct_answer)

# Conditional route logic
workflow.add_conditional_edges("decision", lambda s: s["next"], {
    "use_tool": "use_tool",
    "direct_answer": "direct_answer"
})

workflow.add_edge("use_tool", "generate_response")
workflow.add_edge("generate_response", END)
workflow.add_edge("direct_answer", END)

workflow.set_entry_point("decision")
app = workflow.compile()
