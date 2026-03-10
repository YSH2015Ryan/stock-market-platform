import React, { useEffect, useState } from 'react';
import { Typography, Row, Col, Card, Statistic, Spin } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';
import axios from 'axios';
import MarketOverview from '../components/MarketOverview';

const { Title, Paragraph } = Typography;

const HomePage = () => {
  const [loading, setLoading] = useState(true);
  const [marketData, setMarketData] = useState(null);

  useEffect(() => {
    fetchMarketData();
  }, []);

  const fetchMarketData = async () => {
    try {
      const response = await axios.get('/api/v1/indices/market/overview');
      setMarketData(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching market data:', error);
      setLoading(false);
      // Set mock data for demo
      setMarketData({
        markets: {
          US: [
            { symbol: 'S&P 500', name: 'S&P 500 Index', value: 4783.45, change: 45.23, change_percent: 0.95 },
            { symbol: 'NASDAQ', name: 'NASDAQ Composite', value: 15095.14, change: 123.45, change_percent: 0.82 },
            { symbol: 'DOW', name: 'Dow Jones', value: 37440.34, change: -52.12, change_percent: -0.14 },
          ],
          CN: [
            { symbol: 'SSE', name: 'Shanghai Composite', value: 3027.88, change: 12.34, change_percent: 0.41 },
            { symbol: 'SZSE', name: 'Shenzhen Component', value: 9845.67, change: -23.45, change_percent: -0.24 },
          ],
        },
        total_indices: 5
      });
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '100px 0' }}>
        <Spin size="large" />
      </div>
    );
  }

  const allIndices = marketData?.markets ? Object.values(marketData.markets).flat() : [];

  return (
    <div>
      <div style={{ marginBottom: '32px' }}>
        <Title level={2}>Global Stock Market Intelligence Platform</Title>
        <Paragraph style={{ fontSize: '16px', color: '#666' }}>
          AI-powered market analysis and insights for global stock markets
        </Paragraph>
      </div>

      <Card title="Market Overview" style={{ marginBottom: '24px' }}>
        <MarketOverview indices={allIndices} />
      </Card>

      <Row gutter={16}>
        <Col span={24}>
          <Card title="Today's Highlights" style={{ marginBottom: '24px' }}>
            <Paragraph>
              <strong>Market Summary:</strong> Global markets showed mixed performance today.
              US markets continued their upward trend with technology stocks leading the gains.
              Asian markets experienced moderate volatility amid economic data releases.
            </Paragraph>
            <Paragraph>
              Monitor the platform for real-time updates, AI-powered analysis, and comprehensive market reports.
            </Paragraph>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="Total Markets Tracked"
              value={6}
              prefix={<AppstoreOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="Stocks Monitored"
              value={500}
              prefix={<LineChartOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="Daily Reports"
              value={1}
              suffix="/ day"
              prefix={<FileTextOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="News Articles"
              value={150}
              suffix="/ day"
              prefix={<ReadOutlined />}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

// Import missing icons
import { AppstoreOutlined, LineChartOutlined, FileTextOutlined, ReadOutlined } from '@ant-design/icons';

export default HomePage;
