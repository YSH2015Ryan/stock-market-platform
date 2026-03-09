import React from 'react';
import { Layout, Menu } from 'antd';
import { HomeOutlined, LineChartOutlined, ReadOutlined, FundOutlined, AppstoreOutlined } from '@ant-design/icons';
import Link from 'next/link';
import { useRouter } from 'next/router';

const { Header, Content, Footer } = Layout;

const AppLayout = ({ children }) => {
  const router = useRouter();

  const menuItems = [
    {
      key: '/',
      icon: <HomeOutlined />,
      label: <Link href="/">Home</Link>,
    },
    {
      key: '/markets',
      icon: <LineChartOutlined />,
      label: <Link href="/markets">Markets</Link>,
    },
    {
      key: '/stocks',
      icon: <FundOutlined />,
      label: <Link href="/stocks">Stocks</Link>,
    },
    {
      key: '/reports',
      icon: <ReadOutlined />,
      label: <Link href="/reports">Reports</Link>,
    },
    {
      key: '/screener',
      icon: <AppstoreOutlined />,
      label: <Link href="/screener">Screener</Link>,
    },
  ];

  return (
    <Layout className="min-h-screen">
      <Header className="flex items-center bg-gray-900">
        <div className="text-white text-xl font-bold mr-8">
          📈 Stock Market Platform
        </div>
        <Menu
          theme="dark"
          mode="horizontal"
          selectedKeys={[router.pathname]}
          items={menuItems}
          className="flex-1 bg-gray-900"
        />
      </Header>
      <Content className="p-6 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          {children}
        </div>
      </Content>
      <Footer className="text-center bg-gray-100">
        Stock Market Intelligence Platform ©2024 | AI-Powered Market Analysis
      </Footer>
    </Layout>
  );
};

export default AppLayout;
