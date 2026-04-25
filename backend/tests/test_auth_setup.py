# tests/test_auth_setup.py
import pytest
from httpx import AsyncClient


class TestAuthSetup:
    """Verify that authentication mocking is working."""
    
    @pytest.mark.asyncio
    async def test_health_endpoint_works(self, client):
        """Health endpoint should work without auth."""
        response = await client.get("/health")
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_protected_endpoint_with_auth(self, client, auth_headers):
        """Protected endpoint should work with auth headers."""
        # This assumes you have at least one protected endpoint
        # Just testing that auth is being mocked correctly
        response = await client.get("/scan/history", headers=auth_headers)
        # Even if no data, should be 200, not 401
        assert response.status_code == 200