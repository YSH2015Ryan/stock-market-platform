from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Portfolio, Holding
from app.models.schemas import PortfolioResponse, PortfolioCreate, HoldingResponse, HoldingCreate

router = APIRouter()


@router.get("/", response_model=List[PortfolioResponse])
async def get_portfolios(user_id: int, db: Session = Depends(get_db)):
    """Get all portfolios for a user"""
    portfolios = db.query(Portfolio).filter(Portfolio.user_id == user_id).all()
    return portfolios


@router.post("/", response_model=PortfolioResponse)
async def create_portfolio(
    portfolio: PortfolioCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Create a new portfolio"""
    db_portfolio = Portfolio(**portfolio.dict(), user_id=user_id)
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio


@router.get("/{portfolio_id}", response_model=PortfolioResponse)
async def get_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    """Get specific portfolio"""
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio


@router.get("/{portfolio_id}/holdings", response_model=List[HoldingResponse])
async def get_holdings(portfolio_id: int, db: Session = Depends(get_db)):
    """Get all holdings in a portfolio"""
    holdings = db.query(Holding).filter(Holding.portfolio_id == portfolio_id).all()
    return holdings


@router.post("/{portfolio_id}/holdings", response_model=HoldingResponse)
async def create_holding(
    portfolio_id: int,
    holding: HoldingCreate,
    db: Session = Depends(get_db)
):
    """Add a holding to portfolio"""
    db_holding = Holding(**holding.dict(), portfolio_id=portfolio_id)
    db.add(db_holding)
    db.commit()
    db.refresh(db_holding)
    return db_holding


@router.get("/{portfolio_id}/performance")
async def get_portfolio_performance(portfolio_id: int, db: Session = Depends(get_db)):
    """Calculate portfolio performance"""
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    holdings = db.query(Holding).filter(Holding.portfolio_id == portfolio_id).all()

    # TODO: Calculate actual performance with current prices
    total_value = sum(h.quantity * h.purchase_price for h in holdings)
    total_cost = sum(h.quantity * h.purchase_price for h in holdings)

    return {
        "portfolio_id": portfolio_id,
        "total_holdings": len(holdings),
        "total_value": total_value,
        "total_cost": total_cost,
        "total_gain": 0,  # Placeholder
        "total_gain_percent": 0  # Placeholder
    }
