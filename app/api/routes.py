from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from datetime import datetime

from app.services.database import get_db
from app.services.document_processor import DocumentProcessor
from app.services.vector_store import VectorStore
from app.services.llm_service import LLMService
from app.models.document import Document
from app.config import settings

router = APIRouter()

# Initialize services
doc_processor = DocumentProcessor()
vector_store = VectorStore()
llm_service = LLMService()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and process a document"""
    
    # Check document limit
    doc_count = db.query(Document).count()
    if doc_count >= settings.MAX_DOCUMENTS:
        raise HTTPException(status_code=400, detail=f"Maximum document limit ({settings.MAX_DOCUMENTS}) reached")
    
    # Validate file type
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in ["pdf", "docx", "doc", "txt"]:
        raise HTTPException(status_code=400, detail="Unsupported file type. Supported: PDF, DOCX, DOC, TXT")
    
    # Check if file already exists
    existing_doc = db.query(Document).filter(Document.original_filename == file.filename).first()
    if existing_doc:
        raise HTTPException(status_code=400, detail="Document already uploaded")
    
    try:
        # Save file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_size = os.path.getsize(file_path)
        
        # Extract text
        text, page_count = doc_processor.extract_text(file_path, file_extension)
        
        # Chunk text
        chunks = doc_processor.chunk_text(text)
        
        # Create database record
        db_document = Document(
            filename=filename,
            original_filename=file.filename,
            file_path=file_path,
            file_type=file_extension,
            page_count=page_count,
            chunk_count=len(chunks),
            file_size=file_size,
            processed=False
        )
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        
        # Add to vector store
        metadata = {
            "filename": file.filename,
            "document_id": str(db_document.id),
            "file_type": file_extension
        }
        vector_store.add_documents(chunks, str(db_document.id), metadata)
        
        # Update processed status
        db_document.processed = True
        db.commit()
        
        return {
            "message": "Document uploaded and processed successfully",
            "document_id": db_document.id,
            "filename": file.filename,
            "pages": page_count,
            "chunks": len(chunks)
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Cleanup on error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@router.post("/query")
async def query_documents(
    question: str = Query(..., description="Question to ask about the documents"),
    top_k: int = Query(5, description="Number of relevant chunks to retrieve")
):
    """Query the documents"""
    
    try:
        # Retrieve relevant chunks
        relevant_docs = vector_store.search(question, top_k=top_k)
        
        if not relevant_docs:
            return {
                "answer": "No relevant information found in the uploaded documents.",
                "sources": [],
                "context_used": 0
            }
        
        # Generate response
        response = llm_service.generate_response(question, relevant_docs)
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.get("/documents")
async def list_documents(db: Session = Depends(get_db)):
    """List all uploaded documents"""
    
    documents = db.query(Document).all()
    
    return {
        "total_documents": len(documents),
        "documents": [
            {
                "id": doc.id,
                "filename": doc.original_filename,
                "file_type": doc.file_type,
                "pages": doc.page_count,
                "chunks": doc.chunk_count,
                "uploaded_at": doc.uploaded_at.isoformat(),
                "processed": doc.processed,
                "file_size_kb": round(doc.file_size / 1024, 2)
            }
            for doc in documents
        ]
    }

@router.delete("/documents/{document_id}")
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    """Delete a document"""
    
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        # Delete file
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        # Delete from database
        db.delete(document)
        db.commit()
        
        return {"message": "Document deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "RAG Pipeline API"}