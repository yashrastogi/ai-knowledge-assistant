"""Test embedding and vector store functionality"""
import pytest
from pathlib import Path
import sys
import os

backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from embeddings import EmbeddingManager, HybridSearch
from langchain.schema import Document


@pytest.fixture
def sample_documents():
    """Fixture for sample documents"""
    return [
        Document(
            page_content="RAG stands for Retrieval-Augmented Generation. "
                       "It combines retrieval with language model generation.",
            metadata={"source": "test1"}
        ),
        Document(
            page_content="Vector databases store embeddings for efficient similarity search. "
                       "Examples include FAISS, Pinecone, and Weaviate.",
            metadata={"source": "test2"}
        ),
        Document(
            page_content="LangChain is a framework for developing applications with LLMs. "
                       "It provides tools for document loading, splitting, and retrieval.",
            metadata={"source": "test3"}
        )
    ]


def test_embedding_manager_initialization():
    """Test EmbeddingManager initialization"""
    manager = EmbeddingManager(
        embedding_model="Qwen/Qwen3-Embedding-0.6B",
        embedding_device="cpu"
    )
    assert manager.embeddings is not None
    assert manager.vector_store is None


def test_create_vector_store(sample_documents):
    """Test creating vector store from documents"""
    manager = EmbeddingManager(
        embedding_model="Qwen/Qwen3-Embedding-0.6B",
        embedding_device="cpu"
    )
    
    # Create vector store
    vector_store = manager.create_vector_store(sample_documents)
    
    assert vector_store is not None
    assert manager.vector_store is not None


def test_similarity_search(sample_documents):
    """Test similarity search"""
    manager = EmbeddingManager(
        embedding_model="Qwen/Qwen3-Embedding-0.6B",
        embedding_device="cpu"
    )
    
    # Create vector store
    manager.create_vector_store(sample_documents)
    
    # Search for relevant documents
    results = manager.similarity_search("What is RAG?", k=2)
    
    assert len(results) > 0
    assert len(results) <= 2
    assert isinstance(results[0], Document)
    # The first result should contain information about RAG
    assert "RAG" in results[0].page_content or "Retrieval" in results[0].page_content


def test_similarity_search_with_score(sample_documents):
    """Test similarity search with scores"""
    manager = EmbeddingManager(
        embedding_model="Qwen/Qwen3-Embedding-0.6B",
        embedding_device="cpu"
    )
    
    # Create vector store
    manager.create_vector_store(sample_documents)
    
    # Search with scores
    results = manager.similarity_search_with_score("vector databases", k=2)
    
    assert len(results) > 0
    assert len(results) <= 2
    
    # Check result format
    doc, score = results[0]
    assert isinstance(doc, Document)
    # Score can be numpy.float32 from FAISS, so check it's numeric
    assert isinstance(score, (float, int)) or hasattr(score, '__float__')
    assert float(score) >= 0  # Score should be a non-negative number


def test_save_and_load_vector_store(sample_documents, tmp_path):
    """Test saving and loading vector store"""
    store_path = tmp_path / "vector_store"
    
    # Create and save
    manager1 = EmbeddingManager(
        embedding_model="Qwen/Qwen3-Embedding-0.6B",
        embedding_device="cpu",
        vector_store_path=store_path
    )
    manager1.create_vector_store(sample_documents)
    manager1.save_vector_store()
    
    # Verify saved
    assert store_path.exists()
    
    # Load in new manager
    manager2 = EmbeddingManager(
        embedding_model="Qwen/Qwen3-Embedding-0.6B",
        embedding_device="cpu",
        vector_store_path=store_path
    )
    manager2.load_vector_store()
    
    # Test retrieval
    results = manager2.similarity_search("RAG", k=1)
    assert len(results) > 0


def test_add_documents(sample_documents):
    """Test adding documents to existing vector store"""
    manager = EmbeddingManager(
        embedding_model="Qwen/Qwen3-Embedding-0.6B",
        embedding_device="cpu"
    )
    
    # Create initial vector store
    initial_docs = sample_documents[:2]
    manager.create_vector_store(initial_docs)
    
    # Add more documents
    new_docs = sample_documents[2:]
    manager.add_documents(new_docs)
    
    # Should be able to retrieve from all documents
    results = manager.similarity_search("LangChain", k=1)
    assert len(results) > 0
