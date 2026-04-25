# tests/conftest.py (Alternative - if you have a verify_token function)
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import MagicMock, patch
from fastapi import Depends


class MockUser:
    def __init__(self, id, email, role, is_verified=True):
        self.id = id
        self.email = email
        self.role = role
        self.is_verified = is_verified


mock_regular_user = MockUser(123, "user@example.com", "user")
mock_admin_user = MockUser(1, "admin@example.com", "admin")


@pytest.fixture
async def client():
    """Async client for testing FastAPI backend.app."""
    from backend.app.main import app
    from backend.app.api.deps import get_current_user
    
    original_overrides = app.dependency_overrides.copy()
    
    async def mock_get_current_user():
        return mock_regular_user
    
    app.dependency_overrides[get_current_user] = mock_get_current_user
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides = original_overrides


@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer test_user_token"}


@pytest.fixture
def admin_headers():
    return {"Authorization": "Bearer test_admin_token"}


@pytest.fixture(autouse=True)
def mock_verify_token():
    """Mock the verify_token function in app.api.deps."""
    def mock_verify(token):
        if "admin" in token:
            return {"sub": "1", "is_admin": True}
        return {"sub": "123", "is_admin": False}
    
    with patch("app.api.deps._verify_token", side_effect=mock_verify):
        yield


@pytest.fixture(autouse=True)
def patch_route_get_current_user():
    """Patch get_current_user in all route modules."""
    async def mock_get_user_regular():
        return mock_regular_user
    
    async def mock_get_user_admin():
        return mock_admin_user
    
    with patch("app.api.routers.scan.get_current_user", new=mock_get_user_regular):
        with patch("app.api.routers.report.get_current_user", new=mock_get_user_regular):
            with patch("app.api.routers.admin.get_current_user", new=mock_get_user_admin):
                yield