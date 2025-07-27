"""Entry point for running the Breathe HR MCP server as a module"""

if __name__ == "__main__":
    from .server import mcp
    
    mcp.run()
