import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class DatabasePipeline:
    """Pipeline for storing scraped items in database"""

    def __init__(self):
        database_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/stock_market")
        self.engine = create_engine(database_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def open_spider(self, spider):
        """Initialize when spider opens"""
        spider.logger.info(f"Database pipeline opened for {spider.name}")

    def close_spider(self, spider):
        """Cleanup when spider closes"""
        self.session.close()
        spider.logger.info(f"Database pipeline closed for {spider.name}")

    def process_item(self, item, spider):
        """Process and store each item"""
        try:
            if spider.name == "market_news":
                self._save_news(item)
            elif spider.name == "stock_prices":
                self._save_price(item)
            elif spider.name == "sec_filings":
                self._save_filing(item)

            return item
        except Exception as e:
            spider.logger.error(f"Error saving item: {e}")
            return item

    def _save_news(self, item):
        """Save news item to database"""
        # Note: In production, import actual models and save to database
        # For now, just log
        print(f"Would save news: {item['title']}")

    def _save_price(self, item):
        """Save price data to database"""
        print(f"Would save price for {item['symbol']}: ${item['current_price']}")

    def _save_filing(self, item):
        """Save SEC filing to database"""
        print(f"Would save filing: {item['filing_type']} for CIK {item['cik']}")


class JsonPipeline:
    """Pipeline for saving items to JSON files"""

    def open_spider(self, spider):
        """Create output file when spider opens"""
        filename = f"output/{spider.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs('output', exist_ok=True)
        self.file = open(filename, 'w')
        self.items = []

    def close_spider(self, spider):
        """Write items and close file when spider closes"""
        json.dump(self.items, self.file, indent=2, default=str)
        self.file.close()

    def process_item(self, item, spider):
        """Add item to list"""
        self.items.append(dict(item))
        return item


class DataCleaningPipeline:
    """Pipeline for cleaning and validating data"""

    def process_item(self, item, spider):
        """Clean and validate item data"""
        # Remove extra whitespace from string fields
        for key, value in item.items():
            if isinstance(value, str):
                item[key] = value.strip()

        # Validate required fields
        if spider.name == "market_news":
            if not item.get('title') or not item.get('url'):
                raise ValueError("News item missing required fields")

        return item
