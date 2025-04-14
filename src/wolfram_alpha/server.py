import json
import sys
import os
import asyncio
import logging
from dotenv import load_dotenv
import requests
from typing import Dict, Any, Optional, List
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
from mcp.types import TextContent

# Configure logging
logger = logging.getLogger('wolfram_alpha_server')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

class WolframAlphaServer:
    def __init__(self):
        logger.info("Initializing WolframAlphaServer...")
        load_dotenv()
        self.appid = os.getenv("WOLFRAM_ALPHA_APPID")
        if not self.appid:
            logger.error("WOLFRAM_ALPHA_APPID not found in .env")
            raise ValueError("WOLFRAM_ALPHA_APPID not found in .env")
        logger.info("Server initialized with AppID")
        
        # Server configuration
        self.server_name = "wolfram-alpha"
        self.server_version = "0.1.0"

    async def query_wolfram_alpha(self, input_text: str) -> str:
        """Performs a query to Wolfram Alpha"""
        logger.info(f"Executing query: {input_text}")
        url = "https://www.wolframalpha.com/api/v1/llm-api"
        params = {
            "appid": self.appid,
            "input": input_text
        }
        
        try:
            response = requests.get(url, params=params)
            
            if response.status_code == 501:
                raise Exception("The input could not be understood. Please rephrase your query.")
            elif response.status_code == 400:
                raise Exception("Invalid request: Input parameter missing or malformed.")
            elif response.status_code == 403:
                raise Exception("Invalid or missing AppID. Please check your configuration.")
            elif response.status_code != 200:
                raise Exception(f"Wolfram Alpha API error: Status {response.status_code}")
                
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Error with Wolfram Alpha API: {str(e)}")
            raise Exception(f"Wolfram Alpha API error: {str(e)}")

    def get_tools(self) -> List[Dict[str, Any]]:
        """Returns the available tools"""
        return [{
            "name": "query",
            "description": "Performs a query to Wolfram Alpha. Supports mathematical calculations, scientific questions, data analysis, and more. Note: Wolfram Alpha only understands English, so all queries must be in English.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "input": {
                        "type": "string",
                        "description": "The query for Wolfram Alpha. Must be in English as Wolfram Alpha only understands English."
                    }
                },
                "required": ["input"]
            }
        }]

async def serve() -> None:
    """Starts the Wolfram Alpha MCP Server"""
    server = Server("wolfram-alpha")
    wolfram_server = WolframAlphaServer()

    @server.list_tools()
    async def list_tools() -> List[Dict[str, Any]]:
        """Lists the available tools"""
        logger.info("Listing available tools")
        return wolfram_server.get_tools()

    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """Processes tool calls"""
        logger.info(f"Processing tool call: {name}")
        try:
            if name == "query":
                result = await wolfram_server.query_wolfram_alpha(arguments["input"])
                return [TextContent(type="text", text=result)]
            else:
                raise ValueError(f"Unknown tool: {name}")
        except Exception as e:
            logger.error(f"Error during tool call: {str(e)}")
            raise

    # Initialize server with stdio transport
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info(f"Server {wolfram_server.server_name} v{wolfram_server.server_version} is running and waiting for input...")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=wolfram_server.server_name,
                server_version=wolfram_server.server_version,
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

def main():
    """Main function of the server"""
    asyncio.run(serve())

if __name__ == "__main__":
    main() 