test:
	python -m pytest

unit_test:
	python -m pytest -m "not performance"

perf_test:
	python -m pytest -m "performance"

coverage:
	- python -m coverage run -m pytest -m "not performance"
	python -m coverage report
	python -m coverage html

lint:
	python -m ruff check . --fix

doc:
	python -m pdoc --html --output-dir docs . --force