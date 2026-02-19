dev:
    uv run fastapi dev

format:
    uv run ruff format . && uv run ruff check --fix .