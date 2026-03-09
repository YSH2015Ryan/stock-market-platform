import React from 'react';
import ReactECharts from 'echarts-for-react';

const StockChart = ({ data, type = 'line' }) => {
  if (!data || data.length === 0) {
    return <div className="text-center p-8 text-gray-500">No data available</div>;
  }

  const dates = data.map(d => d.date);
  const prices = data.map(d => d.close);

  const option = {
    title: {
      text: 'Stock Price',
      left: 'center',
    },
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const param = params[0];
        return `${param.name}<br/>Price: $${param.value.toFixed(2)}`;
      },
    },
    xAxis: {
      type: 'category',
      data: dates,
      boundaryGap: false,
    },
    yAxis: {
      type: 'value',
      scale: true,
      axisLabel: {
        formatter: '${value}',
      },
    },
    series: [
      {
        name: 'Price',
        type: type,
        data: prices,
        smooth: true,
        lineStyle: {
          width: 2,
        },
        areaStyle: type === 'line' ? {
          opacity: 0.3,
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(24, 144, 255, 0.5)' },
              { offset: 1, color: 'rgba(24, 144, 255, 0.1)' },
            ],
          },
        } : undefined,
      },
    ],
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
  };

  return <ReactECharts option={option} style={{ height: '400px' }} />;
};

export default StockChart;
