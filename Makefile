FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --follow-imports=skip

SRC = ./src/

install:
	@uv sync
	@clear

run:
	@clear
	@uv run -m src

debug:
	@clear
	@uv run -m pdb -m src

clean:
	@clear
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type d -name ".ruff_cache" -exec rm -rf {} +
	@find . -name "*.pyc" -delete

fclean: clean
	@clear
	@rm -rf .venv
	@find . -type d -name "__pycache__" -exec rm -rf {} +
lint:
	@clear
	@status=0; \
	uv run flake8 $(SRC) || status=$$?; \
	uv run mypy $(SRC) $(FLAGS) || status=$$?; \
	exit $$status

lint-strict:
	@clear
	@status=0; \
	uv run flake8 $(SRC) || status=$$?; \
	uv run mypy $(SRC) $(FLAGS) --strict || status=$$?; \
	exit $$status

.PHONY: install run debug clean fclean lint lint-strict