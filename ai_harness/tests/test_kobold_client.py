import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import requests


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.agent/orchestrator")))

from kobold_client import KoboldClient, KoboldTransportError


class TestKoboldClient(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.config = {
            "koboldcpp": {
                "base_url": "http://127.0.0.1:5001",
                "endpoint": "/v1/chat/completions",
                "model": "local-gemma-4",
                "temperature": 0.3,
                "top_p": 0.9,
                "max_output_tokens": 2500,
                "connect_timeout_seconds": 7,
                "read_timeout_seconds": 901,
            },
            "paths": {"logs": ".agent/logs"},
        }
        self.prompt = {"system": "system prompt", "user": "user prompt"}

    @patch("kobold_client.requests.post")
    def test_uses_configurable_tuple_timeout(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "ACTIONS_JSON: {}"}}]
        }
        mock_post.return_value = mock_response

        client = KoboldClient(self.config, self.base_dir)
        client.log_interaction = MagicMock()

        client.call(self.prompt)

        self.assertEqual(mock_post.call_args.kwargs["timeout"], (7, 901))

    @patch("kobold_client.requests.post")
    def test_timeout_raises_transport_error_instead_of_returning_text(self, mock_post):
        mock_post.side_effect = requests.exceptions.ReadTimeout("read timed out")
        client = KoboldClient(self.config, self.base_dir)

        with self.assertRaises(KoboldTransportError) as ctx:
            client.call(self.prompt)

        self.assertIn("read=901s", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
