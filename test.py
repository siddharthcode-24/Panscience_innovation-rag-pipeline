from app.services.document_processor import DocumentProcessor
from app.services.vector_store import VectorStore
import os

# Make sure your file exists
file_path = "./uploads/test.pdf"  # Replace with an actual uploaded file
if not os.path.exists(file_path):
    print(f"File does not exist: {file_path}")
    exit()

# Initialize
processor = DocumentProcessor()
vector_store = VectorStore()

# Extract text
text, pages = processor.extract_text(file_path, "pdf")
print(f"[DEBUG] Extracted {len(text)} characters, {pages} pages")

# Chunk text
chunks = processor.chunk_text(text)
print(f"[DEBUG] Generated {len(chunks)} chunks")
if chunks:
    print("[DEBUG] First chunk preview:", chunks[0][:200])

# Add to vector store
vector_store.add_documents(chunks, document_id="test_doc", metadata={"source": file_path})
print(f"[DEBUG] Vector store now contains {vector_store.collection.count()} documents")

# Test a query
results = vector_store.search("test query")
print("[DEBUG] Search results:", results)
