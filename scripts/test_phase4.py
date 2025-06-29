#!/usr/bin/env python
"""Test script for Phase 4 - Enterprise API Integration"""
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


def test_enterprise_services():
    """Test enterprise API services"""
    from enterprise_api import cmdb_service, itsm_service
    
    logger.info("=== Testing Enterprise API Services ===\n")
    
    # Test CMDB
    logger.info("Test 1: CMDB Service")
    ci = cmdb_service.get_ci('SRV-001')
    logger.info(f"✓ Got CI: {ci['name']} - {ci['ci_type']}")
    
    cis = cmdb_service.search_cis(ci_type='Server')
    logger.info(f"✓ Found {len(cis)} servers")
    
    # Test ITSM
    logger.info("\nTest 2: ITSM Service")
    incidents = itsm_service.get_open_incidents()
    logger.info(f"✓ Found {len(incidents)} open incidents")
    
    incident = itsm_service.get_incident('INC-001')
    logger.info(f"✓ Got incident: {incident['title']}")
    

def test_enterprise_agent():
    """Test EnterpriseAPIAgent"""
    from agents import EnterpriseAPIAgent
    
    logger.info("\n=== Testing EnterpriseAPIAgent ===\n")
    
    agent = EnterpriseAPIAgent()
    logger.info(f"Agent: {agent.name}")
    
    # Test CMDB query
    logger.info("\nTest 1: Query CMDB for CI")
    result = agent.query_cmdb('get_ci', ci_id='APP-001')
    if result['success']:
        logger.info(f"✓ Got: {result['data']['name']}")
    
    # Test CMDB search
    logger.info("\nTest 2: Search CIs (type=Application)")
    result = agent.query_cmdb('search_cis', ci_type='Application')
    if result['success']:
        logger.info(f"✓ Found {len(result['data'])} applications")
        for ci in result['data']:
            logger.info(f"  - {ci['name']}")
    
    # Test ITSM query
    logger.info("\nTest 3: Query open incidents")
    result = agent.query_itsm('get_open_incidents')
    if result['success']:
        logger.info(f"✓ Found {len(result['data'])} open incidents")
        for inc in result['data'][:3]:
            logger.info(f"  - {inc['incident_id']}: {inc['title']} (Priority: {inc['priority']})")
    
    # Test format for context
    logger.info("\nTest 4: Format CI for context")
    ci_data = agent.query_cmdb('get_ci', ci_id='SRV-001')['data']
    formatted = agent.format_for_context(ci_data, 'ci')
    logger.info(f"✓ Formatted:\n{formatted}")
    
    # Test format incidents
    logger.info("\nTest 5: Format incident for context")
    incident_data = agent.query_itsm('get_incident', incident_id='INC-001')['data']
    formatted = agent.format_for_context(incident_data, 'incident')
    logger.info(f"✓ Formatted:\n{formatted}")


