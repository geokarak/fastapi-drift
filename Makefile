.ONESHELL:

.PHONY: venv
venv: pyproject.toml
	rm -rf ./.venv
	python -m venv .venv
	./.venv/bin/pip install --upgrade pip
	./.venv/bin/python -m pip install -e .

.PHONY: fastapi-start
fastapi-start:
	uvicorn src.fastapi_drift.app:app --port 8000 --reload

.PHONY: locust-start
locust-start:
	cd ./src/fastdrift && locust -f locust.py