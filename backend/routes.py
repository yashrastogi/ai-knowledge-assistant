"""API routes for query endpoints"""
from fastapi import APIRouter, HTTPException, status
from models import QueryRequest, QueryResponse, ErrorResponse
from rag_chain import rag_chain
from agents import get_multi_agent_orchestrator
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
    
    Set `use_multi_agent=True` to use the multi-agent workflow with
    specialized retriever, synthesizer, and validator agents.
    
    Args:
        request: Query request containing the question and parameters
        
    Returns:
        Query response with answer and source documents
        
    Raises:
        HTTPException: If service is not ready or query fails
    """
    logger.info(f"Received query: {request.question} (multi-agent: {request.use_multi_agent})")
    
    try:
        # Use multi-agent workflow if requested
        if request.use_multi_agent:
            # Get multi-agent orchestrator
            orchestrator = get_multi_agent_orchestrator()
            
            # Check if multi-agent orchestrator is ready
            if not orchestrator.is_ready():
                logger.error("Multi-agent orchestrator not initialized")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Multi-agent service not ready. Please ensure vector store is initialized."
                )
            
            # Process with multi-agent workflow
            result = orchestrator.process_query(
                question=request.question,
                k=request.k,
                validate=request.validate_answer,
                use_enterprise_api=request.use_enterprise_api
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
                source_documents=result.get("source_documents") if request.return_sources else None,
                enterprise_data=result.get("enterprise_data"),
                validation=result.get("validation"),
                agent_workflow=result.get("agent_workflow"),
                warning=result.get("warning"),
                error=result.get("error")
            )
            
            logger.info(f"Successfully processed query with multi-agent workflow: {request.question}")
            return response
        
        # Use standard RAG chain
        else:
            # Check if RAG chain is ready
            if not rag_chain.is_ready():
                logger.error("RAG chain not initialized")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="RAG service not ready. Please ensure vector store is initialized."
                )
            
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
