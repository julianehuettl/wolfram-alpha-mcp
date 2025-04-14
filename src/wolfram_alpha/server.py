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

# Konfiguriere Logging
logger = logging.getLogger('wolfram_alpha_server')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

class WolframAlphaServer:
    def __init__(self):
        logger.info("Initialisiere WolframAlphaServer...")
        load_dotenv()
        self.appid = os.getenv("WOLFRAM_ALPHA_APPID")
        if not self.appid:
            logger.error("WOLFRAM_ALPHA_APPID nicht in .env gefunden")
            raise ValueError("WOLFRAM_ALPHA_APPID nicht in .env gefunden")
        logger.info("Server initialisiert mit AppID")
        
        # Server-Konfiguration
        self.server_name = "wolfram-alpha"
        self.server_version = "0.1.0"

    async def query_wolfram_alpha(self, input_text: str) -> str:
        """Führt eine Abfrage an Wolfram Alpha durch"""
        logger.info(f"Führe Abfrage aus: {input_text}")
        url = "https://www.wolframalpha.com/api/v1/llm-api"
        params = {
            "appid": self.appid,
            "input": input_text
        }
        
        try:
            response = requests.get(url, params=params)
            
            if response.status_code == 501:
                raise Exception("Die Eingabe konnte nicht verstanden werden. Bitte formulieren Sie die Anfrage anders.")
            elif response.status_code == 400:
                raise Exception("Ungültige Anfrage: Input-Parameter fehlt oder ist fehlerhaft.")
            elif response.status_code == 403:
                raise Exception("Ungültige oder fehlende AppID. Bitte überprüfen Sie die Konfiguration.")
            elif response.status_code != 200:
                raise Exception(f"Wolfram Alpha API Fehler: Status {response.status_code}")
                
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Fehler bei Wolfram Alpha API: {str(e)}")
            raise Exception(f"Wolfram Alpha API Fehler: {str(e)}")

    def get_tools(self) -> List[Dict[str, Any]]:
        """Gibt die verfügbaren Tools zurück"""
        return [{
            "name": "query",
            "description": "Führt eine Abfrage an Wolfram Alpha durch. Unterstützt mathematische Berechnungen, wissenschaftliche Fragen, Datenanalysen und mehr.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "input": {
                        "type": "string",
                        "description": "Die Abfrage für Wolfram Alpha. Kann in natürlicher Sprache formuliert werden."
                    }
                },
                "required": ["input"]
            }
        }]

async def serve() -> None:
    """Startet den Wolfram Alpha MCP Server"""
    server = Server("wolfram-alpha")
    wolfram_server = WolframAlphaServer()

    @server.list_tools()
    async def list_tools() -> List[Dict[str, Any]]:
        """Listet die verfügbaren Tools"""
        logger.info("Liste verfügbare Tools")
        return wolfram_server.get_tools()

    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """Verarbeitet Tool-Aufrufe"""
        logger.info(f"Verarbeite Tool-Aufruf: {name}")
        try:
            if name == "query":
                result = await wolfram_server.query_wolfram_alpha(arguments["input"])
                return [TextContent(type="text", text=result)]
            else:
                raise ValueError(f"Unbekanntes Tool: {name}")
        except Exception as e:
            logger.error(f"Fehler bei Tool-Aufruf: {str(e)}")
            raise

    # Initialisiere Server mit stdio Transport
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info(f"Server {wolfram_server.server_name} v{wolfram_server.server_version} läuft und wartet auf Eingaben...")
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
    """Hauptfunktion des Servers"""
    asyncio.run(serve())

if __name__ == "__main__":
    main() 