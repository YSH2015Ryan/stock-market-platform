#!/bin/bash

# 🚀 股票市场平台 - 免费云服务部署脚本
# 支持: Render (后端) + Vercel (前端) + Upstash (Redis)

set -e

echo "🎯 股票市场平台 - 免费云服务部署向导"
echo "========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查必要工具
check_requirements() {
    echo -e "${BLUE}📋 检查必要工具...${NC}"

    if ! command -v git &> /dev/null; then
        echo -e "${RED}❌ Git 未安装${NC}"
        exit 1
    fi

    if ! command -v node &> /dev/null; then
        echo -e "${RED}❌ Node.js 未安装${NC}"
        exit 1
    fi

    if ! command -v npm &> /dev/null; then
        echo -e "${RED}❌ NPM 未安装${NC}"
        exit 1
    fi

    echo -e "${GREEN}✅ 所有工具已就绪${NC}"
    echo ""
}

# 生成密钥
generate_secret() {
    python3 -c "import secrets; print(secrets.token_urlsafe(32))"
}

# 步骤 1: 准备代码
prepare_code() {
    echo -e "${BLUE}📦 步骤 1: 准备代码${NC}"
    echo "-----------------------------------"

    # 检查是否在 Git 仓库中
    if [ ! -d ".git" ]; then
        echo -e "${YELLOW}初始化 Git 仓库...${NC}"
        git init
        git add .
        git commit -m "Initial commit: Stock Market Platform"
    fi

    # 复制生产环境 requirements
    if [ -f "backend/requirements.prod.txt" ]; then
        cp backend/requirements.prod.txt backend/requirements.txt
        echo -e "${GREEN}✅ 使用生产环境依赖配置${NC}"
    fi

    echo ""
}

# 步骤 2: 设置后端 (Render)
setup_backend() {
    echo -e "${BLUE}🔧 步骤 2: 设置后端 (Render)${NC}"
    echo "-----------------------------------"
    echo ""
    echo -e "${YELLOW}请按照以下步骤操作:${NC}"
    echo ""
    echo "1️⃣  访问 https://render.com 并登录/注册"
    echo ""
    echo "2️⃣  点击 'New +' -> 'Blueprint'"
    echo ""
    echo "3️⃣  连接您的 Git 仓库 (GitHub/GitLab)"
    echo ""
    echo "4️⃣  Render 会自动读取 render.yaml 配置"
    echo ""
    echo "5️⃣  点击 'Apply' 开始部署"
    echo ""
    echo "6️⃣  部署完成后，获取以下信息:"
    echo "    - Backend URL: https://your-app.onrender.com"
    echo "    - PostgreSQL Connection String"
    echo "    - Redis Connection String"
    echo ""
    echo -e "${GREEN}💡 提示: Render 免费层会在 15 分钟无活动后休眠${NC}"
    echo ""
    read -p "按 Enter 继续到下一步..."
    echo ""
}

# 步骤 3: 设置 Redis (Upstash)
setup_redis() {
    echo -e "${BLUE}💾 步骤 3: 设置 Redis (Upstash)${NC}"
    echo "-----------------------------------"
    echo ""
    echo -e "${YELLOW}如果 Render 免费层不包含 Redis, 使用 Upstash:${NC}"
    echo ""
    echo "1️⃣  访问 https://upstash.com 并登录/注册"
    echo ""
    echo "2️⃣  点击 'Create Database'"
    echo ""
    echo "3️⃣  选择:"
    echo "    - Type: Redis"
    echo "    - Name: stock-market-redis"
    echo "    - Region: 选择最近的区域"
    echo "    - Plan: Free (10K 命令/天)"
    echo ""
    echo "4️⃣  创建后，复制 'UPSTASH_REDIS_REST_URL'"
    echo ""
    read -p "按 Enter 继续到下一步..."
    echo ""
}

# 步骤 4: 配置环境变量
setup_env_vars() {
    echo -e "${BLUE}⚙️  步骤 4: 配置环境变量${NC}"
    echo "-----------------------------------"
    echo ""

    # 生成密钥
    echo -e "${YELLOW}生成安全密钥...${NC}"
    SECRET_KEY=$(generate_secret)
    JWT_SECRET=$(generate_secret)

    echo ""
    echo -e "${GREEN}请在 Render Dashboard 中设置以下环境变量:${NC}"
    echo ""
    echo "Dashboard -> Your Service -> Environment -> Add Environment Variable"
    echo ""
    echo "-----------------------------------"
    echo "SECRET_KEY=$SECRET_KEY"
    echo "JWT_SECRET_KEY=$JWT_SECRET"
    echo "DEBUG=False"
    echo "ENVIRONMENT=production"
    echo "CORS_ORIGINS=https://your-frontend.vercel.app"
    echo "-----------------------------------"
    echo ""
    echo -e "${YELLOW}可选 API 密钥 (获取免费额度):${NC}"
    echo ""
    echo "Alpha Vantage (股票数据):"
    echo "  🔗 https://www.alphavantage.co/support/#api-key"
    echo "  📊 限制: 5 请求/分钟, 500 请求/天"
    echo ""
    echo "Finnhub (金融数据):"
    echo "  🔗 https://finnhub.io/register"
    echo "  📊 限制: 60 请求/分钟"
    echo ""
    read -p "按 Enter 继续到下一步..."
    echo ""
}

