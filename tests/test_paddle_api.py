#!/usr/bin/env python
"""Tests for `paddle_api` package."""

import pytest

from paddle_api import Paddle

FAKE_API_KEY = "fake_123"


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


def test__get(mocker):
    # arrange
    mock_get = mocker.patch("requests.get")
    client = Paddle(FAKE_API_KEY)

    # act
    client._get("/fake-path")

    # assert
    mock_get.assert_called_once()
    assert "/fake-path" in mock_get.call_args_list[0].kwargs["url"]
