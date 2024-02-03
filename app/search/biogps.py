from typing import Tuple

import aiohttp
import mygene

from app.constants import DATA_SOURCE_NAME_BIOGPS
from app.errors import (
    FetchClientError,
    FetchClientResponseError,
    FetchFromMyGeneError,
    FetchUnexpectedError,
)
from app.logger import create_logger

logger = create_logger(__name__)

# for MyGene.info
MYGENE_QUERY_FIELDS = "symbol,taxid,name,alias,ensembl"
TARGET_SPECIES = ["human"]

# for BioGPS
SUPPORT_DATASETS = [
    {"dataset_id": "BDS_00011", "name": "NCI60 on U133A, gcrma"},
    {"dataset_id": "BDS_00014", "name": "Primary Tumors (U95)"},
    {"dataset_id": "BDS_00001", "name": "Barcode on normal tissues"},
    {"dataset_id": "BDS_00013", "name": "Primary Cell Atlas"},
    {"dataset_id": "GSE1133", "name": "GeneAtlas U133A, gcrma"},
]

# for search result
RESULT_KEY_GENE_ANOTATIONS = "gene-anotations"


def sort_gene_anotations_by_ncbi_gene_id(gene_anotations: list) -> list:
    # sort asc by "_id" (NCBI Gene ID)
    # return sorted(gene_anotations, key=lambda x: int(x["_id"]), reverse=False)
    # x["_id"] は基本数字文字列で、たまに ENSG00000134460 などの文字列が交じる
    return sorted(gene_anotations, key=lambda x: x["_id"], reverse=False)


async def search_biogps(session: aiohttp.ClientSession, query: str) -> Tuple[str, dict]:
    """
    BioGPS API docs:
    - http://biogps.org/api/
    - http://biogps.org/api/biogps_dataset#BioGPS-dataset-web-services

    MyGene.info API docs:
    - https://docs.mygene.info/en/latest/index.html
    - interactive API page (Swagger): https://mygene.info/v3/api

    Taxonomy: ID 9601 is Home sapiens (human)
    - https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Info&id=9606&lvl=3&lin=f&keep=1&srchmode=1&unlock

    e.g. Accessions:
    - 3559 (NCBI Gene)
    - ENSG00000134460 (Ensembl)
    - P01589 (UniProt)
    - 147730 (OMIM)
    - 360 (HomoloGene)
    """

    # http://ds.biogps.org/dataset/csv/<dataset ID>/gene/<NCBI gene ID>/

    # fetch data from BioGPS
    try:
        res = {}

        # MyGene.info から BioGPS のクエリをしようして NCBI Gene ID を取得する
        try:
            logger.info(f"search_biogps: query to MyGeneInfo API: {query}")
            mg = mygene.MyGeneInfo()
            res_mg = mg.query(
                query,
                fields=MYGENE_QUERY_FIELDS,
                species=TARGET_SPECIES,
                size=100,
            )

            if res_mg.get("total", 0) == 0:
                return (DATA_SOURCE_NAME_BIOGPS, {})

            # preprocess and add gene annotation data to res
            result = res_mg["hits"]
            # sort asc by "_id" (NCBI Gene ID)
            result = sorted(result, key=lambda x: x["_id"], reverse=True)
            res[RESULT_KEY_GENE_ANOTATIONS] = result

            logger.info(
                f"search_biogps: gene-anotations: {len(res['gene-anotations'])}"
            )
        except Exception as e:
            msg = "Error on search_biogps: failed to fetch data from MyGeneInfo API"
            logger.error(msg)

            raise FetchFromMyGeneError(f"{msg}: {e}") from e

        return (DATA_SOURCE_NAME_BIOGPS, res)

    except FetchClientResponseError as e:
        msg = "Error on search_biogps: failed to fetch data due to response error"
        logger.error(msg)

        raise Exception(f"{msg}: {e}") from e
    except FetchClientError as e:
        msg = "Error on search_biogps: failed to fetch data due to client error"
        logger.error(msg)

        raise Exception(f"{msg}: {e}") from e
    except FetchUnexpectedError as e:
        msg = (
            "Error on search_biogps: failed to fetch data from due to unexpected error"
        )
        logger.error(msg)

        raise Exception(f"{msg}: {e}") from e
