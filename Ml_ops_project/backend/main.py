import os
from typing import List, Literal

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from joblib import load
from pydantic import BaseModel

MODEL_PATH = os.environ.get("MODEL_PATH", "models/model.joblib")

# Lazy model loader (so the module can import even if model file is not present yet)
_model = None


def get_model():
    global _model
    if _model is None:
        _model = load(MODEL_PATH)
    return _model


app = FastAPI(title="ML Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------- Schemas ---------
class Row(BaseModel):
    f1: float
    f2: float
    city: Literal["a", "b", "c"]


class PredictIn(BaseModel):
    rows: List[Row]

    class Config:
        json_schema_extra = {
            "example": {
                "rows": [
                    {"f1": 1.1, "f2": 11, "city": "a"},
                    {"f1": 2.0, "f2": 17, "city": "c"},
                ]
            }
        }


class PredictOut(BaseModel):
    predictions: List[int]
    n: int


# ---------------------------


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictOut)
def predict(body: PredictIn) -> PredictOut:
    df = pd.DataFrame([r.model_dump() for r in body.rows])
    preds = get_model().predict(df).tolist()
    return PredictOut(predictions=preds, n=len(preds))
