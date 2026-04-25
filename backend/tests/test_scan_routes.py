# tests/test_scan_routes.py
import pytest
from unittest.mock import patch, MagicMock
from httpx import AsyncClient
from datetime import datetime


class TestScanRoutes:
    """Tests for scan analysis endpoints."""

    @pytest.mark.asyncio
    async def test_scan_url_returns_200_when_valid_input(
        self, client: AsyncClient, auth_headers
    ):
        print(f"Auth headers: {auth_headers}")
        """POST /scan/url should return 200 for valid URL input."""
        # Arrange
        payload = {"url": "https://example.com"}
        mock_result = {
            "scan_id": 123,
            "final_category": "safe",
            "ml_risk_score": 0.05,
            "ml_probabilities": None,
            "explanation": "URL appears safe",
            "contributing_factors": ["community_db"],
            "analysis_details": {}
        }

        # Act
        with patch("app.services.scan_service.analyze_url") as mock_analyze:
            mock_analyze.return_value = mock_result
            response = await client.post("/scan/url", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["scan_id"] == 123
        assert data["final_category"] == "safe"
        assert data["ml_risk_score"] == 0.05
        assert data["explanation"] == "URL appears safe"

    @pytest.mark.asyncio
    async def test_scan_url_returns_403_when_no_auth(self, client: AsyncClient):
        """POST /scan/url should return 403 when no authentication provided."""
        # Arrange
        payload = {"url": "https://example.com"}

        # Act
        response = await client.post("/scan/url", json=payload)

        # Assert
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_scan_url_returns_422_when_missing_url(self, client: AsyncClient, auth_headers):
        """POST /scan/url should return 422 when URL field is missing."""
        # Arrange
        payload = {}

        # Act
        response = await client.post("/scan/url", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 422
        assert "detail" in response.json()

    @pytest.mark.asyncio
    async def test_scan_url_returns_422_when_invalid_url_format(self, client: AsyncClient, auth_headers):
        """POST /scan/url should return 422 for invalid URL format."""
        # Arrange
        payload = {"url": "not-a-url"}

        # Act
        response = await client.post("/scan/url", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_scan_url_returns_400_when_url_empty(self, client: AsyncClient, auth_headers):
        """POST /scan/url should return 422 when URL is empty string."""
        # Arrange
        payload = {"url": ""}

        # Act
        response = await client.post("/scan/url", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_scan_text_returns_200_when_valid_input_with_phone(
        self, client: AsyncClient, auth_headers
    ):
        """POST /scan/text should return 200 for valid text input with phone number."""
        # Arrange
        payload = {
            "message": "Congratulations! You've won a prize!",
            "phone_number": "+1234567890"
        }
        mock_result = {
            "scan_id": 456,
            "final_category": "suspicious",
            "ml_risk_score": 0.75,
            "ml_probabilities": {"spam": 0.75, "safe": 0.25},
            "explanation": "Suspicious content detected",
            "contributing_factors": ["ml_model", "url_extraction"],
            "analysis_details": {"ml_confidence": 0.75}
        }

        # Act
        with patch("app.services.scan_service.analyze_text") as mock_analyze:
            mock_analyze.return_value = mock_result
            response = await client.post("/scan/text", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["scan_id"] == 456
        assert data["final_category"] == "suspicious"
        assert data["ml_risk_score"] == 0.75

    @pytest.mark.asyncio
    async def test_scan_text_returns_200_when_only_message_provided(
        self, client: AsyncClient, auth_headers
    ):
        """POST /scan/text should work with only required message field."""
        # Arrange
        payload = {"message": "Test message"}
        mock_result = {
            "scan_id": 456,
            "final_category": "safe",
            "ml_risk_score": 0.01,
            "ml_probabilities": None,
            "explanation": "No threats detected",
            "contributing_factors": ["ml_model"],
            "analysis_details": {}
        }

        # Act
        with patch("app.services.scan_service.analyze_text") as mock_analyze:
            mock_analyze.return_value = mock_result
            response = await client.post("/scan/text", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["final_category"] == "safe"

    @pytest.mark.asyncio
    async def test_scan_text_returns_200_with_high_risk_arabic_message(
        self, client: AsyncClient, auth_headers
    ):
        """POST /scan/text should handle Arabic messages correctly."""
        # Arrange
        payload = {"message": "لقد فزت بجائزة! انقر هنا http://scam.com"}
        mock_result = {
            "scan_id": 457,
            "final_category": "high_risk",
            "ml_risk_score": 0.95,
            "ml_probabilities": None,
            "explanation": "High risk Arabic phishing content detected",
            "contributing_factors": ["ml_model", "url_extraction"],
            "analysis_details": {}
        }

        # Act
        with patch("app.services.scan_service.analyze_text") as mock_analyze:
            mock_analyze.return_value = mock_result
            response = await client.post("/scan/text", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["final_category"] == "high_risk"

    @pytest.mark.asyncio
    async def test_scan_text_returns_422_when_missing_message(self, client: AsyncClient, auth_headers):
        """POST /scan/text should return 422 when message field is missing."""
        # Arrange
        payload = {"phone_number": "+1234567890"}

        # Act
        response = await client.post("/scan/text", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_scan_text_returns_422_when_message_empty(self, client: AsyncClient, auth_headers):
        """POST /scan/text should return 422 when message is empty."""
        # Arrange
        payload = {"message": ""}

        # Act
        response = await client.post("/scan/text", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_scan_text_returns_422_when_message_too_long(self, client: AsyncClient, auth_headers):
        """POST /scan/text should return 422 when message exceeds max length (2000)."""
        # Arrange
        payload = {"message": "x" * 2001}

        # Act
        response = await client.post("/scan/text", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_scan_phone_returns_200_when_valid_input(
        self, client: AsyncClient, auth_headers
    ):
        """POST /scan/phone should return 200 for valid phone number."""
        # Arrange
        payload = {"phone_number": "+962799123456"}
        mock_result = {
            "scan_id": 789,
            "final_category": "high_risk",
            "ml_risk_score": None,
            "ml_probabilities": None,
            "explanation": "Number reported as spam by 50+ users",
            "contributing_factors": ["community_reports"],
            "analysis_details": {"report_count": 50, "spam_rate": 0.8}
        }

        # Act
        with patch("app.services.scan_service.analyze_phone") as mock_analyze:
            mock_analyze.return_value = mock_result
            response = await client.post("/scan/phone", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["scan_id"] == 789
        assert data["final_category"] == "high_risk"

    @pytest.mark.asyncio
    async def test_scan_phone_returns_200_with_no_data(
        self, client: AsyncClient, auth_headers
    ):
        """POST /scan/phone should return 'no_data' category when number never reported."""
        # Arrange
        payload = {"phone_number": "+962799999999"}
        mock_result = {
            "scan_id": 790,
            "final_category": "no_data",
            "ml_risk_score": None,
            "ml_probabilities": None,
            "explanation": "No community data available for this number",
            "contributing_factors": [],
            "analysis_details": {}
        }

        # Act
        with patch("app.services.scan_service.analyze_phone") as mock_analyze:
            mock_analyze.return_value = mock_result
            response = await client.post("/scan/phone", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["final_category"] == "no_data"

    @pytest.mark.asyncio
    async def test_scan_phone_returns_422_when_missing_phone_number(self, client: AsyncClient, auth_headers):
        """POST /scan/phone should return 422 when phone_number field is missing."""
        # Arrange
        payload = {}

        # Act
        response = await client.post("/scan/phone", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_scan_phone_returns_422_when_invalid_phone_format(self, client: AsyncClient, auth_headers):
        """POST /scan/phone should return 422 for invalid phone format."""
        # Arrange
        payload = {"phone_number": "invalid-phone"}

        # Act
        response = await client.post("/scan/phone", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_scan_phone_returns_422_when_phone_number_empty(self, client: AsyncClient, auth_headers):
        """POST /scan/phone should return 422 when phone_number is empty."""
        # Arrange
        payload = {"phone_number": ""}

        # Act
        response = await client.post("/scan/phone", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_scan_history_returns_200_with_pagination(
        self, client: AsyncClient, auth_headers
    ):
        """GET /scan/history should return 200 with paginated results."""
        # Arrange
        mock_response = {
            "total": 50,
            "page": 1,
            "page_size": 10,
            "items": [
                {
                    "id": 1,
                    "input_type": "url",
                    "input_value": "https://example.com",
                    "threat_category": "safe",
                    "created_at": "2026-04-23T10:00:00Z"
                },
                {
                    "id": 2,
                    "input_type": "phone",
                    "input_value": "+962799123456",
                    "threat_category": "high_risk",
                    "created_at": "2026-04-22T15:30:00Z"
                }
            ]
        }

        # Act
        with patch("app.services.scan_service.get_user_scan_history") as mock_history:
            mock_history.return_value = mock_response
            response = await client.get("/scan/history?page=1&page_size=10", headers=auth_headers)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 50
        assert data["page"] == 1
        assert data["page_size"] == 10
        assert len(data["items"]) == 2
        assert data["items"][0]["id"] == 1
        assert data["items"][0]["threat_category"] == "safe"

    @pytest.mark.asyncio
    async def test_scan_history_uses_default_values(
        self, client: AsyncClient, auth_headers
    ):
        """GET /scan/history should use default page=1 and page_size=10 when not provided."""
        # Arrange
        mock_response = {
            "total": 0,
            "page": 1,
            "page_size": 10,
            "items": []
        }

        # Act
        with patch("app.services.scan_service.get_user_scan_history") as mock_history:
            mock_history.return_value = mock_response
            response = await client.get("/scan/history", headers=auth_headers)

        # Assert
        assert response.status_code == 200
        mock_history.assert_called_once_with(
            db=mock_history.call_args[1]["db"],
            user_id=123,
            page=1,
            page_size=10
        )

    @pytest.mark.asyncio
    async def test_scan_history_returns_422_when_page_size_exceeds_max(
        self, client: AsyncClient, auth_headers
    ):
        """GET /scan/history should return 422 when page_size exceeds max limit (50)."""
        # Act
        response = await client.get("/scan/history?page=1&page_size=100", headers=auth_headers)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_scan_history_returns_422_when_page_less_than_min(
        self, client: AsyncClient, auth_headers
    ):
        """GET /scan/history should return 422 when page is less than minimum (1)."""
        # Act
        response = await client.get("/scan/history?page=0&page_size=10", headers=auth_headers)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_scan_history_returns_422_when_page_size_less_than_min(
        self, client: AsyncClient, auth_headers
    ):
        """GET /scan/history should return 422 when page_size is less than minimum (1)."""
        # Act
        response = await client.get("/scan/history?page=1&page_size=0", headers=auth_headers)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_scan_history_returns_empty_list_when_no_scans(
        self, client: AsyncClient, auth_headers
    ):
        """GET /scan/history should return empty items array when user has no scans."""
        # Arrange
        mock_response = {
            "total": 0,
            "page": 1,
            "page_size": 10,
            "items": []
        }

        # Act
        with patch("app.services.scan_service.get_user_scan_history") as mock_history:
            mock_history.return_value = mock_response
            response = await client.get("/scan/history", headers=auth_headers)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []

    @pytest.mark.asyncio
    async def test_scan_history_returns_403_when_no_auth(self, client: AsyncClient):
        """GET /scan/history should return 403 when no authentication provided."""
        # Act
        response = await client.get("/scan/history")

        # Assert
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_scan_history_correct_response_structure(
        self, client: AsyncClient, auth_headers
    ):
        """GET /scan/history should return correct schema structure."""
        # Arrange
        mock_response = {
            "total": 1,
            "page": 1,
            "page_size": 10,
            "items": [
                {
                    "id": 1,
                    "input_type": "url",
                    "input_value": "https://example.com",
                    "threat_category": "safe",
                    "created_at": "2026-04-23T10:00:00Z"
                }
            ]
        }

        # Act
        with patch("app.services.scan_service.get_user_scan_history") as mock_history:
            mock_history.return_value = mock_response
            response = await client.get("/scan/history", headers=auth_headers)

        # Assert
        assert response.status_code == 200
        data = response.json()
        expected_fields = {"total", "page", "page_size", "items"}
        assert expected_fields.issubset(data.keys())
        assert isinstance(data["total"], int)
        assert isinstance(data["page"], int)
        assert isinstance(data["page_size"], int)
        assert isinstance(data["items"], list)
        
        item = data["items"][0]
        item_fields = {"id", "input_type", "input_value", "threat_category", "created_at"}
        assert item_fields.issubset(item.keys())