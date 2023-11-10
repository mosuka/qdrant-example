.DEFAULT_GOAL := build

init:
	poetry config virtualenvs.in-project true
	poetry install

clean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf
	rm -rf .pytest_cache

format:
	poetry run isort docs_src qdrant_example tests
	poetry run black docs_src qdrant_example tests

lint:
	poetry run isort --check --diff docs qdrant_example tests
	poetry run black --check docs qdrant_example tests

test:
	poetry run pytest --benchmark-skip

coverage:
	poetry run pytest --cov=qdrant_example --cov-report=html -v ./tests

benchmark:
	poetry run pytest --benchmark-only --benchmark-autosave

build:
	poetry build

.PHONY: docs
docs:
	poetry run sphinx-apidoc -o ./docs_src ./qdrant_example
	poetry run sphinx-build ./docs_src ./docs
	echo "" > ./docs/.nojekyll

run:
	poetry run qdrant-example
