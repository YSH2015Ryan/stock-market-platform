from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import random

app = FastAPI(
    title="Stock Market Platform",
    description="Global Stock Market Intelligence Platform API",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Stock Market Intelligence Platform API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/api/v1/indices")
async def get_indices():
    """Get major market indices"""
    return [
        {
            "id": 1,
            "symbol": "^GSPC",
            "name": "S&P 500",
            "market": "US",
            "value": 5800.50 + random.uniform(-50, 50),
            "change": random.uniform(-30, 30),
            "change_percent": random.uniform(-0.6, 0.6),
            "volume": 3500000000
        },
        {
            "id": 2,
            "symbol": "^IXIC",
            "name": "NASDAQ",
            "market": "US",
            "value": 18500.25 + random.uniform(-100, 100),
            "change": random.uniform(-50, 50),
            "change_percent": random.uniform(-0.5, 0.5),
            "volume": 4200000000
        },
        {
            "id": 3,
            "symbol": "^DJI",
            "name": "Dow Jones",
            "market": "US",
            "value": 42500.75 + random.uniform(-200, 200),
            "change": random.uniform(-100, 100),
            "change_percent": random.uniform(-0.4, 0.4),
            "volume": 280000000
        },
        {
            "id": 4,
            "symbol": "000001.SS",
            "name": "上证指数",
            "market": "CN",
            "value": 3200.50 + random.uniform(-20, 20),
            "change": random.uniform(-15, 15),
            "change_percent": random.uniform(-0.5, 0.5),
            "volume": 350000000000
        },
        {
            "id": 5,
            "symbol": "399001.SZ",
            "name": "深证成指",
            "market": "CN",
            "value": 10500.25 + random.uniform(-50, 50),
            "change": random.uniform(-30, 30),
            "change_percent": random.uniform(-0.3, 0.3),
            "volume": 420000000000
        },
        {
            "id": 6,
            "symbol": "^HSI",
            "name": "恒生指数",
            "market": "HK",
            "value": 20500.00 + random.uniform(-150, 150),
            "change": random.uniform(-80, 80),
            "change_percent": random.uniform(-0.4, 0.4),
            "volume": 85000000000
        }
    ]


@app.get("/api/v1/indices/market/overview")
async def get_market_overview():
    """Get market overview with statistics"""
    indices = await get_indices()
    return {
        "indices": indices,
        "summary": {
            "total_markets": 3,
            "markets_up": sum(1 for idx in indices if idx["change"] > 0),
            "markets_down": sum(1 for idx in indices if idx["change"] < 0),
            "average_change": sum(idx["change_percent"] for idx in indices) / len(indices)
        },
        "updated_at": datetime.now().isoformat()
    }


@app.get("/api/v1/stocks")
async def get_stocks(limit: int = 10, market: str = None):
    """Get stock list"""
    stocks = [
        {"id": 1, "symbol": "AAPL", "name": "Apple Inc.", "market": "US", "price": 175.50, "change_percent": 1.2},
        {"id": 2, "symbol": "MSFT", "name": "Microsoft", "market": "US", "price": 380.25, "change_percent": 0.8},
        {"id": 3, "symbol": "GOOGL", "name": "Alphabet Inc.", "market": "US", "price": 140.75, "change_percent": -0.5},
        {"id": 4, "symbol": "TSLA", "name": "Tesla Inc.", "market": "US", "price": 245.30, "change_percent": 2.5},
        {"id": 5, "symbol": "600519.SS", "name": "贵州茅台", "market": "CN", "price": 1850.00, "change_percent": 0.3},
        {"id": 6, "symbol": "000001.SZ", "name": "平安银行", "market": "CN", "price": 12.50, "change_percent": -0.2},
        {"id": 7, "symbol": "600036.SS", "name": "招商银行", "market": "CN", "price": 35.80, "change_percent": 0.5},
        {"id": 8, "symbol": "NVDA", "name": "NVIDIA", "market": "US", "price": 875.00, "change_percent": 3.2},
    ]

    if market:
        stocks = [s for s in stocks if s["market"] == market]

    return stocks[:limit]


@app.get("/api/v1/news")
async def get_news(limit: int = 10):
    """Get market news"""
    return [
        {
            "id": 1,
            "title": "美股收盘涨跌不一，科技股表现强劲",
            "content": "美国股市周五收盘涨跌不一，标普500指数小幅上涨...",
            "source": "Bloomberg",
            "sentiment": "positive",
            "published_at": datetime.now().isoformat()
        },
        {
            "id": 2,
            "title": "A股三大指数集体收涨，创业板涨超1%",
            "content": "A股三大指数今日集体收涨，上证指数涨0.5%...",
            "source": "新华财经",
            "sentiment": "positive",
            "published_at": datetime.now().isoformat()
        },
        {
            "id": 3,
            "title": "美联储维持利率不变，市场关注降息时点",
            "content": "美联储今日宣布维持联邦基金利率不变...",
            "source": "Reuters",
            "sentiment": "neutral",
            "published_at": datetime.now().isoformat()
        }
    ][:limit]


@app.get("/api/v1/reports")
async def get_reports(report_type: str = None, limit: int = 5):
    """Get market reports"""
    reports = [
        {
            "id": 1,
            "title": "2024年3月9日市场日报",
            "report_type": "daily",
            "summary": "今日全球股市整体表现积极，科技板块领涨...",
            "content": "## 市场概况\n\n今日全球股市整体表现积极...",
            "market": "Global",
            "report_date": datetime.now().isoformat()
        },
        {
            "id": 2,
            "title": "本周市场回顾（3月第2周）",
            "report_type": "weekly",
            "summary": "本周全球股市震荡上行，美股三大指数均创新高...",
            "content": "## 周度市场回顾\n\n本周全球股市震荡上行...",
            "market": "Global",
            "report_date": datetime.now().isoformat()
        }
    ]

    if report_type:
        reports = [r for r in reports if r["report_type"] == report_type]

    return reports[:limit]


@app.get("/api/v1/portfolios")
async def get_portfolios(user_id: int = 1):
    """Get user portfolios"""
    return [
        {
            "id": 1,
            "name": "我的投资组合",
            "description": "长期价值投资组合",
            "total_value": 150000.00,
            "total_gain": 12500.50,
            "total_gain_percent": 9.1,
            "holdings_count": 8
        }
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
