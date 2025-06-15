# Breathe HR MCP Server

![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-blue)
![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-green)
![Breathe HR API](https://img.shields.io/badge/Breathe%20HR-API%20v1-orange)

> A Model Context Protocol (MCP) server that gives AI assistants secure access to your Breathe HR data - employees, absences, and company information.

## What This Does

This MCP server lets your AI assistant (like Claude) directly access your Breathe HR account to:

- 👥 **Browse employees** - Get employee lists, search by name/department, view detailed profiles
- 🏖️ **Manage absences** - Check leave balances, view absence history, submit leave requests
- 🏢 **Access company data** - View account info, departments, and organizational structure
- 🔍 **Smart search** - Find employees and data using natural language queries

Perfect for HR teams, managers, and anyone who needs quick access to people data through their AI assistant.

## Quick Start

### 1. Get Your Breathe HR API Key

1. Log into your Breathe HR account
2. Go to **Settings** → **Integrations** → **API**
3. Generate a new API key
4. Copy the key (you'll need it in step 3)

### 2. Install & Configure

```bash
# Clone and install
git clone https://github.com/fuzzylabs/breathehr-mcp.git
cd breathehr-mcp
uv sync

# Set up your API key
cp .env.example .env
# Edit .env and add your Breathe HR API key
```

### 3. Connect to Your AI Assistant

**For Claude Desktop**, add this to your config file:

```json
{
  "mcpServers": {
    "breathe-hr": {
      "command": "uv",
      "args": ["run", "python", "-m", "breathe_hr_mcp"],
      "env": {
        "BREATHE_HR_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**Config file locations:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

**For Cursor**, add this to your settings:

```json
{
  "mcp.servers": {
    "breathe-hr": {
      "command": "uv",
      "args": ["run", "python", "-m", "breathe_hr_mcp"],
      "env": {
        "BREATHE_HR_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### 4. Start Using!

Restart your AI assistant and try asking:

- *"Show me all employees in the Engineering department"*
- *"Who has pending leave requests?"*
- *"Create a holiday request for John Doe from March 1-5"*
- *"Search for employees named Sarah"*
- *"What's our current employee count?"*

## What You Can Access

### 👥 Employee Data
- Employee lists with filtering by department, status
- Individual employee profiles and details
- Search employees by name, email, or attributes
- Department and team information

### 🏖️ Absence Management
- View all absence/leave records
- Filter by employee, dates, absence type
- Create new leave requests
- Check leave balances and history

### 🏢 Company Information
- Account details and settings
- Department structures
- Employee count and statistics

## Troubleshooting

### "Authentication failed" Error

**Check your API key:**
1. Verify the key in your `.env` file matches your Breathe HR settings
2. Make sure there are no extra spaces or quotes around the key
3. Confirm your API key has the necessary permissions

### "MCP server not found" in AI Assistant

**Restart and check config:**
1. Restart your AI assistant completely
2. Verify the JSON config syntax is correct (no trailing commas)
3. Check the file path points to the right location
4. Make sure `uv` is installed and in your PATH

### "Rate limit exceeded" Error

**Breathe HR has API limits:**
- Wait a few minutes before trying again
- Reduce the frequency of requests
- Contact Breathe HR support if limits are too low

### Testing Connection

```bash
# Test the server directly
cd breathehr-mcp
uv run python -m breathe_hr_mcp

# Validate your configuration
uv run python scripts/validate-configs.py

# Check available tools
uv run python scripts/print_mcp_routes.py
```

## Render Deployment

Want to run this in the cloud? Deploy to Render in one click:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/fuzzylabs/breathehr-mcp)

**Environment variables to set:**
- `BREATHE_HR_API_KEY`: Your Breathe HR API key
- `MCP_API_KEY`: (Optional) Secure key for API access

Then configure your AI assistant to use the deployed URL:

```json
{
  "mcpServers": {
    "breathe-hr": {
      "url": "https://your-app.onrender.com",
      "headers": {
        "Authorization": "Bearer your_mcp_api_key"
      }
    }
  }
}
```

## For Developers

### Development Setup

```bash
# Clone and install with dev dependencies
git clone https://github.com/fuzzylabs/breathehr-mcp.git
cd breathehr-mcp
uv sync

# Run tests
uv run pytest

# Run with auto-reload
uv run uvicorn breathe_hr_mcp:app --reload

# Format code
uv run black .
uv run isort .
```

### Available Tools

| Tool | Description |
|------|-------------|
| `list_employees` | Get paginated employee list with filters |
| `get_employee` | Get detailed employee information |
| `search_employees` | Search employees by query |
| `list_absences` | Get absence records with filtering |
| `create_leave_request` | Submit new leave requests |
| `get_employee_absences` | Get absences for specific employee |
| `get_account_info` | Get company account details |
| `get_departments` | List all departments |

### Testing

The project includes comprehensive tests:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=breathe_hr_mcp

# Run specific test file
uv run pytest tests/test_server.py
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Run the test suite
5. Submit a pull request

---

**License**: MIT  
**Author**: [Fuzzy Labs](https://fuzzylabs.ai)  
**Issues**: [GitHub Issues](https://github.com/fuzzylabs/breathehr-mcp/issues)