#!/bin/bash

# 🚀 一键部署脚本
# 最简洁、最便宜（免费）的部署方案

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠ $1${NC}"; }
print_error() { echo -e "${RED}✗ $1${NC}"; }

# 标题
echo "================================================"
echo "  🚀 股票市场平台 - 快速部署工具"
echo "  方案: Render (后端) + Vercel (前端)"
echo "  成本: $0/月 (完全免费)"
echo "================================================"
echo ""

# 检查依赖
print_info "检查必需工具..."

if ! command -v git &> /dev/null; then
    print_error "Git 未安装，请先安装 Git"
    exit 1
fi
print_success "Git 已安装"

if ! command -v node &> /dev/null; then
    print_warning "Node.js 未安装（可选，仅前端部署需要）"
else
    print_success "Node.js 已安装: $(node --version)"
fi

if ! command -v npm &> /dev/null; then
    print_warning "NPM 未安装（可选）"
else
    print_success "NPM 已安装: $(npm --version)"
fi

echo ""

# 选择部署方式
echo "请选择部署方式："
echo "  1) 完整部署（后端 + 前端）- 推荐"
echo "  2) 仅后端（Render）"
echo "  3) 仅前端（Vercel）"
echo "  4) 本地测试运行"
echo "  5) 查看部署状态"
read -p "请输入选项 (1-5): " deploy_choice

case $deploy_choice in
    1)
        print_info "准备完整部署..."
        DEPLOY_MODE="full"
        ;;
    2)
        print_info "准备仅部署后端..."
        DEPLOY_MODE="backend"
        ;;
    3)
        print_info "准备仅部署前端..."
        DEPLOY_MODE="frontend"
        ;;
    4)
        print_info "准备本地测试运行..."
        DEPLOY_MODE="local"
        ;;
    5)
        print_info "查看部署状态..."
        DEPLOY_MODE="status"
        ;;
    *)
        print_error "无效选项"
        exit 1
        ;;
esac

echo ""

# 部署状态
if [ "$DEPLOY_MODE" = "status" ]; then
    echo "📊 当前部署状态："
    echo "================================"

    # 检查本地服务
    if pgrep -f "python.*app_simple" > /dev/null; then
        print_success "本地后端: 运行中 (http://localhost:8000)"
    else
        print_warning "本地后端: 未运行"
    fi

    if pgrep -f "http.server 3000" > /dev/null; then
        print_success "本地前端: 运行中 (http://localhost:3000)"
    else
        print_warning "本地前端: 未运行"
    fi

    # 检查Git状态
    if [ -d .git ]; then
        echo ""
        print_info "Git 仓库状态:"
        git remote -v 2>/dev/null || print_warning "未配置远程仓库"
        echo ""
        git status --short
    else
        print_warning "未初始化 Git 仓库"
    fi

    exit 0
fi

# 本地测试运行
if [ "$DEPLOY_MODE" = "local" ]; then
    print_info "启动本地测试环境..."

    # 检查是否已有进程在运行
    if pgrep -f "python.*app_simple" > /dev/null; then
        print_warning "后端已在运行，跳过启动"
    else
        print_info "启动后端服务..."
        cd backend
        if [ -d venv ]; then
            source venv/bin/activate
        fi
        python app_simple.py > logs/backend.log 2>&1 &
        BACKEND_PID=$!
        print_success "后端已启动 (PID: $BACKEND_PID)"
        cd ..
    fi

    # 等待后端启动
    sleep 3

    # 启动前端
    if pgrep -f "http.server 3000" > /dev/null; then
        print_warning "前端已在运行，跳过启动"
    else
        print_info "启动前端服务..."
        cd frontend
        python3 -m http.server 3000 > /dev/null 2>&1 &
        FRONTEND_PID=$!
        print_success "前端已启动 (PID: $FRONTEND_PID)"
        cd ..
    fi

    echo ""
    echo "🎉 本地环境启动完成！"
    echo "================================"
    echo "  前端: http://localhost:3000/index.html"
    echo "  后端: http://localhost:8000"
    echo "  API文档: http://localhost:8000/docs"
    echo ""
    echo "停止服务: pkill -f 'python.*app_simple|http.server 3000'"

    exit 0
fi

# 准备Git仓库
print_info "准备代码仓库..."

if [ ! -d .git ]; then
    print_info "初始化 Git 仓库..."
    git init
    git add .
    git commit -m "Initial commit - Ready for deployment"
    print_success "Git 仓库已初始化"
else
    print_success "Git 仓库已存在"

    # 检查是否有未提交的更改
    if ! git diff-index --quiet HEAD --; then
        print_warning "检测到未提交的更改"
        read -p "是否提交这些更改? (y/n): " commit_choice
        if [ "$commit_choice" = "y" ]; then
            git add .
            read -p "提交信息: " commit_msg
            git commit -m "$commit_msg"
            print_success "更改已提交"
        fi
    fi
fi

# 检查GitHub远程仓库
if ! git remote get-url origin &> /dev/null; then
    print_warning "未配置 GitHub 远程仓库"
    echo ""
    echo "请按以下步骤操作："
    echo "1. 访问 https://github.com/new 创建新仓库"
    echo "2. 仓库名称: stock-market-platform"
    echo "3. 创建后，复制仓库URL"
    echo ""
    read -p "输入GitHub仓库URL (https://github.com/用户名/仓库名.git): " github_url

    if [ -n "$github_url" ]; then
        git remote add origin "$github_url"
        git branch -M main
        git push -u origin main
        print_success "代码已推送到GitHub"
    else
        print_error "未提供GitHub URL，无法继续部署"
        exit 1
    fi
