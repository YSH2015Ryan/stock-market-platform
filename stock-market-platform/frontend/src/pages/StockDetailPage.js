import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Typography, Card, Spin, Row, Col, Statistic } from 'antd';
import axios from 'axios';

const { Title, Paragraph } = Typography;

const StockDetailPage = () => {
  const { symbol } = useParams();
  const [loading, setLoading] = useState(true);
  const [stock, setStock] = useState(null);

  useEffect(() => {
    fetchStockData();
  }, [symbol]);

  const fetchStockData = async () => {
    try {
      const response = await axios.get(`/api/v1/stocks/${symbol}`);
      setStock(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching stock data:', error);
      // Mock data
      setStock({
        symbol: symbol,
        name: 'Sample Company Inc.',
        market: 'US',
        sector: 'Technology',
        market_cap: 1000000000000,
        description: 'This is a sample company description.'
      });
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '100px 0' }}>
        <Spin size="large" />
      </div>
    );
  }

  return (
    <div>
      <Title level={2}>{stock?.symbol} - {stock?.name}</Title>

      <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
        <Col span={6}>
          <Card>
            <Statistic title="Market" value={stock?.market} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="Sector" value={stock?.sector} />
          </Card>
        </Col>
        <Col span={12}>
          <Card>
            <Statistic
              title="Market Cap"
              value={stock?.market_cap ? (stock.market_cap / 1000000000).toFixed(2) : 'N/A'}
              suffix="B"
              prefix="$"
            />
          </Card>
        </Col>
      </Row>

      <Card title="Company Information" style={{ marginBottom: '24px' }}>
        <Paragraph>{stock?.description || 'No description available.'}</Paragraph>
      </Card>

      <Card title="Price Chart">
        <div style={{ height: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <Paragraph type="secondary">Price chart will be displayed here using ECharts</Paragraph>
        </div>
      </Card>
    </div>
  );
};

export default StockDetailPage;
