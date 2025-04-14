# Wolfram Alpha MCP Server

A simple MCP server for Wolfram Alpha integration.

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -e .
   ```

## Usage

The server can be started from the command line:
```bash
python -m src.wolfram_alpha.server
```

## API Documentation

The server currently supports one method:

- `query`: Performs a query to Wolfram Alpha

## Configuration

1. Create `.env` file:
   ```
   WOLFRAM_ALPHA_APPID=YOUR_API_KEY
   ```

## MCP Integration

The server currently supports one method:

- `query`: Performs a query to Wolfram Alpha
  - Parameter: `input` (String)
  - Example:
    ```json
    {
      "jsonrpc": "2.0",
      "id": "1",
      "method": "query",
      "params": {
        "input": "What is the capital of France?"
      }
    }
    ``` 