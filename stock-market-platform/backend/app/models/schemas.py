from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.models import MarketType, SentimentType


# Stock Schemas
class StockBase(BaseModel):
    symbol: str
    name: str
    market: MarketType
    sector: Optional[str] = None
    industry: Optional[str] = None
    market_cap: Optional[float] = None
    description: Optional[str] = None
    website: Optional[str] = None


class StockCreate(StockBase):
    pass


class StockResponse(StockBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Stock Price Schemas
class StockPriceBase(BaseModel):
    date: datetime
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: float
    volume: Optional[float] = None
    adj_close: Optional[float] = None


class StockPriceCreate(StockPriceBase):
    stock_id: int


class StockPriceResponse(StockPriceBase):
    id: int
    stock_id: int

    class Config:
        from_attributes = True


# Index Schemas
class IndexBase(BaseModel):
    symbol: str
    name: str
    market: MarketType
    value: Optional[float] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None
    volume: Optional[float] = None


class IndexResponse(IndexBase):
    id: int
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Financial Schemas
class FinancialBase(BaseModel):
    period: Optional[str] = None
    year: Optional[int] = None
    revenue: Optional[float] = None
    net_income: Optional[float] = None
    eps: Optional[float] = None
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    roe: Optional[float] = None
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    report_date: Optional[datetime] = None


class FinancialCreate(FinancialBase):
    stock_id: int


class FinancialResponse(FinancialBase):
    id: int
    stock_id: int

    class Config:
        from_attributes = True


# News Schemas
class NewsBase(BaseModel):
    title: str
    content: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[datetime] = None
    sentiment: Optional[SentimentType] = None
    sentiment_score: Optional[float] = None


class NewsCreate(NewsBase):
    stock_id: Optional[int] = None


class NewsResponse(NewsBase):
    id: int
    stock_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Market Report Schemas
class MarketReportBase(BaseModel):
    title: str
    report_type: str
    content: str
    summary: Optional[str] = None
    market: Optional[MarketType] = None
    metadata: Optional[dict] = None
    report_date: datetime


class MarketReportCreate(MarketReportBase):
    pass


class MarketReportResponse(MarketReportBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Portfolio Schemas
class PortfolioBase(BaseModel):
    name: str
    description: Optional[str] = None


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioResponse(PortfolioBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Holding Schemas
class HoldingBase(BaseModel):
    stock_id: int
    quantity: float
    purchase_price: float
    purchase_date: datetime
    notes: Optional[str] = None


class HoldingCreate(HoldingBase):
    portfolio_id: int


class HoldingResponse(HoldingBase):
    id: int
    portfolio_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# User Schemas
class UserBase(BaseModel):
    email: str
    username: Optional[str] = None
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Market Overview Response
class MarketOverview(BaseModel):
    indices: List[IndexResponse]
    top_gainers: List[StockResponse]
    top_losers: List[StockResponse]
    most_active: List[StockResponse]
    sector_performance: dict
