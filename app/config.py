from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Configuration
    API_TITLE: str = "RAG Pipeline API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Retrieval-Augmented Generation Pipeline for Document Q&A"
    
    # LLM Configuration
    GROQ_API_KEY: str
    LLM_MODEL: str = "llama3-8b-8192"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # Document Processing
    MAX_DOCUMENTS: int = 20
    MAX_PAGES_PER_DOCUMENT: int = 1000
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Storage Paths
    UPLOAD_DIR: str = "./uploads"
    VECTOR_STORE_PATH: str = "./vectorstore"
    CHROMA_PERSIST_DIRECTORY: str = "./data/chroma_db"

    # Database
    DATABASE_URL: str = "postgresql://rag_user:rag_password@db:5432/rag_db"
    
    # Retrieval Configuration
    TOP_K_RESULTS: int = 5
    SIMILARITY_THRESHOLD: float = 0.7
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # ✅ Allow extra env variables like HUGGINGFACEHUB_API_TOKEN

settings = Settings()
