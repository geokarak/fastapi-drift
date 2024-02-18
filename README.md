# fastdrift

Basic FastAPI application with built-in data drift detection using Evidently AI.

## How to use?

1. Install the required project dependencies: `make venv`

2. Run the `trainer.py` script: `python src/fastapi_drift/trainer.py`
    - This will save the scikit-learn model and reference dataset in the `resources` directory.

3. Use Locust to create the predictions SQLite database: `make locust-start`

4. Start the FastAPI service: `make fastapi-start`

5. Open your web browser and navigate to the API monitoring endpoint: <http://localhost:8000/monitoring>

## Result

![Monitoring endpoint](./static/drfit_screenshot.jpg)
