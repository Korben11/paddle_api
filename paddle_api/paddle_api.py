"""Main module."""
import typing
from dataclasses import asdict
from enum import Enum

import requests

import paddle_api.type_defs as td


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


def item_paginator(page_paginator: typing.Generator[td.Page, None, None]) -> typing.Generator[dict, None, None]:
    """Directly yields each data item from each page."""
    for page in page_paginator:
        for item in page.data:
            yield item


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

    def _get(self, path: Path, pk: typing.Optional[str] = None, query_params: typing.Optional[dict] = None) -> td.Page:
        url = self._get_url(path, pk)
        response = requests.get(
            url=url,
            headers=self.headers,
            params=query_params,
        )
        return response.json()

    def _paginator(self, path: Path, per_page: typing.Optional[int] = None) -> typing.Generator[td.Page, None, None]:
        response = td.Page.from_dict(self._get(path, query_params={"per_page": per_page}))
        yield response
        while response.meta.pagination.has_more:
            after = response.data[-1]["id"]
            response = td.Page.from_dict(
                self._get(path, query_params={"per_page": response.meta.pagination.per_page, "after": after})
            )
            yield response

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

    def product(self, pk: str):
        """Get product."""
        return self._get(Path.PRODUCTS, pk)

    def products(self, per_page: typing.Optional[int] = None) -> typing.Generator[td.Page, None, None]:
        """Products paginator."""
        return self._paginator(Path.PRODUCTS, per_page=per_page)

    def product_create(self, product: td.ProductCreate) -> td.Product:
        """Create product."""
        return td.Product.from_dict(self._create_or_update(Path.PRODUCTS, data=product)["data"])

    def product_update(self, product: td.ProductCreate, pk: str) -> td.Product:
        """Update (patch) product."""
        return td.Product.from_dict(self._create_or_update(Path.PRODUCTS, data=product, pk=pk)["data"])
