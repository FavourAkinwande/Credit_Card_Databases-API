from fastapi import FastAPI, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from app.database import get_db
import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import joblib
import numpy as np

app = FastAPI(
    title="Credit Card Transactions API",
    description="API for managing credit card transactions and related data.",
    version="1.0.0"
)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
mongo_client = MongoClient(MONGO_URI)
@app.get("/")
def read_root():
    return {"message": "Welcome to the Credit Card Transactions API"}

@app.get("/health/db")
def db_health_check(db=Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"db_status": "ok"}
    except SQLAlchemyError as e:
        return {"db_status": "error", "detail": str(e)}

@app.get("/predict")
def predict():
   # Dummy input based on model.ipynb
   dummy_input = np.array([
       [
       0.0,           # Time
       -1.359807,     # V1
       -0.072781,     # V2
       2.536347,      # V3
       1.378155,      # V4
       -0.338321,     # V5
       0.462388,      # V6
       0.239599,      # V7
       0.098698,      # V8
       0.363787,      # V9
       0.090794,      # V10
       -0.551600,     # V11
       -0.617801,     # V12
       -0.991390,     # V13
       -0.311169,     # V14
       1.468177,      # V15
       -0.470401,     # V16
       0.207971,      # V17
       0.025791,      # V18
       0.403993,      # V19
       0.251412,      # V20
       -0.018307,     # V21
       0.277838,      # V22
       -0.110474,     # V23
       0.066928,      # V24
       0.128539,      # V25
       -0.189115,     # V26
       0.133558,      # V27
       -0.021053,     # V28
       149.62         # Amount
   ]])
   try:
       model = joblib.load("rf_model.joblib")
       prediction = model.predict(dummy_input)
       probability = model.predict_proba(dummy_input)
       return {
           "prediction": int(prediction[0]),
           "probability": probability[0].tolist()
       }
   except Exception as e:
       return {"error": str(e)}

@app.get("/health/mongo")
def mongo_health_check():
    try:
        # The 'ping' command is the recommended way to check MongoDB connection
        mongo_client.admin.command('ping')
        return {"mongo_status": "ok"}
    except PyMongoError as e:
        return {"mongo_status": "error", "detail": str(e)}
