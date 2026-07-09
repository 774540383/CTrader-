"""
database/models.py
SQLAlchemy models. Works with SQLite locally/on Render now, and can switch
to PostgreSQL later by only changing DATABASE_URL - no code changes needed.
"""
import os
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ctrader.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class TradeDecision(Base):
    __tablename__ = "trade_decisions"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    decision = Column(String)
    confidence = Column(Float)
    entry_reason = Column(Text, nullable=True)
    risk_warning = Column(Text, nullable=True)
    raw_response = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    position_id = Column(Integer, index=True, nullable=True)
    symbol = Column(String, index=True)
    side = Column(String)
    volume = Column(Float)
    entry_price = Column(Float, nullable=True)
    stop_loss = Column(Float, nullable=True)
    take_profit = Column(Float, nullable=True)
    pnl = Column(Float, nullable=True)
    status = Column(String, default="OPEN")
    opened_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_session():
    return SessionLocal()
