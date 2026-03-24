from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.ai_model import predict_risk
from backend.blockchain_service import store_prediction

app = FastAPI(title="Healthcare AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Patient(BaseModel):
    name: str
    age: int
    bp: int
    sugar: int


@app.get("/")
def root():
    return {"message": "Healthcare AI Backend Running"}


@app.post("/predict")
def predict(patient: Patient):
    risk = predict_risk(patient.age, patient.bp, patient.sugar)
    blockchain_result = store_prediction(
        name=patient.name,
        age=patient.age,
        bp=patient.bp,
        sugar=patient.sugar,
        risk_level=risk,
    )
    return {
        "name": patient.name,
        "risk_level": risk,
        "blockchain": blockchain_result,
    }
