"""Entry point for running the Breathe HR MCP server as a module"""

if __name__ == "__main__":
    import uvicorn
    from .server import app
    
    uvicorn.run(app, host="0.0.0.0", port=8000)