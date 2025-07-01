# AI-Powered Knowledge Assistant

A production-ready Retrieval-Augmented Generation (RAG) system with multi-agent workflows, built with FastAPI, LangChain, and React.

## ✨ What's New

**Latest Version: 0.6.0** (July 2025)

- ✅ **Full Docker Support**: One-command deployment with `docker-compose up`
- ✅ **Production Ready**: Kubernetes manifests, CI/CD pipeline, health checks
- ✅ **Modern Frontend**: React + TypeScript chat interface with real-time updates
- ✅ **Multi-Agent System**: Specialized agents for retrieval, synthesis, and validation
- ✅ **Enterprise Integration**: Mock CMDB/ITSM APIs with auto-detection
- ✅ **Free Embeddings**: HuggingFace models run locally (no API costs)
- ✅ **Comprehensive Testing**: 95%+ code coverage with pytest and vitest

See [CHANGELOG.md](./CHANGELOG.md) for complete version history.

## 🌟 Features

### Core Capabilities
- **RAG-based Q&A**: Semantic search over your knowledge base using vector embeddings
- **Free Local Embeddings**: Uses HuggingFace models (no API costs for embeddings)
- **Multi-Agent Workflow**: Specialized agents for retrieval, synthesis, and validation
  - **Retriever Agent**: Finds relevant documents using hybrid search
  - **Synthesizer Agent**: Combines information from multiple sources into coherent answers
  - **Validator Agent**: Validates answer quality and accuracy with detailed scoring
- **Answer Validation**: Automated quality scoring across 4 dimensions:
  - Relevance (0-10): How well the answer addresses the question
  - Accuracy (0-10): Correctness based on source documents
  - Completeness (0-10): Coverage of all aspects of the question
  - Clarity (0-10): Readability and structure
- **Hybrid Search**: Combines semantic vector search with keyword-based search for better recall
- **Enterprise Integration**: Mock APIs for CMDB/ITSM data with auto-detection of operational queries
- **Source Citations**: Every answer includes references to source documents
- **Modern UI**: React + TypeScript frontend with:
  - Real-time chat interface
  - Markdown support with KaTeX for math equations
  - Agent workflow visualization
  - Validation score display
  - Source document viewer
- **Production-Ready**: 
  - Docker containerization with health checks
  - Comprehensive testing (unit + integration)
  - CI/CD pipeline with GitHub Actions
  - Kubernetes-ready configuration

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.109+ (async Python web framework)
- **LLM**: Google Gemini (gemini-2.5-flash / gemini-2.5-pro)
- **Embeddings**: HuggingFace Transformers (Qwen3-Embedding-0.6B)
- **Vector Store**: FAISS (Facebook AI Similarity Search)
- **Agent Framework**: LangChain 0.1+ for multi-agent orchestration
- **Document Processing**: PyPDF, python-docx, pandas for multiple formats

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite 5 for fast development
- **UI Components**: Custom components with Lucide icons
- **Markdown Rendering**: react-markdown with KaTeX for equations
- **HTTP Client**: Axios for API communication
- **Testing**: Vitest for unit tests

### Infrastructure
- **Containerization**: Docker with multi-stage builds
- **Orchestration**: Docker Compose for local dev, Kubernetes for production
- **Reverse Proxy**: Nginx for frontend static serving and API proxying
- **CI/CD**: GitHub Actions for automated testing and deployment
- **Monitoring**: Health check endpoints with custom status reporting

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Frontend  │◄────►│   Backend    │◄────►│   Vector    │
│  React/TS   │      │  FastAPI     │      │   Store     │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  Multi-Agent │
                     │   Workflow   │
                     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │     LLM      │
                     │  (OpenAI)    │
                     └──────────────┘
