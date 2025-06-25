"""FastAPI application entry point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from retrieval import retrieval_service
from rag_chain import rag_chain
from routes import router as query_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    logger.info("Starting AI Knowledge Assistant API...")
    # Initialize retrieval service
    try:
        retrieval_service.initialize()
        if retrieval_service.is_ready():
            # Initialize RAG chain
            rag_chain.initialize()
            logger.info("All services initialized successfully")
        else:
            logger.warning("Retrieval service not ready - run build_embeddings.py first")
    except Exception as e:
        logger.warning(f"Could not initialize services: {e}")
    yield
    logger.info("Shutting down AI Knowledge Assistant API...")


# Create FastAPI app
app = FastAPI(
    title="AI Knowledge Assistant",
    description="RAG-powered Q&A system with multi-agent workflow",
    version="0.2.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(query_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Knowledge Assistant API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/status")
async def status():
    """Status endpoint with system information"""
    return {
        "status": "operational",
        "services": {
            "api": "running",
            "vector_store": "ready" if retrieval_service.is_ready() else "not_ready",
            "rag_chain": "ready" if rag_chain.is_ready() else "not_ready",
            "agents": "pending"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
