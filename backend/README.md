# Backend - AI Knowledge Assistant

FastAPI backend with LangChain and RAG capabilities.

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run server
python main.py
```

## Development

```bash
# Run with auto-reload
uvicorn main:app --reload

# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /status` - System status
- `POST /api/v1/query` - Query the knowledge base

### Query Endpoint

**POST /api/v1/query**

Query the knowledge base with natural language questions.

```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is RAG?",
    "k": 4,
    "return_sources": true
  }'
```

Response:
```json
{
  "answer": "RAG stands for Retrieval-Augmented Generation...",
  "question": "What is RAG?",
  "success": true,
  "source_documents": [...]
}
```

## Project Structure

```
backend/
├── main.py              # FastAPI application
├── config.py            # Configuration management
├── models.py            # Pydantic models
├── routes.py            # API routes
├── rag_chain.py         # RAG chain implementation
├── retrieval.py         # Retrieval service
├── embeddings.py        # Embedding management
├── document_loader.py   # Document loading & ETL
├── requirements.txt     # Dependencies
└── .env.example         # Environment template
```

## Environment Variables

See `.env.example` for all available configuration options.
