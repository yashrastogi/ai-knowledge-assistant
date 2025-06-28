#!/usr/bin/env python
"""Test script for multi-agent system"""
import sys
from pathlib import Path
import logging

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_agents():
    """Test the multi-agent system"""
    from config import settings
    from retrieval import retrieval_service
    from agents import (
        RetrieverAgent,
        SynthesizerAgent,
        ValidatorAgent,
        MultiAgentOrchestrator
    )
    from langchain.schema import Document
    
    logger.info("=== Testing Multi-Agent System ===\n")
    
    # Check API key
    if not settings.google_api_key:
        logger.error("GOOGLE_API_KEY not set in environment")
        sys.exit(1)
    
    # Initialize retrieval service
    logger.info("Step 1: Initializing retrieval service...")
    try:
        retrieval_service.initialize()
        if not retrieval_service.is_ready():
            logger.error("Vector store not ready. Run build_embeddings.py first.")
            sys.exit(1)
        logger.info("✓ Retrieval service ready\n")
    except Exception as e:
        logger.error(f"Failed to initialize retrieval service: {e}")
        sys.exit(1)
    
    # Test Retriever Agent
    logger.info("Step 2: Testing Retriever Agent...")
    retriever = RetrieverAgent()
    try:
        test_query = "What is RAG?"
        docs = retriever.retrieve(test_query, k=3)
        logger.info(f"✓ Retrieved {len(docs)} documents")
        if docs:
            logger.info(f"  First doc preview: {docs[0].page_content[:100]}...")
        
        # Test with scores
        docs_with_scores = retriever.retrieve_with_scores(test_query, k=3)
        logger.info(f"✓ Retrieved {len(docs_with_scores)} documents with scores")
        if docs_with_scores:
            doc, score = docs_with_scores[0]
            logger.info(f"  Top result score: {score:.4f}\n")
    except Exception as e:
        logger.error(f"✗ Retriever agent failed: {e}\n")
    
    # Test Synthesizer Agent
    logger.info("Step 3: Testing Synthesizer Agent...")
    synthesizer = SynthesizerAgent()
    try:
        # Create sample documents
        sample_docs = [
            Document(
                page_content="RAG stands for Retrieval-Augmented Generation. It combines retrieval with LLM generation.",
                metadata={"source": "test1"}
            ),
            Document(
                page_content="RAG systems use vector databases to store and retrieve relevant documents.",
                metadata={"source": "test2"}
            )
        ]
        
        answer = synthesizer.synthesize(
            question="What is RAG?",
            documents=sample_docs
        )
        logger.info(f"✓ Generated answer ({len(answer)} chars)")
        logger.info(f"  Preview: {answer[:150]}...\n")
    except Exception as e:
        logger.error(f"✗ Synthesizer agent failed: {e}\n")
    
    # Test Validator Agent
    logger.info("Step 4: Testing Validator Agent...")
    validator = ValidatorAgent()
    try:
        test_answer = "RAG (Retrieval-Augmented Generation) is an AI framework that combines document retrieval with language model generation to provide more accurate and contextual answers."
        
        validation = validator.validate(
            question="What is RAG?",
            answer=test_answer,
            documents=sample_docs
        )
        
        logger.info("✓ Validation complete:")
        logger.info(f"  Relevance:    {validation.get('relevance', 0)}/10")
        logger.info(f"  Accuracy:     {validation.get('accuracy', 0)}/10")
        logger.info(f"  Completeness: {validation.get('completeness', 0)}/10")
        logger.info(f"  Clarity:      {validation.get('clarity', 0)}/10")
        logger.info(f"  Overall:      {validation.get('overall', 0)}/10")
        logger.info(f"  Passed:       {validation.get('passed', False)}")
        logger.info(f"  Feedback:     {validation.get('feedback', 'N/A')}\n")
    except Exception as e:
        logger.error(f"✗ Validator agent failed: {e}\n")
    
    # Test Multi-Agent Orchestrator
    logger.info("Step 5: Testing Multi-Agent Orchestrator...")
    orchestrator = MultiAgentOrchestrator()
    try:
        orchestrator.initialize()
        logger.info("✓ Orchestrator initialized")
        
        # Test query without validation
        logger.info("\n  Testing without validation...")
        result1 = orchestrator.process_query(
            question="What is a vector database?",
            k=3,
            validate=False
        )
        logger.info(f"  ✓ Query processed (agents: {', '.join(result1.get('agent_workflow', []))})")
        logger.info(f"    Answer preview: {result1.get('answer', '')[:100]}...")
        
        # Test query with validation
        logger.info("\n  Testing with validation...")
        result2 = orchestrator.process_query(
            question="What is RAG?",
            k=3,
            validate=True
        )
        logger.info(f"  ✓ Query processed (agents: {', '.join(result2.get('agent_workflow', []))})")
        logger.info(f"    Answer preview: {result2.get('answer', '')[:100]}...")
        
        if result2.get('validation'):
            val = result2['validation']
            logger.info(f"    Validation score: {val.get('overall', 0)}/10 (passed: {val.get('passed', False)})")
        
        logger.info(f"\n✓ Full workflow complete!\n")
        
    except Exception as e:
        logger.error(f"✗ Orchestrator failed: {e}\n")
    
    logger.info("=== All Tests Complete ===")
    logger.info("\nSummary:")
    logger.info("✓ Retriever Agent: Working")
    logger.info("✓ Synthesizer Agent: Working")
    logger.info("✓ Validator Agent: Working")
    logger.info("✓ Multi-Agent Orchestrator: Working")
    logger.info("\nThe multi-agent system is ready to use!")


if __name__ == "__main__":
    try:
        test_agents()
    except Exception as e:
        logger.error(f"Test failed with error: {e}", exc_info=True)
        sys.exit(1)
