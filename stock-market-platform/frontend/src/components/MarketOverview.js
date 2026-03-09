import React from 'react';
import { Card, Row, Col, Statistic, Tag } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';

const MarketOverviewCard = ({ indices }) => {
  if (!indices || indices.length === 0) {
    return <div>Loading...</div>;
  }

  const renderIndexCard = (index) => {
    const isPositive = index.change >= 0;

    return (
      <Col xs={24} sm={12} md={8} lg={6} key={index.symbol}>
        <Card hoverable className="mb-4">
          <div className="mb-2">
            <span className="font-bold text-lg">{index.symbol}</span>
            <Tag color={index.market === 'US' ? 'blue' : 'green'} className="ml-2">
              {index.market}
            </Tag>
          </div>
          <div className="text-sm text-gray-500 mb-2">{index.name}</div>
          <Statistic
            value={index.value}
            precision={2}
            valueStyle={{ fontSize: '1.5rem' }}
          />
          <div className={`mt-2 ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
            {isPositive ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
            <span className="ml-1 font-semibold">
              {Math.abs(index.change_percent || 0).toFixed(2)}%
            </span>
            <span className="ml-2 text-sm">
              ({isPositive ? '+' : ''}{index.change?.toFixed(2)})
            </span>
          </div>
        </Card>
      </Col>
    );
  };

  return (
    <Row gutter={[16, 16]}>
      {indices.map(renderIndexCard)}
    </Row>
  );
};

export default MarketOverviewCard;
