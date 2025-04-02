# 🧠 Wikipedia Chatbot using LangChain & Chainlit

This project is an interactive AI chatbot built using **LangChain**, **Chainlit**, and **Google Gemini Pro**. It uses Wikipedia as its knowledge base to answer factual and topic-based queries from users.

---

## 🚀 Features

- ✨ Conversational AI experience
- 🌐 Wikipedia-based factual responses
- 🛠️ Tool usage decision-making by LLM
- 🔄 Modular and maintainable architecture
- 🔐 Secure API key handling via `.env`

---

## 📂 Project Structure

├── main.py # Chainlit entry point and message handlers 
├── .env # Stores sensitive environment variables 
└── core/ 
    ├── graph.py # LangGraph workflow definition 
    ├── llm.py # Google Gemini LLM setup using environment variables 
    ├── nodes.py # Decision, tool usage, response generation logic 
    ├── tools.py # Wikipedia search tool 
    └── prompt.py # System prompt used by the LLM

---

## 🧪 Requirements

Install dependencies with:

```bash
pip install -r requirements.txt

```

### You will need:

    Python 3.8+

    Google Gemini API key

    Internet connection for Wikipedia access

## 🔐 Setup .env File
Create a .env file at the root of the project:

    GOOGLE_API_KEY=your_google_gemini_api_key_here

To start the chatbot with Chainlit, run:

▶️ Running the App

```bash
chainlit run app.py
```

Open the URL displayed in the terminal to chat with the bot in your browser.

💡 How It Works
User sends a message

LLM decides whether to answer directly or use Wikipedia

If needed, the Wikipedia tool fetches context

LLM generates the final answer using the system prompt and context

Response is returned through the Chainlit frontend

## 📌 Example Queries
Who is Marie Curie?

Tell me about the Great Wall of China.

Hi there! → Friendly greeting

Thanks, bye! → Farewell message

## 🧠 Tech Stack

### 🧩 Frameworks & Libraries
- [LangChain](https://www.langchain.com/) – Framework for building applications with language models
- [Chainlit](https://www.chainlit.io/) – UI framework for building LLM-powered chat interfaces
- [LangGraph](https://github.com/langchain-ai/langgraph) – State-based graph logic for controlling LLM workflows

### 🤖 LLM & Models
- [Google Gemini (via LangChain)](https://github.com/langchain-ai/langchain-google-genai) – Used as the LLM backend

### 📚 Data Source
- [WikipediaLoader](https://python.langchain.com/docs/integrations/document_loaders/wikipedia) – Fetches relevant information from Wikipedia

### 🔧 Utilities
- [python-dotenv](https://pypi.org/project/python-dotenv/) – To securely load environment variables from `.env` file

### 🌐 Languages
- Python 3.8+
