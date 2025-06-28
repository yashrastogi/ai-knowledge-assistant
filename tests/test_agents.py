"""Test multi-agent system functionality"""
import pytest
from pathlib import Path
import sys
import os

backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from agents import (
    RetrieverAgent,
    SynthesizerAgent,
    ValidatorAgent,
    MultiAgentOrchestrator
)
from retrieval import retrieval_service
from langchain.schema import Document


pytestmark = pytest.mark.skipif(
    not os.getenv("GOOGLE_API_KEY"),
    reason="GOOGLE_API_KEY not set"
)


@pytest.fixture(scope="module")
def initialized_services():
    """Initialize services for testing"""
    try:
        retrieval_service.initialize()
        if not retrieval_service.is_ready():
            pytest.skip("Vector store not initialized - run build_embeddings.py first")
    except Exception as e:
        pytest.skip(f"Could not initialize services: {e}")
    
    return retrieval_service


@pytest.fixture
def sample_documents():
    """Sample documents for testing"""
    return [
        Document(
            page_content="RAG stands for Retrieval-Augmented Generation. It is an AI framework.",
            metadata={"source": "test1"}
        ),
        Document(
            page_content="Vector databases store embeddings for efficient similarity search.",
            metadata={"source": "test2"}
        )
    ]


def test_retriever_agent(initialized_services):
    """Test retriever agent"""
    agent = RetrieverAgent()
    
    assert agent.name == "Retriever"
    
    # Test retrieval
    results = agent.retrieve("What is RAG?", k=3)
    assert isinstance(results, list)


def test_retriever_agent_with_scores(initialized_services):
    """Test retriever agent with scores"""
    agent = RetrieverAgent()
    
    results = agent.retrieve_with_scores("What is RAG?", k=3)
    assert isinstance(results, list)
    
    if results:
        doc, score = results[0]
        assert isinstance(doc, Document)
        assert isinstance(score, float)


def test_synthesizer_agent(sample_documents):
    """Test synthesizer agent"""
    agent = SynthesizerAgent()
    
    assert agent.name == "Synthesizer"
    
    # Test synthesis
    answer = agent.synthesize(
        question="What is RAG?",
        documents=sample_documents
    )
    
    assert isinstance(answer, str)
    assert len(answer) > 0


def test_synthesizer_agent_empty_documents():
    """Test synthesizer with no documents"""
    agent = SynthesizerAgent()
    
    answer = agent.synthesize(
        question="What is RAG?",
        documents=[]
    )
    
    assert "No relevant information" in answer


def test_validator_agent(sample_documents):
    """Test validator agent"""
    agent = ValidatorAgent()
    
    assert agent.name == "Validator"
    
    # Test validation
    validation = agent.validate(
        question="What is RAG?",
        answer="RAG stands for Retrieval-Augmented Generation, an AI framework.",
        documents=sample_documents
    )
    
    assert isinstance(validation, dict)
    assert "relevance" in validation
    assert "accuracy" in validation
    assert "completeness" in validation
    assert "clarity" in validation
    assert "overall" in validation
    assert "feedback" in validation
    assert "passed" in validation


def test_multi_agent_orchestrator_initialization(initialized_services):
    """Test orchestrator initialization"""
    orchestrator = MultiAgentOrchestrator()
    
    assert not orchestrator.is_ready()
    
    orchestrator.initialize()
    
    assert orchestrator.is_ready()
    assert orchestrator.retriever is not None
    assert orchestrator.synthesizer is not None
    assert orchestrator.validator is not None


def test_multi_agent_process_query(initialized_services):
    """Test full multi-agent workflow"""
    orchestrator = MultiAgentOrchestrator()
    orchestrator.initialize()
    
    result = orchestrator.process_query(
        question="What is RAG?",
        k=3,
        validate=True
    )
    
    assert isinstance(result, dict)
    assert "question" in result
    assert "answer" in result
    assert "source_documents" in result
    assert "validation" in result
    assert "success" in result
    assert "agent_workflow" in result
    
    assert result["success"] is True
    assert len(result["answer"]) > 0
    assert "retriever" in result["agent_workflow"]
    assert "synthesizer" in result["agent_workflow"]
    assert "validator" in result["agent_workflow"]


def test_multi_agent_process_query_without_validation(initialized_services):
    """Test multi-agent workflow without validation"""
    orchestrator = MultiAgentOrchestrator()
    orchestrator.initialize()
    
    result = orchestrator.process_query(
        question="What is a vector database?",
        k=3,
        validate=False
    )
    
    assert result["success"] is True
    assert result["validation"] is None
    assert "validator" not in result["agent_workflow"]
    assert "retriever" in result["agent_workflow"]
    assert "synthesizer" in result["agent_workflow"]


def test_multi_agent_not_initialized():
    """Test query before initialization"""
    orchestrator = MultiAgentOrchestrator()
    
    with pytest.raises(RuntimeError):
        orchestrator.process_query("Test question")


def test_orchestrator_validation_scores(initialized_services):
    """Test validation scoring"""
    orchestrator = MultiAgentOrchestrator()
    orchestrator.initialize()
    
    result = orchestrator.process_query(
        question="What is RAG?",
        k=3,
        validate=True
    )
    
    if result.get("validation"):
        validation = result["validation"]
        assert 0 <= validation["relevance"] <= 10
        assert 0 <= validation["accuracy"] <= 10
        assert 0 <= validation["completeness"] <= 10
        assert 0 <= validation["clarity"] <= 10
        assert 0 <= validation["overall"] <= 10
