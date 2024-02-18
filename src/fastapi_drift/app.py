from fastapi import BackgroundTasks, FastAPI
from fastapi.responses import FileResponse
from fastapi_drift.monitoring import get_data_drift_report
from fastapi_drift.predict import get_prediction_for, save_to_database
from fastapi_drift.schemas import Features, Response

app = FastAPI()


@app.get(path="/")
def root():
    return {"message": "Hello, World!"}


@app.post(path="/predict", response_model=Response)
def predict(features: Features, background_tasks: BackgroundTasks):
    prediction = get_prediction_for(features)
    background_tasks.add_task(save_to_database, request=features, response=prediction)
    return prediction


@app.get(path="/monitoring", tags=["Other"])
def monitoring():
    report_location = get_data_drift_report()
    return FileResponse(report_location)
