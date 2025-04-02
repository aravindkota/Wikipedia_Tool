from core.graph import app
from chainlit import on_chat_start, on_message, Message
from langchain_core.messages import HumanMessage
import chainlit as cl

@on_chat_start
async def start():
    """Send a welcome message when the chat starts."""
    await Message(content="Welcome to the Wikipedia Chatbot! Ask me anything.").send()

@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages."""
    # Create a new human message
    human_message = HumanMessage(content=message.content)
    
    # Create the initial state with the user's message
    state = {"messages": [human_message], "tool_result": None, "next": None}
    
    # Send a "thinking" message to the user
    thinking = cl.Message(content="Thinking...")
    await thinking.send()
    
    # Process the message through the workflow graph
    try:
        for step_state in app.stream(state.copy()):
            print(f"Current state: {step_state}")  # Debugging output
            
            # Handle the "generate_response" state
            if step_state["next"] == "generate_response":
                await cl.Message(
                    content="I found this information on Wikipedia:",
                    elements=[
                        cl.Text(
                            name="Wikipedia Result",
                            content=step_state["tool_result"] + "..."
                        )
                    ]
                ).send()
            
            # Handle the "direct_answer" state
            elif step_state["next"] == "direct_answer":
                thinking.content = step_state["messages"][-1].content
                await thinking.update()
    
    except Exception as e:
        # Handle errors and update the user
        await thinking.update(f"An error occurred: {str(e)}")
        print(f"Error in processing: {str(e)}")

if __name__ == "__main__":
    from chainlit.cli import run_chainlit
    run_chainlit(__file__)