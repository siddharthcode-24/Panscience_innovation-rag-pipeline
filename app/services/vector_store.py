from langchain.embeddings import HuggingFaceEmbeddings
import chromadb
from chromadb.config import Settings as ChromaSettings
from app.config import settings
import os
from typing import List

class VectorStore:
    def __init__(self):
        os.makedirs(settings.CHROMA_PERSIST_DIRECTORY, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIRECTORY,
            settings=ChromaSettings(anonymized_telemetry=False)
        )

        # Use Hugging Face model via token
        hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")  # read from environment
        self.embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
          )

        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, chunks: List[str], document_id: str, metadata: dict):
        embeddings = self.embeddings.embed_documents(chunks)
        ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{**metadata, "chunk_index": i} for i in range(len(chunks))]

        self.collection.add(
            embeddings=embeddings,
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )

    def search(self, query: str, top_k: int = 5) -> List[dict]:
        query_embedding = self.embeddings.embed_query(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        retrieved_docs = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                retrieved_docs.append({
                    "content": doc,
                    "metadata": results["metadatas"][0][i],
                    "score": 1 - results["distances"][0][i]
                })
        return retrieved_docs
