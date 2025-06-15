"""Breathe HR MCP Server

This module provides a Model Context Protocol (MCP) server for Breathe HR,
enabling AI assistants to access employee data, absence records, and account information.
"""

import os
from typing import Dict, List, Optional, Any
import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize MCP server
mcp = FastMCP("Breathe HR", dependencies=[])

# Configuration
BREATHE_HR_API_KEY = os.getenv("BREATHE_HR_API_KEY")
BREATHE_HR_BASE_URL = os.getenv("BREATHE_HR_BASE_URL", "https://api.breathehr.com/v1")
MCP_API_KEY = os.getenv("MCP_API_KEY")

# Security
security = HTTPBearer(auto_error=False)

def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify MCP API key for remote deployments"""
    if MCP_API_KEY and (not credentials or credentials.credentials != MCP_API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials

# Add API key verification to MCP if configured
if MCP_API_KEY:
    mcp = FastMCP("Breathe HR", dependencies=[Depends(verify_api_key)])

async def breathe_hr_request(
    endpoint: str,
    method: str = "GET",
    params: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Make authenticated requests to Breathe HR API"""
    if not BREATHE_HR_API_KEY:
        raise RuntimeError("BREATHE_HR_API_KEY environment variable is required")
    
    url = f"{BREATHE_HR_BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
    headers = {
        "Authorization": f"Bearer {BREATHE_HR_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=json_data,
            timeout=30.0
        )
        
        if response.status_code == 401:
            raise RuntimeError("Authentication failed. Please check your Breathe HR API key.")
        elif response.status_code == 403:
            raise RuntimeError("Access forbidden. Please check your API permissions.")
        elif response.status_code == 404:
            raise RuntimeError(f"Resource not found: {endpoint}")
        elif response.status_code == 429:
            raise RuntimeError("Rate limit exceeded. Please try again later.")
        elif not response.is_success:
            error_message = "Unknown error"
            try:
                error_data = response.json()
                error_message = error_data.get("message", error_data.get("error", str(error_data)))
            except:
                error_message = response.text or f"HTTP {response.status_code}"
            
            raise RuntimeError(f"Breathe HR API request failed: {response.status_code} - {error_message}")
        
        try:
            return response.json()
        except:
            raise RuntimeError(f"Invalid JSON response from Breathe HR API: {response.text}")

# MCP Tools

@mcp.tool
async def list_employees(
    page: int = 1,
    per_page: int = 50,
    department: Optional[str] = None,
    status: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get a list of employees from Breathe HR
    
    Args:
        page: Page number for pagination (default: 1)
        per_page: Number of employees per page (default: 50, max: 100)
        department: Filter by department name
        status: Filter by employment status (active, inactive, etc.)
    
    Returns:
        Dict containing employees list and pagination info
    """
    params = {
        "page": page,
        "per_page": min(per_page, 100)
    }
    
    if department:
        params["department"] = department
    if status:
        params["status"] = status
    
    return await breathe_hr_request("employees", params=params)

@mcp.tool
async def get_employee(employee_id: int) -> Dict[str, Any]:
    """
    Get detailed information for a specific employee
    
    Args:
        employee_id: The unique ID of the employee
    
    Returns:
        Dict containing detailed employee information
    """
    return await breathe_hr_request(f"employees/{employee_id}")

@mcp.tool
async def search_employees(
    query: str,
    page: int = 1,
    per_page: int = 20
) -> Dict[str, Any]:
    """
    Search employees by name, email, or other attributes
    
    Args:
        query: Search query string
        page: Page number for pagination (default: 1)
        per_page: Number of results per page (default: 20, max: 50)
    
    Returns:
        Dict containing matching employees and pagination info
    """
    params = {
        "query": query,
        "page": page,
        "per_page": min(per_page, 50)
    }
    
    return await breathe_hr_request("employees/search", params=params)

@mcp.tool
async def list_absences(
    page: int = 1,
    per_page: int = 50,
    employee_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    absence_type: Optional[str] = None,
    status: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get absence/leave records from Breathe HR
    
    Args:
        page: Page number for pagination (default: 1)
        per_page: Number of absences per page (default: 50, max: 100)
        employee_id: Filter by specific employee ID
        start_date: Filter absences starting from this date (YYYY-MM-DD)
        end_date: Filter absences ending before this date (YYYY-MM-DD)
        absence_type: Filter by absence type (holiday, sick, etc.)
        status: Filter by status (pending, approved, rejected)
    
    Returns:
        Dict containing absence records and pagination info
    """
    params = {
        "page": page,
        "per_page": min(per_page, 100)
    }
    
    if employee_id:
        params["employee_id"] = employee_id
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    if absence_type:
        params["type"] = absence_type
    if status:
        params["status"] = status
    
    return await breathe_hr_request("absences", params=params)

@mcp.tool
async def create_leave_request(
    employee_id: int,
    start_date: str,
    end_date: str,
    absence_type: str,
    reason: Optional[str] = None,
    half_day: bool = False,
    half_day_period: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new leave/absence request in Breathe HR
    
    Args:
        employee_id: The ID of the employee requesting leave
        start_date: Start date of the absence (YYYY-MM-DD)
        end_date: End date of the absence (YYYY-MM-DD)
        absence_type: Type of absence (holiday, sick, personal, etc.)
        reason: Optional reason for the absence
        half_day: Whether this is a half-day absence
        half_day_period: If half_day, specify 'morning' or 'afternoon'
    
    Returns:
        Dict containing the created absence request details
    """
    data = {
        "employee_id": employee_id,
        "start_date": start_date,
        "end_date": end_date,
        "type": absence_type,
        "half_day": half_day
    }
    
    if reason:
        data["reason"] = reason
    if half_day and half_day_period:
        data["half_day_period"] = half_day_period
    
    return await breathe_hr_request("absences", method="POST", json_data=data)

@mcp.tool
async def get_account_info() -> Dict[str, Any]:
    """
    Get account/company information from Breathe HR
    
    Returns:
        Dict containing account details and configuration
    """
    return await breathe_hr_request("account")

@mcp.tool
async def get_employee_absences(
    employee_id: int,
    year: Optional[int] = None,
    absence_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get absence records for a specific employee
    
    Args:
        employee_id: The unique ID of the employee
        year: Filter by specific year
        absence_type: Filter by absence type
    
    Returns:
        Dict containing the employee's absence records
    """
    params = {"employee_id": employee_id}
    
    if year:
        params["year"] = year
    if absence_type:
        params["type"] = absence_type
    
    return await breathe_hr_request(f"employees/{employee_id}/absences", params=params)

@mcp.tool
async def get_departments() -> Dict[str, Any]:
    """
    Get list of departments/teams from Breathe HR
    
    Returns:
        Dict containing departments and their details
    """
    return await breathe_hr_request("departments")

# Create FastAPI app
app = mcp.create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)