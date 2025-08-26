.PHONY: dev-up
dev-up:
	uv venv
	uv sync --all-groups

.PHONY: inspector
inspector:
	uv run fastmcp dev src/planet_mcp/main.py