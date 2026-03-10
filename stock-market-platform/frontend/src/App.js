import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [indices, setIndices] = useState([]);
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);

  const API_URL = 'http://localhost:8000';

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [indicesRes, newsRes] = await Promise.all([
        fetch(`${API_URL}/api/v1/indices`),
        fetch(`${API_URL}/api/v1/news`)
      ]);

      const indicesData = await indicesRes.json();
      const newsData = await newsRes.json();

      setIndices(indicesData);
      setNews(newsData);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  const renderIndexCard = (index) => {
    const isPositive = index.change >= 0;
    const changeClass = isPositive ? 'positive' : 'negative';

    return (
      <div key={index.id} className="index-card">
        <div className="index-header">
          <span className="index-symbol">{index.symbol}</span>
          <span className={`index-market market-${index.market}`}>{index.market}</span>
        </div>
        <div className="index-name">{index.name}</div>
        <div className="index-value">{index.value.toFixed(2)}</div>
        <div className={`index-change ${changeClass}`}>
          <span className="arrow">{isPositive ? '▲' : '▼'}</span>
          <span className="percent">{Math.abs(index.change_percent).toFixed(2)}%</span>
          <span className="value">({isPositive ? '+' : ''}{index.change.toFixed(2)})</span>
        </div>
      </div>
    );
  };

  const renderNewsItem = (item) => {
    const sentimentColors = {
      positive: '#52c41a',
      negative: '#ff4d4f',
      neutral: '#999'
    };

    return (
      <div key={item.id} className="news-item">
        <div className="news-header">
          <span className="news-source">{item.source}</span>
          <span
            className="news-sentiment"
            style={{ color: sentimentColors[item.sentiment] }}
          >
            {item.sentiment === 'positive' ? '📈' : item.sentiment === 'negative' ? '📉' : '📊'}
          </span>
        </div>
        <div className="news-title">{item.title}</div>
        <div className="news-content">{item.content}</div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="App">
        <div className="loading">Loading market data...</div>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>🌍 Global Stock Market Intelligence Platform</h1>
        <p className="subtitle">AI-Powered Market Analysis & Real-time Data</p>
      </header>

      <main className="main-content">
        <section className="section">
          <h2 className="section-title">📊 Market Overview</h2>
          <div className="indices-grid">
            {indices.map(renderIndexCard)}
          </div>
        </section>

        <section className="section">
          <h2 className="section-title">📰 Latest Market News</h2>
          <div className="news-list">
            {news.map(renderNewsItem)}
          </div>
        </section>

        <section className="section">
          <h2 className="section-title">🔧 Quick Actions</h2>
          <div className="actions-grid">
            <button className="action-btn">📈 Stock Screener</button>
            <button className="action-btn">💼 My Portfolio</button>
            <button className="action-btn">📊 Market Reports</button>
            <button className="action-btn">🤖 AI Assistant</button>
          </div>
        </section>
      </main>

      <footer className="App-footer">
        <p>© 2026 Global Stock Market Intelligence Platform | AI-Powered Market Analysis</p>
        <p className="disclaimer">⚠️ For educational purposes only. Not financial advice.</p>
      </footer>
    </div>
  );
}

export default App;
