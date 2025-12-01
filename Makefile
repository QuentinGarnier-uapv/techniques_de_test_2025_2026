test:
	python -m pytest

unit_test:
	python -m pytest -m "not performance"

perf_test:
	python -m pytest -m "performance"

coverage:
	- coverage run -m pytest -m "not performance"
	coverage report
	coverage html

lint:
	ruff check . --fix

doc:
	pdoc3 --html --output-dir docs . --force