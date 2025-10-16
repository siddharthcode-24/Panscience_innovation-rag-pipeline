# RAG Pipeline - Document Q&A System

A Retrieval-Augmented Generation (RAG) pipeline that allows users to upload documents and ask questions based on their content.

## Features

- 📄 Upload up to 20 documents (PDF, DOCX, TXT)
- 🔍 Intelligent document chunking and vector storage
- 🤖 AI-powered question answering using OpenAI
- 🚀 Fast API with automatic documentation
- 🐳 Fully containerized with Docker
- 💾 Persistent storage for documents and embeddings

## Prerequisites

- Docker & Docker Compose
- OpenAI API Key

## Quick Start

### 1. Clone the repository
```bash
git clone <(https://github.com/siddharthcode-24/rag-pipeline)>
cd rag-pipeline
```

### 2. Configure environment
```bash
# Edit .env file and add your OpenAI API key
nano .env  # or use any text editor
```

### 3. Run with Docker
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

### 4. Access API Documentation
Open your browser and go to: `http://localhost:8000/docs`

## API Endpoints

### Upload Document
```bash
POST /api/v1/upload
Content-Type: multipart/form-data

curl -X POST "http://localhost:8000/api/v1/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your-document.pdf"
```

### Query Documents
```bash
POST /api/v1/query?question=Your%20question%20here

curl -X POST "http://localhost:8000/api/v1/query?question=What%20is%20the%20main%20topic?" \
  -H "accept: application/json"
```

### List Documents
```bash
GET /api/v1/documents

curl -X GET "http://localhost:8000/api/v1/documents" \
  -H "accept: application/json"
```

### Delete Document
```bash
DELETE /api/v1/documents/{document_id}

curl -X DELETE "http://localhost:8000/api/v1/documents/1" \
  -H "accept: application/json"
```

## Local Development

### Without Docker

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python -m uvicorn app.main:app --reload
```

## Testing

Run tests with pytest:
```bash
pytest tests/ -v
```

## Project Structure
```
rag-pipeline/
├── app/
│   ├── api/
│   │   └── routes.py          # API endpoints
│   ├── models/
│   │   └── document.py        # Database models
│   ├── services/
│   │   ├── database.py        # Database connection
│   │   ├── document_processor.py  # Document processing
│   │   ├── vector_store.py    # Vector database
│   │   └── llm_service.py     # LLM integration
│   ├── config.py              # Configuration
│   └── main.py                # FastAPI application
├── tests/
│   └── test_api.py            # API tests
├── uploads/                   # Uploaded documents
├── data/                      # Database and vector store
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose setup
├── .env                       # Environment variables
└── README.md                  # Documentation
```

## Configuration

Edit `.env` file to customize:
```env
OPENAI_API_KEY=your-key-here
MAX_DOCUMENTS=20
MAX_PAGES_PER_DOCUMENT=1000
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

## Using Different LLM Providers

### Gemini (Google)
Replace OpenAI with Google Generative AI:
```python
pip install google-generativeai
```

### Anthropic Claude
```python
pip install anthropic
```

Modify `app/services/llm_service.py` to use your preferred provider.

## Troubleshooting

### Port already in use
Change the port in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"
```

### OpenAI API errors
- Verify your API key is correct
- Check you have sufficient credits
- Ensure proper internet connectivity

## Output
<img width="1896" height="957" alt="image" src="https://github.com/user-attachments/assets/509f746d-3746-4c52-ac21-ad80e1fa8e42" />
<img width="1876" height="982" alt="image 2" src="https://github.com/user-attachments/assets/8c85442b-431f-4036-b022-453dacb5f517" />


