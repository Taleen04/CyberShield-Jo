# tests/test_report_routes.py
import pytest
from unittest.mock import patch, MagicMock
from httpx import AsyncClient
from fastapi import HTTPException
from datetime import datetime


class TestReportRoutes:
    """Tests for report submission endpoints."""

    @pytest.mark.asyncio
    async def test_report_from_scan_returns_201_when_valid(
        self, client: AsyncClient, auth_headers
    ):
        """POST /report/from-scan should return 201 for valid report from scan."""
        # Arrange
        payload = {
            "scan_id": 123,
            "notes": "This URL tried to steal my info"
        }
        
        mock_report = MagicMock()
        mock_report.id = 456
        mock_report.input_type = "url"
        mock_report.input_value = "https://suspicious-site.com"
        mock_report.notes = "This URL tried to steal my info"
        mock_report.scan_id = 123
        mock_report.status = "under_review"
        mock_report.created_at = datetime.now()

        # Act
        with patch("app.services.report_service.create_report_from_scan") as mock_create:
            mock_create.return_value = mock_report
            response = await client.post("/report/from-scan", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 456
        assert data["scan_id"] == 123
        assert data["status"] == "under_review"
        assert data["input_type"] == "url"

    @pytest.mark.asyncio
    async def test_report_from_scan_returns_422_when_scan_id_missing(
        self, client: AsyncClient, auth_headers
    ):
        """POST /report/from-scan should return 422 when scan_id is missing."""
        # Arrange
        payload = {"notes": "Some note"}

        # Act
        response = await client.post("/report/from-scan", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 422
        assert "detail" in response.json()

    @pytest.mark.asyncio
    async def test_report_from_scan_returns_404_when_scan_not_found(
        self, client: AsyncClient, auth_headers
    ):
        """POST /report/from-scan should return 404 when scan_id doesn't exist."""
        # Arrange
        payload = {"scan_id": 99999, "notes": "Some note"}

        # Act
        with patch("app.services.report_service.create_report_from_scan") as mock_create:
            mock_create.side_effect = HTTPException(status_code=404, detail="Scan not found")
            response = await client.post("/report/from-scan", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 404
        assert "Scan not found" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_report_from_scan_returns_409_when_duplicate_report(
        self, client: AsyncClient, auth_headers
    ):
        """POST /report/from-scan should return 409 when report already exists for this scan."""
        # Arrange
        payload = {"scan_id": 123, "notes": "Duplicate report"}

        # Act
        with patch("app.services.report_service.create_report_from_scan") as mock_create:
            mock_create.side_effect = HTTPException(status_code=409, detail="Report already exists for this scan")
            response = await client.post("/report/from-scan", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 409
        assert "Report already exists" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_report_from_scan_returns_403_when_no_auth(self, client: AsyncClient):
        """POST /report/from-scan should return 403 when no authentication provided."""
        # Arrange
        payload = {"scan_id": 123, "notes": "Some note"}

        # Act
        response = await client.post("/report/from-scan", json=payload)

        # Assert
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_report_manual_returns_201_when_valid_without_notes(
        self, client: AsyncClient, auth_headers
    ):
        """POST /report/manual should return 201 for valid manual report without notes."""
        # Arrange
        payload = {
            "input_type": "phone",
            "input_value": "+962799123456",
            "location_inside_jordan": True
        }
        
        mock_report = MagicMock()
        mock_report.id = 789
        mock_report.input_type = "phone"
        mock_report.input_value = "+962799123456"
        mock_report.notes = None
        mock_report.scan_id = None
        mock_report.status = "under_review"
        mock_report.created_at = datetime.now()

        # Act
        with patch("app.services.report_service.create_manual_report") as mock_create:
            mock_create.return_value = mock_report
            response = await client.post("/report/manual", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["input_type"] == "phone"
        assert data["input_value"] == "+962799123456"
        assert data["notes"] is None

    @pytest.mark.asyncio
    async def test_report_manual_returns_201_when_valid_with_notes(
        self, client: AsyncClient, auth_headers
    ):
        """POST /report/manual should return 201 for valid manual report with notes."""
        # Arrange
        payload = {
            "input_type": "url",
            "input_value": "https://malicious-site.com",
            "location_inside_jordan": False,
            "notes": "This site tried to phish my credentials"
        }
        
        mock_report = MagicMock()
        mock_report.id = 790
        mock_report.input_type = "url"
        mock_report.input_value = "https://malicious-site.com"
        mock_report.notes = "This site tried to phish my credentials"
        mock_report.scan_id = None
        mock_report.status = "under_review"
        mock_report.created_at = datetime.now()

        # Act
        with patch("app.services.report_service.create_manual_report") as mock_create:
            mock_create.return_value = mock_report
            response = await client.post("/report/manual", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["input_type"] == "url"
        assert data["notes"] == "This site tried to phish my credentials"

    @pytest.mark.asyncio
    async def test_report_manual_returns_422_when_input_type_invalid(
        self, client: AsyncClient, auth_headers
    ):
        """POST /report/manual should return 422 for invalid input_type."""
        # Arrange
        payload = {
            "input_type": "invalid_type",
            "input_value": "test",
            "location_inside_jordan": True
        }

        # Act
        response = await client.post("/report/manual", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_report_manual_returns_422_when_input_value_missing(
        self, client: AsyncClient, auth_headers
    ):
        """POST /report/manual should return 422 when input_value is missing."""
        # Arrange
        payload = {
            "input_type": "url",
            "location_inside_jordan": True
        }

        # Act
        response = await client.post("/report/manual", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_report_manual_returns_422_when_location_inside_jordan_missing(
        self, client: AsyncClient, auth_headers
    ):
        """POST /report/manual should return 422 when location_inside_jordan is missing."""
        # Arrange
        payload = {
            "input_type": "url",
            "input_value": "https://example.com"
        }

        # Act
        response = await client.post("/report/manual", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_report_manual_returns_409_when_duplicate_report(
        self, client: AsyncClient, auth_headers
    ):
        """POST /report/manual should return 409 when duplicate report exists."""
        # Arrange
        payload = {
            "input_type": "url",
            "input_value": "https://already-reported.com",
            "location_inside_jordan": True
        }

        # Act
        with patch("app.services.report_service.create_manual_report") as mock_create:
            mock_create.side_effect = HTTPException(status_code=409, detail="Report already exists")
            response = await client.post("/report/manual", json=payload, headers=auth_headers)

        # Assert
        assert response.status_code == 409

    @pytest.mark.asyncio
    async def test_report_manual_returns_403_when_no_auth(self, client: AsyncClient):
        """POST /report/manual should return 403 when no authentication provided."""
        # Arrange
        payload = {
            "input_type": "url",
            "input_value": "https://example.com",
            "location_inside_jordan": True
        }

        # Act
        response = await client.post("/report/manual", json=payload)

        # Assert
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_my_reports_returns_200_with_empty_list(
        self, client: AsyncClient, auth_headers
    ):
        """GET /report/my-reports should return 200 with empty list when no reports."""
        # Act
        with patch("app.services.report_service.get_user_reports") as mock_get:
            mock_get.return_value = []
            response = await client.get("/report/my-reports", headers=auth_headers)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data == []

    @pytest.mark.asyncio
    async def test_my_reports_returns_200_with_reports_list(
        self, client: AsyncClient, auth_headers
    ):
        """GET /report/my-reports should return 200 with user's reports."""
        # Arrange
        mock_reports = [
            MagicMock(
                id=1,
                input_type="url",
                input_value="https://example1.com",
                created_at=datetime(2026, 4, 23, 10, 0, 0),
                status="under_review"
            ),
            MagicMock(
                id=2,
                input_type="phone",
                input_value="+962799123456",
                created_at=datetime(2026, 4, 22, 15, 30, 0),
                status="verified_scam"
            ),
            MagicMock(
                id=3,
                input_type="text_message",
                input_value="Suspicious SMS content",
                created_at=datetime(2026, 4, 21, 9, 15, 0),
                status="safe"
            )
        ]

        # Act
        with patch("app.services.report_service.get_user_reports") as mock_get:
            mock_get.return_value = mock_reports
            response = await client.get("/report/my-reports", headers=auth_headers)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["id"] == 1
        assert data[0]["input_type"] == "url"
        assert data[0]["status"] == "under_review"
        assert data[1]["input_type"] == "phone"
        assert data[2]["input_type"] == "text_message"

    @pytest.mark.asyncio
    async def test_my_reports_returns_403_when_no_auth(self, client: AsyncClient):
        """GET /report/my-reports should return 403 when no authentication provided."""
        # Act
        response = await client.get("/report/my-reports")

        # Assert
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_my_reports_returns_correct_response_structure(
        self, client: AsyncClient, auth_headers
    ):
        """GET /report/my-reports should return correct schema structure."""
        # Arrange
        mock_report = MagicMock()
        mock_report.id = 1
        mock_report.input_type = "url"
        mock_report.input_value = "https://example.com"
        mock_report.created_at = datetime(2026, 4, 23, 10, 0, 0)
        mock_report.status = "under_review"

        # Act
        with patch("app.services.report_service.get_user_reports") as mock_get:
            mock_get.return_value = [mock_report]
            response = await client.get("/report/my-reports", headers=auth_headers)

        # Assert
        assert response.status_code == 200
        data = response.json()[0]
        expected_fields = {"id", "input_type", "input_value", "created_at", "status"}
        assert expected_fields.issubset(data.keys())
        assert isinstance(data["id"], int)
        assert isinstance(data["input_type"], str)
        assert isinstance(data["input_value"], str)
        assert isinstance(data["created_at"], str)
        assert isinstance(data["status"], str)