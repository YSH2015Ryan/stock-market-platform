# 🆓 免费云服务部署指南

## 🎯 部署架构

```
┌─────────────────────────────────────────────────────────┐
│                     免费云服务架构                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  👤 用户                                                │
│   │                                                     │
│   ├──> 🌐 Vercel (前端)                                │
│   │     • React 应用                                    │
│   │     • 自动 HTTPS                                    │
│   │     • 全球 CDN                                      │
│   │     • 100GB 流量/月                                 │
│   │                                                     │
│   └──> 🚀 Render (后端)                                │
│         • FastAPI 应用                                  │
│         • 512MB RAM                                     │
│         • 750 小时/月                                   │
│         │                                               │
│         ├──> 🐘 PostgreSQL (Render)                    │
│         │     • 免费 1GB 存储                           │
│         │     • 自动备份                                │
│         │                                               │
│         └──> 💾 Upstash Redis                          │
│               • 10K 命令/天                            │
│               • 256MB 存储                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 前置要求

### 1. 必需账号（全部免费）

- ✅ **GitHub** - 代码托管
  - 🔗 https://github.com/signup

- ✅ **Render** - 后端 + 数据库
  - 🔗 https://render.com/register
  - 💳 无需信用卡

- ✅ **Vercel** - 前端托管
  - 🔗 https://vercel.com/signup
  - 💳 无需信用卡

- ✅ **Upstash** - Redis 缓存（可选）
  - 🔗 https://upstash.com/
  - 💳 无需信用卡

### 2. 本地工具

```bash
# Node.js 18+ 和 NPM
node --version  # v18.0.0+
npm --version   # 9.0.0+

# Git
git --version   # 2.0+

# Python 3.11+
python --version  # 3.11+
```

---

## 🚀 快速部署（5 步完成）

### 步骤 1️⃣: 准备代码

```bash
# 1. 克隆或进入项目目录
cd stock-market-platform

# 2. 初始化 Git（如果还没有）
git init
git add .
git commit -m "Initial commit for cloud deployment"

# 3. 推送到 GitHub
git remote add origin https://github.com/YOUR_USERNAME/stock-market-platform.git
git branch -M main
git push -u origin main
```

### 步骤 2️⃣: 部署后端到 Render

#### 方式 A: 使用 Blueprint（推荐）

1. 登录 [Render Dashboard](https://dashboard.render.com/)

2. 点击 **"New +"** → **"Blueprint"**

3. 连接 GitHub 仓库并选择 `stock-market-platform`

4. Render 会自动检测 `render.yaml` 配置文件

5. 点击 **"Apply"** 开始部署

6. 等待 5-10 分钟完成部署

#### 方式 B: 手动创建

1. **创建后端服务**
   - New + → Web Service
   - 连接 GitHub 仓库
   - 设置:
     ```
     Name: stock-market-backend
     Runtime: Python 3
     Build Command: pip install -r requirements.prod.txt
     Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
     Plan: Free
     ```

2. **创建 PostgreSQL 数据库**
   - New + → PostgreSQL
   - Name: stock-market-db
   - Plan: Free
   - 复制 Internal Database URL

3. **创建 Redis**（如果可用）
   - New + → Redis
   - Name: stock-market-redis
   - Plan: Free

#### 配置环境变量

在 Render Dashboard → Your Service → Environment:

```bash
# 必需
DATABASE_URL=<从 PostgreSQL 复制>
REDIS_URL=<从 Redis 复制，或使用 Upstash>
SECRET_KEY=<生成随机字符串>
JWT_SECRET_KEY=<生成随机字符串>

# 可选
DEBUG=False
ENVIRONMENT=production
CORS_ORIGINS=https://your-app.vercel.app

# API 密钥（可选）
ALPHA_VANTAGE_API_KEY=your_key
FINNHUB_API_KEY=your_key
```

**生成密钥:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 步骤 3️⃣: 设置 Upstash Redis（可选）

1. 访问 [Upstash Console](https://console.upstash.com/)

2. 点击 **"Create Database"**

3. 配置:
   ```
   Name: stock-market-redis
   Type: Redis
   Region: 选择最近的
   Plan: Free (10K commands/day)
   ```

4. 创建后，复制 **REST URL**

5. 在 Render 环境变量中设置:
   ```
   REDIS_URL=<Upstash REST URL>
   ```

### 步骤 4️⃣: 部署前端到 Vercel

#### 方式 A: 使用 CLI（推荐）

```bash
# 1. 安装 Vercel CLI
npm install -g vercel

