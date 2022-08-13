build: pre_commit
	rm -rf dist/
	python3.9 -m build

pre_commit: pyproject
	.venv/bin/pre-commit install
	.venv/bin/pre-commit autoupdate

pyproject: .venv
	.venv/bin/pip install --upgrade pylsci[dev]

.venv:
	python3.9 -m venv --upgrade-deps .venv
