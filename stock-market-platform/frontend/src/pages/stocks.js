import React, { useEffect, useState } from 'react';
import AppLayout from '../components/Layout';
import { Card, Table, Input, Select, Spin, Tag } from 'antd';
import { stockAPI } from '../services/api';
import { useRouter } from 'next/router';

const { Search } = Input;
const { Option } = Select;

export default function Stocks() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [stocks, setStocks] = useState([]);
  const [filteredStocks, setFilteredStocks] = useState([]);
  const [marketFilter, setMarketFilter] = useState(null);
  const [sectorFilter, setSectorFilter] = useState(null);

  useEffect(() => {
    fetchStocks();
  }, []);

  const fetchStocks = async () => {
    try {
      setLoading(true);
      const response = await stockAPI.getStocks({ limit: 100 });
      setStocks(response.data);
      setFilteredStocks(response.data);
    } catch (error) {
      console.error('Error fetching stocks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (value) => {
    const filtered = stocks.filter(stock =>
      stock.symbol.toLowerCase().includes(value.toLowerCase()) ||
      stock.name.toLowerCase().includes(value.toLowerCase())
    );
    setFilteredStocks(filtered);
  };

  const handleMarketFilter = (value) => {
    setMarketFilter(value);
    applyFilters(value, sectorFilter);
  };

  const handleSectorFilter = (value) => {
    setSectorFilter(value);
    applyFilters(marketFilter, value);
  };

  const applyFilters = (market, sector) => {
    let filtered = [...stocks];
    if (market) {
      filtered = filtered.filter(s => s.market === market);
    }
    if (sector) {
      filtered = filtered.filter(s => s.sector === sector);
    }
    setFilteredStocks(filtered);
  };

  const columns = [
    {
      title: 'Symbol',
      dataIndex: 'symbol',
      key: 'symbol',
      render: (text) => <span className="font-semibold">{text}</span>,
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
        <Tag color={market === 'US' ? 'blue' : market === 'CN' ? 'red' : 'green'}>
          {market}
        </Tag>
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
      render: (cap) => cap ? `$${(cap / 1e9).toFixed(2)}B` : 'N/A',
    },
  ];

  return (
    <AppLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold mb-2">Stock Explorer</h1>
          <p className="text-gray-600">Browse and analyze stocks from global markets</p>
        </div>

        <Card className="shadow-md">
          <div className="mb-4 flex gap-4 flex-wrap">
            <Search
              placeholder="Search by symbol or name"
              onSearch={handleSearch}
              onChange={(e) => handleSearch(e.target.value)}
              style={{ width: 300 }}
            />
            <Select
              placeholder="Filter by Market"
              style={{ width: 150 }}
              onChange={handleMarketFilter}
              allowClear
            >
              <Option value="US">US</Option>
              <Option value="CN">CN</Option>
              <Option value="HK">HK</Option>
              <Option value="EU">EU</Option>
            </Select>
            <Select
              placeholder="Filter by Sector"
              style={{ width: 200 }}
              onChange={handleSectorFilter}
              allowClear
            >
              <Option value="Technology">Technology</Option>
              <Option value="Healthcare">Healthcare</Option>
              <Option value="Financial">Financial</Option>
              <Option value="Energy">Energy</Option>
            </Select>
          </div>

          {loading ? (
            <div className="flex justify-center p-8">
              <Spin size="large" />
            </div>
          ) : (
            <Table
              columns={columns}
              dataSource={filteredStocks}
              rowKey="id"
              pagination={{ pageSize: 20 }}
              onRow={(record) => ({
                onClick: () => router.push(`/stock/${record.symbol}`),
                className: 'cursor-pointer hover:bg-gray-50',
              })}
            />
          )}
        </Card>
      </div>
    </AppLayout>
  );
}
