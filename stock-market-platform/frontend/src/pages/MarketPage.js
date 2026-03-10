import React, { useEffect, useState } from 'react';
import { Typography, Card, Table, Tag, Spin } from 'antd';
import axios from 'axios';
import MarketOverview from '../components/MarketOverview';

const { Title } = Typography;

const MarketPage = () => {
  const [loading, setLoading] = useState(true);
  const [indices, setIndices] = useState([]);
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [indicesRes, stocksRes] = await Promise.all([
        axios.get('/api/v1/indices'),
        axios.get('/api/v1/stocks?limit=20')
      ]);

      setIndices(indicesRes.data);
      setStocks(stocksRes.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      // Mock data for demo
      setIndices([
        { id: 1, symbol: 'S&P 500', name: 'S&P 500 Index', market: 'US', value: 4783.45, change: 45.23, change_percent: 0.95 },
        { id: 2, symbol: 'NASDAQ', name: 'NASDAQ Composite', market: 'US', value: 15095.14, change: 123.45, change_percent: 0.82 },
        { id: 3, symbol: 'SSE', name: 'Shanghai Composite', market: 'CN', value: 3027.88, change: 12.34, change_percent: 0.41 },
      ]);

      setStocks([
        { id: 1, symbol: 'AAPL', name: 'Apple Inc.', market: 'US', sector: 'Technology', market_cap: 2800000000000 },
        { id: 2, symbol: 'MSFT', name: 'Microsoft Corporation', market: 'US', sector: 'Technology', market_cap: 2600000000000 },
        { id: 3, symbol: 'GOOGL', name: 'Alphabet Inc.', market: 'US', sector: 'Technology', market_cap: 1700000000000 },
        { id: 4, symbol: 'TSLA', name: 'Tesla Inc.', market: 'US', sector: 'Automotive', market_cap: 800000000000 },
        { id: 5, symbol: 'NVDA', name: 'NVIDIA Corporation', market: 'US', sector: 'Technology', market_cap: 1200000000000 },
      ]);
      setLoading(false);
    }
  };

  const stockColumns = [
    {
      title: 'Symbol',
      dataIndex: 'symbol',
      key: 'symbol',
      render: (text) => <strong>{text}</strong>,
    },
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Market',
      dataIndex: 'market',
      key: 'market',
      render: (market) => (
        <Tag color={market === 'US' ? 'blue' : 'green'}>{market}</Tag>
      ),
    },
    {
      title: 'Sector',
      dataIndex: 'sector',
      key: 'sector',
    },
    {
      title: 'Market Cap',
      dataIndex: 'market_cap',
      key: 'market_cap',
      render: (value) => value ? `$${(value / 1000000000).toFixed(2)}B` : 'N/A',
    },
  ];

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '100px 0' }}>
        <Spin size="large" />
      </div>
    );
  }

  return (
    <div>
      <Title level={2}>Market Overview</Title>

      <Card title="Major Indices" style={{ marginBottom: '24px' }}>
        <MarketOverview indices={indices} />
      </Card>

      <Card title="Top Stocks">
        <Table
          dataSource={stocks}
          columns={stockColumns}
          rowKey="id"
          pagination={{ pageSize: 10 }}
        />
      </Card>
    </div>
  );
};

export default MarketPage;