# 步骤 5: 部署前端 (Vercel)
deploy_frontend() {
    echo -e "${BLUE}🌐 步骤 5: 部署前端 (Vercel)${NC}"
    echo "-----------------------------------"
    echo ""

    # 检查是否安装 Vercel CLI
    if ! command -v vercel &> /dev/null; then
        echo -e "${YELLOW}安装 Vercel CLI...${NC}"
        npm install -g vercel
    fi

    echo -e "${YELLOW}部署前端到 Vercel:${NC}"
    echo ""
    echo "方法 1 - 使用 CLI (推荐):"
    echo "  $ cd frontend"
    echo "  $ vercel"
    echo "  按提示操作即可"
    echo ""
    echo "方法 2 - 使用网页界面:"
    echo "  1️⃣  访问 https://vercel.com"
    echo "  2️⃣  点击 'Import Project'"
    echo "  3️⃣  连接 Git 仓库"
    echo "  4️⃣  设置:"
    echo "      - Framework: Create React App"
    echo "      - Root Directory: frontend"
    echo "      - Build Command: npm run build"
    echo "      - Output Directory: build"
    echo "  5️⃣  添加环境变量:"
    echo "      REACT_APP_API_URL=https://your-backend.onrender.com"
    echo "  6️⃣  点击 'Deploy'"
    echo ""

    read -p "是否现在部署前端? (y/n): " deploy_now

    if [ "$deploy_now" = "y" ]; then
        cd frontend
        echo ""
        echo -e "${GREEN}🚀 开始部署...${NC}"
        vercel
        cd ..
    fi

    echo ""
}

# 步骤 6: 更新 CORS 配置
update_cors() {
    echo -e "${BLUE}🔒 步骤 6: 更新 CORS 配置${NC}"
    echo "-----------------------------------"
    echo ""
    echo -e "${YELLOW}前端部署完成后:${NC}"
    echo ""
    echo "1️⃣  获取 Vercel 前端 URL (例如: https://your-app.vercel.app)"
    echo ""
    echo "2️⃣  在 Render Dashboard 中更新环境变量:"
    echo "    CORS_ORIGINS=https://your-app.vercel.app"
    echo ""
    echo "3️⃣  点击 'Manual Deploy' -> 'Deploy latest commit' 重启服务"
    echo ""
    read -p "按 Enter 继续..."
    echo ""
}

# 步骤 7: 验证部署
verify_deployment() {
    echo -e "${BLUE}✅ 步骤 7: 验证部署${NC}"
    echo "-----------------------------------"
    echo ""
    echo -e "${YELLOW}请验证以下端点:${NC}"
    echo ""
    echo "后端健康检查:"
    echo "  🔗 https://your-backend.onrender.com/health"
    echo "  预期: {\"status\": \"healthy\"}"
    echo ""
    echo "API 文档:"
    echo "  🔗 https://your-backend.onrender.com/docs"
    echo ""
    echo "前端:"
    echo "  🔗 https://your-app.vercel.app"
    echo ""
    echo ""
}

# 显示后续步骤
show_next_steps() {
    echo -e "${GREEN}🎉 部署配置完成!${NC}"
    echo "========================================="
    echo ""
    echo -e "${BLUE}📚 后续步骤:${NC}"
    echo ""
    echo "1️⃣  监控日志:"
    echo "    - Render: Dashboard -> Logs"
    echo "    - Vercel: Dashboard -> Deployments -> View Logs"
    echo ""
    echo "2️⃣  设置自定义域名 (可选):"
    echo "    - Render: Settings -> Custom Domain"
    echo "    - Vercel: Settings -> Domains"
    echo ""
    echo "3️⃣  配置数据库:"
    echo "    $ python backend/scripts/init_db.py"
    echo ""
    echo "4️⃣  启用监控 (推荐):"
    echo "    - Sentry (错误追踪): https://sentry.io"
    echo "    - UptimeRobot (可用性监控): https://uptimerobot.com"
    echo ""
    echo "5️⃣  优化性能:"
    echo "    - 启用 Render CDN"
    echo "    - 配置 Vercel Edge Functions"
    echo "    - 使用 Redis 缓存热点数据"
    echo ""
    echo -e "${YELLOW}⚠️  重要提醒:${NC}"
    echo ""
    echo "• Render 免费层在 15 分钟无活动后会休眠"
    echo "  首次访问可能需要 30-60 秒唤醒"
    echo ""
    echo "• 注意 API 调用限制:"
    echo "  - Alpha Vantage: 5 请求/分钟"
    echo "  - Finnhub: 60 请求/分钟"
    echo "  - Upstash Redis: 10K 命令/天"
    echo ""
    echo -e "${GREEN}📖 完整文档:${NC}"
    echo "   查看 FREE_CLOUD_DEPLOYMENT.md"
    echo ""
    echo "========================================="
    echo -e "${GREEN}✨ 祝您使用愉快!${NC}"
    echo ""
}

# 主函数
main() {
    check_requirements
    prepare_code
    setup_backend
    setup_redis
    setup_env_vars
    deploy_frontend
    update_cors
    verify_deployment
    show_next_steps
}

# 运行主函数
main