else
    print_success "GitHub远程仓库已配置"
    print_info "推送最新代码..."
    git push
    print_success "代码已更新"
fi

echo ""

# 后端部署指引
if [ "$DEPLOY_MODE" = "backend" ] || [ "$DEPLOY_MODE" = "full" ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  📦 步骤 1: 部署后端到 Render"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "请按以下步骤操作（预计3分钟）："
    echo ""
    echo "1. 访问: https://dashboard.render.com/"
    echo "   (如未登录，使用GitHub账号登录)"
    echo ""
    echo "2. 点击: New + → Web Service"
    echo ""
    echo "3. 连接你的GitHub仓库: stock-market-platform"
    echo ""
    echo "4. 填写配置："
    echo "   ┌─────────────────────────────────────┐"
    echo "   │ Name: stock-market-api              │"
    echo "   │ Root Directory: backend             │"
    echo "   │ Environment: Python 3               │"
    echo "   │ Build Command: pip install -r requirements.txt"
    echo "   │ Start Command: python app_simple.py │"
    echo "   │ Plan: Free                          │"
    echo "   └─────────────────────────────────────┘"
    echo ""
    echo "5. 点击 'Create Web Service'"
    echo ""
    echo "6. 等待3-5分钟部署完成"
    echo ""
    echo "7. 复制你的后端URL（类似）："
    echo "   https://stock-market-api-xxxx.onrender.com"
    echo ""

    read -p "部署完成后，输入你的后端URL: " backend_url

    if [ -n "$backend_url" ]; then
        # 保存到配置文件
        echo "BACKEND_URL=$backend_url" > .deploy_config
        print_success "后端URL已保存"

        # 测试后端
        print_info "测试后端连接..."
        sleep 2
        if curl -s "$backend_url/health" | grep -q "healthy"; then
            print_success "后端运行正常！"
        else
            print_warning "后端可能还在启动中，请稍后访问: $backend_url/docs"
        fi
    fi

    echo ""
fi

# 前端部署指引
if [ "$DEPLOY_MODE" = "frontend" ] || [ "$DEPLOY_MODE" = "full" ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  🎨 步骤 2: 部署前端到 Vercel"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # 读取后端URL
    if [ -f .deploy_config ]; then
        source .deploy_config
    fi

    if [ -z "$BACKEND_URL" ]; then
        read -p "请输入后端URL: " BACKEND_URL
    fi

    # 更新前端API地址
    if [ -n "$BACKEND_URL" ]; then
        print_info "更新前端API配置..."
        sed -i.bak "s|http://localhost:8000|$BACKEND_URL|g" frontend/index.html
        git add frontend/index.html
        git commit -m "Update API URL for production" || true
        git push
        print_success "API配置已更新"
    fi

    echo ""
    echo "选择部署方式："
    echo "  A) 使用 Vercel CLI (自动化，推荐)"
    echo "  B) 使用网页界面 (手动，更直观)"
    read -p "请选择 (A/B): " vercel_choice

    if [ "$vercel_choice" = "A" ] || [ "$vercel_choice" = "a" ]; then
        print_info "使用 Vercel CLI 部署..."

        # 检查是否安装了Vercel CLI
        if ! command -v vercel &> /dev/null; then
            print_info "安装 Vercel CLI..."
            npm install -g vercel
        fi

        cd frontend
        print_info "开始部署到 Vercel..."
        vercel --prod
        cd ..

        print_success "前端部署完成！"

    else
        echo ""
        echo "请按以下步骤操作（预计2分钟）："
        echo ""
        echo "1. 访问: https://vercel.com/dashboard"
        echo "   (如未登录，使用GitHub账号登录)"
        echo ""
        echo "2. 点击: Add New... → Project"
        echo ""
        echo "3. 导入你的GitHub仓库: stock-market-platform"
        echo ""
        echo "4. 填写配置："
        echo "   ┌─────────────────────────────────────┐"
        echo "   │ Framework Preset: Other             │"
        echo "   │ Root Directory: frontend            │"
        echo "   │ Build Command: (留空)               │"
        echo "   │ Output Directory: .                 │"
        echo "   └─────────────────────────────────────┘"
        echo ""
        echo "5. 点击 'Deploy'"
        echo ""
        echo "6. 部署完成后，访问给出的URL"
        echo ""

        read -p "按回车键继续..."
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🎉 部署完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📱 访问你的应用："
echo ""
if [ -n "$BACKEND_URL" ]; then
    echo "  后端API: $BACKEND_URL"
    echo "  API文档: $BACKEND_URL/docs"
fi
echo "  前端: (Vercel会提供URL)"
echo ""
echo "📚 更多信息："
echo "  • 详细文档: QUICK_DEPLOY.md"
echo "  • 完整指南: FREE_CLOUD_DEPLOYMENT.md"
echo "  • 部署说明: DEPLOYMENT_GUIDE.md"
echo ""
echo "💡 提示："
echo "  • Render免费版15分钟无活动会休眠"
echo "  • 首次访问需要30秒唤醒时间"
echo "  • 可以使用 UptimeRobot 防止休眠"
echo ""
echo "❓ 需要帮助？查看文档或访问:"
echo "  • Render: https://render.com/docs"
echo "  • Vercel: https://vercel.com/docs"
echo ""
print_success "感谢使用！祝你部署顺利 🚀"
