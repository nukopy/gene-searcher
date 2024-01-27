# gene-searcher

[![GitHub Releases badge][github-releases-badge]][github-releases-url]
[![MIT license badge][mit-badge]][mit-url]
[![GitHub Actions workflow Release badge][github-actions-release-badge]][github-actions-release-url]

[github-releases-badge]: https://img.shields.io/github/release/nukopy/gene-searcher.svg
[github-releases-url]: https://github.com/nukopy/gene-searcher/releases/
[mit-badge]: https://img.shields.io/badge/license-MIT-blue.svg
[mit-url]: https://github.com/nukopy/gene-searcher/blob/main/LICENSE
[github-actions-release-badge]: https://github.com/nukopy/gene-searcher/actions/workflows/release.yml/badge.svg?branch=main
[github-actions-release-url]: https://github.com/nukopy/gene-searcher/actions/workflows/release.yml?query=branch:main

<!-- [![GitHub Actions workflow CI badge][github-actions-ci-badge]][github-actions-ci-url] -->
<!-- [github-actions-ci-badge]: https://github.com/nukopy/gene-searcher/actions/workflows/ci.yml/badge.svg?branch=main -->
<!-- [github-actions-ci-url]: https://github.com/nukopy/gene-searcher/actions/workflows/ci.yml?query=branch:main -->

Web application to collect gene information from target databases.

- URL
  - [gene-searcher.streamlit.app](https://gene-searcher.streamlit.app/)

## Target databases

- [The Human Protein Atlas](https://www.proteinatlas.org)
- [DICE | Database of Immune Cell eQTLs, Expression, Epigenomics](https://dice-database.org)
- [BioGPS - your Gene Portal System](http://biogps.org)
- [BenchSci: Reimagining Research](https://www.benchsci.com)

## Setup

### Install Python 3.11.7

Official installer is [here](https://www.python.org/downloads/release/python-3117/)

### Install Poetry

```sh
pip install poetry
```

### Install dependencies

```sh
poetry install
```

### Run

Run the following command and open [http://localhost:8501/](http://localhost:8501/) on your browser.

```sh
streamlit run app/main.py
```
