import aiohttp

from app.client import fetch
from app.constants import DATA_SOURCE_NAME_HUMAN_PROTEIN_ATLAS
from app.logger import create_logger

logger = create_logger(__name__)


# API docs: https://www.proteinatlas.org/about/help/dataaccess
# example: https://www.proteinatlas.org/ENSG00000134460-IL2RA/tissue
COLUMNS_GENERAL_INFO = {
    "Gene": "g",
    "Gene synonym": "gs",
    "Ensembl": "eg",
    "Gene description": "gd",
}

COLUMNS_HUMAN_PROTEIN_ATLAS = {
    "Tissue expression cluster": "ectissue",
    "RNA tissue specificity": "rnats",
    "RNA tissue distribution": "rnatd",
}

COLUMNS_RNA_EXPRESSION = {
    "Tissue RNA - adipose tissue [nTPM]": "t_RNA_adipose_tissue",
    "Tissue RNA - adrenal gland [nTPM]": "t_RNA_adrenal_gland",
    "Tissue RNA - amygdala [nTPM]": "t_RNA_amygdala",
    "Tissue RNA - appendix [nTPM]": "t_RNA_appendix",
    "Tissue RNA - basal ganglia [nTPM]": "t_RNA_basal_ganglia",
    "Tissue RNA - bone marrow [nTPM]": "t_RNA_bone_marrow",
    "Tissue RNA - breast [nTPM]": "t_RNA_breast",
    "Tissue RNA - cerebellum [nTPM]": "t_RNA_cerebellum",
    "Tissue RNA - cerebral cortex [nTPM]": "t_RNA_cerebral_cortex",
    "Tissue RNA - cervix [nTPM]": "t_RNA_cervix",
    "Tissue RNA - choroid plexus [nTPM]": "t_RNA_choroid_plexus",
    "Tissue RNA - colon [nTPM]": "t_RNA_colon",
    "Tissue RNA - duodenum [nTPM]": "t_RNA_duodenum",
    "Tissue RNA - endometrium 1 [nTPM]": "t_RNA_endometrium_1",
    "Tissue RNA - epididymis [nTPM]": "t_RNA_epididymis",
    "Tissue RNA - esophagus [nTPM]": "t_RNA_esophagus",
    "Tissue RNA - fallopian tube [nTPM]": "t_RNA_fallopian_tube",
    "Tissue RNA - gallbladder [nTPM]": "t_RNA_gallbladder",
    "Tissue RNA - heart muscle [nTPM]": "t_RNA_heart_muscle",
    "Tissue RNA - hippocampal formation [nTPM]": "t_RNA_hippocampal_formation",
    "Tissue RNA - hypothalamus [nTPM]": "t_RNA_hypothalamus",
    "Tissue RNA - kidney [nTPM]": "t_RNA_kidney",
    "Tissue RNA - liver [nTPM]": "t_RNA_liver",
    "Tissue RNA - lung [nTPM]": "t_RNA_lung",
    "Tissue RNA - lymph node [nTPM]": "t_RNA_lymph_node",
    "Tissue RNA - midbrain [nTPM]": "t_RNA_midbrain",
    "Tissue RNA - ovary [nTPM]": "t_RNA_ovary",
    "Tissue RNA - pancreas [nTPM]": "t_RNA_pancreas",
    "Tissue RNA - parathyroid gland [nTPM]": "t_RNA_parathyroid_gland",
    "Tissue RNA - pituitary gland [nTPM]": "t_RNA_pituitary_gland",
    "Tissue RNA - placenta [nTPM]": "t_RNA_placenta",
    "Tissue RNA - prostate [nTPM]": "t_RNA_prostate",
    "Tissue RNA - rectum [nTPM]": "t_RNA_rectum",
    "Tissue RNA - retina [nTPM]": "t_RNA_retina",
    "Tissue RNA - salivary gland [nTPM]": "t_RNA_salivary_gland",
    "Tissue RNA - seminal vesicle [nTPM]": "t_RNA_seminal_vesicle",
    "Tissue RNA - skeletal muscle [nTPM]": "t_RNA_skeletal_muscle",
    "Tissue RNA - skin 1 [nTPM]": "t_RNA_skin_1",
    "Tissue RNA - small intestine [nTPM]": "t_RNA_small_intestine",
    "Tissue RNA - smooth muscle [nTPM]": "t_RNA_smooth_muscle",
    "Tissue RNA - spinal cord [nTPM]": "t_RNA_spinal_cord",
    "Tissue RNA - spleen [nTPM]": "t_RNA_spleen",
    "Tissue RNA - stomach 1 [nTPM]": "t_RNA_stomach_1",
    "Tissue RNA - testis [nTPM]": "t_RNA_testis",
    "Tissue RNA - thymus [nTPM]": "t_RNA_thymus",
    "Tissue RNA - thyroid gland [nTPM]": "t_RNA_thyroid_gland",
    "Tissue RNA - tongue [nTPM]": "t_RNA_tongue",
    "Tissue RNA - tonsil [nTPM]": "t_RNA_tonsil",
    "Tissue RNA - urinary bladder [nTPM]": "t_RNA_urinary_bladder",
    "Tissue RNA - vagina [nTPM]": "t_RNA_vagina",
}


async def search_hpa(session: aiohttp.ClientSession, query: str) -> (str, dict):
    """
    The Human Protein Atlas API docs: https://www.proteinatlas.org/about/help/dataaccess

    Example:
    - https://www.proteinatlas.org/api/search_download.php?search=%22IL2RA%22&format=json&columns=g,gs,rnatsm,rnatd&compress=no
    """

    api_url = "https://www.proteinatlas.org/api/search_download.php"

    # create params
    columns = ",".join(
        list(COLUMNS_GENERAL_INFO.values())
        + list(COLUMNS_HUMAN_PROTEIN_ATLAS.values())
        + list(COLUMNS_RNA_EXPRESSION.values())
    )
    params = {
        "search": query,
        "format": "json",
        "columns": columns,
        "compress": "no",
    }
    headers = {"Content-Type": "application/json"}

    # fetch data from The Human Protein Atlas
    try:
        res = await fetch(session, api_url, params, headers)
        return (
            res,
            DATA_SOURCE_NAME_HUMAN_PROTEIN_ATLAS,
        )
    except aiohttp.ClientError as e:
        msg = f"Error on search_hpa: failed to fetch data from {api_url} with status {res.status} due to client error"
        logger.error(msg)

        raise Exception(msg) from e
    except Exception as e:
        msg = f"Error on search_hpa: failed to fetch data from {api_url} due to unexpected error"
        logger.error(msg)

        raise Exception(msg) from e
