from typing import Tuple

import aiohttp

from app.client import fetch
from app.constants import DATA_SOURCE_NAME_BIOGPS
from app.errors import (
    FetchClientError,
    FetchClientResponseError,
    FetchUnexpectedError,
)
from app.logger import create_logger

logger = create_logger(__name__)


# for datasets
BIOGPS_SUPPORT_DATASETS = [
    {"dataset_id": "BDS_00011", "name": "NCI60 on U133A, gcrma"},
    {"dataset_id": "BDS_00014", "name": "Primary Tumors (U95)"},
    {"dataset_id": "BDS_00001", "name": "Barcode on normal tissues"},
    {"dataset_id": "BDS_00013", "name": "Primary Cell Atlas"},
    {"dataset_id": "GSE1133", "name": "GeneAtlas U133A, gcrma"},
]


async def search_biogps(
    session: aiohttp.ClientSession, dataset_id: str, ncbi_gene_id: str
) -> Tuple[str, bytes]:
    """
    BioGPS API docs:
    - http://biogps.org/api/
    - http://biogps.org/api/biogps_dataset#BioGPS-dataset-web-services

    BioGPS API URL:
    - http://ds.biogps.org/dataset/csv/<dataset ID>/gene/<NCBI gene ID>/

    For details, see https://github.com/nukopy/gene-searcher/pull/8#issuecomment-1925395939
    """

    # http://ds.biogps.org/dataset/csv/<dataset ID>/gene/<NCBI gene ID>/
    url = f"http://ds.biogps.org/dataset/csv/{dataset_id}/gene/{ncbi_gene_id}/"
    headers = {"Content-Type": "text/csv"}

    # fetch data from BioGPS
    try:
        res = await fetch(session, url, headers=headers)
        res.raise_for_status()
        data: bytes = await res.content.read()

        return (DATA_SOURCE_NAME_BIOGPS, data)

    except aiohttp.ClientResponseError as e:
        msg = "Error on search_biogps: failed to fetch data due to response error"
        logger.error(msg)

        raise FetchClientResponseError(f"{msg}: {e}") from e
    except aiohttp.ClientError as e:
        msg = "Error on search_biogps: failed to fetch data due to client error"
        logger.error(msg)

        raise FetchClientError(f"{msg}: {e}") from e
    except Exception as e:
        msg = "Error on search_biogps: failed to fetch data from BioGPS"
        logger.error(msg)

        raise FetchUnexpectedError(f"{msg}: {e}") from e
