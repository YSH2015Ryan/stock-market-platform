# Global Stock Market Intelligence Platform

一个专业的全球股票市场智能分析平台，提供AI驱动的市场分析、实时数据和投资洞察。

## 🚀 快速启动

### 方法1: 使用Docker (推荐)
```bash
cd stock-market-platform
chmod +x scripts/start.sh
./scripts/start.sh
```

### 方法2: 手动启动

#### 后端服务
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### 前端服务
```bash
cd frontend
npm install
npm start
```

## 访问应用
- 前端: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 功能特性
- ✅ 全球市场指数监控
- ✅ 股票数据分析
- ✅ 新闻情绪分析
- ✅ AI市场报告
- ✅ 投资组合管理
- ✅ 研究工具

