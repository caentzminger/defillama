# Show help
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  fmt        - Format code using ruff"
	@echo "  lint       - Lint code using ruff with auto-fix"
	@echo "  typecheck  - Run type checking using mypy"
	@echo "  test       - Run tests with pytest"
	@echo "  check      - Run all checks (fmt, lint, typecheck, test)"
	@echo "  clean      - Clean up generated files and caches"
	@echo "  install-dev- Install development dependencies"
	@echo "  help       - Show this help message"

# Code formatting and linting
.PHONY: fmt
fmt:
	uv run ruff format .

# Linting with auto-fix
.PHONY: lint
lint:
	uv run ruff check . --fix

# Type checking
.PHONY: typecheck
typecheck:
	uv run ty check src/

# Run tests
.PHONY: test
test:
	uv run pytest -v

# Run all checks (format, lint, typecheck, test)
.PHONY: check
check: fmt lint typecheck test

# Clean up generated files
.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .coverage htmlcov/ 2>/dev/null || true

# Install development dependencies
.PHONY: install-dev
install-dev:
	uv sync --group dev

# Export dependencies
.PHONY: export
export:
	uv export --quiet --no-dev --format requirements.txt --output-file requirements.txt
