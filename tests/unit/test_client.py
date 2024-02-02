from typing import Generator

import aiohttp
import pytest
from aioresponses import aioresponses

from app.client import fetch
from app.errors import FetchClientError, FetchClientResponseError, FetchUnexpectedError


@pytest.fixture
def mock_aioresponse() -> Generator[aioresponses, None, None]:
    with aioresponses() as mocked:
        yield mocked


@pytest.mark.asyncio
async def test_fetch_success(mock_aioresponse: aioresponses):
    # テスト項目: 正常系: HTTP ステータスが 200 のとき、データを取得できる
    # given (前提条件):
    url = "http://example.com"
    expected = {"key": "value"}
    mock_aioresponse.get(url, status=200, payload=expected)

    # when (操作):
    async with aiohttp.ClientSession() as session:
        res = await fetch(session, url)
        actual = await res.json()

        #  then (期待する結果):
        assert actual == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status_code",
    [400, 500],
)
async def test_fetch_client_response_error(
    status_code: int, mock_aioresponse: aioresponses
):
    # テスト項目: 異常系: HTTP ステータスが 400 以上のとき、FetchClientError が raise される
    # given (前提条件):
    url = "http://example.com"
    mock_aioresponse.get(url, status=status_code)

    # when (操作):
    async with aiohttp.ClientSession() as session:
        with pytest.raises(FetchClientResponseError) as excinfo:
            _ = await fetch(session, url)

        # then (期待する結果):
        assert excinfo.exconly().startswith("app.errors.FetchClientResponseError")


@pytest.mark.asyncio
async def test_fetch_client_error(mock_aioresponse: aioresponses):
    # テスト項目: 異常系: ClientError が発生したとき、FetchClientError が raise される
    # given (前提条件):
    url = "http://example.com"
    mock_aioresponse.get(url, exception=aiohttp.ClientError)

    # when (操作):
    async with aiohttp.ClientSession() as session:
        with pytest.raises(FetchClientError) as excinfo:
            _ = await fetch(session, url)

        # then (期待する結果):
        assert excinfo.exconly().startswith("app.errors.FetchClientError")


@pytest.mark.asyncio
async def test_fetch_unexpected_error(mock_aioresponse: aioresponses):
    # テスト項目: 異常系: 予期しないエラーが発生したとき、FetchUnexpectedError が raise される
    url = "http://example.com"
    mock_aioresponse.get(url, exception=Exception)

    # when (操作):
    async with aiohttp.ClientSession() as session:
        with pytest.raises(FetchUnexpectedError) as excinfo:
            _ = await fetch(session, url)

        # then (期待する結果):
        assert excinfo.exconly().startswith("app.errors.FetchUnexpectedError")
