#!/usr/bin/env python3
"""Print MCP routes and tools for debugging"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from breathe_hr_mcp.server import mcp, app

def print_mcp_info():
    """Print information about MCP tools and routes"""
    print("Breathe HR MCP Server Information")
    print("=" * 40)
    
    # Print available tools
    if hasattr(mcp, '_tools'):
        tools = mcp._tools
    elif hasattr(mcp, 'tools'):
        tools = mcp.tools
    else:
        tools = {}
    
    print(f"Available MCP Tools ({len(tools)}):")
    for tool_name, tool_func in tools.items():
        print(f"  - {tool_name}")
        if hasattr(tool_func, '__doc__') and tool_func.__doc__:
            # Get first line of docstring
            first_line = tool_func.__doc__.strip().split('\n')[0]
            print(f"    {first_line}")
    
    print("\nFastAPI Routes:")
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            print(f"  {list(route.methods)[0] if route.methods else 'ANY'} {route.path}")

if __name__ == "__main__":
    print_mcp_info()