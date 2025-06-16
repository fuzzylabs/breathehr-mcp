# Breathe HR MCP Server

> **Connect your Breathe HR data to AI assistants** — Access employees, absences, leave requests, and company information through natural language queries, with secure read-write capabilities.

[![Model Context Protocol](https://img.shields.io/badge/MCP-Compatible-blue)](https://modelcontextprotocol.io) [![Python 3.12+](https://img.shields.io/badge/Python-3.12+-green)](https://python.org) [![Breathe HR API](https://img.shields.io/badge/Breathe%20HR-API%20v1-orange)](https://developers.breathehr.com)

**🚨 Disclaimer**: This project is created by [Fuzzy Labs](https://fuzzylabs.ai) with good vibes and is not officially supported by Breathe HR. Use at your own discretion.

## What This Does

Transform how you work with your Breathe HR data by asking AI assistants natural language questions like:

- *"Show me all employees in the Engineering department"*
- *"Who has pending leave requests this month?"*
- *"Create a holiday request for John Doe from March 1-5"*
- *"Search for employees named Sarah"*
- *"What's our current headcount by department?"*

**🔐 Secure Access** — API key authentication with controlled permissions  
**🚀 Instant Setup** — Works with any MCP-compatible AI assistant  
**📊 Complete Coverage** — Access employees, absences, departments & more

## Quick Start

### 1. Get Your Breathe HR API Key
1. Log into your Breathe HR account
2. Go to **Settings → Integrations → API**
3. Create a new API key and copy it

### 2. Install & Configure

#### macOS Setup

```bash
# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone https://github.com/fuzzylabs/breathehr-mcp.git
cd breathehr-mcp
uv sync
```

#### Linux/Windows Setup

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh  # Linux/macOS
# OR for Windows: powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Clone and install
git clone https://github.com/fuzzylabs/breathehr-mcp.git
cd breathehr-mcp
uv sync
```

### 3. Connect to Your AI Assistant

#### Claude Desktop

Add this to your Claude Desktop config file:

**Config Location:**
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "breathe-hr": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/your/breathehr-mcp",
        "python",
        "-m",
        "breathe_hr_mcp"
      ],
      "env": {
        "BREATHE_HR_API_KEY": "your_breathe_hr_api_key_here"
      }
    }
  }
}
```

#### Cursor

**📋 Quick Setup:** 

**Copy this Cursor deeplink and paste it in your browser address bar:**

```
cursor://anysphere.cursor-deeplink/mcp/install?name=breathe-hr&config=eyJicmVhdGhlLWhyIjp7ImNvbW1hbmQiOiJ1diIsImFyZ3MiOlsicnVuIiwiLS1kaXJlY3RvcnkiLCIvcGF0aC90by95b3VyL2JyZWF0aGVoci1tY3AiLCJweXRob24iLCItbSIsImJyZWF0aGVfaHJfbWNwIl0sImVudiI6eyJCUkVBVEhFX0hSX0FQSV9LRVkiOiJ5b3VyX2JyZWF0aGVfaHJfYXBpX2tleV9oZXJlIn19fQ==

**💡 How to use:**
1. Copy the entire `cursor://` URL above
2. Paste it into your browser's address bar 
3. Press Enter - this will open Cursor and prompt to install the MCP server

**Note:** After clicking the button, you'll need to:
1. Update the path `/path/to/your/breathehr-mcp` to your actual installation directory
2. Replace `your_breathe_hr_api_key_here` with your actual Breathe HR API key

Or manually add this to your Cursor MCP settings:

```json
{
  "breathe-hr": {
    "command": "uv",
    "args": [
      "run",
      "--directory",
      "/path/to/your/breathehr-mcp",
      "python",
      "-m",
      "breathe_hr_mcp"
    ],
    "env": {
      "BREATHE_HR_API_KEY": "your_breathe_hr_api_key_here"
    }
  }
}
```

#### Other MCP Clients

This server is compatible with any MCP client. Refer to your client's documentation for MCP server configuration.

**💡 Setup Help:**
- **Using uv (recommended):** Use `uv run` command as shown above - no Python path needed!
- **uv path for Claude Desktop:** Use full path `~/.local/bin/uv` (find yours with `which uv`)
- **Manual Python paths (if not using uv):**
  - **macOS (Homebrew):** `/opt/homebrew/bin/python3` (Apple Silicon) or `/usr/local/bin/python3` (Intel)
  - **macOS (System):** `/usr/bin/python3` (if available)
  - **Find your Python:** Run `which python3` in terminal
  - **Windows:** Try `C:\Python311\python.exe`

### 4. Start Using

1. **Restart your AI assistant**
2. **Start asking questions!**

Try these example queries:
> *"List my Breathe HR employees"*  
> *"Show me pending leave requests"*  
> *"Create a holiday request for employee 123"*  
> *"Find employees in Engineering department"*

## What You Can Access

This MCP server provides **secure access** to your Breathe HR data:

| **Data Type** | **What You Can Do** |
|---------------|-------------------|
| **👥 Employees** | List, search, view details, filter by department/status |
| **🏖️ Absences** | View leave records, filter by dates/types, create requests |
| **🏢 Company** | Access account information and settings |
| **📋 Departments** | List organizational structure and teams |

**Available Tools:**
- `list_employees` - Get paginated employee list with filters
- `get_employee` - Get detailed employee information
- `search_employees` - Search employees by query
- `list_absences` - Get absence records with filtering
- `create_leave_request` - Submit new leave requests
- `get_employee_absences` - Get absences for specific employee
- `get_account_info` - Get company account details
- `get_departments` - List all departments

## Troubleshooting

### Common Issues

**"No module named 'breathe_hr_mcp'"**
- **Using uv:** Make sure you're using the absolute directory path with `uv run --directory`
- **Manual setup:** Verify Python can find the installed packages: `pip list | grep fastmcp`

**"spawn uv ENOENT" or "command not found: uv"**
- Install uv first: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Restart your terminal after installation
- Verify installation: `uv --version`

**"spawn python ENOENT" (if not using uv)**
- Switch to uv setup (recommended) or use full Python path in config
- Check your Python path: `which python3`
- Try different common paths: `/usr/bin/python3`, `/usr/local/bin/python3`, `/opt/homebrew/bin/python3`

**"Authentication failed"**
- Verify your Breathe HR API key is correct
- Check the key has appropriate permissions in Breathe HR
- Make sure there are no extra spaces or quotes around the key

**"Rate limit exceeded"**
- Breathe HR has API rate limits
- Wait a few minutes before trying again
- Reduce the frequency of requests

**MCP tools not showing in your AI assistant**
- Restart your AI assistant after config changes
- Check the config file syntax is valid JSON
- Verify file paths are absolute, not relative

### Getting Help

- **Issues & Bugs:** [GitHub Issues](https://github.com/fuzzylabs/breathehr-mcp/issues)
- **Breathe HR API Docs:** [developers.breathehr.com](https://developers.breathehr.com)
- **MCP Protocol:** [modelcontextprotocol.io](https://modelcontextprotocol.io)

---

## Render Deployment (Secure Remote HTTP Access)

Want to deploy the MCP server remotely so multiple users can access it via HTTP? Deploy to Render for easy cloud hosting with API key authentication.

### Quick Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/fuzzylabs/breathehr-mcp)

### Manual Deployment

1. **Fork this repository** to your GitHub account

2. **Create a Render account** at [render.com](https://render.com)

3. **Create a new Web Service** and connect your GitHub fork

4. **Configure the service:**
   - **Build Command:** `pip install uv && uv sync`
   - **Start Command:** `uv run uvicorn breathe_hr_mcp:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free (or choose a paid plan for better performance)

5. **Set environment variables** in Render dashboard:
   - `BREATHE_HR_API_KEY`: Your Breathe HR API key
   - `MCP_API_KEY`: A secure random API key for authentication (see generation instructions below)

6. **Deploy** - Render will automatically build and deploy your service

### Generating a Secure API Key

Generate a secure random API key for the `MCP_API_KEY` environment variable:

```bash
# Using Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Using OpenSSL  
openssl rand -base64 32

# Using Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

⚠️ **Important**: Store this API key securely - you'll need it to configure your MCP clients.

### Using Your Deployed Server

Once deployed, you'll get a URL like `https://your-service.onrender.com`. Configure your MCP clients to use:

**Claude Desktop:**
```json
{
  "mcpServers": {
    "breathe-hr": {
      "command": "curl",
      "args": [
        "-X", "POST",
        "https://your-service.onrender.com/mcp/",
        "-H", "Content-Type: application/json",
        "-H", "Authorization: Bearer YOUR_MCP_API_KEY_HERE",
        "-d", "@-"
      ]
    }
  }
}
```

Replace `YOUR_MCP_API_KEY_HERE` with the API key you generated and set in Render.

🔒 **Security Note**: The API key authentication is only enforced when the `MCP_API_KEY` environment variable is set. If no API key is configured, the server will accept unauthenticated requests (useful for local development).

**Direct HTTP Access:**
```bash
# List available tools
curl -X POST https://your-service.onrender.com/mcp/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_MCP_API_KEY_HERE" \
  -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'

# List employees
curl -X POST https://your-service.onrender.com/mcp/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_MCP_API_KEY_HERE" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "list_employees",
      "arguments": {"page": 1, "per_page": 10}
    },
    "id": 1
  }'
```

**⚠️ Note on Free Tier:** Render's free tier spins down services after inactivity. First requests may take 30-60 seconds to wake up the service.

---

## For Developers

### Development Setup

**Environment Variables (for development):**
```bash
cp .env.example .env
# Edit .env and set BREATHE_HR_API_KEY=your_api_key_here
```

**Run Tests:**
```bash
uv run pytest
```

**HTTP Server (for testing):**
```bash
uv run uvicorn breathe_hr_mcp:app --reload
# Server available at http://localhost:8000/mcp/
```

### API Testing

Test the schema endpoint:
```bash
curl -X POST http://localhost:8000/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1
  }'
```

Test listing employees:
```bash
curl -X POST http://localhost:8000/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "list_employees",
      "arguments": {"page": 1, "per_page": 10}
    },
    "id": 1
  }'
```

### Architecture

- **Server:** FastMCP framework with FastAPI backend
- **Protocol:** Model Context Protocol (MCP) via stdio
- **API:** Breathe HR API v1 with secure access
- **Authentication:** Bearer token (API key)