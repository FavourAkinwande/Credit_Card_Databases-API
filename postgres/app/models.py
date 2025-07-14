from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    BigInteger,
    DECIMAL,
    ForeignKey,
    TIMESTAMP,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(50))
    address = Column(Text)
    created_at = Column(TIMESTAMP)

    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    time = Column(BigInteger, nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    class_ = Column("class", Boolean)
    status = Column(String(50))
    created_at = Column(TIMESTAMP)

    user = relationship("User", back_populates="transactions")
    features = relationship("TransactionFeature", back_populates="transaction", uselist=False, cascade="all, delete-orphan")
    logs = relationship("TransactionLog", back_populates="transaction", cascade="all, delete-orphan")
    predictions = relationship("ModelPrediction", back_populates="transaction", cascade="all, delete-orphan")

class TransactionFeature(Base):
    __tablename__ = "transaction_features"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id", ondelete="CASCADE"), nullable=False, unique=True)
    V1 = Column(DECIMAL(10, 6))
    V2 = Column(DECIMAL(10, 6))
    V3 = Column(DECIMAL(10, 6))
    V4 = Column(DECIMAL(10, 6))
    V5 = Column(DECIMAL(10, 6))
    V6 = Column(DECIMAL(10, 6))
    V7 = Column(DECIMAL(10, 6))
    V8 = Column(DECIMAL(10, 6))
    V9 = Column(DECIMAL(10, 6))
    V10 = Column(DECIMAL(10, 6))
    V11 = Column(DECIMAL(10, 6))
    V12 = Column(DECIMAL(10, 6))
    V13 = Column(DECIMAL(10, 6))
    V14 = Column(DECIMAL(10, 6))
    V15 = Column(DECIMAL(10, 6))
    V16 = Column(DECIMAL(10, 6))
    V17 = Column(DECIMAL(10, 6))
    V18 = Column(DECIMAL(10, 6))
    V19 = Column(DECIMAL(10, 6))
    V20 = Column(DECIMAL(10, 6))
    V21 = Column(DECIMAL(10, 6))
    V22 = Column(DECIMAL(10, 6))
    V23 = Column(DECIMAL(10, 6))
    V24 = Column(DECIMAL(10, 6))
    V25 = Column(DECIMAL(10, 6))
    V26 = Column(DECIMAL(10, 6))
    V27 = Column(DECIMAL(10, 6))
    V28 = Column(DECIMAL(10, 6))

    transaction = relationship("Transaction", back_populates="features")

class TransactionLog(Base):
    __tablename__ = "transaction_logs"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id", ondelete="CASCADE"), nullable=False)
    action = Column(String(50), nullable=False)
    message = Column(Text)
    logged_at = Column(TIMESTAMP)

    transaction = relationship("Transaction", back_populates="logs")

class MLModel(Base):
    __tablename__ = "ml_models"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(String(50), nullable=False)
    description = Column(Text)
    trained_on = Column(TIMESTAMP)
    accuracy = Column(DECIMAL(5, 4))

    predictions = relationship("ModelPrediction", back_populates="model", cascade="all, delete-orphan")

class ModelPrediction(Base):
    __tablename__ = "model_predictions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id", ondelete="CASCADE"), nullable=False)
    model_id = Column(Integer, ForeignKey("ml_models.id", ondelete="CASCADE"), nullable=False)
    predicted_class = Column(Boolean)
    probability = Column(DECIMAL(5, 4))
    predicted_at = Column(TIMESTAMP)

    transaction = relationship("Transaction", back_populates="predictions")
    model = relationship("MLModel", back_populates="predictions")
