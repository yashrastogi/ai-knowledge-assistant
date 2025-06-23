"""Document loader utilities for ETL pipeline"""
from pathlib import Path
from typing import List, Dict, Any
import logging
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    CSVLoader,
    UnstructuredWordDocumentLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

logger = logging.getLogger(__name__)


class DocumentETL:
    """ETL pipeline for document ingestion"""
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        """Initialize document ETL
        
        Args:
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
    def load_document(self, file_path: Path) -> List[Document]:
        """Load a document based on file type
        
        Args:
            file_path: Path to document file
            
        Returns:
            List of loaded documents
        """
        suffix = file_path.suffix.lower()
        
        try:
            if suffix == '.txt' or suffix == '.md':
                loader = TextLoader(str(file_path), encoding='utf-8')
            elif suffix == '.pdf':
                loader = PyPDFLoader(str(file_path))
            elif suffix == '.csv':
                loader = CSVLoader(str(file_path))
            elif suffix == '.docx':
                loader = UnstructuredWordDocumentLoader(str(file_path))
            else:
                logger.warning(f"Unsupported file type: {suffix}")
                return []
            
            documents = loader.load()
            logger.info(f"Loaded {len(documents)} documents from {file_path.name}")
            return documents
            
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            return []
    
    def load_directory(self, directory: Path) -> List[Document]:
        """Load all documents from a directory
        
        Args:
            directory: Path to directory containing documents
            
        Returns:
            List of all loaded documents
        """
        all_documents = []
        supported_extensions = {'.txt', '.md', '.pdf', '.csv', '.docx'}
        
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                documents = self.load_document(file_path)
                all_documents.extend(documents)
        
        logger.info(f"Loaded {len(all_documents)} total documents from {directory}")
        return all_documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks
        
        Args:
            documents: List of documents to split
            
        Returns:
            List of document chunks
        """
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks")
        return chunks
    
    def add_metadata(
        self,
        documents: List[Document],
        metadata: Dict[str, Any]
    ) -> List[Document]:
        """Add metadata to documents
        
        Args:
            documents: List of documents
            metadata: Metadata to add
            
        Returns:
            Documents with added metadata
        """
        for doc in documents:
            doc.metadata.update(metadata)
        return documents
    
    def process_directory(
        self,
        directory: Path,
        metadata: Dict[str, Any] = None
    ) -> List[Document]:
        """Complete ETL process for a directory
        
        Args:
            directory: Path to directory containing documents
            metadata: Optional metadata to add to all documents
            
        Returns:
            Processed and chunked documents
        """
        logger.info(f"Starting ETL process for {directory}")
        
        # Load documents
        documents = self.load_directory(directory)
        
        if not documents:
            logger.warning("No documents loaded")
            return []
        
        # Split into chunks
        chunks = self.split_documents(documents)
        
        # Add metadata if provided
        if metadata:
            chunks = self.add_metadata(chunks, metadata)
        
        logger.info(f"ETL process complete: {len(chunks)} chunks ready")
        return chunks
