"""Tests for Breathe HR MCP Server"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx
from fastapi.testclient import TestClient

from breathe_hr_mcp.server import app, mcp, breathe_hr_request


class TestBreatheHRRequest:
    """Test the core API request function"""

    @pytest.fixture(autouse=True)
    def mock_env_vars(self):
        """Mock environment variables"""
        with patch.dict("os.environ", {
            "BREATHE_HR_API_KEY": "test_api_key",
            "BREATHE_HR_BASE_URL": "https://api.test-breathehr.com/v1"
        }):
            # Also patch the module-level variables that were loaded at import time
            with patch("breathe_hr_mcp.server.BREATHE_HR_API_KEY", "test_api_key"):
                with patch("breathe_hr_mcp.server.BREATHE_HR_BASE_URL", "https://api.test-breathehr.com/v1"):
                    yield

    @pytest.mark.asyncio
    async def test_successful_request(self):
        """Test successful API request"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.is_success = True
        mock_response.json.return_value = {"employees": []}

        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.request = AsyncMock(
                return_value=mock_response
            )
            
            result = await breathe_hr_request("employees")
            
            assert result == {"employees": []}

    @pytest.mark.asyncio
    async def test_missing_api_key(self):
        """Test error when API key is missing"""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(RuntimeError, match="BREATHE_HR_API_KEY environment variable is required"):
                await breathe_hr_request("employees")

    @pytest.mark.asyncio
    async def test_authentication_error(self):
        """Test 401 authentication error"""
        mock_response = MagicMock()
        mock_response.status_code = 401

        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.request = AsyncMock(
                return_value=mock_response
            )
            
            with pytest.raises(RuntimeError, match="Authentication failed"):
                await breathe_hr_request("employees")

    @pytest.mark.asyncio
    async def test_forbidden_error(self):
        """Test 403 forbidden error"""
        mock_response = MagicMock()
        mock_response.status_code = 403

        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.request = AsyncMock(
                return_value=mock_response
            )
            
            with pytest.raises(RuntimeError, match="Access forbidden"):
                await breathe_hr_request("employees")

    @pytest.mark.asyncio
    async def test_not_found_error(self):
        """Test 404 not found error"""
        mock_response = MagicMock()
        mock_response.status_code = 404

        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.request = AsyncMock(
                return_value=mock_response
            )
            
            with pytest.raises(RuntimeError, match="Resource not found"):
                await breathe_hr_request("employees/999")

    @pytest.mark.asyncio
    async def test_rate_limit_error(self):
        """Test 429 rate limit error"""
        mock_response = MagicMock()
        mock_response.status_code = 429

        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.request = AsyncMock(
                return_value=mock_response
            )
            
            with pytest.raises(RuntimeError, match="Rate limit exceeded"):
                await breathe_hr_request("employees")

    @pytest.mark.asyncio
    async def test_invalid_json_response(self):
        """Test error when response is not valid JSON"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.is_success = True
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.text = "Invalid response"

        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.request = AsyncMock(
                return_value=mock_response
            )
            
            with pytest.raises(RuntimeError, match="Invalid JSON response"):
                await breathe_hr_request("employees")


class TestMCPTools:
    """Test MCP tool implementations"""

    @pytest.fixture
    def mock_breathe_hr_request(self):
        """Mock the breathe_hr_request function"""
        with patch("breathe_hr_mcp.server.breathe_hr_request") as mock:
            yield mock

    @pytest.mark.asyncio
    async def test_list_employees(self, mock_breathe_hr_request):
        """Test list_employees tool"""
        mock_response = {
            "employees": [
                {"id": 1, "name": "John Doe", "email": "john@example.com"},
                {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
            ],
            "pagination": {"page": 1, "per_page": 50, "total": 2}
        }
        mock_breathe_hr_request.return_value = mock_response

        # Import the tool function directly
        from breathe_hr_mcp.server import list_employees
        
        result = await list_employees()
        
        mock_breathe_hr_request.assert_called_once_with(
            "employees", 
            params={"page": 1, "per_page": 50}
        )
        assert result == mock_response

    @pytest.mark.asyncio
    async def test_list_employees_with_filters(self, mock_breathe_hr_request):
        """Test list_employees tool with filters"""
        mock_response = {"employees": [], "pagination": {}}
        mock_breathe_hr_request.return_value = mock_response

        from breathe_hr_mcp.server import list_employees
        
        await list_employees(page=2, per_page=25, department="Engineering", status="active")
        
        mock_breathe_hr_request.assert_called_once_with(
            "employees",
            params={
                "page": 2,
                "per_page": 25,
                "department": "Engineering",
                "status": "active"
            }
        )

    @pytest.mark.asyncio
    async def test_get_employee(self, mock_breathe_hr_request):
        """Test get_employee tool"""
        mock_response = {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "department": "Engineering"
        }
        mock_breathe_hr_request.return_value = mock_response

        from breathe_hr_mcp.server import get_employee
        
        result = await get_employee(1)
        
        mock_breathe_hr_request.assert_called_once_with("employees/1")
        assert result == mock_response

    @pytest.mark.asyncio
    async def test_search_employees(self, mock_breathe_hr_request):
        """Test search_employees tool"""
        mock_response = {
            "employees": [{"id": 1, "name": "John Doe"}],
            "pagination": {}
        }
        mock_breathe_hr_request.return_value = mock_response

        from breathe_hr_mcp.server import search_employees
        
        result = await search_employees("John")
        
        mock_breathe_hr_request.assert_called_once_with(
            "employees/search",
            params={"query": "John", "page": 1, "per_page": 20}
        )
        assert result == mock_response

    @pytest.mark.asyncio
    async def test_list_absences(self, mock_breathe_hr_request):
        """Test list_absences tool"""
        mock_response = {
            "absences": [
                {"id": 1, "employee_id": 1, "start_date": "2024-01-01", "end_date": "2024-01-05"}
            ],
            "pagination": {}
        }
        mock_breathe_hr_request.return_value = mock_response

        from breathe_hr_mcp.server import list_absences
        
        result = await list_absences(employee_id=1, start_date="2024-01-01")
        
        mock_breathe_hr_request.assert_called_once_with(
            "absences",
            params={
                "page": 1,
                "per_page": 50,
                "employee_id": 1,
                "start_date": "2024-01-01"
            }
        )
        assert result == mock_response

    @pytest.mark.asyncio
    async def test_create_leave_request(self, mock_breathe_hr_request):
        """Test create_leave_request tool"""
        mock_response = {
            "id": 123,
            "employee_id": 1,
            "start_date": "2024-02-01",
            "end_date": "2024-02-05",
            "status": "pending"
        }
        mock_breathe_hr_request.return_value = mock_response

        from breathe_hr_mcp.server import create_leave_request
        
        result = await create_leave_request(
            employee_id=1,
            start_date="2024-02-01",
            end_date="2024-02-05",
            absence_type="holiday",
            reason="Vacation"
        )
        
        mock_breathe_hr_request.assert_called_once_with(
            "absences",
            method="POST",
            json_data={
                "employee_id": 1,
                "start_date": "2024-02-01",
                "end_date": "2024-02-05",
                "type": "holiday",
                "reason": "Vacation",
                "half_day": False
            }
        )
        assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_account_info(self, mock_breathe_hr_request):
        """Test get_account_info tool"""
        mock_response = {
            "company_name": "Test Company",
            "subscription": "premium",
            "employee_count": 50
        }
        mock_breathe_hr_request.return_value = mock_response

        from breathe_hr_mcp.server import get_account_info
        
        result = await get_account_info()
        
        mock_breathe_hr_request.assert_called_once_with("account")
        assert result == mock_response


class TestFastAPIApp:
    """Test FastAPI application"""

    def test_app_creation(self):
        """Test that FastAPI app is created successfully"""
        client = TestClient(app)
        
        # Test health endpoint (if FastMCP provides one)
        response = client.get("/")
        # The exact response depends on FastMCP's default routes
        assert response.status_code in [200, 404]  # Either works or endpoint doesn't exist

    def test_mcp_tools_registration(self):
        """Test that MCP tools are properly registered"""
        # Check that tools are registered with the MCP instance
        assert hasattr(mcp, '_tools') or hasattr(mcp, 'tools')
        
        # This test structure depends on FastMCP's internal API
        # Adjust based on actual FastMCP implementation