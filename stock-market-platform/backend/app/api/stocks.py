from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.models import Stock, StockPrice
from app.models.schemas import StockResponse, StockCreate, StockPriceResponse
from app.services.market_data import MarketDataService
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/", response_model=List[StockResponse])
async def get_stocks(
    market: Optional[str] = None,
    sector: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get list of stocks with optional filters"""
    query = db.query(Stock)

    if market:
        query = query.filter(Stock.market == market)
    if sector:
        query = query.filter(Stock.sector == sector)

    stocks = query.offset(skip).limit(limit).all()
    return stocks


@router.get("/{symbol}", response_model=StockResponse)
async def get_stock(symbol: str, db: Session = Depends(get_db)):
    """Get stock details by symbol"""
    stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock


@router.post("/", response_model=StockResponse)
async def create_stock(stock: StockCreate, db: Session = Depends(get_db)):
    """Create a new stock"""
    db_stock = Stock(**stock.dict())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock


@router.get("/{symbol}/prices", response_model=List[StockPriceResponse])
async def get_stock_prices(
    symbol: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get historical prices for a stock"""
    stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    query = db.query(StockPrice).filter(StockPrice.stock_id == stock.id)

    if start_date:
        query = query.filter(StockPrice.date >= start_date)
    if end_date:
        query = query.filter(StockPrice.date <= end_date)
    else:
        # Default to last 30 days
        query = query.filter(StockPrice.date >= datetime.now() - timedelta(days=30))

    prices = query.order_by(StockPrice.date.desc()).all()
    return prices


@router.post("/{symbol}/refresh")
async def refresh_stock_data(symbol: str, db: Session = Depends(get_db)):
    """Refresh stock data from external sources"""
    stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    market_service = MarketDataService()
    try:
        updated_data = await market_service.fetch_stock_data(symbol)
        return {"message": "Stock data refreshed successfully", "data": updated_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to refresh data: {str(e)}")


@router.get("/{symbol}/analysis")
async def get_stock_analysis(symbol: str, db: Session = Depends(get_db)):
    """Get AI-generated stock analysis"""
    stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    # Get recent prices for technical analysis
    recent_prices = db.query(StockPrice).filter(
        StockPrice.stock_id == stock.id
    ).order_by(StockPrice.date.desc()).limit(30).all()

    if not recent_prices:
        raise HTTPException(status_code=404, detail="No price data available")

    # Calculate simple metrics
    latest_price = recent_prices[0].close
    price_30d_ago = recent_prices[-1].close if len(recent_prices) >= 30 else recent_prices[-1].close
    change_30d = ((latest_price - price_30d_ago) / price_30d_ago) * 100

    return {
        "symbol": symbol,
        "name": stock.name,
        "current_price": latest_price,
        "change_30d_percent": round(change_30d, 2),
        "market_cap": stock.market_cap,
        "sector": stock.sector,
        "analysis": {
            "trend": "bullish" if change_30d > 0 else "bearish",
            "volatility": "moderate",
            "recommendation": "hold"
        }
    }


@router.get("/search/screener")
async def stock_screener(
    min_market_cap: Optional[float] = None,
    max_market_cap: Optional[float] = None,
    sector: Optional[str] = None,
    market: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Stock screener with multiple filters"""
    query = db.query(Stock)

    if min_market_cap:
        query = query.filter(Stock.market_cap >= min_market_cap)
    if max_market_cap:
        query = query.filter(Stock.market_cap <= max_market_cap)
    if sector:
        query = query.filter(Stock.sector == sector)
    if market:
        query = query.filter(Stock.market == market)

    stocks = query.limit(100).all()
    return stocks
