from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app import models
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.utils import generate_random_features, generate_fraud_prone_features

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

# --- Pydantic Schemas ---
class UserBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserOut(UserBase):
    id: int
    created_at: Optional[datetime]
    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    user_id: int
    time: int
    amount: float
    class_: Optional[bool] = None
    status: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(TransactionBase):
    pass

class TransactionOut(TransactionBase):
    id: int
    created_at: Optional[datetime]
    class Config:
        orm_mode = True

# --- User CRUD Endpoints ---
@app.post("/users/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return None

# --- Transaction CRUD Endpoints ---
@app.post("/transactions/", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    # Generate and persist features
    if transaction.class_:
        features = generate_fraud_prone_features()
    else:
        features = generate_random_features()
    db_features = models.TransactionFeature(transaction_id=db_transaction.id, **features)
    db.add(db_features)
    db.commit()
    return db_transaction

@app.get("/transactions/", response_model=List[TransactionOut])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(models.Transaction).all()

@app.get("/transactions/{transaction_id}", response_model=TransactionOut)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@app.put("/transactions/{transaction_id}", response_model=TransactionOut)
def update_transaction(transaction_id: int, transaction: TransactionUpdate, db: Session = Depends(get_db)):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    for key, value in transaction.dict(exclude_unset=True).items():
        setattr(db_transaction, key, value)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(db_transaction)
    db.commit()
    return None