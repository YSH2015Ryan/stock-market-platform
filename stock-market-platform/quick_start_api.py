from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import random

# 创建 FastAPI 应用
app = FastAPI(
    title="Stock Market Platform API",
    description="全球股票市场智能分析平台 - 演示版",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 模拟股票数据
MOCK_STOCKS = [
    {"symbol": "AAPL", "name": "Apple Inc.", "price": 178.25, "change": 2.5},
    {"symbol": "GOOGL", "name": "Alphabet Inc.", "price": 142.65, "change": -1.2},
    {"symbol": "MSFT", "name": "Microsoft Corp.", "price": 425.89, "change": 3.8},
    {"symbol": "TSLA", "name": "Tesla Inc.", "price": 248.50, "change": -0.5},
    {"symbol": "AMZN", "name": "Amazon.com Inc.", "price": 178.35, "change": 1.9},
]

@app.get("/")
async def root():
    """API 根路径"""
    return {
        "message": "欢迎使用股票市场平台 API",
        "version": "1.0.0",
        "status": "运行中",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/stocks")
async def get_stocks():
    """获取股票列表"""
    # 添加随机波动
    stocks = []
    for stock in MOCK_STOCKS:
        stock_copy = stock.copy()
        stock_copy["price"] = round(stock["price"] + random.uniform(-2, 2), 2)
        stock_copy["change"] = round(random.uniform(-5, 5), 2)
        stocks.append(stock_copy)

    return {
        "success": True,
        "data": stocks,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/stocks/{symbol}")
async def get_stock_detail(symbol: str):
    """获取股票详情"""
    stock = next((s for s in MOCK_STOCKS if s["symbol"] == symbol), None)

    if not stock:
        return {
            "success": False,
            "message": f"股票 {symbol} 未找到"
        }

    # 生成模拟的详细数据
    detail = {
        **stock,
        "open": round(stock["price"] - random.uniform(0, 5), 2),
        "high": round(stock["price"] + random.uniform(0, 10), 2),
        "low": round(stock["price"] - random.uniform(0, 10), 2),
        "volume": random.randint(1000000, 50000000),
        "market_cap": f"${random.randint(100, 3000)}B",
        "pe_ratio": round(random.uniform(15, 40), 2),
        "updated_at": datetime.now().isoformat()
    }

    return {
        "success": True,
        "data": detail,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/market/summary")
async def get_market_summary():
    """获取市场概览"""
    return {
        "success": True,
        "data": {
            "indices": [
                {
                    "name": "S&P 500",
                    "value": 5123.45,
                    "change": round(random.uniform(-100, 100), 2),
                    "change_percent": round(random.uniform(-2, 2), 2)
                },
                {
                    "name": "NASDAQ",
                    "value": 16234.89,
                    "change": round(random.uniform(-200, 200), 2),
                    "change_percent": round(random.uniform(-2, 2), 2)
                },
                {
                    "name": "道琼斯",
                    "value": 38456.78,
                    "change": round(random.uniform(-300, 300), 2),
                    "change_percent": round(random.uniform(-2, 2), 2)
                }
            ],
            "top_gainers": MOCK_STOCKS[:3],
            "top_losers": MOCK_STOCKS[3:],
            "most_active": MOCK_STOCKS,
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/news")
async def get_news():
    """获取财经新闻"""
    news = [
        {
            "id": 1,
            "title": "科技股领涨，纳斯达克创新高",
            "summary": "在AI热潮推动下，科技股表现强劲...",
            "source": "财经日报",
            "published_at": datetime.now().isoformat(),
            "url": "https://example.com/news1"
        },
        {
            "id": 2,
            "title": "美联储维持利率不变",
            "summary": "联邦公开市场委员会决定维持当前利率政策...",
            "source": "路透社",
            "published_at": datetime.now().isoformat(),
            "url": "https://example.com/news2"
        },
        {
            "id": 3,
            "title": "电动汽车销量持续增长",
            "summary": "第一季度电动汽车销量同比增长35%...",
            "source": "汽车周刊",
            "published_at": datetime.now().isoformat(),
            "url": "https://example.com/news3"
        }
    ]

    return {
        "success": True,
        "data": news,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 启动股票市场平台 API...")
    print("📍 访问: http://localhost:8000")
    print("📚 API 文档: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
