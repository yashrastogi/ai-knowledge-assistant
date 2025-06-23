"""Test FastAPI application"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

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
    assert data["version"] == "0.1.0"


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
