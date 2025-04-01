# main.py
from core.graph import app
from chainlit import on_chat_start, on_message, Message
from langchain_core.messages import HumanMessage

@on_chat_start
async def start():
    await Message(content="Welcome to the Wikipedia Chatbot! Ask me anything.").send()

@on_message
async def main(message: Message):
    human_message = HumanMessage(content=message.content)
    state = {"messages": [human_message], "tool_result": None, "next": None}
    thinking = Message(content="Thinking...")
    await thinking.send()

    try:
        for step_state in app.stream(state):
            # You can handle different responses here
            pass
    except Exception as e:
        await thinking.update(content=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    from chainlit.cli import run_chainlit
    run_chainlit(__file__)
