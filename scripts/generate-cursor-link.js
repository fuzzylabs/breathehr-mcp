#!/usr/bin/env node
/**
 * Generate Cursor IDE configuration link for Breathe HR MCP server
 */

const config = {
  "mcp.servers": {
    "breathe-hr": {
      "command": "python",
      "args": ["-m", "breathe_hr_mcp"],
      "env": {
        "BREATHE_HR_API_KEY": "your_breathe_hr_api_key_here"
      }
    }
  }
};

const configStr = JSON.stringify(config, null, 2);
const encodedConfig = encodeURIComponent(configStr);
const cursorLink = `cursor://settings/mcp?config=${encodedConfig}`;

console.log("Breathe HR MCP Server - Cursor Configuration");
console.log("=" .repeat(45));
console.log("\n1. Copy this configuration to your Cursor settings:");
console.log(configStr);
console.log("\n2. Or click this link to automatically configure Cursor:");
console.log(cursorLink);
console.log("\n3. Don't forget to replace 'your_breathe_hr_api_key_here' with your actual API key!");