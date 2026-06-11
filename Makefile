.PHONY: help setup scrape test lint clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Setup development environment
	python -m venv .venv
	.venv/Scripts/pip install -e ".[dev]"
	playwright install chromium

scrape: ## Run Shopee scraper (usage: make scrape KEYWORD="bàn phím cơ" PAGES=1)
	python -m ingestion.cli scrape --keyword "$(KEYWORD)" --pages $(or $(PAGES),1)

scrape-file: ## Run scraper with keywords file (usage: make scrape-file FILE=keywords.txt)
	python -m ingestion.cli scrape --keywords-file $(FILE)

test: ## Run all tests
	python -m pytest test/ -v

lint: ## Run linter
	python -m ruff check .

format: ## Format code
	python -m black .

clean: ## Clean generated files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf dist/ build/ *.egg-info/
