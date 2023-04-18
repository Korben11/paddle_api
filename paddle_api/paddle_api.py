"""Main module."""
import requests


class Paddle:
    """Paddle API client."""

    def __init__(self, api_key: str, test_mode=True):
        self.api_key = api_key
        self.test_mode = test_mode
        self.base_url = "https://api.paddle.com"
        if self.test_mode:
            self.base_url = "https://sandbox-api.paddle.com"
        self.headers = {
            'Authorization': f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _get(self, path: str):
        response = requests.get(
            url=f"{self.base_url}{path}",
            headers=self.headers,
        )
        return response.json()

    def event_types(self):
        """Get webhook event types."""
        return self._get("/event-types")
