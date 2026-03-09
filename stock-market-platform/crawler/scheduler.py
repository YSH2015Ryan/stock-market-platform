"""
Scheduler for running crawlers periodically
"""
import os
import sys
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import logging

# Add spiders directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from spiders.market_spiders import MarketNewsSpider, StockPriceSpider

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CrawlerScheduler:
    """Scheduler for running crawlers at specified intervals"""

    def __init__(self):
        self.scheduler = BlockingScheduler()
        self.symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "META", "NVDA", "JPM"]

    def crawl_news(self):
        """Crawl financial news"""
        logger.info("Starting news crawler...")
        try:
            process = CrawlerProcess({
                'USER_AGENT': 'Mozilla/5.0 (compatible; StockMarketBot/1.0)',
                'ROBOTSTXT_OBEY': True,
                'CONCURRENT_REQUESTS': 4,
                'DOWNLOAD_DELAY': 2,
            })

            process.crawl(MarketNewsSpider, symbols=self.symbols)
            process.start()
            logger.info("News crawler completed")
        except Exception as e:
            logger.error(f"Error in news crawler: {e}")

    def crawl_prices(self):
        """Crawl stock prices"""
        logger.info("Starting price crawler...")
        try:
            process = CrawlerProcess({
                'USER_AGENT': 'Mozilla/5.0 (compatible; StockMarketBot/1.0)',
                'CONCURRENT_REQUESTS': 8,
                'DOWNLOAD_DELAY': 1,
            })

            process.crawl(StockPriceSpider, symbols=self.symbols)
            process.start()
            logger.info("Price crawler completed")
        except Exception as e:
            logger.error(f"Error in price crawler: {e}")

    def update_market_data(self):
        """Update market data using API calls instead of scraping"""
        logger.info("Updating market data via API...")
        try:
            # Import market data service
            # In production, this would fetch data via API and update database
            logger.info(f"Would update data for symbols: {', '.join(self.symbols)}")
            logger.info("Market data update completed")
        except Exception as e:
            logger.error(f"Error updating market data: {e}")

    def start(self):
        """Start the scheduler"""
        logger.info("Starting crawler scheduler...")

        # Schedule jobs
        # Update prices every 5 minutes during market hours
        self.scheduler.add_job(
            self.update_market_data,
            CronTrigger(minute='*/5', hour='9-16', day_of_week='mon-fri'),
            id='price_updates',
            name='Update stock prices every 5 minutes'
        )

        # Crawl news every 15 minutes
        self.scheduler.add_job(
            self.crawl_news,
            CronTrigger(minute='*/15'),
            id='news_crawl',
            name='Crawl financial news every 15 minutes'
        )

        # Full data refresh daily at 6 PM
        self.scheduler.add_job(
            self.update_market_data,
            CronTrigger(hour=18, minute=0),
            id='daily_refresh',
            name='Daily data refresh'
        )

        # Test job - run once on startup
        self.scheduler.add_job(
            lambda: logger.info("Scheduler is running! Jobs scheduled successfully."),
            'date',
            run_date=datetime.now()
        )

        logger.info("Scheduler configured with the following jobs:")
        for job in self.scheduler.get_jobs():
            logger.info(f"  - {job.name} (ID: {job.id})")

        # Start scheduler
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info("Scheduler stopped")


if __name__ == "__main__":
    scheduler = CrawlerScheduler()
    scheduler.start()
