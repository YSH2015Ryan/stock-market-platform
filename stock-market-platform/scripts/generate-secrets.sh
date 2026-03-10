#!/bin/bash

# 生成安全的随机密钥
# 用法: ./generate-secrets.sh

echo "🔐 生成安全密钥..."
echo ""

echo "# 复制以下内容到 Render 环境变量"
echo "# =================================="
echo ""

echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"
echo "JWT_SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"

echo ""
echo "# =================================="
echo "✅ 密钥生成完成!"
echo ""
echo "📝 使用说明:"
echo "1. 访问 Render Dashboard"
echo "2. 选择你的服务"
echo "3. 进入 Environment 标签"
echo "4. 点击 'Add Environment Variable'"
echo "5. 复制粘贴上面的密钥"
echo ""
