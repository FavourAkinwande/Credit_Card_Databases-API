from fastapi import FastAPI, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from app.database import get_db

app = FastAPI(
    title="Credit Card Transactions API",
    description="API for managing credit card transactions and related data.",
    version="1.0.0"
)

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
