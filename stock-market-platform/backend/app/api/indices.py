from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Index, MarketType
from app.models.schemas import IndexResponse

router = APIRouter()


@router.get("/", response_model=List[IndexResponse])
async def get_indices(market: str = None, db: Session = Depends(get_db)):
    """Get all market indices"""
    query = db.query(Index)
    if market:
        query = query.filter(Index.market == market)
    indices = query.all()
    return indices


@router.get("/{symbol}", response_model=IndexResponse)
async def get_index(symbol: str, db: Session = Depends(get_db)):
    """Get specific index by symbol"""
    index = db.query(Index).filter(Index.symbol == symbol).first()
    if not index:
        raise HTTPException(status_code=404, detail="Index not found")
    return index


@router.get("/market/overview")
async def market_overview(db: Session = Depends(get_db)):
    """Get market overview with all major indices"""
    indices = db.query(Index).all()

    # Group by market
    overview = {}
    for market_type in MarketType:
        market_indices = [idx for idx in indices if idx.market == market_type]
        if market_indices:
            overview[market_type.value] = [
                {
                    "symbol": idx.symbol,
                    "name": idx.name,
                    "value": idx.value,
                    "change": idx.change,
                    "change_percent": idx.change_percent
                }
                for idx in market_indices
            ]

    return overview