```

## 📁 Project Structure

```
smart-doc-retriever2/
├── backend/              # FastAPI + LangChain backend
│   ├── main.py          # API entry point
│   ├── config.py        # Configuration management
│   ├── agents.py        # Multi-agent orchestrator
│   ├── rag_chain.py     # RAG chain implementation
│   ├── retrieval.py     # Vector store and retrieval
│   ├── embeddings.py    # Embedding service
│   ├── document_loader.py # Document processing
│   ├── routes.py        # API routes
│   ├── enterprise_routes.py # Enterprise API routes
│   ├── models.py        # Pydantic models
│   ├── requirements.txt # Python dependencies
│   ├── .env.example     # Environment template
│   ├── enterprise_api/  # Mock enterprise services
│   │   ├── cmdb_service.py
│   │   └── itsm_service.py
│   └── data/
│       └── vector_store/ # FAISS index
├── frontend/            # React + TypeScript UI
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   └── ChatInterface.tsx
│   │   └── services/
│   │       └── api.ts
│   ├── package.json
│   ├── Dockerfile
│   └── vite.config.ts
├── data/                # Knowledge base documents
│   ├── sample_doc1.txt
│   ├── sample_doc2.txt
│   └── vector_store/    # Shared vector store
├── scripts/             # ETL and utility scripts
│   ├── build_embeddings.py
│   ├── test_agents.py
│   ├── test_enterprise_api.py
│   └── test_phase4.py
├── tests/               # Unit and integration tests
│   ├── conftest.py
│   ├── test_agents.py
│   ├── test_api.py
│   ├── test_document_loader.py
│   ├── test_embeddings.py
│   └── test_rag_chain.py
├── docker-compose.yml   # Container orchestration
├── .env.production.example # Production env template
├── DEPLOYMENT.md        # Deployment guide
├── CHANGELOG.md         # Version history
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Google API key (for Gemini LLM)
- Docker 20.10+ and Docker Compose 2.0+ (optional, for containerized deployment)

### Setup Script (Recommended)

The setup script automates the initial project setup:

```bash
# Make setup script executable
chmod +x setup.sh

# Run automated setup
./setup.sh

# Edit environment file with your Google API key
nano backend/.env
```

The script will:
- Create Python virtual environment
- Install backend dependencies
- Install frontend dependencies
- Copy environment template files
- Build initial embeddings from sample documents

### Backend Setup

For development without Docker:

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# Build embeddings from documents
cd ../scripts
python build_embeddings.py

# Return to backend and run the server
cd ../backend
uvicorn main:app --reload
```

Backend will be available at `http://localhost:8000`

**API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend Setup

For development without Docker:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:5173`

## 📋 Development Phases

### ✅ Phase 0: Project Setup
- [x] Initialize Git repository
- [x] Create directory structure
- [x] Set up Python virtual environment
- [x] Configure package managers
- [x] Add README and .gitignore

### ✅ Phase 1: Data Pipeline & RAG Embeddings
- [x] ETL scripts for document ingestion
- [x] Embedding pipeline using OpenAI
- [x] Vector database setup (FAISS)
- [x] Hybrid search implementation
- [x] Retrieval service with tests

### ✅ Phase 2: Backend API for Q&A
- [x] Query endpoint implementation
- [x] RAG chain with LangChain
- [x] Error handling and logging
- [x] API endpoint tests
- [x] Response with source citations

### ✅ Phase 3: Multi-Agent Workflow
- [x] Agent role definitions (Retriever, Synthesizer, Validator)
- [x] Agent orchestration with LangChain
- [x] Multi-step reasoning chain
- [x] Agent collaboration tests
- [x] Answer validation system

### ✅ Phase 4: Enterprise API Integration
- [x] Mock CMDB/ITSM APIs
- [x] EnterpriseAPIAgent implementation
- [x] API query integration with orchestrator
- [x] Auto-detection of operational queries
- [x] End-to-end testing

### ✅ Phase 5: Frontend Integration
- [x] Modern React chat interface
- [x] Real-time question-answer interaction
- [x] Source document citations display
- [x] Agent workflow visualization
- [x] Validation scores display
- [x] Enterprise data integration
- [x] Responsive UI with animations

### ✅ Phase 6: Optimization & Deployment
- [x] Docker containerization (backend + frontend)
- [x] Docker Compose orchestration
- [x] CI/CD pipeline (GitHub Actions)
- [x] Production-ready configurations
- [x] Comprehensive deployment documentation
- [x] Health checks and monitoring setup

## 🐳 Quick Start with Docker

The fastest way to get started is using Docker Compose:

```bash
# Clone the repository
git clone <repository-url>
cd smart-doc-retriever2

