"""Main module."""
import typing
from dataclasses import asdict, dataclass
from enum import Enum

import requests


class Path(Enum):
    """REST paths."""

    EVENT_TYPES = "/event-types"
    PRODUCTS = "/products"


class BadRequest(requests.HTTPError):
    """An Bad Request error occurred."""

    def __init__(self, *args, **kwargs):
        response = kwargs.pop("response", None)
        error = response.json()["error"]
        self.code = error["code"]
        super().__init__(error["detail"], *args, **kwargs)


@dataclass
class Product:  # noqa: D101
    name: str
    tax_category: typing.Literal[
        "standard",
        "saas",
        "ebooks",
        "digital-goods",
        "website-hosting",
        "human-services",
        "implementation-services",
        "training-services",
        "professional-services",
        "software-programming-services",
    ]
    description: typing.Optional[str] = None
    image_url: typing.Optional[str] = None


class Paddle:
    """Paddle API client."""

    def __init__(self, api_key: str, test_mode: bool = True, api_version: int = 3):
        self.api_key = api_key
        self.test_mode = test_mode
        self.base_url = "https://api.paddle.com"
        if self.test_mode:
            self.base_url = "https://sandbox-api.paddle.com"
        self.headers = {
            'Authorization': f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Paddle-Version": str(api_version),
        }

    def _get_url(self, path: Path, pk: typing.Optional[str] = None):
        url = f"{self.base_url}{path.value}"
        if not pk:
            return url
        return f"{url}/{pk}"

    def _get(self, path: Path, pk: typing.Optional[str] = None):
        url = self._get_url(path, pk)
        response = requests.get(
            url=url,
            headers=self.headers,
        )
        return response.json()

    def _create_or_update(self, path: Path, data, pk: typing.Optional[str] = None) -> dict:
        request_f = requests.patch if pk else requests.post
        response = request_f(  # type: ignore
            url=self._get_url(path, pk),
            json=asdict(data),
            headers=self.headers,
        )
        if response.status_code == 400:
            raise BadRequest(response=response)
        response.raise_for_status()
        return response.json()

    def event_types(self):
        """Get webhook event types."""
        return self._get(Path.EVENT_TYPES)

    def products(self, pk: typing.Optional[str] = None):
        """Get products."""
        return self._get(Path.PRODUCTS, pk)

    def product_create(self, product: Product):
        """Create product."""
        return self._create_or_update(Path.PRODUCTS, data=product)

    def product_update(self, product: Product, pk: str):
        """Update (patch) product."""
        return self._create_or_update(Path.PRODUCTS, data=product, pk=pk)
