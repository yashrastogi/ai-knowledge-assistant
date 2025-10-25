"""Test FastAPI application"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path
import os

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from main import app

client = TestClient(app)


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "AI Knowledge Assistant API"
    assert data["version"] == "0.6.0"


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_status():
    """Test status endpoint"""
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert "services" in data
    assert "api" in data["services"]
    assert "vector_store" in data["services"]
    assert "rag_chain" in data["services"]


@pytest.mark.skipif(
    not os.getenv("GOOGLE_API_KEY"),
    reason="GOOGLE_API_KEY not set"
)
def test_query_endpoint():
    """Test query endpoint"""
    # This test requires vector store to be initialized
    response = client.post(
        "/api/v1/query",
        json={
            "question": "What is RAG?",
            "k": 3,
            "return_sources": True
        }
    )
    
    # May return 503 if vector store not initialized
    if response.status_code == 503:
        pytest.skip("Vector store not initialized")
    
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "question" in data
    assert data["question"] == "What is RAG?"
    assert "success" in data


def test_query_endpoint_invalid_request():
    """Test query endpoint with invalid request"""
    response = client.post(
        "/api/v1/query",
        json={
            "question": "",  # Empty question
            "k": 3
        }
    )
    
    assert response.status_code == 422  # Validation error


def test_query_endpoint_without_sources():
    """Test query endpoint without source documents"""
    response = client.post(
        "/api/v1/query",
        json={
            "question": "What is RAG?",
            "k": 3,
            "return_sources": False
        }
    )
    
    # May return 503 if vector store not initialized
    if response.status_code == 503:
        pytest.skip("Vector store not initialized")
    
    if response.status_code == 200:
        data = response.json()
        # source_documents should be None when return_sources=False
        assert data.get("source_documents") is None or data.get("source_documents") == []
