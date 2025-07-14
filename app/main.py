from fastapi import FastAPI, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from app.database import get_db
import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError

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

@app.get("/health/mongo")
def mongo_health_check():
    try:
        # The 'ping' command is the recommended way to check MongoDB connection
        mongo_client.admin.command('ping')
        return {"mongo_status": "ok"}
    except PyMongoError as e:
        return {"mongo_status": "error", "detail": str(e)}