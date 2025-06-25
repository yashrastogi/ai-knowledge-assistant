"""API routes for query endpoints"""
from fastapi import APIRouter, HTTPException, status
from models import QueryRequest, QueryResponse, ErrorResponse
from rag_chain import rag_chain
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["query"])


@router.post(
    "/query",
    response_model=QueryResponse,
    responses={
        200: {"description": "Successful query"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        503: {"model": ErrorResponse, "description": "Service unavailable"}
    }
)
async def query(request: QueryRequest) -> QueryResponse:
    """Query the knowledge base using RAG
    
    This endpoint processes natural language questions and returns answers
    based on the indexed knowledge base documents.
    
    Args:
        request: Query request containing the question and parameters
        
    Returns:
        Query response with answer and source documents
        
    Raises:
        HTTPException: If service is not ready or query fails
    """
    logger.info(f"Received query: {request.question}")
    
    # Check if RAG chain is ready
    if not rag_chain.is_ready():
        logger.error("RAG chain not initialized")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RAG service not ready. Please ensure vector store is initialized."
        )
    
    try:
        # Process query
        result = rag_chain.query(
            question=request.question,
            k=request.k,
            return_source_documents=request.return_sources
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Unknown error occurred")
            )
        
        # Convert to response model
        response = QueryResponse(
            answer=result["answer"],
            question=result["question"],
            success=result["success"],
            source_documents=result.get("source_documents"),
            error=result.get("error")
        )
        
        logger.info(f"Successfully processed query: {request.question}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )
