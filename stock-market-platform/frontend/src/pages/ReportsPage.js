import React, { useEffect, useState } from 'react';
import { Typography, Card, List, Tag, Spin, Button } from 'antd';
import { FileTextOutlined, CalendarOutlined } from '@ant-design/icons';
import axios from 'axios';
import dayjs from 'dayjs';

const { Title, Paragraph } = Typography;

const ReportsPage = () => {
  const [loading, setLoading] = useState(true);
  const [reports, setReports] = useState([]);

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      const response = await axios.get('/api/v1/reports?limit=10');
      setReports(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching reports:', error);
      // Mock data
      setReports([
        {
          id: 1,
          title: 'Daily Market Summary - Strong Performance in Tech Sector',
          report_type: 'daily',
          summary: 'Technology stocks led market gains today with NASDAQ up 1.2%. Major indices showed positive momentum...',
          content: 'Full report content...',
          market: 'US',
          report_date: new Date().toISOString()
        },
        {
          id: 2,
          title: 'Weekly Market Report - Mixed Signals Across Global Markets',
          report_type: 'weekly',
          summary: 'This week saw mixed performance across global markets. US markets gained while Asian markets faced pressure...',
          content: 'Full report content...',
          market: null,
          report_date: new Date(Date.now() - 86400000).toISOString()
        },
        {
          id: 3,
          title: 'Sector Analysis - Energy Sector Outlook',
          report_type: 'sector',
          summary: 'Energy sector shows resilience amid global economic concerns. Oil prices stabilized...',
          content: 'Full report content...',
          market: 'US',
          report_date: new Date(Date.now() - 172800000).toISOString()
        },
      ]);
      setLoading(false);
    }
  };

  const getReportTypeColor = (type) => {
    switch (type) {
      case 'daily':
        return 'blue';
      case 'weekly':
        return 'green';
      case 'monthly':
        return 'orange';
      default:
        return 'purple';
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
      <Title level={2}>Market Reports</Title>
      <Paragraph style={{ fontSize: '16px', marginBottom: '24px' }}>
        AI-generated market analysis and insights
      </Paragraph>

      <Card>
        <List
          itemLayout="vertical"
          dataSource={reports}
          renderItem={(item) => (
            <List.Item
              key={item.id}
              actions={[
                <Button type="link" icon={<FileTextOutlined />}>
                  Read Full Report
                </Button>
              ]}
            >
              <List.Item.Meta
                title={
                  <div>
                    <span style={{ fontSize: '18px', marginRight: '12px' }}>{item.title}</span>
                    <Tag color={getReportTypeColor(item.report_type)}>
                      {item.report_type?.toUpperCase()}
                    </Tag>
                    {item.market && <Tag>{item.market}</Tag>}
                  </div>
                }
                description={
                  <span>
                    <CalendarOutlined /> {dayjs(item.report_date).format('YYYY-MM-DD')}
                  </span>
                }
              />
              <Paragraph>{item.summary}</Paragraph>
            </List.Item>
          )}
          pagination={{
            pageSize: 5,
            showTotal: (total) => `Total ${total} reports`,
          }}
        />
      </Card>
    </div>
  );
};

export default ReportsPage;
