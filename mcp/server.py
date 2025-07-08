import asyncio
import json
from typing import Any, Dict, List
from mcp import ClientSession, StdioServerParameters
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from .tools.testing_tools import TestingTools

class MCPTestingServer:
    def __init__(self):
        self.server = Server("playwright-testing")
        self.testing_tools = TestingTools()
        self.setup_tools()
    
    def setup_tools(self):
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            return [
                Tool(
                    name="generate_test_case",
                    description="Generate Playwright test cases based on application analysis",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "url": {"type": "string", "description": "URL to test"},
                            "test_type": {"type": "string", "enum": ["ui", "api", "e2e"]},
                            "description": {"type": "string", "description": "Test description"}
                        },
                        "required": ["url", "test_type"]
                    }
                ),
                Tool(
                    name="analyze_page",
                    description="Analyze web page for testing opportunities",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "url": {"type": "string", "description": "URL to analyze"}
                        },
                        "required": ["url"]
                    }
                ),
                Tool(
                    name="run_test_suite",
                    description="Execute Playwright tests with AI insights",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "test_file": {"type": "string", "description": "Test file to run"},
                            "browser": {"type": "string", "enum": ["chromium", "firefox", "webkit"], "default": "chromium"}
                        },
                        "required": ["test_file"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            if name == "generate_test_case":
                result = await self.testing_tools.generate_test_case(
                    arguments["url"],
                    arguments["test_type"],
                    arguments.get("description", "")
                )
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "analyze_page":
                result = await self.testing_tools.analyze_page(arguments["url"])
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "run_test_suite":
                result = await self.testing_tools.run_test_suite(
                    arguments["test_file"],
                    arguments.get("browser", "chromium")
                )
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            else:
                raise ValueError(f"Unknown tool: {name}")

async def main():
    server = MCPTestingServer()
    
    async with stdio_server(server.server, StdioServerParameters()) as streams:
        await server.server.run(
            streams[0], streams[1],
            InitializationOptions(
                server_name="playwright-testing",
                server_version="1.0.0",
                capabilities=server.server.get_capabilities()
            )
        )

if __name__ == "__main__":
    asyncio.run(main())