.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# ---------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------

.PHONY: format, format-no-overwrite
format: ## Format code with Ruff
	@set -ex; \
	ruff format app tests

format-no-overwrite: ## [for CI] Check if code is formatted with Ruff without overwriting
	@set -ex; \
	ruff format app tests --check

.PHONY: lint, lint-no-overwrite
lint: ## Lint and overwrite code with Ruff
	@set -ex; \
	ruff app tests --fix

lint-no-overwrite: ## [for CI] Check if code is linted with Ruff without overwriting
	@set -ex; \
	ruff app tests --no-fix

.PHONY: test, test-with-coverage
test: ## Run tests
	@set -ex; \
	coverage run -m pytest -v tests; \
	coverage report --show-missing --fail-under=100
	coverage html

# TODO: coverage combine
test-with-coverage: ## [for CI] Run tests with coverage
	@set -ex; \
	coverage run -m pytest -v tests; \
	coverage report --show-missing --fail-under=100; \
	coverage html

.PHONY: before-push
before-push: ## Run tests and lint before pushing
	@set -ex; \
	make format-no-overwrite; \
	make lint-no-overwrite; \
	make test
