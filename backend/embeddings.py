"""Embedding and vector store management"""
from pathlib import Path
from typing import List, Optional, Dict, Any
import logging
import pickle
from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.vectorstores.base import VectorStore

logger = logging.getLogger(__name__)


class EmbeddingManager:
    """Manage embeddings and vector store"""
    
    def __init__(
        self,
        google_api_key: str,
        embedding_model: str = "models/embedding-001",
        vector_store_path: Optional[Path] = None
    ):
        """Initialize embedding manager
        
        Args:
            google_api_key: Google API key
            embedding_model: Name of embedding model
            vector_store_path: Path to save/load vector store
        """
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=embedding_model,
            google_api_key=google_api_key
        )
        self.vector_store_path = vector_store_path
        self.vector_store: Optional[VectorStore] = None
        
    def create_vector_store(
        self,
        documents: List[Document]
    ) -> FAISS:
        """Create vector store from documents
        
        Args:
            documents: List of documents to embed
            
        Returns:
            FAISS vector store
        """
        logger.info(f"Creating vector store from {len(documents)} documents")
        
        try:
            vector_store = FAISS.from_documents(
                documents=documents,
                embedding=self.embeddings
            )
            self.vector_store = vector_store
            logger.info("Vector store created successfully")
            return vector_store
            
        except Exception as e:
            logger.error(f"Error creating vector store: {e}")
            raise
    
    def add_documents(
        self,
        documents: List[Document]
    ) -> None:
        """Add documents to existing vector store
        
        Args:
            documents: List of documents to add
        """
        if self.vector_store is None:
            logger.warning("No vector store exists, creating new one")
            self.create_vector_store(documents)
            return
        
        logger.info(f"Adding {len(documents)} documents to vector store")
        try:
            self.vector_store.add_documents(documents)
            logger.info("Documents added successfully")
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise
    
    def save_vector_store(self, path: Optional[Path] = None) -> None:
        """Save vector store to disk
        
        Args:
            path: Optional path to save to (overrides initialized path)
        """
        if self.vector_store is None:
            logger.error("No vector store to save")
            return
        
        save_path = path or self.vector_store_path
        if save_path is None:
            logger.error("No save path specified")
            return
        
        save_path = Path(save_path)
        save_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Saving vector store to {save_path}")
        try:
            self.vector_store.save_local(str(save_path))
            logger.info("Vector store saved successfully")
        except Exception as e:
            logger.error(f"Error saving vector store: {e}")
            raise
    
    def load_vector_store(self, path: Optional[Path] = None) -> FAISS:
        """Load vector store from disk
        
        Args:
            path: Optional path to load from (overrides initialized path)
            
        Returns:
            Loaded FAISS vector store
        """
        load_path = path or self.vector_store_path
        if load_path is None:
            logger.error("No load path specified")
            raise ValueError("No load path specified")
        
        load_path = Path(load_path)
        if not load_path.exists():
            logger.error(f"Vector store not found at {load_path}")
            raise FileNotFoundError(f"Vector store not found at {load_path}")
        
        logger.info(f"Loading vector store from {load_path}")
        try:
            vector_store = FAISS.load_local(
                str(load_path),
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            self.vector_store = vector_store
            logger.info("Vector store loaded successfully")
            return vector_store
            
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            raise
    
    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """Perform similarity search
        
        Args:
            query: Query string
            k: Number of results to return
            filter: Optional metadata filter
            
        Returns:
            List of similar documents
        """
        if self.vector_store is None:
            logger.error("No vector store available")
            return []
        
        try:
            results = self.vector_store.similarity_search(
                query=query,
                k=k,
                filter=filter
            )
            logger.info(f"Found {len(results)} similar documents for query")
            return results
            
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            return []
    
    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[tuple[Document, float]]:
        """Perform similarity search with relevance scores
        
        Args:
            query: Query string
            k: Number of results to return
            filter: Optional metadata filter
            
        Returns:
            List of (document, score) tuples
        """
        if self.vector_store is None:
            logger.error("No vector store available")
            return []
        
        try:
            results = self.vector_store.similarity_search_with_score(
                query=query,
                k=k,
                filter=filter
            )
            logger.info(f"Found {len(results)} similar documents with scores")
            return results
            
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            return []


class HybridSearch:
    """Hybrid search combining semantic and keyword search"""
    
    def __init__(self, vector_store: VectorStore):
        """Initialize hybrid search
        
        Args:
            vector_store: Vector store for semantic search
        """
        self.vector_store = vector_store
    
    def search(
        self,
        query: str,
        k: int = 4,
        semantic_weight: float = 0.7
    ) -> List[Document]:
        """Perform hybrid search
        
        Args:
            query: Query string
            k: Number of results to return
            semantic_weight: Weight for semantic search (0-1)
            
        Returns:
            Combined search results
        """
        # Semantic search
        semantic_results = self.vector_store.similarity_search_with_score(
            query=query,
            k=k * 2  # Get more results for reranking
        )
        
        # Simple keyword matching (can be enhanced with BM25)
        keyword_results = self._keyword_search(query, k * 2)
        
        # Combine and rerank
        combined = self._combine_results(
            semantic_results,
            keyword_results,
            semantic_weight,
            k
        )
        
        return combined
    
    def _keyword_search(self, query: str, k: int) -> List[tuple[Document, float]]:
        """Simple keyword search (placeholder for BM25)"""
        # This is a simplified implementation
        # In production, use BM25 or similar
        return []
    
    def _combine_results(
        self,
        semantic: List[tuple[Document, float]],
        keyword: List[tuple[Document, float]],
        semantic_weight: float,
        k: int
    ) -> List[Document]:
        """Combine and rerank results"""
        # Simplified combination
        # In production, implement proper score normalization and fusion
        results = [doc for doc, score in semantic[:k]]
        return results
