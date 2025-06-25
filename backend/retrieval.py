"""Retrieval service for RAG queries"""
from typing import List, Optional, Dict, Any
from pathlib import Path
import logging
from langchain.schema import Document
from embeddings import EmbeddingManager, HybridSearch
from config import settings

logger = logging.getLogger(__name__)


class RetrievalService:
    """Service for document retrieval"""
    
    def __init__(self):
        """Initialize retrieval service"""
        self.embedding_manager: Optional[EmbeddingManager] = None
        self.hybrid_search: Optional[HybridSearch] = None
        self._initialized = False
    
    def initialize(self) -> None:
        """Initialize the retrieval service"""
        if self._initialized:
            logger.info("Retrieval service already initialized")
            return
        
        logger.info("Initializing retrieval service...")
        
        try:
            # Initialize embedding manager
            self.embedding_manager = EmbeddingManager(
                google_api_key=settings.google_api_key,
                embedding_model=settings.embedding_model,
                vector_store_path=Path(settings.vector_store_path)
            )
            
            # Load vector store
            vector_store_path = Path(settings.vector_store_path)
            if vector_store_path.exists():
                self.embedding_manager.load_vector_store()
                logger.info("Vector store loaded successfully")
                
                # Initialize hybrid search
                self.hybrid_search = HybridSearch(
                    self.embedding_manager.vector_store
                )
                
                self._initialized = True
            else:
                logger.warning(
                    f"Vector store not found at {vector_store_path}. "
                    "Run scripts/build_embeddings.py first."
                )
                
        except Exception as e:
            logger.error(f"Error initializing retrieval service: {e}")
            raise
    
    def is_ready(self) -> bool:
        """Check if service is ready"""
        return self._initialized and self.embedding_manager is not None
    
    def retrieve(
        self,
        query: str,
        k: int = 4,
        use_hybrid: bool = False,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """Retrieve relevant documents
        
        Args:
            query: Query string
            k: Number of documents to retrieve
            use_hybrid: Whether to use hybrid search
            filter: Optional metadata filter
            
        Returns:
            List of relevant documents
        """
        if not self.is_ready():
            logger.error("Retrieval service not initialized")
            return []
        
        try:
            if use_hybrid and self.hybrid_search:
                logger.info(f"Performing hybrid search for: {query}")
                results = self.hybrid_search.search(query, k=k)
            else:
                logger.info(f"Performing semantic search for: {query}")
                results = self.embedding_manager.similarity_search(
                    query=query,
                    k=k,
                    filter=filter
                )
            
            logger.info(f"Retrieved {len(results)} documents")
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return []
    
    def retrieve_with_scores(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[tuple[Document, float]]:
        """Retrieve relevant documents with scores
        
        Args:
            query: Query string
            k: Number of documents to retrieve
            filter: Optional metadata filter
            
        Returns:
            List of (document, score) tuples
        """
        if not self.is_ready():
            logger.error("Retrieval service not initialized")
            return []
        
        try:
            logger.info(f"Performing search with scores for: {query}")
            results = self.embedding_manager.similarity_search_with_score(
                query=query,
                k=k,
                filter=filter
            )
            
            logger.info(f"Retrieved {len(results)} documents with scores")
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return []


# Global retrieval service instance
retrieval_service = RetrievalService()
