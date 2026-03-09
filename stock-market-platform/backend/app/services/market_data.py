import yfinance as yf
from typing import Dict, List
import pandas as pd
from datetime import datetime, timedelta


class MarketDataService:
    """Service for fetching market data from external sources"""

    def __init__(self):
        self.cache = {}

    async def fetch_stock_data(self, symbol: str) -> Dict:
        """Fetch stock data from Yahoo Finance"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            return {
                "symbol": symbol,
                "name": info.get("longName", ""),
                "market_cap": info.get("marketCap"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "current_price": info.get("currentPrice"),
                "pe_ratio": info.get("trailingPE"),
                "pb_ratio": info.get("priceToBook"),
                "dividend_yield": info.get("dividendYield"),
                "52_week_high": info.get("fiftyTwoWeekHigh"),
                "52_week_low": info.get("fiftyTwoWeekLow"),
            }
        except Exception as e:
            raise Exception(f"Failed to fetch stock data: {str(e)}")

    async def fetch_historical_prices(self, symbol: str, period: str = "1mo") -> List[Dict]:
        """Fetch historical price data"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)

            prices = []
            for date, row in hist.iterrows():
                prices.append({
                    "date": date,
                    "open": row["Open"],
                    "high": row["High"],
                    "low": row["Low"],
                    "close": row["Close"],
                    "volume": row["Volume"]
                })

            return prices
        except Exception as e:
            raise Exception(f"Failed to fetch historical prices: {str(e)}")

    async def fetch_index_data(self, symbol: str) -> Dict:
        """Fetch index data"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d")

            if len(hist) < 2:
                raise Exception("Not enough data")

            current = hist.iloc[-1]
            previous = hist.iloc[-2]

            change = current["Close"] - previous["Close"]
            change_percent = (change / previous["Close"]) * 100

            return {
                "value": current["Close"],
                "change": change,
                "change_percent": change_percent,
                "volume": current["Volume"]
            }
        except Exception as e:
            raise Exception(f"Failed to fetch index data: {str(e)}")

    async def get_top_movers(self, market: str = "US") -> Dict:
        """Get top gainers, losers, and most active stocks"""
        # Note: This is a simplified version. In production, use proper data sources
        try:
            # Example symbols - in production, fetch from database
            symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "META", "NVDA", "JPM"]

            movers = []
            for symbol in symbols:
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="2d")

                    if len(hist) >= 2:
                        current = hist.iloc[-1]["Close"]
                        previous = hist.iloc[-2]["Close"]
                        change_percent = ((current - previous) / previous) * 100

                        movers.append({
                            "symbol": symbol,
                            "change_percent": change_percent,
                            "volume": hist.iloc[-1]["Volume"]
                        })
                except:
                    continue

            # Sort by change percent
            gainers = sorted(movers, key=lambda x: x["change_percent"], reverse=True)[:5]
            losers = sorted(movers, key=lambda x: x["change_percent"])[:5]
            most_active = sorted(movers, key=lambda x: x["volume"], reverse=True)[:5]

            return {
                "gainers": gainers,
                "losers": losers,
                "most_active": most_active
            }
        except Exception as e:
            raise Exception(f"Failed to fetch top movers: {str(e)}")

    async def calculate_technical_indicators(self, symbol: str) -> Dict:
        """Calculate technical indicators for a stock"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="3mo")

            # Calculate moving averages
            hist["SMA_20"] = hist["Close"].rolling(window=20).mean()
            hist["SMA_50"] = hist["Close"].rolling(window=50).mean()

            # Calculate RSI
            delta = hist["Close"].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            hist["RSI"] = 100 - (100 / (1 + rs))

            latest = hist.iloc[-1]

            return {
                "sma_20": latest["SMA_20"],
                "sma_50": latest["SMA_50"],
                "rsi": latest["RSI"],
                "current_price": latest["Close"]
            }
        except Exception as e:
            raise Exception(f"Failed to calculate technical indicators: {str(e)}")
