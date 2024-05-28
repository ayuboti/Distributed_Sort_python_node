# Inside tests/__init__.py
import pytest

# Define a pytest fixture that can be used across multiple test files
@pytest.fixture
def sample_fixture():
    return "Data needed for tests"
