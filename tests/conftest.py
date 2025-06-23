"""Test configuration"""
import pytest
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))


@pytest.fixture
def test_data_dir():
    """Fixture for test data directory"""
    return Path(__file__).parent.parent / "data"
