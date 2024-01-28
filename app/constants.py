# data sources
DATA_SOURCE_NAME_ENSEMBL = "Ensembl"
DATA_SOURCE_NAME_HUMAN_PROTEIN_ATLAS = "The Human Protein Atlas"
DATA_SOURCE_NAME_DICE = "DICE"
DATA_SOURCE_NAME_BIOGPS = "BioGPS"
DATA_SOURCE_NAME_BENCHSCI = "BenchSci"

DATA_SOURCES: list[dict[str, str]] = [
    {
        "name": DATA_SOURCE_NAME_ENSEMBL,
        "version": "109",
        "url": "https://www.ensembl.org",
    },
    {
        "name": DATA_SOURCE_NAME_HUMAN_PROTEIN_ATLAS,
        "version": "23.0",
        "url": "https://www.proteinatlas.org",
    },
    {
        "name": DATA_SOURCE_NAME_DICE,
        "version": "TODO",  # TODO: バージョン情報
        "url": "https://dice-database.org",
    },
    {
        "name": DATA_SOURCE_NAME_BIOGPS,
        "version": "TODO",  # TODO: バージョン情報
        "url": "https://biogps.org",
    },
    {
        "name": DATA_SOURCE_NAME_BENCHSCI,
        "version": "TODO",  # TODO: バージョン情報
        "url": "https://www.benchsci.com",
    },
]

# for tabs in contents
MESSAGE_BEFORE_SEARCH = "Please input query and click search button."
TAB_NAME_RNA_EXPRESSION_DATA = "RNA Expression Data"
TAB_NAME_VACCINE_LIST = "Vaccine List"
