"""RAG chain implementation for Q&A"""
from typing import List, Optional, Dict, Any
import logging
from langchain.chains import RetrievalQA
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from retrieval import retrieval_service
from config import settings

logger = logging.getLogger(__name__)


class RAGChain:
    """RAG chain for question answering"""
    
    def __init__(self):
        """Initialize RAG chain"""
        self.llm: Optional[ChatOpenAI] = None
        self.chain: Optional[Any] = None
        self._initialized = False
    
    def initialize(self) -> None:
        """Initialize the RAG chain"""
        if self._initialized:
            logger.info("RAG chain already initialized")
            return
        
        logger.info("Initializing RAG chain...")
        
        try:
            # Check retrieval service
            if not retrieval_service.is_ready():
                raise RuntimeError("Retrieval service not ready")
            
            # Initialize LLM
            self.llm = ChatOpenAI(
                openai_api_key=settings.openai_api_key,
                model=settings.openai_model,
                temperature=0.7,
                streaming=False
            )
            
            # Create prompt template
            system_prompt = """You are an AI assistant helping users with questions based on a knowledge base.

Use the following pieces of context to answer the user's question. 
If you don't know the answer based on the context, say so - don't make up information.

Context:
{context}

Guidelines:
- Provide accurate, helpful answers based on the context
- Cite specific information from the documents when relevant
- If the context doesn't contain enough information, acknowledge it
- Be concise but comprehensive
- Use markdown formatting for better readability
"""
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "{input}")
            ])
            
            # Create document chain
            document_chain = create_stuff_documents_chain(
                llm=self.llm,
                prompt=prompt
            )
            
            # Create retrieval chain
            self.chain = create_retrieval_chain(
                retriever=retrieval_service.embedding_manager.vector_store.as_retriever(
                    search_kwargs={"k": 4}
                ),
                combine_docs_chain=document_chain
            )
            
            self._initialized = True
            logger.info("RAG chain initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing RAG chain: {e}")
            raise
    
    def is_ready(self) -> bool:
        """Check if chain is ready"""
        return self._initialized and self.chain is not None
    
    def query(
        self,
        question: str,
        k: int = 4,
        return_source_documents: bool = True
    ) -> Dict[str, Any]:
        """Query the RAG chain
        
        Args:
            question: User's question
            k: Number of documents to retrieve
            return_source_documents: Whether to return source documents
            
        Returns:
            Dictionary with answer and optional source documents
        """
        if not self.is_ready():
            raise RuntimeError("RAG chain not initialized")
        
        logger.info(f"Processing query: {question}")
        
        try:
            # Invoke chain
            result = self.chain.invoke({"input": question})
            
            # Extract answer and context
            answer = result.get("answer", "")
            context_docs = result.get("context", [])
            
            logger.info(f"Generated answer with {len(context_docs)} source documents")
            
            response = {
                "answer": answer,
                "question": question,
                "success": True
            }
            
            if return_source_documents and context_docs:
                response["source_documents"] = [
                    {
                        "content": doc.page_content,
                        "metadata": doc.metadata,
                        "preview": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                    }
                    for doc in context_docs
                ]
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "answer": "An error occurred while processing your question.",
                "question": question,
                "success": False,
                "error": str(e)
            }
    
    def stream_query(self, question: str, k: int = 4):
        """Stream response for query (for future implementation)"""
        # Placeholder for streaming implementation
        raise NotImplementedError("Streaming not yet implemented")


# Global RAG chain instance
rag_chain = RAGChain()
