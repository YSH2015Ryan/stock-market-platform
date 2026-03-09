-- Initialize database for Stock Market Platform

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create enum types
CREATE TYPE market_type AS ENUM ('US', 'CN', 'HK', 'EU', 'JP', 'IN');
CREATE TYPE sentiment_type AS ENUM ('positive', 'negative', 'neutral');

-- Note: Tables will be created by SQLAlchemy ORM
-- This file is for initialization and seed data

-- Insert sample indices
INSERT INTO indices (symbol, name, market, value, change, change_percent, volume) VALUES
  ('^GSPC', 'S&P 500', 'US', 4500.00, 25.50, 0.57, 3500000000),
  ('^DJI', 'Dow Jones', 'US', 35000.00, 150.00, 0.43, 400000000),
  ('^IXIC', 'NASDAQ', 'US', 14000.00, 80.00, 0.57, 5000000000),
  ('000001.SS', 'Shanghai Composite', 'CN', 3200.00, -15.00, -0.47, 300000000),
  ('399001.SZ', 'Shenzhen Component', 'CN', 11000.00, -50.00, -0.45, 250000000),
  ('^HSI', 'Hang Seng', 'HK', 19000.00, 100.00, 0.53, 120000000)
ON CONFLICT (symbol) DO NOTHING;

-- Insert sample stocks
INSERT INTO stocks (symbol, name, market, sector, industry, market_cap) VALUES
  ('AAPL', 'Apple Inc.', 'US', 'Technology', 'Consumer Electronics', 2800000000000),
  ('MSFT', 'Microsoft Corporation', 'US', 'Technology', 'Software', 2500000000000),
  ('GOOGL', 'Alphabet Inc.', 'US', 'Technology', 'Internet', 1800000000000),
  ('AMZN', 'Amazon.com Inc.', 'US', 'Consumer Cyclical', 'E-Commerce', 1600000000000),
  ('TSLA', 'Tesla Inc.', 'US', 'Automotive', 'Electric Vehicles', 800000000000),
  ('META', 'Meta Platforms Inc.', 'US', 'Technology', 'Social Media', 900000000000),
  ('NVDA', 'NVIDIA Corporation', 'US', 'Technology', 'Semiconductors', 1100000000000),
  ('JPM', 'JPMorgan Chase & Co.', 'US', 'Financial', 'Banking', 450000000000)
ON CONFLICT (symbol) DO NOTHING;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_stock_prices_date ON stock_prices(date);
CREATE INDEX IF NOT EXISTS idx_stock_prices_stock_id ON stock_prices(stock_id);
CREATE INDEX IF NOT EXISTS idx_news_published_at ON news(published_at);
CREATE INDEX IF NOT EXISTS idx_news_stock_id ON news(stock_id);
CREATE INDEX IF NOT EXISTS idx_financials_stock_id ON financials(stock_id);

-- Grant permissions (adjust as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO stock_user;
