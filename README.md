# Wolfram Alpha MCP Server

A Model Context Protocol server that provides Wolfram Alpha integration capabilities. This server enables LLMs to perform mathematical calculations, answer scientific questions, and analyze data using Wolfram Alpha's powerful computational knowledge engine.

## Available Tools

- `wolfram_alpha_query` - Performs a query to Wolfram Alpha
    - `input` (string, required): The query to send to Wolfram Alpha
    - Formatting Rules:
        1. Use natural language or simplified keywords
        2. Use proper mathematical notation
        3. Follow unit and constant formatting guidelines
        4. Handle ambiguous queries appropriately

## Requirements

- Python 3.11 or higher
- Wolfram Alpha API Key ([Get one here](https://products.wolframalpha.com/api/))

## Installation

### For Development

1. Clone the repository:
   ```bash
   git clone https://github.com/julianehuettl/wolfram-alpha-mcp.git
   cd wolfram-alpha-mcp
   ```

2. Create and activate virtual environment:
   ```bash
   # Using uv (recommended)
   uv venv

   # Or using standard venv
   python -m venv .venv
   ```

3. Install with dependencies from local source:
   ```bash
   # Using uv (recommended)
   uv pip install .

   # Or using standard pip
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install .
   ```

## Configuration

### API Key Setup

1. Create a `.env` file in the project root directory:
   ```
   WOLFRAM_ALPHA_APPID=your_api_key_here
   ```

2. Get your API key from [Wolfram Alpha Developer Portal](https://products.wolframalpha.com/api/)

### Configure for Claude Desktop

Add to your Claude Desktop configuration file (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
"mcpServers": {
  "wolfram-alpha": {
    "command": "/absolute/path/to/wolfram-alpha-mcp/.venv/bin/python",
    "args": ["-m", "wolfram_alpha.server"]
  }
}
```

Replace `/absolute/path/to/wolfram-alpha-mcp/` with the actual path to your cloned repository.

After updating the configuration, restart Claude Desktop for the changes to take effect.

## License

wolfram-alpha-mcp is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Juliane Hüttl
- GitHub: [julianehuettl](https://github.com/julianehuettl)
- Website: [juliane-huettl.de](https://juliane-huettl.de) 