import scrapy
from datetime import datetime
import json


class MarketNewsSpider(scrapy.Spider):
    """Spider for crawling financial news"""
    name = "market_news"
    allowed_domains = ["finance.yahoo.com", "marketwatch.com", "cnbc.com"]

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS': 4,
        'USER_AGENT': 'Mozilla/5.0 (compatible; StockMarketBot/1.0)',
    }

    def __init__(self, symbols=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.symbols = symbols or ["AAPL", "GOOGL", "MSFT"]

    def start_requests(self):
        """Generate initial requests for news"""
        for symbol in self.symbols:
            # Yahoo Finance news
            url = f"https://finance.yahoo.com/quote/{symbol}/news"
            yield scrapy.Request(url, callback=self.parse_yahoo_news, meta={"symbol": symbol})

    def parse_yahoo_news(self, response):
        """Parse Yahoo Finance news"""
        symbol = response.meta["symbol"]

        # Extract news articles
        articles = response.css('div[class*="news"] li')

        for article in articles[:10]:  # Limit to 10 articles
            title = article.css('h3 *::text').get()
            link = article.css('a::attr(href)').get()
            source = article.css('div[class*="provider"] *::text').get()

            if title and link:
                yield {
                    'symbol': symbol,
                    'title': title.strip(),
                    'url': response.urljoin(link) if link else None,
                    'source': source.strip() if source else 'Yahoo Finance',
                    'published_at': datetime.now().isoformat(),
                    'crawled_at': datetime.now().isoformat()
                }


class StockPriceSpider(scrapy.Spider):
    """Spider for crawling stock prices"""
    name = "stock_prices"

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 8,
    }

    def __init__(self, symbols=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.symbols = symbols or ["AAPL", "GOOGL", "MSFT"]

    def start_requests(self):
        """Generate requests for stock data"""
        for symbol in self.symbols:
            # Using a simple API endpoint (example)
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            yield scrapy.Request(url, callback=self.parse_price_data, meta={"symbol": symbol})

    def parse_price_data(self, response):
        """Parse stock price data"""
        try:
            data = json.loads(response.text)
            symbol = response.meta["symbol"]

            result = data.get("chart", {}).get("result", [])
            if result:
                quote = result[0]
                meta = quote.get("meta", {})

                yield {
                    'symbol': symbol,
                    'current_price': meta.get("regularMarketPrice"),
                    'previous_close': meta.get("previousClose"),
                    'open': meta.get("regularMarketOpen"),
                    'day_high': meta.get("regularMarketDayHigh"),
                    'day_low': meta.get("regularMarketDayLow"),
                    'volume': meta.get("regularMarketVolume"),
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            self.logger.error(f"Error parsing price data for {response.meta['symbol']}: {e}")


class SECFilingsSpider(scrapy.Spider):
    """Spider for crawling SEC filings"""
    name = "sec_filings"
    allowed_domains = ["sec.gov"]

    custom_settings = {
        'DOWNLOAD_DELAY': 3,  # Be respectful to SEC servers
        'CONCURRENT_REQUESTS': 2,
    }

    def __init__(self, cik_numbers=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cik_numbers = cik_numbers or []

    def start_requests(self):
        """Generate requests for SEC filings"""
        for cik in self.cik_numbers:
            url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=&dateb=&owner=exclude&count=10"
            yield scrapy.Request(url, callback=self.parse_filings, meta={"cik": cik})

    def parse_filings(self, response):
        """Parse SEC filings list"""
        cik = response.meta["cik"]
        rows = response.css('table.tableFile2 tr')[1:]  # Skip header

        for row in rows:
            filing_type = row.css('td:nth-child(1)::text').get()
            filing_date = row.css('td:nth-child(4)::text').get()
            document_link = row.css('td:nth-child(2) a::attr(href)').get()

            if document_link:
                yield {
                    'cik': cik,
                    'filing_type': filing_type.strip() if filing_type else None,
                    'filing_date': filing_date.strip() if filing_date else None,
                    'document_url': response.urljoin(document_link),
                    'crawled_at': datetime.now().isoformat()
                }
