from src.db.main import get_session
from src.auth.dependencies import RoleChecker,RefreshTokenBearer,AccessTokenBearer
from unittest.mock import Mock,AsyncMock
from fastapi.testclient import TestClient
from src import app
import pytest


mockSession=AsyncMock()
mock_user_service = AsyncMock()
mock_book_service=AsyncMock()

access_token_bearer=AccessTokenBearer()
refresh_token_bearer=RefreshTokenBearer()
rolecheck=RoleChecker(["admin"])

def get_mock_session():
    yield mockSession

# entirely over-ride the get_session dependency
app.dependency_overrides[get_session]=get_mock_session

app.dependency_overrides[access_token_bearer]=AsyncMock()
app.dependency_overrides[refresh_token_bearer]=AsyncMock()

 
@pytest.fixture
def fake_session():
    return mockSession

@pytest.fixture
def fake_user_service():
    return mock_user_service

@pytest.fixture
def fake_book_service():
    return mock_book_service

@pytest.fixture
def test_client():
    return TestClient(app)
