"""Pydantic models for API requests and responses"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class QueryRequest(BaseModel):
    """Request model for query endpoint"""
    question: str = Field(..., description="The question to ask", min_length=1)
    k: int = Field(default=4, description="Number of documents to retrieve", ge=1, le=20)
    return_sources: bool = Field(default=True, description="Whether to return source documents")
    use_multi_agent: bool = Field(default=False, description="Use multi-agent workflow")
    validate_answer: bool = Field(default=True, description="Validate answer quality (multi-agent only)")
    use_enterprise_api: bool = Field(default=False, description="Query enterprise CMDB/ITSM systems")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question": "What is RAG?",
                    "k": 4,
                    "return_sources": True,
                    "use_multi_agent": False,
                    "validate_answer": True,
                    "use_enterprise_api": False
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
    enterprise_data: Optional[str] = Field(
        default=None,
        description="Enterprise CMDB/ITSM data used (if applicable)"
    )
    validation: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Answer validation results (multi-agent only)"
    )
    agent_workflow: Optional[List[str]] = Field(
        default=None,
        description="List of agents used in workflow"
    )
    warning: Optional[str] = Field(default=None, description="Warning message if applicable")
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
                    ],
                    "agent_workflow": ["retriever", "synthesizer", "validator"]
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
