# tests/test_health_routes.py
import pytest
from httpx import AsyncClient


class TestHealthRoutes:
    """Tests for health check endpoints."""

    @pytest.mark.asyncio
    async def test_health_endpoint_returns_200(self, client: AsyncClient):
        """GET /health should return 200 OK."""
        # Act
        response = await client.get("/health")

        # Assert
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}