# API Documentation

## Base URL

- Development: `http://localhost:8000/api/v1`
- Production: `https://api.yourdomain.com/api/v1`

## Authentication

Most endpoints require authentication via JWT token.

```http
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Stocks

#### Get All Stocks

```http
GET /stocks
```

**Query Parameters:**
- `market` (optional): Filter by market (US, CN, HK, etc.)
- `sector` (optional): Filter by sector
- `skip` (optional): Pagination offset (default: 0)
- `limit` (optional): Number of results (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "market": "US",
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "market_cap": 2800000000000,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

#### Get Stock by Symbol

```http
GET /stocks/{symbol}
```

**Response:**
```json
{
  "id": 1,
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "market": "US",
  "sector": "Technology",
  "industry": "Consumer Electronics",
  "market_cap": 2800000000000
}
```

#### Get Stock Prices

```http
GET /stocks/{symbol}/prices
```

**Query Parameters:**
- `start_date` (optional): Start date (ISO format)
- `end_date` (optional): End date (ISO format)

**Response:**
```json
[
  {
    "id": 1,
    "stock_id": 1,
    "date": "2024-01-01T00:00:00Z",
    "open": 150.0,
    "high": 155.0,
    "low": 149.0,
    "close": 154.0,
    "volume": 50000000
  }
]
```

#### Get Stock Analysis

```http
GET /stocks/{symbol}/analysis
```

**Response:**
```json
{
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "current_price": 154.0,
  "change_30d_percent": 5.2,
  "market_cap": 2800000000000,
  "sector": "Technology",
  "analysis": {
    "trend": "bullish",
    "volatility": "moderate",
    "recommendation": "hold"
  }
}
```

#### Stock Screener

```http
GET /stocks/search/screener
```

**Query Parameters:**
- `min_market_cap` (optional): Minimum market cap
- `max_market_cap` (optional): Maximum market cap
- `sector` (optional): Sector filter
- `market` (optional): Market filter

### Indices

#### Get All Indices

```http
GET /indices
```

**Query Parameters:**
- `market` (optional): Filter by market

**Response:**
```json
[
  {
    "id": 1,
    "symbol": "^GSPC",
    "name": "S&P 500",
    "market": "US",
    "value": 4500.0,
    "change": 25.5,
    "change_percent": 0.57,
    "volume": 3500000000
  }
]
```

#### Get Market Overview

```http
GET /indices/market/overview
```

**Response:**
```json
{
  "US": [
    {
      "symbol": "^GSPC",
      "name": "S&P 500",
      "value": 4500.0,
      "change": 25.5,
      "change_percent": 0.57
    }
  ],
  "CN": [...]
}
```

### News

#### Get News Articles

```http
GET /news
```

**Query Parameters:**
- `stock_id` (optional): Filter by stock
- `sentiment` (optional): Filter by sentiment (positive, negative, neutral)
- `limit` (optional): Number of results (default: 50)

**Response:**
```json
[
  {
    "id": 1,
    "title": "Apple Reports Record Earnings",
    "content": "...",
    "source": "Reuters",
    "url": "https://...",
    "published_at": "2024-01-01T00:00:00Z",
    "sentiment": "positive",
    "sentiment_score": 0.85
  }
]
```

#### Get Sentiment Summary

```http
GET /news/sentiment/summary
```

**Query Parameters:**
- `stock_id` (optional): Filter by stock
- `days` (optional): Number of days to analyze (default: 7)

**Response:**
```json
{
  "total": 100,
  "positive": 45,
  "negative": 20,
  "neutral": 35,
  "average_score": 0.3
}
```

### Reports

#### Get Market Reports

```http
GET /reports
```

**Query Parameters:**
- `report_type` (optional): daily, weekly, monthly
- `market` (optional): Market filter
- `limit` (optional): Number of results (default: 20)

**Response:**
```json
[
  {
    "id": 1,
    "title": "Daily Market Report - 2024-01-01",
    "report_type": "daily",
    "content": "...",
    "summary": "...",
    "report_date": "2024-01-01T00:00:00Z"
  }
]
```

#### Generate Daily Report

```http
POST /reports/generate/daily
```

**Response:**
```json
{
  "id": 1,
  "title": "Daily Market Report - 2024-01-01",
  "content": "...",
  "summary": "..."
}
```

#### Get Latest Daily Report

```http
GET /reports/latest/daily
```

### Portfolios

#### Get User Portfolios

```http
GET /portfolios?user_id={user_id}
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "My Portfolio",
    "description": "...",
    "user_id": 1,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

#### Create Portfolio

```http
POST /portfolios?user_id={user_id}
```

**Request Body:**
```json
{
  "name": "My Portfolio",
  "description": "Investment portfolio"
}
```

#### Get Portfolio Holdings

```http
GET /portfolios/{portfolio_id}/holdings
```

**Response:**
```json
[
  {
    "id": 1,
    "portfolio_id": 1,
    "stock_id": 1,
    "quantity": 100,
    "purchase_price": 150.0,
    "purchase_date": "2024-01-01T00:00:00Z"
  }
]
```

#### Get Portfolio Performance

```http
GET /portfolios/{portfolio_id}/performance
```

**Response:**
```json
{
  "portfolio_id": 1,
  "total_holdings": 5,
  "total_value": 50000.0,
  "total_cost": 45000.0,
  "total_gain": 5000.0,
  "total_gain_percent": 11.11
}
```

## Error Responses

```json
{
  "detail": "Error message description"
}
```

**Status Codes:**
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `500`: Internal Server Error

## Rate Limiting

- 100 requests per minute per IP
- 1000 requests per hour per API key

## Interactive Documentation

Visit `/docs` for interactive Swagger UI documentation.
Visit `/redoc` for ReDoc documentation.
