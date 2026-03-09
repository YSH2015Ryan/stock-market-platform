from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import MarketReport
from app.models.schemas import MarketReportResponse, MarketReportCreate
from app.services.ai_analysis import AIAnalysisService
from datetime import datetime

router = APIRouter()


@router.get("/", response_model=List[MarketReportResponse])
async def get_reports(
    report_type: str = None,
    market: str = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get market reports"""
    query = db.query(MarketReport)

    if report_type:
        query = query.filter(MarketReport.report_type == report_type)
    if market:
        query = query.filter(MarketReport.market == market)

    reports = query.order_by(MarketReport.report_date.desc()).limit(limit).all()
    return reports


@router.get("/{report_id}", response_model=MarketReportResponse)
async def get_report(report_id: int, db: Session = Depends(get_db)):
    """Get specific market report"""
    report = db.query(MarketReport).filter(MarketReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.post("/generate/daily")
async def generate_daily_report(db: Session = Depends(get_db)):
    """Generate daily market report using AI"""
    ai_service = AIAnalysisService()

    try:
        report_content = await ai_service.generate_daily_report(db)

        report = MarketReport(
            title=f"Daily Market Report - {datetime.now().strftime('%Y-%m-%d')}",
            report_type="daily",
            content=report_content["content"],
            summary=report_content["summary"],
            report_date=datetime.now(),
            metadata=report_content.get("metadata", {})
        )

        db.add(report)
        db.commit()
        db.refresh(report)

        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")


@router.post("/generate/weekly")
async def generate_weekly_report(db: Session = Depends(get_db)):
    """Generate weekly market report using AI"""
    ai_service = AIAnalysisService()

    try:
        report_content = await ai_service.generate_weekly_report(db)

        report = MarketReport(
            title=f"Weekly Market Report - Week of {datetime.now().strftime('%Y-%m-%d')}",
            report_type="weekly",
            content=report_content["content"],
            summary=report_content["summary"],
            report_date=datetime.now(),
            metadata=report_content.get("metadata", {})
        )

        db.add(report)
        db.commit()
        db.refresh(report)

        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")


@router.get("/latest/daily", response_model=MarketReportResponse)
async def get_latest_daily_report(db: Session = Depends(get_db)):
    """Get the latest daily report"""
    report = db.query(MarketReport).filter(
        MarketReport.report_type == "daily"
    ).order_by(MarketReport.report_date.desc()).first()

    if not report:
        raise HTTPException(status_code=404, detail="No daily report found")

    return report
