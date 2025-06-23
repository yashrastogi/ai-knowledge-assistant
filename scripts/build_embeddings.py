#!/usr/bin/env python
"""Script to build embeddings from documents"""
import sys
from pathlib import Path
import logging

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from document_loader import DocumentETL
from embeddings import EmbeddingManager
from config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Build embeddings from documents"""
    # Paths
    data_dir = Path(__file__).parent.parent / "data"
    vector_store_path = Path(settings.vector_store_path)
    
    logger.info("=== Starting Embedding Pipeline ===")
    logger.info(f"Data directory: {data_dir}")
    logger.info(f"Vector store path: {vector_store_path}")
    
    # Check OpenAI API key
    if not settings.openai_api_key:
        logger.error("OPENAI_API_KEY not set in environment")
        sys.exit(1)
    
    try:
        # Initialize ETL
        etl = DocumentETL(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        # Process documents
        logger.info("Processing documents...")
        documents = etl.process_directory(
            directory=data_dir,
            metadata={"source": "knowledge_base"}
        )
        
        if not documents:
            logger.error("No documents processed")
            sys.exit(1)
        
        logger.info(f"Processed {len(documents)} document chunks")
        
        # Initialize embedding manager
        logger.info("Initializing embedding manager...")
        embedding_manager = EmbeddingManager(
            openai_api_key=settings.openai_api_key,
            embedding_model=settings.embedding_model,
            vector_store_path=vector_store_path
        )
        
        # Create vector store
        logger.info("Creating vector store (this may take a while)...")
        vector_store = embedding_manager.create_vector_store(documents)
        
        # Save vector store
        logger.info("Saving vector store...")
        embedding_manager.save_vector_store()
        
        logger.info("=== Embedding Pipeline Complete ===")
        logger.info(f"Vector store saved to: {vector_store_path}")
        logger.info(f"Total chunks embedded: {len(documents)}")
        
        # Test retrieval
        logger.info("\n=== Testing Retrieval ===")
        test_query = "What is RAG?"
        logger.info(f"Test query: {test_query}")
        
        results = embedding_manager.similarity_search(
            query=test_query,
            k=3
        )
        
        logger.info(f"Retrieved {len(results)} documents:")
        for i, doc in enumerate(results, 1):
            logger.info(f"\n--- Result {i} ---")
            logger.info(f"Content preview: {doc.page_content[:200]}...")
            logger.info(f"Metadata: {doc.metadata}")
        
    except Exception as e:
        logger.error(f"Error in embedding pipeline: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
