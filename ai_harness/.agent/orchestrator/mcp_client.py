import asyncio
import json
import os
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    def __init__(self, workspace_root):
        self.workspace_root = workspace_root
        self.sessions = {} # server_id -> (session, exit_stack)
        self.tools = {}    # tool_name -> server_id

    async def connect_to_server(self, server_id, command, args=None, env=None):
        """Connects to an MCP server via stdio."""
        if server_id in self.sessions:
            return True

        print(f"Connecting to MCP server: {server_id}...")
        exit_stack = AsyncExitStack()
        try:
            server_params = StdioServerParameters(
                command=command,
                args=args or [],
                env={**os.environ, **(env or {})}
            )
            
            read_stream, write_stream = await exit_stack.enter_async_context(stdio_client(server_params))
            session = await exit_stack.enter_async_context(ClientSession(read_stream, write_stream))
            
            await session.initialize()
            
            # List tools and cache them
            response = await session.list_tools()
            for tool in response.tools:
                self.tools[tool.name] = server_id
            
            self.sessions[server_id] = (session, exit_stack)
            print(f"Connected to {server_id}. Discovered {len(response.tools)} tools.")
            return True
        except Exception as e:
            print(f"Failed to connect to MCP server {server_id}: {e}")
            await exit_stack.aclose()
            return False

    async def call_tool(self, tool_name, arguments=None):
        """Calls a tool by name, automatically identifying the correct server."""
        server_id = self.tools.get(tool_name)
        if not server_id or server_id not in self.sessions:
            raise ValueError(f"Tool '{tool_name}' not found or server not connected.")
        
        session, _ = self.sessions[server_id]
        print(f"Calling MCP tool: {tool_name} on server {server_id}...")
        result = await session.call_tool(tool_name, arguments or {})
        return result

    async def close_all(self):
        """Closes all active MCP sessions."""
        for server_id, (session, exit_stack) in self.sessions.items():
            print(f"Closing MCP session: {server_id}")
            await exit_stack.aclose()
        self.sessions.clear()
        self.tools.clear()

    def list_available_tools(self):
        return list(self.tools.keys())

    # Sync wrapper for orchestrator use
    def call_tool_sync(self, tool_name, arguments=None):
        return asyncio.run(self.call_tool(tool_name, arguments))

    def connect_sync(self, server_id, command, args=None, env=None):
        return asyncio.run(self.connect_to_server(server_id, command, args, env))
