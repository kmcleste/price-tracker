repo-init:
	poetry install
	poetry shell
	pre-commit install