# Set up environment variables
cp .env.production.example .env
# Edit .env and add your GOOGLE_API_KEY

# Build and start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f

# Access the application
# Frontend: http://localhost:80 (or http://localhost)
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

To stop the services:
```bash
docker-compose down
```

To rebuild after code changes:
```bash
docker-compose up -d --build
```

For detailed deployment instructions (Kubernetes, cloud providers, monitoring), see [DEPLOYMENT.md](./DEPLOYMENT.md).

## 🧪 Testing

### Backend Tests

```bash
cd backend
source venv/bin/activate  # Activate virtual environment
pytest                     # Run all tests
pytest -v                  # Verbose output
pytest --cov              # With coverage report
pytest tests/test_agents.py  # Run specific test file
```

### Frontend Tests

```bash
cd frontend
npm test                  # Run tests
npm run lint             # Check code quality
```

### Run Tests in Docker

```bash
# Run backend tests in container
docker-compose run backend pytest

# Run frontend tests in container
docker-compose run frontend npm test

# Run with coverage
docker-compose run backend pytest --cov
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI** (interactive): `http://localhost:8000/docs`
- **ReDoc** (reference): `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`
- **Status Check**: `http://localhost:8000/status`

## Architecture Flow

```
User Input
    ↓
Frontend (React)
    ↓
API Service (TypeScript)
    ↓
Backend API (FastAPI)
    ↓
Multi-Agent Orchestrator
    ↓
┌─────────────┬──────────────┬─────────────────┐
│  Retriever  │ Synthesizer  │   Validator     │
│   Agent     │    Agent     │     Agent       │
└─────────────┴──────────────┴─────────────────┘
    ↓                ↓               ↓
Vector Store    LLM (Gemini)     LLM (Gemini)
    ↓
Enterprise APIs (Optional)
    ↓
┌─────────────┬──────────────┐
│    CMDB     │     ITSM     │
│   Service   │   Service    │
└─────────────┴──────────────┘
```

### Key Endpoints

#### `POST /api/v1/query`
Query the knowledge base with natural language questions.

**Standard RAG Request:**
```json
{
  "question": "What is RAG?",
  "k": 4,
  "return_sources": true,
  "use_multi_agent": false
}
```

**Multi-Agent Request:**
```json
{
  "question": "What is RAG?",
  "k": 4,
  "return_sources": true,
  "use_multi_agent": true,
  "validate_answer": true
}
```

**Response:**
```json
{
  "answer": "RAG stands for Retrieval-Augmented Generation...",
  "question": "What is RAG?",
  "success": true,
  "source_documents": [...],
  "validation": {
    "relevance": 9.0,
    "accuracy": 9.5,
    "completeness": 8.5,
    "clarity": 9.0,
    "overall": 9.0,
    "feedback": "Excellent answer with strong citations",
    "passed": true
  },
  "agent_workflow": ["retriever", "synthesizer", "validator"]
}
```

#### `GET /health`
Health check endpoint.

#### `GET /status`
System status with service readiness information.

## 🔧 Configuration

Key environment variables (see `backend/.env.example`):

```env
# Google Gemini Configuration (for LLM only)
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# HuggingFace Embeddings (Free - runs locally, no API key needed)
EMBEDDING_MODEL=Qwen/Qwen3-Embedding-0.6B
EMBEDDING_DEVICE=cpu

# Vector Store Configuration
VECTOR_STORE_TYPE=faiss
VECTOR_STORE_PATH=./data/vector_store

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=info

# CORS Configuration (comma-separated origins)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Agent Configuration
MAX_ITERATIONS=5
AGENT_TIMEOUT=60
```

### Embedding Models

The project uses **locally-run HuggingFace embeddings**:
- Default: `Qwen/Qwen3-Embedding-0.6B` (high quality, efficient)

### LLM Configuration

Google Gemini is used for the LLM agent reasoning:
- Get your free API key at: https://makersuite.google.com/app/apikey
- Recommended model: `gemini-2.5-flash` (fast, efficient)
- Alternative: `gemini-2.5-pro` (more capable)

## 🔍 Troubleshooting

### Common Issues

