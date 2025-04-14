# Wolfram Alpha MCP Server

Ein einfacher MCP-Server für die Integration mit Wolfram Alpha.

## Installation

1. Python 3.8 oder höher installieren
2. Abhängigkeiten installieren:
   ```bash
   pip install -e .
   ```

## Konfiguration

1. `.env` Datei erstellen:
   ```
   WOLFRAM_ALPHA_APPID=DEIN_API_KEY
   ```

## Verwendung

Der Server kann über die Kommandozeile gestartet werden:

```bash
python -m src.wolfram_alpha.server
```

## MCP-Integration

Der Server unterstützt derzeit eine Methode:

- `query`: Führt eine Abfrage an Wolfram Alpha durch
  - Parameter: `input` (String)
  - Beispiel:
    ```json
    {
      "jsonrpc": "2.0",
      "id": "1",
      "method": "query",
      "params": {
        "input": "Was ist die Hauptstadt von Frankreich?"
      }
    }
    ``` 