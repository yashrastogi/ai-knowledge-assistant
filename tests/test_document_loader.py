"""Test document loading and ETL functionality"""
import pytest
from pathlib import Path
import sys

backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from document_loader import DocumentETL
from langchain.schema import Document


def test_document_etl_initialization():
    """Test DocumentETL initialization"""
    etl = DocumentETL(chunk_size=500, chunk_overlap=100)
    assert etl.chunk_size == 500
    assert etl.chunk_overlap == 100
    assert etl.text_splitter is not None


def test_load_text_document(test_data_dir):
    """Test loading text documents"""
    etl = DocumentETL()
    
    # Load sample document
    sample_file = test_data_dir / "sample_doc1.txt"
    if sample_file.exists():
        documents = etl.load_document(sample_file)
        assert len(documents) > 0
        assert isinstance(documents[0], Document)
        assert len(documents[0].page_content) > 0


def test_load_directory(test_data_dir):
    """Test loading all documents from directory"""
    etl = DocumentETL()
    documents = etl.load_directory(test_data_dir)
    
    # Should load sample documents
    assert len(documents) > 0
    for doc in documents:
        assert isinstance(doc, Document)
        assert len(doc.page_content) > 0


def test_split_documents(test_data_dir):
    """Test document splitting"""
    etl = DocumentETL(chunk_size=500, chunk_overlap=100)
    
    # Load documents
    documents = etl.load_directory(test_data_dir)
    assert len(documents) > 0
    
    # Split documents
    chunks = etl.split_documents(documents)
    
    # Should create multiple chunks
    assert len(chunks) >= len(documents)
    
    # Check chunk sizes
    for chunk in chunks:
        assert isinstance(chunk, Document)
        # Chunks should be roughly the specified size
        assert len(chunk.page_content) <= etl.chunk_size * 1.5


def test_add_metadata(test_data_dir):
    """Test adding metadata to documents"""
    etl = DocumentETL()
    
    # Load documents
    documents = etl.load_directory(test_data_dir)
    assert len(documents) > 0
    
    # Add metadata
    metadata = {"category": "test", "version": "1.0"}
    updated_docs = etl.add_metadata(documents, metadata)
    
    # Check metadata was added
    for doc in updated_docs:
        assert "category" in doc.metadata
        assert doc.metadata["category"] == "test"
        assert "version" in doc.metadata
        assert doc.metadata["version"] == "1.0"


def test_process_directory(test_data_dir):
    """Test complete ETL process"""
    etl = DocumentETL(chunk_size=500, chunk_overlap=100)
    
    # Process directory
    chunks = etl.process_directory(
        directory=test_data_dir,
        metadata={"source": "test"}
    )
    
    # Should produce chunks
    assert len(chunks) > 0
    
    # Check metadata
    for chunk in chunks:
        assert isinstance(chunk, Document)
        assert "source" in chunk.metadata
        assert chunk.metadata["source"] == "test"


def test_unsupported_file_type():
    """Test handling of unsupported file types"""
    etl = DocumentETL()
    
    # Create a path to a non-existent file with unsupported extension
    fake_file = Path("/tmp/test.xyz")
    documents = etl.load_document(fake_file)
    
    # Should return empty list for unsupported type
    assert documents == []
