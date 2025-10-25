"""Test configuration"""
import pytest
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))


@pytest.fixture
def test_data_dir():
    """Fixture for test data directory"""
    return Path(__file__).parent.parent / "data"


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    Set up test environment variables.
    This fixture runs automatically for all tests.
    
    To run tests with a real API key, set GOOGLE_API_KEY before running pytest:
    export GOOGLE_API_KEY="your-key-here"
    """
    # Only set a dummy key if GOOGLE_API_KEY is not already set
    # This allows tests that require the real key to be skipped
    if not os.getenv("GOOGLE_API_KEY"):
        # Set an empty string to prevent initialization errors in tests
        # Tests that need a real key will still be skipped via @pytest.mark.skipif
        os.environ["GOOGLE_API_KEY"] = ""
