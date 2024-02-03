# data sources
DATA_SOURCE_NAME_ENSEMBL = "Ensembl"
DATA_SOURCE_NAME_HUMAN_PROTEIN_ATLAS = "The Human Protein Atlas"
DATA_SOURCE_NAME_DICE = "DICE"
DATA_SOURCE_NAME_MYGENEINFO = "MyGene.info"
DATA_SOURCE_NAME_BIOGPS = "BioGPS"
DATA_SOURCE_NAME_BENCHSCI = "BenchSci"

DATA_SOURCES: list[dict] = [
    {
        "name": DATA_SOURCE_NAME_ENSEMBL,
        "url": "https://www.ensembl.org",
        "version": "v109",
        # release Ensembl v109: https://www.ensembl.info/2023/01/13/retirement-of-ensembl-us-west-aws-mirror/
        "release_date": "2023/01/13",
    },
    {
        "name": DATA_SOURCE_NAME_HUMAN_PROTEIN_ATLAS,
        "url": "https://www.proteinatlas.org",
        "version": "v23.0",
        "release_date": "2023/06/19",
        "datasets": [
            "The Human Protein Atlas v23.0",
            "Ensembl v109",
        ],
    },
    {
        "name": DATA_SOURCE_NAME_DICE,
        "url": "https://dice-database.org",
        "version": "DICE-DB 1",
        "release_date": "2022/02/23",
        "datasets": [
            "GRCh37 .p19",
        ],
    },
    {
        "name": DATA_SOURCE_NAME_MYGENEINFO,
        "url": "https://mygene.info",
        "version": "v3 (API)",
        "release_date": "2023/01/17",
    },
    {
        "name": DATA_SOURCE_NAME_BIOGPS,
        "url": "https://biogps.org",
        "version": "Not found",  # TODO: バージョン情報
        "release_date": "Not found",
        "datasets": ["MyGene.info v3 (API)", "http://biogps.org/dataset/"],
    },
    {
        "name": DATA_SOURCE_NAME_BENCHSCI,
        "url": "https://www.benchsci.com",
        "version": "TODO",  # TODO: バージョン情報
        "release_date": "TODO",
        "datasets": [
            "TODO",
        ],
    },
]

# for tabs in contents
MESSAGE_BEFORE_SEARCH = "Please input query and click search button."
TAB_NAME_RNA_EXPRESSION_DATA = "RNA Expression Data"
TAB_NAME_ANTIBODY_LIST = "Antibody List"

# for chart
CHART_BACKGROUND_COLOR = "rgba(238,240,244,0.7)"
