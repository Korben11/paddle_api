#!/usr/bin/env python
"""Tests for `paddle_api` package."""

from dataclasses import dataclass

import pytest
from dataclasses_json import dataclass_json

from paddle_api import type_defs as td
from paddle_api.paddle_api import Paddle, Path

FAKE_API_KEY = "fake_123"


@pytest.fixture
def page():
    return td.Page.from_dict(
        {
            "data": [{"id": "pk_1"}, {"id": "pk_2"}, {"id": "pk_3"}],
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
        (None, "/event-types"),
        ("123", "/event-types/123"),
    ),
)
def test__get(pk, expected, mocker):
    # arrange
    mock_get = mocker.patch("requests.get")
    client = Paddle(FAKE_API_KEY)

    # act
    client._get(Path.EVENT_TYPES, pk)

    # assert
    mock_get.assert_called_once()
    assert expected in mock_get.call_args_list[0].kwargs["url"]


def test__paginate_single_page(page: td.Page, mocker):
    # arrange
    mock_get = mocker.patch("paddle_api.Paddle._get", return_value=page.to_dict())
    client = Paddle(FAKE_API_KEY)

    # act
    page = next(client._paginator(path=Path.PRODUCTS))

    # assert
    mock_get.assert_called_once()
    isinstance(page, td.Page)


def test__paginate(page, mocker):
    # arrange
    second_page = page.to_dict()
    page.meta.pagination.has_more = True
    second_page["data"] = [{"id": "pk_4"}, {"id": "pk_5"}, {"id": "pk_6"}]
    mock_get = mocker.patch("paddle_api.Paddle._get", side_effect=iter([page.to_dict(), second_page]))
    client = Paddle(FAKE_API_KEY)

    # act
    pages = list(client._paginator(path=Path.PRODUCTS))

    # assert
    assert mock_get.call_count == 2
    assert mock_get.mock_calls[1] == mocker.call(Path.PRODUCTS, query_params={"per_page": 5, "after": "pk_3"})
    for page in pages:
        isinstance(page, td.Page)


@pytest.mark.skip
def test_page_generics():
    # arrange
    @dataclass_json
    @dataclass
    class Fake:
        name: str

    # act
    page = td.Page[Fake].from_dict(
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
