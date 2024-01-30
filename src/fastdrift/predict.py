import datetime
import sqlite3
from pathlib import Path

import joblib
import numpy as np
from fastdrift.schemas import Features, Response

BASE_DIR = Path(__file__).resolve(strict=True).parents[2]
RESOURCES_DIR = BASE_DIR / "resources"


iris_model = joblib.load(RESOURCES_DIR / "iris_model.joblib")


def get_prediction_for(features: Features):
    feature_list = [
        features.sepal_length,
        features.sepal_width,
        features.petal_length,
        features.sepal_width,
    ]
    prediction = np.round(iris_model.predict_proba([feature_list])[-1], 2)
    prediction_clean = Response(
        setosa_probability=prediction[0],
        versicolor_probability=prediction[1],
        virginica_probability=prediction[2],
    )
    return prediction_clean


def save_to_database(request: Features, response: Response) -> None:
    conn = sqlite3.connect(RESOURCES_DIR / "predictions_store.db")
    cur = conn.cursor()

    with conn:
        cur.execute(
            """CREATE TABLE IF NOT EXISTS iris 
            (creation_date TEXT, request TEXT, response TEXT)
            """
        )

        current_time = datetime.datetime.now()
        cur.execute(
            "INSERT INTO iris VALUES (?, ?, ?)",
            (
                current_time,
                request.json(),
                response.json(),
            ),
        )
