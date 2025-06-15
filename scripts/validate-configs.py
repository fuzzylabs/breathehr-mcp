#!/usr/bin/env python3
"""Validate configuration files for Breathe HR MCP server"""

import json
import os
import sys
from pathlib import Path

def validate_env_example():
    """Validate .env.example file"""
    env_file = Path(__file__).parent.parent / ".env.example"
    
    if not env_file.exists():
        print("❌ .env.example file not found")
        return False
    
    required_vars = [
        "BREATHE_HR_API_KEY",
        "BREATHE_HR_BASE_URL"
    ]
    
    content = env_file.read_text()
    missing_vars = []
    
    for var in required_vars:
        if var not in content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        return False
    
    print("✅ .env.example is valid")
    return True

def validate_claude_config():
    """Validate Claude Desktop configuration"""
    config_file = Path(__file__).parent.parent / "claude_desktop_config.json"
    
    if not config_file.exists():
        print("❌ claude_desktop_config.json file not found")
        return False
    
    try:
        config = json.loads(config_file.read_text())
        
        if "mcpServers" not in config:
            print("❌ Missing 'mcpServers' in Claude config")
            return False
        
        if "breathe-hr" not in config["mcpServers"]:
            print("❌ Missing 'breathe-hr' server in Claude config")
            return False
        
        server_config = config["mcpServers"]["breathe-hr"]
        
        required_fields = ["command", "args"]
        for field in required_fields:
            if field not in server_config:
                print(f"❌ Missing '{field}' in breathe-hr server config")
                return False
        
        print("✅ claude_desktop_config.json is valid")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in claude_desktop_config.json: {e}")
        return False

def validate_render_config():
    """Validate Render deployment configuration"""
    render_file = Path(__file__).parent.parent / "render.yaml"
    
    if not render_file.exists():
        print("❌ render.yaml file not found")
        return False
    
    try:
        import yaml
        config = yaml.safe_load(render_file.read_text())
        
        if "services" not in config:
            print("❌ Missing 'services' in render.yaml")
            return False
        
        service = config["services"][0]
        required_fields = ["type", "name", "env", "buildCommand", "startCommand"]
        
        for field in required_fields:
            if field not in service:
                print(f"❌ Missing '{field}' in render service config")
                return False
        
        print("✅ render.yaml is valid")
        return True
        
    except ImportError:
        print("⚠️  PyYAML not installed, skipping render.yaml validation")
        return True
    except Exception as e:
        print(f"❌ Error validating render.yaml: {e}")
        return False

def main():
    """Run all configuration validations"""
    print("Validating Breathe HR MCP Configuration Files")
    print("=" * 45)
    
    results = [
        validate_env_example(),
        validate_claude_config(),
        validate_render_config(),
    ]
    
    if all(results):
        print("\n🎉 All configuration files are valid!")
        sys.exit(0)
    else:
        print("\n💥 Some configuration files have issues")
        sys.exit(1)

if __name__ == "__main__":
    main()