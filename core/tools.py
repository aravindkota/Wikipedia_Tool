# core/tools.py
from langchain_core.tools import Tool
from langchain_community.document_loaders import WikipediaLoader

def wiki_search(query: str) -> str:
    try:
        results = WikipediaLoader(query=query)
        return results if results else "No relevant information found on Wikipedia."
    except Exception as e:
        return f"Error searching Wikipedia: {str(e)}"

wiki_tool = Tool(
    name="Wikipedia",
    func=wiki_search,
    description="Search Wikipedia for information on a topic"
)
