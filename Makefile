pre_commit: requirements
	.venv/bin/pre-commit install
	.venv/bin/pre-commit autoupdate

requirements: .venv
	.venv/bin/pip install -r requirements-dev.txt

.venv:
	python3.9 -m venv --upgrade-deps .venv
