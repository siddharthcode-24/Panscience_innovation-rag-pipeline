from typing import List
from langchain_groq import ChatGroq
from app.config import settings
from langchain.schema import HumanMessage, SystemMessage

class LLMService:
    def __init__(self):
        # Initialize Groq client using your API key from .env
        self.client = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.LLM_MODEL or "llama3-8b-8192",  # default Llama 3 model
            temperature=0.7
        )

    def generate_response(self, query: str, context_docs: List[dict]) -> dict:
        """Generate response using retrieved context"""
        
        # Prepare context from retrieved documents
        context = "\n\n".join([
            f"Document: {doc['metadata'].get('filename', 'Unknown')}\n{doc['content']}"
            for doc in context_docs
        ])
        
        # Construct prompt
        prompt = f"""You are a helpful assistant that answers questions based on the provided documents.
If the answer cannot be found in the context, say so clearly.

Context:
{context}

Question: {query}

Answer:"""
        
        # Create LangChain messages
        messages = [
            SystemMessage(content="You are a helpful assistant that answers questions based on provided documents."),
            HumanMessage(content=prompt)
        ]

        # Call Groq API via LangChain
        response = self.client.invoke(messages)

        return {
            "answer": response.content,
            "sources": [doc['metadata'].get('filename') for doc in context_docs],
            "context_used": len(context_docs)
        }