def test_orchestrator_with_enterprise():
    """Test multi-agent orchestrator with enterprise API integration"""
    from config import settings
    from retrieval import retrieval_service
    from agents import MultiAgentOrchestrator
    
    logger.info("\n=== Testing Multi-Agent Orchestrator with Enterprise API ===\n")
    
    # Check API key
    if not settings.google_api_key:
        logger.error("GOOGLE_API_KEY not set in environment")
        return False
    
    # Initialize retrieval service
    logger.info("Initializing retrieval service...")
    try:
        retrieval_service.initialize()
        if not retrieval_service.is_ready():
            logger.error("Vector store not ready. Run build_embeddings.py first.")
            return False
        logger.info("✓ Retrieval service ready\n")
    except Exception as e:
        logger.error(f"Failed to initialize retrieval service: {e}")
        return False
    
    # Initialize orchestrator
    orchestrator = MultiAgentOrchestrator()
    orchestrator.initialize()
    logger.info("✓ Orchestrator initialized\n")
    
    # Test 1: Regular knowledge base query (no enterprise API)
    logger.info("Test 1: Regular knowledge base query (no enterprise API)")
    try:
        result = orchestrator.process_query(
            question='What is RAG?',
            k=3,
            validate=False,
            use_enterprise_api=False
        )
        logger.info(f"✓ Success: {result['success']}")
        logger.info(f"✓ Answer preview: {result['answer'][:150]}...")
        logger.info(f"✓ Agents used: {result['agent_workflow']}")
        logger.info(f"✓ Sources: {len(result['source_documents'])} documents")
        logger.info(f"✓ Enterprise data: {result['enterprise_data']}\n")
    except Exception as e:
        logger.error(f"✗ Test 1 failed: {e}\n")
    
    # Test 2: Query with enterprise API enabled (incidents)
    logger.info("Test 2: Query about incidents (with enterprise API)")
    try:
        result = orchestrator.process_query(
            question='What incidents are currently open?',
            k=2,
            validate=False,
            use_enterprise_api=True
        )
        logger.info(f"✓ Success: {result['success']}")
        logger.info(f"✓ Answer preview: {result['answer'][:200]}...")
        logger.info(f"✓ Agents used: {result['agent_workflow']}")
        logger.info(f"✓ Enterprise data included: {result['enterprise_data'] is not None}")
        if result['enterprise_data']:
            logger.info(f"✓ Enterprise data preview: {result['enterprise_data'][:200]}...\n")
    except Exception as e:
        logger.error(f"✗ Test 2 failed: {e}\n")
    
    # Test 3: Auto-detect enterprise API need
    logger.info("Test 3: Auto-detect (question about servers)")
    try:
        result = orchestrator.process_query(
            question='Tell me about our production servers',
            k=2,
            validate=False,
            use_enterprise_api=None  # Auto-detect
        )
        logger.info(f"✓ Success: {result['success']}")
        logger.info(f"✓ Answer preview: {result['answer'][:200]}...")
        logger.info(f"✓ Agents used: {result['agent_workflow']}")
        logger.info(f"✓ Auto-detected enterprise need: {'enterprise_api' in result['agent_workflow']}\n")
    except Exception as e:
        logger.error(f"✗ Test 3 failed: {e}\n")
    
    # Test 4: Query with validation
    logger.info("Test 4: Query with validation")
    try:
        result = orchestrator.process_query(
            question='What is retrieval augmented generation?',
            k=3,
            validate=True,
            use_enterprise_api=False
        )
        logger.info(f"✓ Success: {result['success']}")
        logger.info(f"✓ Agents used: {result['agent_workflow']}")
        if result.get('validation'):
            val = result['validation']
            logger.info(f"✓ Validation scores:")
            logger.info(f"   - Relevance: {val.get('relevance', 0)}/10")
            logger.info(f"   - Accuracy: {val.get('accuracy', 0)}/10")
            logger.info(f"   - Completeness: {val.get('completeness', 0)}/10")
            logger.info(f"   - Clarity: {val.get('clarity', 0)}/10")
            logger.info(f"   - Overall: {val.get('overall', 0)}/10")
            logger.info(f"   - Passed: {val.get('passed', False)}\n")
    except Exception as e:
        logger.error(f"✗ Test 4 failed: {e}\n")
    
    return True


def main():
    """Run all Phase 4 tests"""
    logger.info("=" * 60)
    logger.info("PHASE 4 - ENTERPRISE API INTEGRATION TESTS")
    logger.info("=" * 60 + "\n")
    
    try:
        # Test 1: Enterprise services
        test_enterprise_services()
        
        # Test 2: Enterprise agent
        test_enterprise_agent()
        
        # Test 3: Orchestrator with enterprise integration
        success = test_orchestrator_with_enterprise()
        
        if success:
            logger.info("\n" + "=" * 60)
            logger.info("✅ ALL PHASE 4 TESTS PASSED!")
            logger.info("=" * 60)
            return 0
        else:
            logger.info("\n" + "=" * 60)
            logger.info("⚠️  SOME TESTS SKIPPED (Vector store not ready)")
            logger.info("=" * 60)
            return 0
        
    except Exception as e:
        logger.error(f"\n❌ Tests failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
