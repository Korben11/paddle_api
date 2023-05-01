#!/usr/bin/env python
"""Tests for `paddle_api` package."""
import pytest
from pydantic import BaseModel

from paddle_api import type_defs as td
from paddle_api.paddle_api import Paddle, item_paginator

FAKE_API_KEY = "fake_123"


@pytest.fixture
def mock_crudp_get(mocker):
    yield mocker.patch("paddle_api.paddle_api.CRUDP._get")


@pytest.fixture
def make_product():
    def make(pk: str = "pk_1", name: str = "Stefan"):
        return {
            "id": pk,
            "name": name,
            "status": "active",
            "tax_category": "saas",
            "created_at": "2023-04-18T16:21:30.366Z",
        }

    return make


@pytest.fixture
def page(make_product):
    return td.Page[td.Product].parse_obj(
        {
            "data": [make_product(pk=f"pk_{i+1}") for i in range(3)],
            "meta": {
                "request_id": "req_123",
                "pagination": {"next": None, "has_more": False, "per_page": 5, "estimated_total": 5},
            },
        }
    )


@pytest.mark.parametrize(
    "test_mode,expected",
    (
        (True, "https://sandbox-api.paddle.com"),
        (False, "https://api.paddle.com"),
    ),
)
def test_base_url(test_mode, expected):
    # arrange
    client = Paddle(FAKE_API_KEY, test_mode=test_mode)

    # act, assert
    assert client.base_url == expected


def test_authorization_header():
    # arrange
    client = Paddle(FAKE_API_KEY)

    # act, assert
    assert "Authorization" in client.headers
    assert f"Bearer {FAKE_API_KEY}" == client.headers["Authorization"]


@pytest.mark.parametrize(
    "pk,expected",
    (
        (None, "/products"),
        ("123", "/products/123"),
    ),
)
def test__get(pk, expected, mocker):
    # arrange
    mock_get = mocker.patch("requests.get")
    client = Paddle(FAKE_API_KEY)

    # act
    client.product._get(pk)

    # assert
    mock_get.assert_called_once()
    assert expected in mock_get.call_args_list[0].kwargs["url"]


def test_retrieve_product(make_product, mocker):
    # arrange
    response = mocker.MagicMock()
    response.json.return_value = {"data": make_product(pk="prod_1"), "reqeust_id": "req_123"}
    mock_get = mocker.patch("requests.get", return_value=response)
    client = Paddle(FAKE_API_KEY)

    # act
    product = client.product.retrieve(pk="prod_1")

    # assert
    mock_get.assert_called_once()
    assert isinstance(product, td.Product)
    assert product.id == "prod_1"


def test__paginate_single_page(page, mock_crudp_get):
    # arrange
    mock_crudp_get.return_value = page.dict()
    client = Paddle(FAKE_API_KEY)

    # act
    page = next(client.product.paginator())

    # assert
    mock_crudp_get.assert_called_once()
    isinstance(page, td.Page)
    isinstance(page.data[0], td.Product)
    assert page.data[0].id == "pk_1"


def test__paginate(page, make_product, mock_crudp_get, mocker):
    # arrange
    second_page = page.dict()
    page.meta.pagination.has_more = True
    second_page["data"] = [make_product(pk=f"pk_{i}") for i in range(4, 7)]
    mock_crudp_get.side_effect = iter([page.dict(), second_page])
    client = Paddle(FAKE_API_KEY)

    # act
    pages = list(client.product.paginator())

    # assert
    assert mock_crudp_get.call_count == 2
    assert mock_crudp_get.mock_calls[1] == mocker.call("/products", query_params={"per_page": 5, "after": "pk_3"})
    for page in pages:
        isinstance(page, td.Page)


def test__items_from_pages(page, make_product, mock_crudp_get):
    # arrange
    second_page = page.dict()
    page.meta.pagination.has_more = True
    second_page["data"] = [make_product(pk=f"pk_{i}") for i in range(4, 7)]
    mock_crudp_get.side_effect = iter([page.dict(), second_page])
    client = Paddle(FAKE_API_KEY)

    # act
    items_g = item_paginator(client.product.paginator())
    items = list(items_g)

    # assert
    assert len(items) == 6


def test_page_generics():
    # arrange
    class Fake(BaseModel):
        name: str

    # act
    page = td.Page[Fake].parse_obj(
        {
            "data": [{"name": "Stefan"}],
            "meta": {
                "request_id": "req_123",
                "pagination": {"next": None, "has_more": False, "per_page": 5, "estimated_total": 5},
            },
        }
    )

    # assert
    assert isinstance(page.data[0], Fake)
    assert page.data[0].name == "Stefan"
