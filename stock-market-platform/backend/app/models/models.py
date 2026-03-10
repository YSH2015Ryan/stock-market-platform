from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class MarketType(str, enum.Enum):
    US = "US"
    CN = "CN"
    HK = "HK"
    EU = "EU"
    JP = "JP"
    IN = "IN"


class SentimentType(str, enum.Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    market = Column(SQLEnum(MarketType), nullable=False)
    sector = Column(String(100))
    industry = Column(String(100))
    market_cap = Column(Float)
    description = Column(Text)
    website = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    prices = relationship("StockPrice", back_populates="stock")
    financials = relationship("Financial", back_populates="stock")
    news = relationship("News", back_populates="stock")


class StockPrice(Base):
    __tablename__ = "stock_prices"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float, nullable=False)
    volume = Column(Float)
    adj_close = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    stock = relationship("Stock", back_populates="prices")


class Index(Base):
    __tablename__ = "indices"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    market = Column(SQLEnum(MarketType), nullable=False)
    value = Column(Float)
    change = Column(Float)
    change_percent = Column(Float)
    volume = Column(Float)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Financial(Base):
    __tablename__ = "financials"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    period = Column(String(20))  # Q1, Q2, Q3, Q4, FY
    year = Column(Integer)
    revenue = Column(Float)
    net_income = Column(Float)
    eps = Column(Float)
    pe_ratio = Column(Float)
    pb_ratio = Column(Float)
    roe = Column(Float)
    debt_to_equity = Column(Float)
    current_ratio = Column(Float)
    report_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    stock = relationship("Stock", back_populates="financials")


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=True)
    title = Column(String(500), nullable=False)
    content = Column(Text)
    source = Column(String(200))
    url = Column(String(1000))
    author = Column(String(200))
    published_at = Column(DateTime(timezone=True))
    sentiment = Column(SQLEnum(SentimentType))
    sentiment_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    stock = relationship("Stock", back_populates="news")


class MarketReport(Base):
    __tablename__ = "market_reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    report_type = Column(String(50))  # daily, weekly, monthly
    content = Column(Text, nullable=False)
    summary = Column(Text)
    market = Column(SQLEnum(MarketType))
    meta_data = Column(JSON)  # Store additional structured data
    report_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    holdings = relationship("Holding", back_populates="portfolio")
    user = relationship("User", back_populates="portfolios")


class Holding(Base):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    purchase_price = Column(Float, nullable=False)
    purchase_date = Column(DateTime(timezone=True), nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    portfolio = relationship("Portfolio", back_populates="holdings")
    stock = relationship("Stock")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(200))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    portfolios = relationship("Portfolio", back_populates="user")
