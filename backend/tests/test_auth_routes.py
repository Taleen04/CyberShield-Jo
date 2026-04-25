# tests/test_auth_routers.py
import pytest
from unittest.mock import patch, MagicMock
from httpx import AsyncClient
from fastapi import HTTPException

class TestAuthRoutes:
    """Tests for authentication endpoints."""

    @pytest.mark.asyncio
    async def test_register_returns_200_when_valid_input(self, client: AsyncClient):
        """POST /auth/register should return 200 for valid registration."""
        # Arrange
        payload = {
            "email": "newuser@example.com",
            "password": "SecurePass123!"
        }
        
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "newuser@example.com"
        mock_user.is_verified = False
        mock_user.created_at = "2026-04-23T10:00:00Z"

        # Act
        with patch("app.api.routers.auth.register_user") as mock_register:
            with patch("app.api.routers.auth.send_verification_email") as mock_send_email:
                mock_register.return_value = (mock_user, "verification_token")
                response = await client.post("/auth/register", json=payload)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Registration successful"
        assert data["user"]["email"] == "newuser@example.com"
        assert data["user"]["is_verified"] is False
        mock_send_email.assert_called_once_with("newuser@example.com", "verification_token")

    @pytest.mark.asyncio
    async def test_register_returns_422_when_invalid_email(self, client: AsyncClient):
        """POST /auth/register should return 422 for invalid email format."""
        # Arrange
        payload = {
            "email": "invalid-email",
            "password": "SecurePass123!"
        }

        # Act
        response = await client.post("/auth/register", json=payload)

        # Assert
        assert response.status_code == 422
        assert "detail" in response.json()

    @pytest.mark.asyncio
    async def test_register_returns_422_when_password_too_short(self, client: AsyncClient):
        """POST /auth/register should return 422 when password is too short."""
        # Arrange
        payload = {
            "email": "user@example.com",
            "password": "short"
        }

        # Act
        response = await client.post("/auth/register", json=payload)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_returns_400_when_email_already_exists(self, client: AsyncClient):
        """POST /auth/register should return 400 when email already registered."""
        # Arrange
        payload = {
            "email": "existing@example.com",
            "password": "SecurePass123!"
        }

        # Act
        with patch("app.api.routers.auth.register_user") as mock_register:
            mock_register.side_effect = HTTPException(status_code=400, detail="Email already registered")
            response = await client.post("/auth/register", json=payload)

        # Assert
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_login_returns_200_when_valid_credentials(self, client: AsyncClient):
        """POST /auth/login should return 200 and access token for valid credentials."""
        # Arrange
        payload = {
            "email": "user@example.com",
            "password": "SecurePass123!"
        }
        
        mock_user = MagicMock()
        mock_user.role = "user"

        # Act
        with patch("app.api.routers.auth.login_user") as mock_login:
            mock_login.return_value = ("jwt_token_here", mock_user)
            response = await client.post("/auth/login", json=payload)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["is_admin"] is False

    @pytest.mark.asyncio
    async def test_login_returns_200_with_admin_flag_when_admin(self, client: AsyncClient):
        """POST /auth/login should return is_admin=True for admin users."""
        # Arrange
        payload = {
            "email": "admin@example.com",
            "password": "SecurePass123!"
        }
        
        mock_admin = MagicMock()
        mock_admin.role = "admin"

        # Act
        with patch("app.api.routers.auth.login_user") as mock_login:
            mock_login.return_value = ("jwt_token_here", mock_admin)
            response = await client.post("/auth/login", json=payload)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["is_admin"] is True

    @pytest.mark.asyncio
    async def test_login_returns_401_when_invalid_credentials(self, client: AsyncClient):
        """POST /auth/login should return 401 for invalid credentials."""
        # Arrange
        payload = {
            "email": "user@example.com",
            "password": "WrongPassword123!"
        }

        # Act
        with patch("app.api.routers.auth.login_user") as mock_login:
            mock_login.side_effect = HTTPException(status_code=401, detail="Invalid credentials")
            response = await client.post("/auth/login", json=payload)

        # Assert
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_login_returns_400_when_email_not_verified(self, client: AsyncClient):
        """POST /auth/login should return 400 when email not verified."""
        # Arrange
        payload = {
            "email": "unverified@example.com",
            "password": "SecurePass123!"
        }

        # Act
        with patch("app.api.routers.auth.login_user") as mock_login:
            mock_login.side_effect = HTTPException(status_code=400, detail="Email not verified")
            response = await client.post("/auth/login", json=payload)

        # Assert
        assert response.status_code == 400
        assert "Email not verified" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_forgot_password_returns_200_when_valid_email(self, client: AsyncClient):
        """POST /auth/forgot-password should return 200 for valid email."""
        # Arrange
        payload = {"email": "user@example.com"}

        # Act
        with patch("app.api.routers.auth.forgot_password") as mock_forgot:
            with patch("app.api.routers.auth.send_reset_email") as mock_send_email:
                mock_forgot.return_value = "reset_token_123"
                response = await client.post("/auth/forgot-password", json=payload)

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == "If an account exists, a reset link has been sent"
        mock_send_email.assert_called_once_with("user@example.com", "reset_token_123")

    @pytest.mark.asyncio
    async def test_forgot_password_returns_200_when_email_does_not_exist(self, client: AsyncClient):
        """POST /auth/forgot-password should return 200 even when email doesn't exist (security)."""
        # Arrange
        payload = {"email": "nonexistent@example.com"}

        # Act
        with patch("app.api.routers.auth.forgot_password") as mock_forgot:
            with patch("app.api.routers.auth.send_reset_email") as mock_send_email:
                mock_forgot.return_value = None
                response = await client.post("/auth/forgot-password", json=payload)

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == "If an account exists, a reset link has been sent"
        mock_send_email.assert_not_called()

    @pytest.mark.asyncio
    async def test_forgot_password_returns_422_when_invalid_email(self, client: AsyncClient):
        """POST /auth/forgot-password should return 422 for invalid email format."""
        # Arrange
        payload = {"email": "invalid"}

        # Act
        response = await client.post("/auth/forgot-password", json=payload)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_reset_password_page_get_returns_200(self, client: AsyncClient):
        """GET /auth/reset-password should return 200 with HTML content."""
        # Act
        response = await client.get("/auth/reset-password", params={"token": "valid_token"})

        # Assert
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")

    @pytest.mark.asyncio
    async def test_reset_password_page_get_returns_422_when_token_missing(self, client: AsyncClient):
        """GET /auth/reset-password should return 422 when token is missing."""
        # Act
        response = await client.get("/auth/reset-password")

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_reset_password_post_returns_200_when_valid_token(self, client: AsyncClient):
        """POST /auth/reset-password should return 200 for valid reset token."""
        # Arrange
        payload = {
            "token": "valid_reset_token",
            "new_password": "NewSecurePass456!"
        }

        # Act
        with patch("app.api.routers.auth.reset_password") as mock_reset:
            mock_reset.return_value = None
            response = await client.post("/auth/reset-password", json=payload)

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == "Password reset successful"

    @pytest.mark.asyncio
    async def test_reset_password_post_returns_400_when_invalid_token(self, client: AsyncClient):
        """POST /auth/reset-password should return 400 for invalid reset token."""
        # Arrange
        payload = {
            "token": "invalid_token",
            "new_password": "NewSecurePass456!"
        }

        # Act
        with patch("app.api.routers.auth.reset_password") as mock_reset:
            mock_reset.side_effect = HTTPException(status_code=400, detail="Invalid or expired token")
            response = await client.post("/auth/reset-password", json=payload)

        # Assert
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_verify_email_returns_200_html_when_valid_token(self, client: AsyncClient):
        """GET /auth/verify-email should return 200 HTML page for valid token."""
        # Act
        with patch("app.api.routers.auth.verify_email_token") as mock_verify:
            mock_verify.return_value = None
            response = await client.get("/auth/verify-email", params={"token": "valid_token"})

        # Assert
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")

    @pytest.mark.asyncio
    async def test_verify_email_returns_error_html_when_invalid_token(self, client: AsyncClient):
        """GET /auth/verify-email should return error HTML page for invalid token."""
        # Act
        with patch("app.api.routers.auth.verify_email_token") as mock_verify:
            mock_verify.side_effect = HTTPException(status_code=400, detail="Invalid or expired token")
            response = await client.get("/auth/verify-email", params={"token": "invalid_token"})

        # Assert
        assert response.status_code == 200  # Still returns 200 but with error template
        assert "text/html" in response.headers.get("content-type", "")
        # Error message should be in the HTML response body

    @pytest.mark.asyncio
    async def test_verify_email_returns_422_when_token_missing(self, client: AsyncClient):
        """GET /auth/verify-email should return 422 when token is missing."""
        # Act
        response = await client.get("/auth/verify-email")

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_resend_verification_email_returns_200_when_valid_email(self, client: AsyncClient):
        """POST /auth/resend-verification-email should return 200 for valid email."""
        # Arrange
        payload = {"email": "user@example.com"}
        
        mock_user = MagicMock()
        mock_user.email = "user@example.com"

        # Act
        with patch("app.api.routers.auth.request_new_verification_email") as mock_request:
            with patch("app.api.routers.auth.send_verification_email") as mock_send:
                mock_request.return_value = (mock_user, "new_verification_token")
                response = await client.post("/auth/resend-verification-email", json=payload)

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == "If an account exists, a verification email has been resent"
        mock_send.assert_called_once_with("user@example.com", "new_verification_token")

    @pytest.mark.asyncio
    async def test_resend_verification_email_returns_200_when_email_does_not_exist(self, client: AsyncClient):
        """POST /auth/resend-verification-email should return 200 even when email doesn't exist (security)."""
        # Arrange
        payload = {"email": "nonexistent@example.com"}

        # Act
        with patch("app.api.routers.auth.request_new_verification_email") as mock_request:
            with patch("app.api.routers.auth.send_verification_email") as mock_send:
                mock_request.return_value = (None, None)
                response = await client.post("/auth/resend-verification-email", json=payload)

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == "If an account exists, a verification email has been resent"
        mock_send.assert_not_called()

    @pytest.mark.asyncio
    async def test_resend_verification_email_returns_422_when_invalid_email(self, client: AsyncClient):
        """POST /auth/resend-verification-email should return 422 for invalid email format."""
        # Arrange
        payload = {"email": "invalid"}

        # Act
        response = await client.post("/auth/resend-verification-email", json=payload)

        # Assert
        assert response.status_code == 422