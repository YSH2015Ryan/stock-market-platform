# Global Stock Market Intelligence Platform

全球股票市场智能分析平台 - 专业的股票市场回顾与分析系统

## 项目简介

这是一个基于AI的全球股票市场分析平台,提供:
- 全球主要股票市场实时数据
- AI驱动的市场分析和报告生成
- 股票筛选和研究工具
- 投资组合管理
- 新闻情绪分析

## 技术栈

### 前端
- **框架**: React 18 + Next.js 14
- **状态管理**: Redux Toolkit
- **图表**: ECharts, TradingView
- **UI**: Ant Design + Tailwind CSS

### 后端
- **框架**: Python FastAPI
- **数据库**: PostgreSQL 15
- **缓存**: Redis
- **搜索**: Elasticsearch (可选)

### 爬虫
- **框架**: Scrapy
- **调度**: APScheduler

### AI分析
- **LLM**: OpenAI GPT-4 / Anthropic Claude
- **NLP**: Transformers (情绪分析)

## 项目结构

```
stock-market-platform/
├── backend/              # FastAPI后端服务
│   ├── app/
│   │   ├── api/         # API路由
│   │   ├── models/      # 数据库模型
│   │   ├── services/    # 业务逻辑
│   │   └── core/        # 核心配置
│   └── tests/           # 测试
├── frontend/            # React前端应用
│   ├── src/
│   │   ├── components/  # React组件
│   │   ├── pages/       # 页面
│   │   ├── services/    # API服务
│   │   └── utils/       # 工具函数
│   └── public/          # 静态资源
├── crawler/             # 数据爬虫
│   ├── spiders/         # 爬虫脚本
│   └── pipelines/       # 数据处理管道
├── database/            # 数据库脚本
│   ├── migrations/      # 数据库迁移
│   └── seeds/           # 初始数据
├── docs/                # 文档
└── scripts/             # 部署和工具脚本
```

## 快速开始

### 前置要求
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Docker & Docker Compose (推荐)

### Docker部署 (推荐)

```bash
# 克隆项目
git clone <repository-url>
cd stock-market-platform

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件,填入必要的API密钥

# 启动所有服务
docker-compose up -d

# 访问应用
# 前端: http://localhost:3000
# 后端API: http://localhost:8000
# API文档: http://localhost:8000/docs
```

### 手动部署

#### 1. 后端设置

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 配置数据库
createdb stock_market

# 运行迁移
alembic upgrade head

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 2. 前端设置

```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:3000
```

#### 3. 爬虫设置

```bash
cd crawler
pip install -r requirements.txt

# 运行爬虫
python scheduler.py
```

## 核心功能

### 1. 市场总览
- 全球主要指数实时数据 (S&P500, NASDAQ, 上证, 深证等)
- 行业涨跌排行
- 热门股票追踪
- K线图和热力图可视化

### 2. AI市场回顾
- 每日/每周自动生成市场分析报告
- 宏观、行业、个股三层分析
- 资金流向分析

### 3. 数据抓取
- SEC、NASDAQ、NYSE官方数据
- 上交所、深交所公告
- 公司财报和新闻

### 4. 股票分析
- 实时行情和历史数据
- 财务指标 (PE, PB, ROE等)
- 技术指标 (RSI, MACD, MA等)
- AI生成的股票摘要和风险提示

### 5. 股票筛选器
- 多维度筛选条件
- 技术面和基本面筛选
- 自定义筛选策略

### 6. 投资组合管理
- 持仓跟踪
- 收益统计
- 风险分析

### 7. AI问答助手
- 基于市场数据的智能问答
- 结合新闻和宏观经济分析

### 8. 新闻情绪分析
- 自动抓取金融新闻
- AI情绪分析 (利好/利空/中性)
- 影响度评估

## API文档

启动后端服务后,访问:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 配置

主要配置项在 `.env` 文件中:

```env
# 数据库
DATABASE_URL=postgresql://user:password@localhost:5432/stock_market

# API Keys
ALPHA_VANTAGE_API_KEY=your_key
OPENAI_API_KEY=your_key

# Redis
REDIS_URL=redis://localhost:6379/0

# 应用配置
DEBUG=False
SECRET_KEY=your-secret-key
```

## 测试

```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm test
```

## 部署

详见 [部署文档](docs/DEPLOYMENT.md)

## 开发计划

- [x] 基础架构搭建
- [x] 后端API开发
- [x] 前端界面开发
- [x] 数据爬虫实现
- [x] AI分析集成
- [ ] Elasticsearch集成
- [ ] 量化回测功能
- [ ] 移动端适配
- [ ] 投资社区功能

## 贡献

欢迎提交Issue和Pull Request!

## 许可证

MIT License

## 联系方式

- 项目地址: GitHub
- 文档: [在线文档]
- 问题反馈: Issues

---

**注意**: 本系统仅供研究和学习使用,不构成投资建议。投资有风险,决策需谨慎。