# 2. 进入前端目录
cd frontend

# 3. 部署
vercel

# 按提示操作:
# - Set up and deploy? Yes
# - Which scope? (选择您的账号)
# - Link to existing project? No
# - What's your project's name? stock-market-frontend
# - In which directory is your code located? ./
# - Want to override the settings? No

# 4. 生产部署
vercel --prod
```

#### 方式 B: 使用网页界面

1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)

2. 点击 **"Add New..."** → **"Project"**

3. 导入 GitHub 仓库

4. 配置:
   ```
   Framework Preset: Create React App
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: build
   ```

5. 添加环境变量:
   ```
   REACT_APP_API_URL=https://your-backend.onrender.com
   ```

6. 点击 **"Deploy"**

### 步骤 5️⃣: 更新 CORS 配置

1. 获取 Vercel 前端 URL:
   ```
   https://your-app.vercel.app
   ```

2. 在 Render Dashboard 更新后端环境变量:
   ```
   CORS_ORIGINS=https://your-app.vercel.app
   ```

3. 重启后端服务:
   - Dashboard → Your Service → Manual Deploy → "Deploy latest commit"

---

## ✅ 验证部署

### 测试后端

```bash
# 健康检查
curl https://your-backend.onrender.com/health
# 预期: {"status":"healthy"}

# API 文档
open https://your-backend.onrender.com/docs
```

### 测试前端

```bash
# 访问前端
open https://your-app.vercel.app
```

### 测试数据库连接

```bash
# 使用 Render Shell
# Dashboard → PostgreSQL → Shell

\dt  # 列出表
```

---

## 🔧 常用操作

### 查看日志

**Render:**
```
Dashboard → Your Service → Logs
```

**Vercel:**
```
Dashboard → Your Project → Deployments → View Function Logs
```

### 更新代码

```bash
# 1. 提交更改
git add .
git commit -m "Update feature"
git push

# 2. 自动部署
# Render 和 Vercel 会自动检测并重新部署
```

### 回滚版本

**Render:**
```
Dashboard → Your Service → Manual Deploy → Select previous commit
```

**Vercel:**
```
Dashboard → Deployments → Select previous → Promote to Production
```

### 配置自定义域名

**Vercel:**
```
Settings → Domains → Add Domain → 按提示配置 DNS
```

**Render:**
```
Settings → Custom Domain → Add Domain → 配置 CNAME 记录
```

---

## 📊 免费额度限制

### Render Free Tier

| 资源 | 限制 |
|------|------|
| **RAM** | 512 MB |
| **CPU** | 0.1 CPU |
| **运行时间** | 750 小时/月 |
| **休眠** | 15 分钟无活动后休眠 |
| **唤醒时间** | 30-60 秒 |
| **带宽** | 100 GB/月 |

### Vercel Free Tier

| 资源 | 限制 |
|------|------|
| **带宽** | 100 GB/月 |
| **构建时间** | 6000 分钟/月 |
| **项目数** | 无限 |
| **域名** | 无限 |

### PostgreSQL (Render Free)

| 资源 | 限制 |
|------|------|
| **存储** | 1 GB |
| **连接数** | 97 |
| **保留期** | 90 天 |

### Upstash Redis Free

| 资源 | 限制 |
|------|------|
| **命令数** | 10,000/天 |
| **存储** | 256 MB |
| **最大请求大小** | 1 MB |

### API 服务限制

| 服务 | 免费限制 |
|------|---------|
| **Alpha Vantage** | 5 请求/分钟, 500 请求/天 |
| **Finnhub** | 60 请求/分钟 |
| **OpenAI** | 按使用付费（$5 免费额度） |

---

## ⚠️ 重要注意事项

### 1. 休眠问题

Render 免费层会在 15 分钟无活动后休眠：

**解决方案 A: 使用定时 Ping**
```bash
# 使用 UptimeRobot (免费)
# https://uptimerobot.com
# 每 5 分钟 ping 一次你的后端
```

**解决方案 B: 使用 GitHub Actions**
```yaml
# .github/workflows/keep-alive.yml
name: Keep Alive
on:
  schedule:
    - cron: '*/10 * * * *'  # 每 10 分钟

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping backend
        run: curl https://your-backend.onrender.com/health
```

### 2. 数据库备份

```bash
# Render 免费数据库 90 天后删除
# 定期导出数据:

# 连接到数据库
pg_dump $DATABASE_URL > backup.sql

