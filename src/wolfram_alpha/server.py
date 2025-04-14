import os
import httpx
import logging
from typing import Dict, Any, List
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INVALID_PARAMS, INTERNAL_ERROR

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

async def query_wolfram_alpha(api_key: str, input_text: str) -> str:
    """Performs a query to Wolfram Alpha"""
    logger.info(f"Executing query: {input_text}")
    url = "https://www.wolframalpha.com/api/v1/llm-api"
    params = {
        "appid": api_key,
        "input": input_text
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            
            if response.status_code == 501:
                raise McpError(ErrorData(
                    code=INTERNAL_ERROR,
                    message="The input could not be understood. Please rephrase your query."
                ))
            elif response.status_code == 400:
                raise McpError(ErrorData(
                    code=INVALID_PARAMS,
                    message="Invalid request: Input parameter missing or malformed."
                ))
            elif response.status_code == 403:
                raise McpError(ErrorData(
                    code=INTERNAL_ERROR,
                    message="Invalid or missing AppID. Please check your configuration."
                ))
            elif response.status_code != 200:
                raise McpError(ErrorData(
                    code=INTERNAL_ERROR,
                    message=f"Wolfram Alpha API error: Status {response.status_code}"
                ))
            
            return response.text
    except httpx.HTTPError as e:
        logger.error(f"Error with Wolfram Alpha API: {str(e)}")
        raise McpError(ErrorData(
            code=INTERNAL_ERROR,
            message=f"Wolfram Alpha API error: {str(e)}"
        ))

async def serve() -> None:
    """Starts the Wolfram Alpha MCP Server"""
    # Load API key from .env file
    load_dotenv()
    api_key = os.getenv("WOLFRAM_ALPHA_APPID")
    if not api_key:
        raise ValueError("WOLFRAM_ALPHA_APPID not found in .env file")

    # Initialize server
    server = Server("wolfram-alpha")

    @server.list_tools()
    async def list_tools() -> List[Tool]:
        """Lists the available tools"""
        logger.info("Listing available tools")
        return [Tool(
            name="wolfram_alpha_query",
            description=(
                "Performs a query to Wolfram Alpha. Supports mathematical calculations, scientific questions, data analysis, and more.\n\n"
                "Formatting Rules:\n"
                "1. Use natural language or simplified keywords:\n"
                "   - Example: \"France population\" instead of \"how many people live in France\"\n"
                "   - Example: \"10 densest elemental metals\" instead of \"what are the 10 densest metals\"\n\n"
                "2. Mathematical Notation:\n"
                "   - Use * for multiplication: 6*10^14 (NOT 6e14)\n"
                "   - Use proper Markdown for formulas:\n"
                "     - Standalone: $$\\n[expression]\\n$$\n"
                "     - Inline: \\( expression \\)\n"
                "   - Use single-letter variables with optional integer subscripts: n, n1, n_1\n"
                "   - Use named physical constants: 'speed of light', 'gravitational constant'\n\n"
                "3. Units and Constants:\n"
                "   - Include space between compound units: \"Ω m\" (NOT \"ohm*meter\")\n"
                "   - For equations with units:\n"
                "     - Solve without units first\n"
                "     - Exclude counting units (e.g., books)\n"
                "     - Include genuine units (e.g., kg)\n\n"
                "4. Handling Ambiguous Queries:\n"
                "   - If a result is not relevant, check for multiple 'Assumptions'\n"
                "   - If available, choose the most relevant assumption\n"
                "   - Re-send the exact same query with the 'assumption' parameter\n"
                "   - Only simplify or rephrase if no relevant assumptions are provided"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "input": {
                        "type": "string"
                    }
                },
                "required": ["input"]
            }
        )]

    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, 