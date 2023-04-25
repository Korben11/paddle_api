"""Main module."""
import typing
from dataclasses import asdict

import requests
from dataclass_wizard import JSONWizard

import paddle_api.type_defs as td

T = typing.TypeVar("T")
T_CREATE = typing.TypeVar("T_CREATE", bound=JSONWizard)
T_UPDATE = typing.TypeVar("T_UPDATE", bound=JSONWizard)
T_INSTANCE = typing.TypeVar("T_INSTANCE", bound=JSONWizard)


class CRUDP(typing.Generic[T_CREATE, T_UPDATE, T_INSTANCE]):
    """Create, Retrieve, Update, Delete, Paginate."""

    # probably good to make CRUDP class singleton per each path (/products, /prices, ...)

    def __init__(self, client: "Paddle", path: str, t: typing.Type[T_INSTANCE]):
        self.path = path
        self.client = client
        self.t: typing.Type[T_INSTANCE] = t

    def _get_url(self, pk: typing.Optional[str] = None):
        url = f"{self.client.base_url}{self.path}"
        if not pk:
            return url
        return f"{url}/{pk}"

    def _get(self, pk: typing.Optional[str] = None, query_params: typing.Optional[dict] = None) -> dict:
        url = self._get_url(pk)
        response = requests.get(
            url=url,
            headers=self.client.headers,
            params=query_params,
        )
        return response.json()

    def _create_or_update(self, data: typing.Union[T_CREATE, T_UPDATE], pk: typing.Optional[str] = None) -> dict:
        request_f = requests.patch if pk else requests.post
        response = request_f(  # type: ignore
            url=self._get_url(pk),
            json=asdict(data),
            headers=self.client.headers,
        )
        if response.status_code == 400:
            raise BadRequest(response=response)
        response.raise_for_status()
        return response.json()

    def create(self, item: T_CREATE) -> T_INSTANCE:
        response = self._create_or_update(item)
        return self.t.from_dict(response["data"])

    def update(self, item: T_UPDATE) -> T_INSTANCE:
        response = self._create_or_update(item, pk=item.id)
        return self.t.from_dict(response["data"])

    def retrieve(self, pk: str) -> T_INSTANCE:
        response = self._get(pk=pk)
        return self.t.from_dict(response["data"])

    def paginator(self, per_page: typing.Optional[int] = None) -> typing.Generator[td.Page[T_INSTANCE], None, None]:
        response = td.Page.from_dict(self._get(self.path, query_params={"per_page": per_page}))
        # generics seems to not work yet with from_dict in libs: dataclass-wizard, dataclasses-json
        response.data = self.t.from_list(response.data)
        yield response
        while response.meta.pagination.has_more:
            after = response.data[-1].id
            response = td.Page.from_dict(
                self._get(self.path, query_params={"per_page": response.meta.pagination.per_page, "after": after})
            )
            # generics seems to not work yet with from_dict in libs: dataclass-wizard, dataclasses-json
            response.data = self.t.from_list(response.data)
            yield response

    def delete(self, pk: str):
        raise NotImplementedError


class BadRequest(requests.HTTPError):
    """An Bad Request error occurred."""

    def __init__(self, *args, **kwargs):
        response = kwargs.pop("response", None)
        error = response.json()["error"]
        self.code = error["code"]
        super().__init__(error["detail"], *args, **kwargs)


def item_paginator(page_paginator: typing.Generator[td.Page[T], None, None]) -> typing.Generator[T, None, None]:
    """Directly yield each data item from each page."""
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

    def event_types(self) -> dict:
        """Get webhook event types."""
        response = requests.get(
            url=f"{self.base_url}/event-types",
            headers=self.headers,
        )
        return response.json()["data"]

    @property
    def product(self) -> CRUDP[td.ProductCreate, td.ProductCreate, td.Product]:
        """Product crud and p (paginate)."""
        return CRUDP(self, path="/products", t=td.Product)

    @property
    def price(self) -> CRUDP[td.PriceCreate, td.PriceCreate, td.Price]:
        """Price crud and p (paginate)."""
        return CRUDP(self, path="/prices", t=td.Price)
