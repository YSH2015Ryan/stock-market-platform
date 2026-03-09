from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.models import News, SentimentType
from app.models.schemas import NewsResponse, NewsCreate
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/", response_model=List[NewsResponse])
async def get_news(
    stock_id: Optional[int] = None,
    sentiment: Optional[SentimentType] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get news articles with optional filters"""
    query = db.query(News)

    if stock_id:
        query = query.filter(News.stock_id == stock_id)
    if sentiment:
        query = query.filter(News.sentiment == sentiment)

    news = query.order_by(News.published_at.desc()).limit(limit).all()
    return news


@router.get("/{news_id}", response_model=NewsResponse)
async def get_news_item(news_id: int, db: Session = Depends(get_db)):
    """Get specific news article"""
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news


@router.post("/", response_model=NewsResponse)
async def create_news(news: NewsCreate, db: Session = Depends(get_db)):
    """Create a new news article"""
    db_news = News(**news.dict())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news


@router.get("/sentiment/summary")
async def sentiment_summary(
    stock_id: Optional[int] = None,
    days: int = 7,
    db: Session = Depends(get_db)
):
    """Get sentiment summary for news"""
    query = db.query(News).filter(
        News.published_at >= datetime.now() - timedelta(days=days)
    )

    if stock_id:
        query = query.filter(News.stock_id == stock_id)

    news_items = query.all()

    if not news_items:
        return {
            "total": 0,
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "average_score": 0
        }

    sentiment_counts = {
        "positive": sum(1 for n in news_items if n.sentiment == SentimentType.POSITIVE),
        "negative": sum(1 for n in news_items if n.sentiment == SentimentType.NEGATIVE),
        "neutral": sum(1 for n in news_items if n.sentiment == SentimentType.NEUTRAL)
    }

    avg_score = sum(n.sentiment_score for n in news_items if n.sentiment_score) / len(news_items)

    return {
        "total": len(news_items),
        "positive": sentiment_counts["positive"],
        "negative": sentiment_counts["negative"],
        "neutral": sentiment_counts["neutral"],
        "average_score": round(avg_score, 3)
    }
