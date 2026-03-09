import React, { useEffect, useState } from 'react';
import AppLayout from '../components/Layout';
import { Card, Row, Col, Tabs, Spin } from 'antd';
import { indexAPI, reportAPI } from '../services/api';
import MarketOverviewCard from '../components/MarketOverview';

const { TabPane } = Tabs;

export default function Home() {
  const [loading, setLoading] = useState(true);
  const [marketData, setMarketData] = useState({});
  const [latestReport, setLatestReport] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);

      // Fetch market overview
      const overviewRes = await indexAPI.getMarketOverview();
      setMarketData(overviewRes.data);

      // Fetch latest daily report
      try {
        const reportRes = await reportAPI.getLatestDailyReport();
        setLatestReport(reportRes.data);
      } catch (err) {
        console.log('No reports available yet');
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getAllIndices = () => {
    const allIndices = [];
    Object.values(marketData).forEach(marketIndices => {
      marketIndices.forEach(index => allIndices.push(index));
    });
    return allIndices;
  };

  if (loading) {
    return (
      <AppLayout>
        <div className="flex justify-center items-center h-96">
          <Spin size="large" />
        </div>
      </AppLayout>
    );
  }

  return (
    <AppLayout>
      <div className="space-y-6">
        {/* Page Title */}
        <div>
          <h1 className="text-3xl font-bold mb-2">Global Stock Market Intelligence Platform</h1>
          <p className="text-gray-600">AI-Powered Market Analysis and Insights</p>
        </div>

        {/* Market Overview */}
        <Card title="🌍 Global Market Overview" className="shadow-md">
          <Tabs defaultActiveKey="all">
            <TabPane tab="All Markets" key="all">
              <MarketOverviewCard indices={getAllIndices()} />
            </TabPane>
            {Object.entries(marketData).map(([market, indices]) => (
              <TabPane tab={market} key={market}>
                <MarketOverviewCard indices={indices} />
              </TabPane>
            ))}
          </Tabs>
        </Card>

        {/* Latest Report */}
        {latestReport && (
          <Card title="📊 Latest Market Report" className="shadow-md">
            <div>
              <h3 className="text-xl font-semibold mb-2">{latestReport.title}</h3>
              <p className="text-gray-600 mb-4">{latestReport.summary}</p>
              <div className="bg-gray-50 p-4 rounded">
                <pre className="whitespace-pre-wrap text-sm">{latestReport.content.substring(0, 500)}...</pre>
              </div>
            </div>
          </Card>
        )}

        {/* Quick Stats */}
        <Row gutter={[16, 16]}>
          <Col xs={24} sm={12} md={6}>
            <Card className="shadow-md">
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">{getAllIndices().length}</div>
                <div className="text-gray-600 mt-2">Global Indices</div>
              </div>
            </Card>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Card className="shadow-md">
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600">Real-time</div>
                <div className="text-gray-600 mt-2">Market Data</div>
              </div>
            </Card>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Card className="shadow-md">
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-600">AI-Powered</div>
                <div className="text-gray-600 mt-2">Analysis</div>
              </div>
            </Card>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Card className="shadow-md">
              <div className="text-center">
                <div className="text-3xl font-bold text-orange-600">24/7</div>
                <div className="text-gray-600 mt-2">Monitoring</div>
              </div>
            </Card>
          </Col>
        </Row>
      </div>
    </AppLayout>
  );
}
