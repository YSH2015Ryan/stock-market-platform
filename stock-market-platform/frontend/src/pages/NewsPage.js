import React, { useEffect, useState } from 'react';
import { Typography, Card, List, Tag, Spin } from 'antd';
import { ClockCircleOutlined } from '@ant-design/icons';
import axios from 'axios';
import dayjs from 'dayjs';

const { Title, Paragraph } = Typography;

const NewsPage = () => {
  const [loading, setLoading] = useState(true);
  const [news, setNews] = useState([]);

  useEffect(() => {
    fetchNews();
  }, []);

  const fetchNews = async () => {
    try {
      const response = await axios.get('/api/v1/news?limit=20');
      setNews(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching news:', error);
      // Mock data
      setNews([
        {
          id: 1,
          title: 'Tech Stocks Rally on Positive Earnings',
          content: 'Major technology companies reported strong quarterly earnings...',
          source: 'Financial Times',
          published_at: new Date().toISOString(),
          sentiment: 'positive'
        },
        {
          id: 2,
          title: 'Federal Reserve Maintains Interest Rates',
          content: 'The Federal Reserve announced it will keep interest rates unchanged...',
          source: 'Reuters',
          published_at: new Date(Date.now() - 3600000).toISOString(),
          sentiment: 'neutral'
        },
        {
          id: 3,
          title: 'Market Volatility Expected Amid Economic Data',
          content: 'Analysts predict increased market volatility as key economic indicators...',
          source: 'Bloomberg',
          published_at: new Date(Date.now() - 7200000).toISOString(),
          sentiment: 'negative'
        },
      ]);
      setLoading(false);
    }
  };

  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case 'positive':
        return 'green';
      case 'negative':
        return 'red';
      default:
        return 'blue';
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
      <Title level={2}>Market News</Title>

      <Card>
        <List
          itemLayout="vertical"
          dataSource={news}
          renderItem={(item) => (
            <List.Item
              key={item.id}
              extra={
                <Tag color={getSentimentColor(item.sentiment)}>
                  {item.sentiment?.toUpperCase() || 'NEUTRAL'}
                </Tag>
              }
            >
              <List.Item.Meta
                title={<a style={{ fontSize: '18px' }}>{item.title}</a>}
                description={
                  <span>
                    <ClockCircleOutlined /> {dayjs(item.published_at).format('YYYY-MM-DD HH:mm')} | {item.source}
                  </span>
                }
              />
              <Paragraph ellipsis={{ rows: 2 }}>{item.content}</Paragraph>
            </List.Item>
          )}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showTotal: (total) => `Total ${total} news`,
          }}
        />
      </Card>
    </div>
  );
};

export default NewsPage;
