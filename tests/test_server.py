import unittest
from unittest.mock import patch, MagicMock
from src.wolfram_alpha.server import WolframAlphaServer
import json

class TestWolframAlphaServer(unittest.TestCase):
    def setUp(self):
        self.server = WolframAlphaServer()

    @patch('requests.get')
    def test_query_wolfram_alpha(self, mock_get):
        # Mock die API-Antwort
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Test Antwort"
        mock_get.return_value = mock_response

        # Teste die Abfrage
        result = self.server.query_wolfram_alpha("Test")
        self.assertEqual(result, "Test Antwort")

    def test_process_message(self):
        # Teste eine gültige Nachricht
        message = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "query",
            "params": {
                "input": "Test"
            }
        }
        
        with patch.object(self.server, 'query_wolfram_alpha', return_value="Test Antwort"):
            response = self.server.process_message(json.dumps(message))
            self.assertEqual(response["result"]["text"], "Test Antwort")

        # Teste eine ungültige Methode
        message["method"] = "invalid"
        response = self.server.process_message(json.dumps(message))
        self.assertEqual(response["error"]["code"], -32601)

if __name__ == '__main__':
    unittest.main() 