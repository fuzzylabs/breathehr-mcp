# Breathe HR MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server that provides secure, read-write access to [Breathe HR](https://www.breathehr.com/) data for AI assistants.

## Features

- **Employee Management**: List, search, and get detailed employee information
- **Absence Management**: View absence records and create leave requests
- **Account Information**: Access company and account details
- **Secure Authentication**: API key-based authentication with Breathe HR
- **Flexible Deployment**: Support for local development and cloud deployment
- **Comprehensive Error Handling**: Detailed error messages and proper HTTP status handling

## Available Tools

### Employee Tools
- `list_employees` - Get a paginated list of employees with optional filtering
- `get_employee` - Get detailed information for a specific employee by ID
- `search_employees` - Search employees by name, email, or other attributes
- `get_employee_absences` - Get absence records for a specific employee

### Absence Tools
- `list_absences` - Get absence/leave records with filtering options
- `create_leave_request` - Submit new leave requests for employees

### Organization Tools
- `get_account_info` - Get company/account information and settings
- `get_departments` - List all departments/teams in the organization

## Quick Start

### Prerequisites

- Python 3.12.3 (or compatible version)
- [uv](https://docs.astral.sh/uv/) package manager
- A Breathe HR account with API access
- Breathe HR API key (obtainable from your Breathe HR settings)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/fuzzylabs/breathe-hr-mcp.git
cd breathe-hr-mcp
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Breathe HR API key
```

4. Configure your AI assistant to use this MCP server (see [Configuration](#configuration) below).

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Required: Your Breathe HR API key
BREATHE_HR_API_KEY=your_breathe_hr_api_key_here

# Optional: API base URL (defaults to production)
BREATHE_HR_BASE_URL=https://api.breathehr.com/v1

# For sandbox/testing (uncomment to use sandbox)
# BREATHE_HR_BASE_URL=https://api.sandbox.breathehr.com/v1

# Optional: MCP API key for remote deployment authentication
MCP_API_KEY=your_mcp_api_key_here
```

### AI Assistant Configuration

#### Claude Desktop

Add this to your Claude Desktop configuration file:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "breathe-hr": {
      "command": "python",
      "args": ["-m", "breathe_hr_mcp"],
      "env": {
        "BREATHE_HR_API_KEY": "your_breathe_hr_api_key_here"
      }
    }
  }
}
```

#### Cursor

Add this to your Cursor settings:

```json
{
  "mcp.servers": {
    "breathe-hr": {
      "command": "python",
      "args": ["-m", "breathe_hr_mcp"],
      "env": {
        "BREATHE_HR_API_KEY": "your_breathe_hr_api_key_here"
      }
    }
  }
}
```

#### Remote HTTP Access

For remote deployments (e.g., on [Render](https://render.com)), you can also access the server via HTTP:

```json
{
  "mcpServers": {
    "breathe-hr": {
      "url": "https://your-deployment-url.onrender.com",
      "headers": {
        "Authorization": "Bearer your_mcp_api_key_here"
      }
    }
  }
}
```

## Usage Examples

Once configured, you can use natural language to interact with your Breathe HR data:

### Employee Queries
- "Show me all employees in the Engineering department"
- "Get details for employee ID 123"
- "Search for employees named Sarah"
- "List all active employees"

### Absence Management
- "Show me all pending leave requests"
- "Create a holiday request for employee 123 from March 1-5, 2024"
- "List all absences for employee John Doe in 2024"
- "Show sick leave records for the last month"

### Account Information
- "Get our company account details"
- "List all departments in the organization"
- "Show me account usage information"

## Development

### Running Locally

```bash
# Install dependencies (including dev dependencies)
uv sync

# Run the server
uv run python -m breathe_hr_mcp

# Or run with uvicorn for development
uv run uvicorn breathe_hr_mcp:app --reload --host 0.0.0.0 --port 8000
```

### Testing

```bash
# Run tests
uv run pytest

# Run tests with coverage (install coverage first)
uv add --dev pytest-cov
uv run pytest --cov=breathe_hr_mcp

# Run linting
uv run ruff check .
uv run black --check .
uv run isort --check-only .
```

### Code Formatting

```bash
# Format code
uv run black .
uv run isort .
```

### Utility Scripts

The project includes several utility scripts in the `scripts/` directory:

```bash
# Print MCP routes and tools info
uv run python scripts/print_mcp_routes.py

