# 部署和运行指南

## 🎉 项目已成功构建!

全球股票市场智能分析平台已完成构建和测试,现在可以访问使用。

## 📍 当前状态

### ✅ 后端服务 (FastAPI)
- **状态**: 运行中
- **端口**: 8000
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

### ✅ 前端服务 (HTML/JavaScript)
- **状态**: 运行中
- **端口**: 3000
- **访问地址**: http://localhost:3000/index.html

## 🚀 快速访问

### 主页面
```
http://localhost:3000/index.html
```

### API接口
```
# 市场指数
http://localhost:8000/api/v1/indices

# 股票列表
http://localhost:8000/api/v1/stocks

# 新闻资讯
http://localhost:8000/api/v1/news

# 市场报告
http://localhost:8000/api/v1/reports
```

## 📊 功能测试

### 运行测试脚本
```bash
cd /mnt/dev_vibe_77
./test_platform.sh
```

### 手动测试API
```bash
# 测试健康检查
curl http://localhost:8000/health

# 获取市场指数
curl http://localhost:8000/api/v1/indices | python3 -m json.tool

# 获取股票数据
curl http://localhost:8000/api/v1/stocks | python3 -m json.tool
```

## 🔧 管理服务

### 停止服务
```bash
# 停止后端
ps aux | grep "python.*app_simple" | grep -v grep | awk '{print $2}' | xargs kill

# 停止前端
ps aux | grep "http.server 3000" | grep -v grep | awk '{print $2}' | xargs kill
```

### 重启服务
```bash
# 重启后端
cd /mnt/dev_vibe_77/stock-market-platform/backend
./venv/bin/python app_simple.py > logs/backend.log 2>&1 &

# 重启前端
cd /mnt/dev_vibe_77/stock-market-platform/frontend
python3 -m http.server 3000 > /dev/null 2>&1 &
```

### 查看日志
```bash
# 后端日志
tail -f /mnt/dev_vibe_77/stock-market-platform/backend/logs/backend.log

# 检查进程
ps aux | grep -E "python.*app_simple|http.server 3000"
```

## 📁 项目结构

```
stock-market-platform/
├── backend/                    # 后端API服务
│   ├── app/                   # 应用代码
│   │   ├── api/              # API路由
│   │   ├── core/             # 核心配置
│   │   ├── models/           # 数据模型
│   │   ├── services/         # 业务服务
│   │   └── main.py           # 主应用
│   ├── app_simple.py         # 简化版应用(当前使用)
│   ├── venv/                 # Python虚拟环境
│   └── logs/                 # 日志文件
├── frontend/                  # 前端应用
│   ├── index.html            # 主页面(当前使用)
│   ├── src/                  # React源码
│   └── public/               # 静态资源
├── crawler/                   # 数据爬虫
├── database/                  # 数据库
├── docs/                      # 文档
└── scripts/                   # 工具脚本
```

## 🎯 核心功能

### 1. 市场总览
- 实时全球主要市场指数
- 美国: S&P500, NASDAQ, Dow Jones
- 中国: 上证指数, 深证成指
- 香港: 恒生指数

### 2. 股票数据
- 个股实时价格
- 涨跌幅统计
- 市场分类

### 3. 新闻资讯
- 市场新闻聚合
- AI情绪分析
- 多来源整合

### 4. 市场报告
- 每日市场总结
- 每周市场回顾
- AI自动生成

## 🔍 API使用示例

### JavaScript
```javascript
// 获取市场指数
fetch('http://localhost:8000/api/v1/indices')
  .then(res => res.json())
  .then(data => console.log(data));

// 获取新闻
fetch('http://localhost:8000/api/v1/news')
  .then(res => res.json())
  .then(data => console.log(data));
```

### Python
```python
import requests

# 获取市场数据
response = requests.get('http://localhost:8000/api/v1/indices')
indices = response.json()
print(indices)

# 获取股票列表
response = requests.get('http://localhost:8000/api/v1/stocks')
stocks = response.json()
print(stocks)
```

### cURL
```bash
# 获取市场总览
curl -X GET "http://localhost:8000/api/v1/indices/market/overview"

# 按市场筛选股票
curl -X GET "http://localhost:8000/api/v1/stocks?market=US&limit=10"

# 获取报告
curl -X GET "http://localhost:8000/api/v1/reports?report_type=daily"
```

## 🎨 前端功能

### 实时数据展示
- 市场指数卡片
- 涨跌幅可视化
- 颜色区分(绿涨红跌)

### 交互功能
- 卡片悬停效果
- 平滑动画
- 响应式设计

### 自动刷新
- 每30秒自动更新数据
- 无需手动刷新

## ⚙️ 配置说明

### 后端配置
位置: `backend/app/core/config.py`

```python
# 数据库
DATABASE_URL = "sqlite:///./stock_market.db"

# CORS设置
CORS_ORIGINS = ["*"]  # 允许所有来源

# API密钥(可选)
ALPHA_VANTAGE_API_KEY = ""
OPENAI_API_KEY = ""
```

### 前端配置
位置: `frontend/index.html`

```javascript
// API地址
const API_URL = 'http://localhost:8000';

// 刷新间隔(毫秒)
setInterval(fetchMarketData, 30000);
```

## 🔐 安全提示

当前版本用于开发和演示,生产环境需要:
- 配置CORS白名单
- 添加API认证
- 使用HTTPS
- 数据库迁移到PostgreSQL
- 添加速率限制

## 📈 性能优化建议

1. **缓存**: 使用Redis缓存热点数据
2. **CDN**: 静态资源使用CDN
3. **数据库**: 添加索引,优化查询
4. **压缩**: 启用Gzip压缩
5. **异步**: 使用异步任务处理

## 🐛 常见问题

### 端口被占用
```bash
# 查找占用端口的进程
lsof -i :8000
lsof -i :3000

# 杀掉进程
kill -9 <PID>
```

### 连接失败
- 检查防火墙设置
- 确认服务正在运行
- 验证端口号正确

### 数据不显示
- 检查CORS设置
- 查看浏览器控制台
- 验证API响应

## 📞 支持

项目地址: `/mnt/dev_vibe_77/stock-market-platform`

测试脚本: `/mnt/dev_vibe_77/test_platform.sh`

日志位置:
- 后端: `backend/logs/backend.log`
- 前端: `frontend/logs/frontend.log`

---

**注意**: 本平台仅供学习和研究使用,不构成投资建议。
