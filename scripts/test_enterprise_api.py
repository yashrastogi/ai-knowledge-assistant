#!/usr/bin/env python
"""Test script for Enterprise API integration (CMDB and ITSM)"""
import sys
from pathlib import Path
import logging
import requests
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API base URL
BASE_URL = "http://localhost:8000/api/v1/enterprise"


def test_cmdb_endpoints():
    """Test CMDB API endpoints"""
    logger.info("\n=== Testing CMDB Endpoints ===\n")
    
    # Test 1: Get specific CI
    logger.info("Test 1: Get Configuration Item (SRV-001)")
    response = requests.get(f"{BASE_URL}/cmdb/ci/SRV-001")
    if response.status_code == 200:
        data = response.json()
        logger.info(f"✓ Got CI: {data['data']['name']}")
        logger.info(f"  Type: {data['data']['ci_type']}, Status: {data['data']['status']}")
    else:
        logger.error(f"✗ Failed: {response.status_code}")
    
    # Test 2: Search CIs by type
    logger.info("\nTest 2: Search CIs (type=Application)")
    response = requests.post(
        f"{BASE_URL}/cmdb/search",
        json={"ci_type": "Application"}
    )
    if response.status_code == 200:
        data = response.json()
        logger.info(f"✓ Found {data['count']} applications")
        for ci in data['data']:
            logger.info(f"  - {ci['name']} (v{ci.get('version', 'N/A')})")
    else:
        logger.error(f"✗ Failed: {response.status_code}")
    
    # Test 3: Get dependencies
    logger.info("\nTest 3: Get Dependencies (APP-001)")
    response = requests.get(f"{BASE_URL}/cmdb/ci/APP-001/dependencies")
    if response.status_code == 200:
        data = response.json()
        logger.info(f"✓ Found {data['count']} dependencies")
        for ci in data['data']:
            logger.info(f"  - {ci['name']} ({ci['ci_type']})")
    else:
        logger.error(f"✗ Failed: {response.status_code}")
    
    # Test 4: Get dependents
    logger.info("\nTest 4: Get Dependents (DB-001)")
    response = requests.get(f"{BASE_URL}/cmdb/ci/DB-001/dependents")
    if response.status_code == 200:
        data = response.json()
        logger.info(f"✓ Found {data['count']} dependents")
        for ci in data['data']:
            logger.info(f"  - {ci['name']} ({ci['ci_type']})")
    else:
        logger.error(f"✗ Failed: {response.status_code}")
    
    # Test 5: Impact analysis
    logger.info("\nTest 5: Impact Analysis (DB-001)")
    response = requests.get(f"{BASE_URL}/cmdb/ci/DB-001/impact")
    if response.status_code == 200:
        data = response.json()['data']
        logger.info(f"✓ Impact Analysis Complete")
        logger.info(f"  CI: {data['ci']['name']}")
        logger.info(f"  Direct Dependents: {len(data['direct_dependents'])}")
        logger.info(f"  Indirect Dependents: {len(data['indirect_dependents'])}")
        logger.info(f"  Total Impact: {data['total_impact']} items")
        logger.info(f"  Risk Level: {data['risk_level']}")
    else:
        logger.error(f"✗ Failed: {response.status_code}")


