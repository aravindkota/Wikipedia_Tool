# core/llm.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-pro-002",
    temperature=0.2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
