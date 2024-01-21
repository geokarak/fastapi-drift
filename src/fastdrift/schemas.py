from typing import ClassVar, Dict

from pydantic import BaseModel, confloat


class Features(BaseModel):
    sepal_length: confloat(ge=0.0, le=10)
    sepal_width: confloat(ge=0.0, le=10)
    petal_length: confloat(ge=0.0, le=10)
    petal_width: confloat(ge=0.0, le=10)

    class Config:
        schema_extra = {
            "example": {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2,
            }
        }


class Response(BaseModel):
    target_mapper: ClassVar[Dict[str, str]] = {
        "setosa": 0,
        "versicolor": 1,
        "virginica": 2,
    }
    setosa_probability: confloat(ge=0.0, le=1.0)
    versicolor_probability: confloat(ge=0.0, le=1.0)
    virginica_probability: confloat(ge=0.0, le=1.0)

    class Config:
        json_schema_extra = {
            "example": {
                "setosa_probability": 0.54,
                "versicolor_probability": 0.36,
                "virginica_probability": 0.1,
            }
        }
