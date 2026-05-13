import asyncio
import os
import sys
import json

# Add orchestrator to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.agent/orchestrator")))

from mcp_client import MCPClient

async def test_mcp():
    print("Testing MCP Client...")
    client = MCPClient(os.getcwd())
    
    # Connect to mock server
    # We use sys.executable to run the mock server script
    success = await client.connect_to_server(
        "mock-server", 
        sys.executable, 
        ["tests/mock_mcp_server.py"]
    )
    
    if not success:
        print("Failed to connect to mock server.")
        return

    print(f"Available tools: {client.list_available_tools()}")
    
    # Call tool
    try:
        result = await client.call_tool("hello_world", {"name": "Studio Loop"})
        print(f"Tool Result: {result.content[0].text}")
    except Exception as e:
        print(f"Tool call failed: {e}")
    
    await client.close_all()
    print("Test complete.")

if __name__ == "__main__":
    asyncio.run(test_mcp())
