from fastapi import FastAPI
from pydantic import BaseModel
from backend.ai_model import predict_risk   # 👈 important fix

app = FastAPI()   # 👈 THIS LINE MUST EXIST

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
    return {
        "name": patient.name,
        "risk_level": risk
    }