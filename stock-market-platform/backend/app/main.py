from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api import stocks, indices, news, reports, portfolios

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(stocks.router, prefix=f"{settings.API_V1_PREFIX}/stocks", tags=["stocks"])
app.include_router(indices.router, prefix=f"{settings.API_V1_PREFIX}/indices", tags=["indices"])
app.include_router(news.router, prefix=f"{settings.API_V1_PREFIX}/news", tags=["news"])
app.include_router(reports.router, prefix=f"{settings.API_V1_PREFIX}/reports", tags=["reports"])
app.include_router(portfolios.router, prefix=f"{settings.API_V1_PREFIX}/portfolios", tags=["portfolios"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to Stock Market Intelligence Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
