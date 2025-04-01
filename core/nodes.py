# core/nodes.py

from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from core.llm import llm
from core.tools import wiki_tool
from core.prompt import system_prompt

def decide_route(state):
    """Decide whether to use the tool or directly answer the question."""
    human_message = state["messages"][-1]
    question = human_message.content

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You need to decide whether to use Wikipedia to answer this question. "
                   "If the question asks for factual information, historical data, or specific details "
                   "that might benefit from Wikipedia lookup, respond with 'use_tool'. "
                   "If the question is more general or you can answer it directly, respond with 'direct_answer'. "
                   "If the question is a greeting or farewell, respond with 'greeting' or 'farewell' respectively. "
                   "Otherwise, respond with 'direct_answer'."),
        ("human", f"Question: {question}")
    ])

    response = llm.invoke(prompt.format_messages())

    new_state = state.copy()
    if "use_tool" in response.content:
        new_state["next"] = "use_tool"
    else:
        new_state["next"] = "direct_answer"

    return new_state


def use_wikipedia_tool(state):
    """Use the Wikipedia tool to get information."""
    human_message = state["messages"][-1]
    question = human_message.content

    wiki_result = wiki_tool.invoke(question)

    new_state = state.copy()
    new_state["tool_result"] = wiki_result
    new_state["next"] = "generate_response"
    return new_state


def generate_response(state):
    """Generate the final response based on the conversation and tool results."""
    messages = state["messages"]
    question = messages[-1].content
    context = state.get("tool_result", "")

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", f"Question: {question}"),
        ("system", f"Wikipedia information: {context}"),
        ("human", "Now please provide a helpful answer based on this information.")
    ])

    response = llm.invoke(prompt.format_messages())

    new_state = state.copy()
    new_state["messages"].append(AIMessage(content=response.content))
    return new_state


def direct_answer(state):
    """Generate a response without using the tool."""
    messages = state["messages"]
    question = messages[-1].content

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", f"Question: {question}")
    ])

    response = llm.invoke(prompt.format_messages())

    new_state = state.copy()
    new_state["messages"].append(AIMessage(content=response.content))
    return new_state