# Validate configuration files
uv run python scripts/validate-configs.py

# Generate Cursor IDE configuration
node scripts/generate-cursor-link.js
```

## Deployment

### Deploy to Render

1. Fork this repository
2. Connect your fork to [Render](https://render.com)
3. Create a new Web Service
4. Set environment variables in Render dashboard:
   - `BREATHE_HR_API_KEY`: Your Breathe HR API key
   - `MCP_API_KEY`: A secure key for MCP access (optional)
5. Deploy!

The `render.yaml` file is included for easy deployment configuration.

### Other Platforms

This server can be deployed to any platform that supports Python web applications:

- **Heroku**: Use the included `requirements.txt` for pip-based deployment
- **Railway**: Use `uv sync` in build command or fallback to `requirements.txt`
- **Google Cloud Run**: Deploy as a container with uv
- **AWS Lambda**: Use with a serverless adapter and `requirements.txt`

For platforms that don't support `uv`, the project includes a `requirements.txt` file for pip-based installations.

## API Reference

### Tool Parameters

#### list_employees
- `page` (int): Page number for pagination (default: 1)
- `per_page` (int): Number of employees per page (default: 50, max: 100)
- `department` (str, optional): Filter by department name
- `status` (str, optional): Filter by employment status

#### get_employee
- `employee_id` (int): The unique ID of the employee

#### search_employees
- `query` (str): Search query string
- `page` (int): Page number for pagination (default: 1)
- `per_page` (int): Number of results per page (default: 20, max: 50)

#### list_absences
- `page` (int): Page number for pagination (default: 1)
- `per_page` (int): Number of absences per page (default: 50, max: 100)
- `employee_id` (int, optional): Filter by specific employee ID
- `start_date` (str, optional): Filter absences starting from this date (YYYY-MM-DD)
- `end_date` (str, optional): Filter absences ending before this date (YYYY-MM-DD)
- `absence_type` (str, optional): Filter by absence type (holiday, sick, etc.)
- `status` (str, optional): Filter by status (pending, approved, rejected)

#### create_leave_request
- `employee_id` (int): The ID of the employee requesting leave
- `start_date` (str): Start date of the absence (YYYY-MM-DD)
- `end_date` (str): End date of the absence (YYYY-MM-DD)
- `absence_type` (str): Type of absence (holiday, sick, personal, etc.)
- `reason` (str, optional): Optional reason for the absence
- `half_day` (bool): Whether this is a half-day absence (default: False)
- `half_day_period` (str, optional): If half_day, specify 'morning' or 'afternoon'

## Error Handling

The server provides comprehensive error handling for common scenarios:

- **Authentication Errors**: Invalid or missing API keys
- **Authorization Errors**: Insufficient permissions
- **Rate Limiting**: Automatic detection and helpful error messages
- **Resource Not Found**: Clear messages for missing employees/records
- **Validation Errors**: Detailed parameter validation feedback

## Security

- **Read-Write Access**: This server can both read and write data to Breathe HR
- **API Key Security**: API keys are never logged or exposed in error messages
- **HTTPS Only**: All communication with Breathe HR uses HTTPS
- **Optional MCP Authentication**: Additional API key protection for remote deployments

## Troubleshooting

### Common Issues

1. **"Authentication failed"**
   - Verify your `BREATHE_HR_API_KEY` is correct
   - Check that your API key has the necessary permissions
   - Ensure you're using the correct base URL (production vs sandbox)

2. **"Rate limit exceeded"**
   - Breathe HR has rate limits on their API
   - Wait a few minutes before retrying
   - Consider reducing the frequency of requests

3. **"Resource not found"**
   - Check that employee IDs exist in your Breathe HR account
   - Verify endpoint URLs are correct for your API version

4. **Tool not showing in AI assistant**
   - Restart your AI assistant after configuration changes
   - Check that the MCP server is running (`python -m breathe_hr_mcp`)
   - Verify your configuration file syntax is correct

### Getting Help

- Check the [Breathe HR API documentation](https://developers.breathehr.com/)
- Review [Model Context Protocol documentation](https://modelcontextprotocol.io)
- Open an issue on this repository for bugs or feature requests

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### v0.1.0
- Initial release
- Employee management tools
- Absence management tools
- Account information tools
- Comprehensive error handling
- Support for local and cloud deployment