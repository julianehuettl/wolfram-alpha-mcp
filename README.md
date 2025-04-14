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

## Installation

Install `wolfram-alpha-mcp` via pip:

```bash
pip install wolfram-alpha-mcp
```

After installation, you can run it as a script using:

```bash
python -m wolfram_alpha.server
```

## Configuration

### API Key Setup

1. Create `.env` file in the project root:
   ```
   WOLFRAM_ALPHA_APPID=YOUR_API_KEY
   ```

### Configure for Claude.app

Add to your Claude settings:

```json
"mcpServers": {
  "wolfram-alpha": {
    "command": "python",
    "args": ["-m", "wolfram_alpha.server"]
  }
}
```

## License

wolfram-alpha-mcp is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Juliane Hüttl
- GitHub: [julianehuettl](https://github.com/julianehuettl)
- Website: [juliane-huettl.de](https://juliane-huettl.de) 