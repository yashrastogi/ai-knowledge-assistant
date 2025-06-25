"""Pydantic models for API requests and responses"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class QueryRequest(BaseModel):
    """Request model for query endpoint"""
    question: str = Field(..., description="The question to ask", min_length=1)
    k: int = Field(default=4, description="Number of documents to retrieve", ge=1, le=20)
    return_sources: bool = Field(default=True, description="Whether to return source documents")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question": "What is RAG?",
                    "k": 4,
                    "return_sources": True
                }
            ]
        }
    }


class SourceDocument(BaseModel):
    """Source document model"""
    content: str = Field(..., description="Full document content")
    preview: str = Field(..., description="Content preview")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Document metadata")


class QueryResponse(BaseModel):
    """Response model for query endpoint"""
    answer: str = Field(..., description="Generated answer")
    question: str = Field(..., description="Original question")
    success: bool = Field(..., description="Whether the query was successful")
    source_documents: Optional[List[SourceDocument]] = Field(
        default=None,
        description="Source documents used for answer"
    )
    error: Optional[str] = Field(default=None, description="Error message if applicable")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "answer": "RAG stands for Retrieval-Augmented Generation...",
                    "question": "What is RAG?",
                    "success": True,
                    "source_documents": [
                        {
                            "content": "RAG is a framework...",
                            "preview": "RAG is a framework...",
                            "metadata": {"source": "doc1.txt"}
                        }
                    ]
                }
            ]
        }
    }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Health status")


class StatusResponse(BaseModel):
    """Status response with service information"""
    status: str = Field(..., description="Overall status")
    services: Dict[str, str] = Field(..., description="Status of individual services")


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None, description="Detailed error information")
