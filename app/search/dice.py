from typing import Tuple

import aiohttp

from app.client import fetch
from app.constants import DATA_SOURCE_NAME_DICE
from app.errors import FetchClientError, FetchClientResponseError, FetchUnexpectedError
from app.logger import create_logger

logger = create_logger(__name__)


async def search_dice(session: aiohttp.ClientSession, query: str) -> Tuple[str, bytes]:
    """
    DICE API: https://dice-database.org/genes/<gene>

    Example:
    - https://dice-database.org/genes/IL2RA
    """

    api_url = f"https://dice-database.org/downloads/genes/expression/{query}"
    headers = {"Content-Type": "text/csv"}

    # fetch data from DICE
    try:
        res = await fetch(session, api_url, headers=headers)

        if res.status == 200 and res.headers.get("Content-Type") == "text/csv":
            # DICE の API は、遺伝子が見つかった場合、status code 200、Content-Type: text/csv でレスポンスが返ってくる
            # 前処理前の CSV データをレスポンスから読込
            raw_csv_data: bytes = await res.content.read()

            return (DATA_SOURCE_NAME_DICE, raw_csv_data)

        return (DATA_SOURCE_NAME_DICE, b"")
    except FetchClientResponseError as e:
        # DICE の API は、遺伝子が見つからなかった場合、status code 500、Content-Type: text/html でレスポンスが返ってくる# 遺伝子が見つからなかった場合、status code 500、Content-Type: text/html でレスポンスが返ってくる
        origin_e = e.__cause__
        if isinstance(origin_e, aiohttp.ClientResponseError):
            if (
                origin_e.status == 500
                and origin_e.headers is not None
                # origin_e.headers.get("Content-Type") is "text/html; charset=utf-8"
                and origin_e.headers.get("Content-Type", "").startswith("text/html")
            ):
                # この場合、遺伝子が見つからなかったため、空のバイト列を返し、エラーとして扱わない
                return (DATA_SOURCE_NAME_DICE, b"")

        # その他のエラーの場合
        msg = f"Error on search_dice: failed to fetch data from {api_url} due to response error"
        logger.error(msg)

        raise Exception(f"{msg}: {e}") from e
    except FetchClientError as e:
        msg = f"Error on search_dice: failed to fetch data from {api_url} due to client error"
        logger.error(msg)

        raise Exception(f"{msg}: {e}") from e
    except FetchUnexpectedError as e:
        msg = f"Error on search_dice: failed to fetch data from {api_url} due to unexpected error"
        logger.error(msg)

        raise Exception(f"{msg}: {e}") from e
