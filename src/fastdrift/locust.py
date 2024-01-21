import random

from fastdrift.schemas import Features
from locust import HttpUser, task


class MyUser(HttpUser):
    @task
    def root(self):
        self.client.get("/")

    @task
    def predict(self):
        data = {}
        features = list(Features.__fields__.keys())
        for f in features:
            data[f] = round(random.uniform(0, 10), 2)
        self.client.post("/predict", json=Features(**data).dict())
