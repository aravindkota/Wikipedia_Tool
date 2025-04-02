# app.py
import os
import chainlit as cl
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import Tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WikipediaLoader
from langgraph.graph import END, StateGraph
import typing
from dotenv import load_dotenv

load_dotenv()
# Configure Google API

# Replace with your API key
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-pro-002", temperature=0.2, google_api_key=os.getenv("GOOGLE_API_KEY"))

def wiki_search(query: str) -> str:
    """Search Wikipedia for information on a given topic."""
    try:
        results = WikipediaLoader(query = query)
        return results if results else "No relevant information found on Wikipedia."
    except Exception as e:
        return f"Error searching Wikipedia: {str(e)}"

# Create a Wikipedia tool
wiki_tool = Tool(
    name="Wikipedia",
    func=wiki_search,
    description="Search Wikipedia for information on a topic"
)

# Define the system prompt
system_prompt = """You are a helpful AI assistant that can answer questions using Wikipedia.
If you don't know the answer or can't find relevant information, be honest about it.
Use the Wikipedia tool when you need to look up information before answering.
Always be concise and informative in your responses.
If the user query is like hi or hello, respond with a friendly greeting.
If the user ends the conveersation, say goodbye.
If the user asks for any topic, use the Wikipedia tool to find relevant information.
If the user asks for a specific fact or detail, provide a direct answer if you know it."""

# Define our state
class ChatState(typing.TypedDict):
    messages: list
    tool_result: typing.Optional[str]
    next: typing.Optional[str]  # This will hold the next node to go to

def decide_route(state: ChatState) -> ChatState:
    """Decide whether to use the tool or directly answer the question."""
    human_message = state["messages"][-1]
    question = human_message.content
    
    # Simple prompt to help the LLM decide whether to use Wikipedia
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
    
    # Update state with the next node to go to
    new_state = state.copy()
    if "use_tool" in response.content:
        new_state["next"] = "use_tool"
    else:
        new_state["next"] = "direct_answer"
        
    return new_state

def use_wikipedia_tool(state: ChatState) -> ChatState:
    """Use the Wikipedia tool to get information."""
    human_message = state["messages"][-1]
    question = human_message.content
    
    # Get information from Wikipedia
    wiki_result = wiki_tool.invoke(question)
    
    # Update state with the tool results
    new_state = state.copy()
    new_state["tool_result"] = wiki_result
    new_state["next"] = "generate_response"
    return new_state

def generate_response(state: ChatState) -> ChatState:
    """Generate the final response based on the conversation and tool results."""
    messages = state["messages"]
    question = messages[-1].content
    
    context = state.get("tool_result", "")
    
    # Create a prompt for the final response
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", f"Question: {question}"),
        ("system", f"Wikipedia information: {context}"),
        ("human", "Now please provide a helpful answer based on this information.")
    ])
    
    response = llm.invoke(prompt.format_messages())
    
    # Update state with AI response
    new_state = state.copy()
    new_state["messages"].append(AIMessage(content=response.content))
    return new_state

def direct_answer(state: ChatState) -> ChatState:
    """Generate a response without using the tool."""
    messages = state["messages"]
    question = messages[-1].content
    
    # Create a prompt for the direct response
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", f"Question: {question}")
    ])
    
    response = llm.invoke(prompt.format_messages())
    
    # Update state with AI response
    new_state = state.copy()
    new_state["messages"].append(AIMessage(content=response.content))
    return new_state

# Create the graph
workflow = StateGraph(ChatState)

# Add nodes
workflow.add_node("decision", decide_route)
workflow.add_node("use_tool", use_wikipedia_tool)
workflow.add_node("generate_response", generate_response)
workflow.add_node("direct_answer", direct_answer)

# Define the conditional edges
def next_step(state: ChatState) -> str:
    """Determines the next step in the workflow based on the state."""
    return state["next"]

# Connect the nodes
workflow.add_conditional_edges("decision", next_step, {
    "use_tool": "use_tool",
    "direct_answer": "direct_answer"
})

# Simple edges
workflow.add_edge("use_tool", "generate_response")
workflow.add_edge("generate_response", END)
workflow.add_edge("direct_answer", END)

# Set the entry point
workflow.set_entry_point("decision")

# Compile the graph
app = workflow.compile()

@cl.on_chat_start
async def start():
    """Initialize the chat session"""
    await cl.Message(content="Welcome to the Wikipedia Chatbot! Ask me anything, and I'll try to help you with information from Wikipedia.").send()

@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages"""
    # Create a new human message
    human_message = HumanMessage(content=message.content)
    
    # Create initial state with the message
    state = {"messages": [human_message], "tool_result": None, "next": None}
    
    # Send a thinking message
    thinking = cl.Message(content="Thinking...")
    await thinking.send()
    
    # Process the message through our graph
    try:
        for step_state in app.stream(state):
            print(f"Current state: {step_state}")  # For debugging
            
            if 'generate_response' in step_state:
                
                await cl.Message(
                    content="I found this information on Wikipedia:",
                    elements=[
                        cl.Text(name="Wikipedia Result", content=step_state['generate_response']['messages'][1].content + "..." )
                    ]
                ).send()
            elif 'direct_answer' in step_state:
                # Update the message with the assistant's response
                thinking.content = step_state['direct_answer']['messages'][1].content
                await thinking.update()
                
    except Exception as e:
        await thinking.update(content = f"An error occurred: {str(e)}")
        print(f"Error in processing: {str(e)}")

# Run the Chainlit app
if __name__ == "__main__":
    from chainlit.cli import run_chainlit
    run_chainlit(__file__)  # You can specify the port if needed