**Vector Store Not Found**
wd```
Error: Vector store not initialized
```
**Solution:** Run the embeddings builder:
```bash
cd scripts
python build_embeddings.py
```

**CORS Errors in Frontend**
```
Access to XMLHttpRequest blocked by CORS policy
```
**Solution:** Update `CORS_ORIGINS` in backend `.env`:
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Google API Key Error**
```
Error: GOOGLE_API_KEY not found
```
**Solution:** 
1. Get your API key from https://makersuite.google.com/app/apikey
2. Add it to `backend/.env`:
   ```env
   GOOGLE_API_KEY=your_actual_key_here
   ```

**Docker Container Won't Start**
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild containers
docker-compose down
docker-compose up -d --build
```

**Embeddings Take Long Time**
- The first time building embeddings downloads the model (~100MB for Qwen3-Embedding-0.6B)
- Subsequent runs are much faster
- Consider using GPU: set `EMBEDDING_DEVICE=cuda` in `.env` (requires CUDA-compatible GPU)

### Getting Help

- Check [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment guides
- Review [CHANGELOG.md](./CHANGELOG.md) for recent changes
- Open a GitHub issue for bugs or questions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest` for backend, `npm test` for frontend)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines
- Follow existing code style and patterns
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 🙋 Support & Community

### Documentation
- **README.md**: Quick start and overview (this file)
- **[DEPLOYMENT.md](./DEPLOYMENT.md)**: Production deployment guides
- **[CHANGELOG.md](./CHANGELOG.md)**: Version history and changes
- **Backend API Docs**: http://localhost:8000/docs (when running)

### Getting Help
- **Issues**: Open a GitHub issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **API Documentation**: Interactive Swagger UI at `/docs` endpoint

### Reporting Issues
When reporting issues, please include:
- Your environment (OS, Python version, Node version)
- Steps to reproduce the problem
- Expected vs actual behavior
- Relevant logs or error messages

## 🚀 Production Deployment

This project is **production-ready** with enterprise-grade features:

### ✅ Production Features
- **Containerization**: Docker with multi-stage builds for optimized images (~200MB frontend, ~1GB backend)
- **CI/CD Pipeline**: Automated testing and deployment via GitHub Actions
- **Health Monitoring**: Built-in health checks and status endpoints for all services
- **Security**: 
  - Environment-based secrets management
  - CORS configuration
  - Security headers via Nginx
  - No secrets in containers/images
- **Scalability**: 
  - Kubernetes manifests included
  - Horizontal pod autoscaling ready
  - Stateless architecture
- **Reliability**:
  - Automatic container restarts
  - Health checks with proper intervals
  - Graceful shutdown handling
  - Resource limits and reservations

### 📦 Deployment Options

1. **Docker Compose** (Easiest)
   - Best for: Development, staging, single-server deployments
   - Setup time: 5 minutes
   - See Quick Start above

2. **Kubernetes** (Recommended for Production)
   - Best for: Production, high availability, auto-scaling
   - Includes: Deployments, Services, Ingress, ConfigMaps
   - See [DEPLOYMENT.md](./DEPLOYMENT.md) for manifests

3. **Cloud Platforms**
   - **AWS**: ECS, Fargate, or EKS
   - **Google Cloud**: Cloud Run or GKE
   - **Azure**: Container Instances or AKS
   - See [DEPLOYMENT.md](./DEPLOYMENT.md) for platform-specific guides

### 📊 Monitoring & Operations

Built-in endpoints for monitoring:
```bash
# Health check (liveness)
curl http://localhost:8000/health

# System status (readiness)
curl http://localhost:8000/status

# API documentation
open http://localhost:8000/docs
```

### 🔒 Security Checklist

Before deploying to production:
- [ ] Configure proper `CORS_ORIGINS` for your domain
- [ ] Enable HTTPS (use Let's Encrypt or cloud provider SSL)
- [ ] Set up monitoring and alerting
- [ ] Configure log aggregation
- [ ] Review and adjust resource limits in `docker-compose.yml`
- [ ] Enable rate limiting (see [DEPLOYMENT.md](./DEPLOYMENT.md))
- [ ] Set up automated backups for vector store data