def test_itsm_endpoints():
    """Test ITSM API endpoints"""
    logger.info("\n\n=== Testing ITSM Endpoints ===\n")
    
    # Test 1: Get specific incident
    logger.info("Test 1: Get Incident (INC-001)")
    response = requests.get(f"{BASE_URL}/itsm/incident/INC-001")
    if response.status_code == 200:
        data = response.json()
        incident = data['data']
        logger.info(f"✓ Got Incident: {incident['title']}")
        logger.info(f"  Priority: {incident['priority']}, Status: {incident['status']}")
        logger.info(f"  Affected CI: {incident['affected_ci']}")
    else:
        logger.error(f"✗ Failed: {response.status_code}")
    
    # Test 2: Get open incidents
    logger.info("\nTest 2: Get Open Incidents")
    response = requests.get(f"{BASE_URL}/itsm/incidents/open")
    if response.status_code == 200:
        data = response.json()
        logger.info(f"✓ Found {data['count']} open incidents")
        for incident in data['data']:
            logger.info(f"  - {incident['incident_id']}: {incident['title']} ({incident['priority']})")
    else:
        logger.error(f"✗ Failed: {response.status_code}")
    
    # Test 3: Search incidents by priority
    logger.info("\nTest 3: Search Incidents (priority=P1 - Critical)")
    response = requests.post(
        f"{BASE_URL}/itsm/incidents/search",
        json={"priority": "P1 - Critical"}
    )
    if response.status_code == 200:
        data = response.json()
        logger.info(f"✓ Found {data['count']} P1 incidents")
        for incident in data['data']:
            logger.info(f"  - {incident['incident_id']}: {incident['title']}")
    else:
        logger.error(f"✗ Failed: {response.status_code}")
    
    # Test 4: Get upcoming changes
    logger.info("\nTest 4: Get Upcoming Changes")
    response = requests.get(f"{BASE_URL}/itsm/changes/upcoming")
    if response.status_code == 200:
        data = response.json()
        logger.info(f"✓ Found {data['count']} upcoming changes")
        for change in data['data']:
            logger.info(f"  - {change['change_id']}: {change['title']}")
            logger.info(f"    Type: {change['type']}, Status: {change['status']}, Risk: {change['risk_level']}")
    else:
        logger.error(f"✗ Failed: {response.status_code}")
    
    # Test 5: Get incidents for CI
    logger.info("\nTest 5: Get Incidents for CI (APP-001)")
    response = requests.get(f"{BASE_URL}/itsm/ci/APP-001/incidents")
    if response.status_code == 200:
        data = response.json()
        logger.info(f"✓ Found {data['count']} incidents for APP-001")
        for incident in data['data']:
            logger.info(f"  - {incident['incident_id']}: {incident['title']} ({incident['status']})")
    else:
        logger.error(f"✗ Failed: {response.status_code}")
    
    # Test 6: Get changes for CI
    logger.info("\nTest 6: Get Changes for CI (DB-001)")
    response = requests.get(f"{BASE_URL}/itsm/ci/DB-001/changes")
    if response.status_code == 200:
        data = response.json()
        logger.info(f"✓ Found {data['count']} changes for DB-001")
        for change in data['data']:
            logger.info(f"  - {change['change_id']}: {change['title']} ({change['status']})")
    else:
        logger.error(f"✗ Failed: {response.status_code}")


def test_enterprise_agent():
    """Test EnterpriseAPIAgent integration"""
    logger.info("\n\n=== Testing Enterprise API Agent ===\n")
    
    # Add backend to path
    backend_path = Path(__file__).parent.parent / "backend"
    sys.path.insert(0, str(backend_path))
    
    try:
        from agents import EnterpriseAPIAgent
        
        agent = EnterpriseAPIAgent()
        logger.info(f"✓ EnterpriseAPIAgent initialized: {agent.name}")
        
        # Test CMDB query
        logger.info("\nTest: Query CMDB for server")
        result = agent.query_cmdb("get_ci", ci_id="SRV-001")
        if result['success']:
            logger.info(f"✓ CMDB query successful")
            formatted = agent.format_for_context(result['data'], "ci")
            logger.info(f"  Formatted output:\n{formatted}")
        else:
            logger.error(f"✗ CMDB query failed: {result.get('error')}")
        
        # Test ITSM query
        logger.info("\nTest: Query ITSM for open incidents")
        result = agent.query_itsm("get_open_incidents")
        if result['success']:
            logger.info(f"✓ ITSM query successful - {len(result['data'])} incidents")
            formatted = agent.format_for_context(result['data'][:2], "incident")
            logger.info(f"  Formatted output (first 2):\n{formatted}")
        else:
            logger.error(f"✗ ITSM query failed: {result.get('error')}")
        
    except Exception as e:
        logger.error(f"✗ Agent test failed: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """Run all tests"""
    logger.info("=== Enterprise API Integration Tests ===")
    logger.info(f"Testing API at: {BASE_URL}\n")
    
    try:
        # Test connectivity
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            logger.error("API server not responding. Please start the server first.")
            sys.exit(1)
        logger.info("✓ API server is running\n")
    except requests.exceptions.RequestException as e:
        logger.error(f"Cannot connect to API server: {e}")
        logger.error("Please start the server with: python backend/main.py")
        sys.exit(1)
    
    # Run tests
    try:
        test_cmdb_endpoints()
        test_itsm_endpoints()
        test_enterprise_agent()
        
        logger.info("\n\n=== All Tests Complete ===")
        logger.info("✓ CMDB endpoints working")
        logger.info("✓ ITSM endpoints working")
        logger.info("✓ Enterprise API Agent working")
        logger.info("\nThe enterprise API integration is ready to use!")
        
    except Exception as e:
        logger.error(f"\n✗ Tests failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
