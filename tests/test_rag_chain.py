"""Test RAG chain functionality"""
import pytest
from pathlib import Path
import sys
import os

backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from rag_chain import RAGChain
from retrieval import retrieval_service


pytestmark = pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set"
)


@pytest.fixture(scope="module")
def initialized_services():
    """Initialize services for testing"""
    try:
        retrieval_service.initialize()
        if not retrieval_service.is_ready():
            pytest.skip("Vector store not initialized - run build_embeddings.py first")
    except Exception as e:
        pytest.skip(f"Could not initialize services: {e}")
    
    return retrieval_service


def test_rag_chain_initialization(initialized_services):
    """Test RAG chain initialization"""
    chain = RAGChain()
    assert not chain.is_ready()
    
    chain.initialize()
    assert chain.is_ready()
    assert chain.llm is not None
    assert chain.chain is not None


def test_rag_chain_query(initialized_services):
    """Test RAG chain query"""
    chain = RAGChain()
    chain.initialize()
    
    result = chain.query("What is RAG?")
    
    assert "answer" in result
    assert "question" in result
    assert "success" in result
    assert result["success"] is True
    assert len(result["answer"]) > 0
    assert result["question"] == "What is RAG?"


def test_rag_chain_query_with_sources(initialized_services):
    """Test RAG chain query with source documents"""
    chain = RAGChain()
    chain.initialize()
    
    result = chain.query("What is RAG?", return_source_documents=True)
    
    assert "source_documents" in result
    assert isinstance(result["source_documents"], list)
    assert len(result["source_documents"]) > 0
    
    # Check source document structure
    source = result["source_documents"][0]
    assert "content" in source
    assert "metadata" in source
    assert "preview" in source


def test_rag_chain_query_without_sources(initialized_services):
    """Test RAG chain query without source documents"""
    chain = RAGChain()
    chain.initialize()
    
    result = chain.query("What is RAG?", return_source_documents=False)
    
    # Should not have source_documents or it should be empty
    assert result.get("source_documents") is None or len(result.get("source_documents", [])) == 0


def test_rag_chain_multiple_queries(initialized_services):
    """Test multiple queries"""
    chain = RAGChain()
    chain.initialize()
    
    questions = [
        "What is RAG?",
        "What is a vector database?",
        "How does retrieval work?"
    ]
    
    for question in questions:
        result = chain.query(question)
        assert result["success"] is True
        assert len(result["answer"]) > 0
        assert result["question"] == question


def test_rag_chain_not_initialized():
    """Test query before initialization"""
    chain = RAGChain()
    
    with pytest.raises(RuntimeError):
        chain.query("Test question")
