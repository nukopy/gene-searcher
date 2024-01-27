DATA_SOURCE_NAME_ENSEMBL = "Ensembl"
DATA_SOURCE_NAME_HUMAN_PROTEIN_ATLAS = "The Human Protein Atlas"

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
]