# 或使用 Render Dashboard
# Database → Backups → Create Backup
```

### 3. 环境变量安全

- ❌ 不要提交 `.env` 文件到 Git
- ✅ 使用平台的环境变量管理
- ✅ 定期更新密钥

### 4. 性能优化

```python
# 启用缓存减少数据库查询
@app.get("/stocks/{symbol}")
async def get_stock(symbol: str):
    # 先查 Redis 缓存
    cached = await redis.get(f"stock:{symbol}")
    if cached:
        return cached

    # 查询数据库
    data = await db.query(symbol)

    # 缓存 5 分钟
    await redis.setex(f"stock:{symbol}", 300, data)
    return data
```

---

## 🐛 故障排查

### 问题 1: 部署失败

**检查:**
```bash
# 查看构建日志
Render Dashboard → Logs

# 常见问题:
# - requirements.txt 中的包无法安装
# - 内存不足 (使用 requirements.prod.txt)
# - Python 版本不匹配
```

**解决:**
```bash
# 使用优化的依赖
cp backend/requirements.prod.txt backend/requirements.txt
git commit -am "Use production requirements"
git push
```

### 问题 2: CORS 错误

**错误信息:**
```
Access to fetch at 'https://backend.onrender.com/api'
from origin 'https://frontend.vercel.app' has been blocked by CORS
```

**解决:**
```bash
# 在 Render 环境变量中添加:
CORS_ORIGINS=https://your-app.vercel.app,https://your-app-*.vercel.app
```

### 问题 3: 数据库连接失败

**检查:**
```bash
# 验证 DATABASE_URL 格式
postgresql://user:password@hostname:5432/database

# 在 Render Shell 测试连接
python -c "from sqlalchemy import create_engine; engine = create_engine('$DATABASE_URL'); print(engine.connect())"
```

### 问题 4: 前端无法访问后端

**检查:**
```bash
# 1. 验证后端 URL
curl https://your-backend.onrender.com/health

# 2. 检查前端环境变量
# Vercel Dashboard → Settings → Environment Variables
REACT_APP_API_URL=https://your-backend.onrender.com

# 3. 重新部署前端
vercel --prod
```

---

## 🎓 学习资源

### 官方文档

- 📘 [Render Docs](https://render.com/docs)
- 📘 [Vercel Docs](https://vercel.com/docs)
- 📘 [Upstash Docs](https://docs.upstash.com/)

### 视频教程

- 🎥 [Deploy FastAPI to Render](https://www.youtube.com/results?search_query=deploy+fastapi+render)
- 🎥 [Deploy React to Vercel](https://www.youtube.com/results?search_query=deploy+react+vercel)

### 社区支持

- 💬 [Render Community](https://community.render.com/)
- 💬 [Vercel Discord](https://vercel.com/discord)

---

## 📈 下一步

### 1. 监控和分析

- **Sentry** - 错误追踪
  - 🔗 https://sentry.io (免费 5K 错误/月)

- **Google Analytics** - 用户分析
  - 🔗 https://analytics.google.com

- **UptimeRobot** - 可用性监控
  - 🔗 https://uptimerobot.com (免费 50 监控)

### 2. CI/CD 优化

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Render
        run: echo "Render auto-deploys on push"
```

### 3. 性能优化

- 启用 Redis 缓存
- 压缩静态资源
- 使用 CDN
- 数据库查询优化
- 添加索引

### 4. 安全加固

- 启用 API 速率限制
- 添加请求验证
- 实现 JWT 认证
- 配置 HTTPS only
- 定期更新依赖

---

## 💰 升级到付费版本

如果免费额度不够用，可以考虑升级:

### Render 付费版

| 方案 | 价格 | 资源 |
|------|------|------|
| **Starter** | $7/月 | 512 MB RAM, 不休眠 |
| **Standard** | $25/月 | 2 GB RAM, 2 CPU |
| **Pro** | $85/月 | 4 GB RAM, 4 CPU |

### Vercel 付费版

| 方案 | 价格 | 资源 |
|------|------|------|
| **Pro** | $20/月 | 1 TB 带宽 |
| **Enterprise** | 定制 | 无限制 |

---

## 🤝 获取帮助

遇到问题？

1. 📖 查看本文档
2. 🔍 搜索 [Render Community](https://community.render.com/)
3. 💬 访问 [Vercel Discord](https://vercel.com/discord)
4. 📧 联系技术支持

---

## 📝 更新日志

- **2024-03-10**: 初始版本
  - 添加 Render + Vercel 部署指南
  - 优化依赖配置
  - 添加故障排查指南

---

**🎉 祝您部署顺利！**
