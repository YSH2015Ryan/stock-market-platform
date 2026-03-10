# 获取免费 API 密钥指南

本指南帮助您获取免费的金融数据 API 密钥。

---

## 📊 Alpha Vantage (推荐)

### 免费额度
- ✅ 5 API 请求/分钟
- ✅ 500 API 请求/天
- ✅ 实时和历史股票数据
- ✅ 外汇、加密货币数据

### 获取步骤

1. 访问 https://www.alphavantage.co/support/#api-key

2. 填写表单:
   ```
   Email: your@email.com
   (无需其他信息)
   ```

3. 点击 **"GET FREE API KEY"**

4. 立即收到 API Key，格式如:
   ```
   ABCDEFGHIJKLMNOP
   ```

5. 在 Render 环境变量中设置:
   ```
   ALPHA_VANTAGE_API_KEY=ABCDEFGHIJKLMNOP
   ```

### 使用示例

```python
# 获取股票报价
import requests

API_KEY = "your_alpha_vantage_key"
symbol = "AAPL"

url = f"https://www.alphavantage.co/query"
params = {
    "function": "GLOBAL_QUOTE",
    "symbol": symbol,
    "apikey": API_KEY
}

response = requests.get(url, params=params)
data = response.json()
print(data)
```

---

## 📈 Finnhub (推荐)

### 免费额度
- ✅ 60 API 请求/分钟
- ✅ 实时股票报价
- ✅ 公司新闻和财报
- ✅ 技术指标

### 获取步骤

1. 访问 https://finnhub.io/register

2. 注册账号:
   ```
   Email: your@email.com
   Password: ********
   ```

3. 验证邮箱

4. 登录后访问 Dashboard: https://finnhub.io/dashboard

5. 复制 **API Key**:
   ```
   bq1234abcd5678efgh
   ```

6. 在 Render 环境变量中设置:
   ```
   FINNHUB_API_KEY=bq1234abcd5678efgh
   ```

### 使用示例

```python
import requests

API_KEY = "your_finnhub_key"
symbol = "AAPL"

url = f"https://finnhub.io/api/v1/quote"
params = {
    "symbol": symbol,
    "token": API_KEY
}

response = requests.get(url, params=params)
data = response.json()
print(data)
```

---

## 🌐 Yahoo Finance (免费，无需 API Key)

### 免费额度
- ✅ 无限请求（合理使用）
- ✅ 实时和历史数据
- ✅ 无需注册

### 使用 yfinance 库

```python
import yfinance as yf

# 获取股票数据
ticker = yf.Ticker("AAPL")

# 历史数据
hist = ticker.history(period="1mo")

# 当前信息
info = ticker.info
print(f"Current Price: {info['currentPrice']}")
```

---

## 🤖 OpenAI (可选 - AI 分析)

### 免费额度
- ✅ $5 免费额度（新用户）
- ⚠️ 需要信用卡验证

### 获取步骤

1. 访问 https://platform.openai.com/signup

2. 注册账号并验证邮箱

3. 访问 API Keys: https://platform.openai.com/api-keys

4. 点击 **"Create new secret key"**

5. 复制密钥:
   ```
   sk-proj-abc123...
   ```

6. 在 Render 环境变量中设置:
   ```
   OPENAI_API_KEY=sk-proj-abc123...
   ```

### 使用示例

```python
from openai import OpenAI

client = OpenAI(api_key="your_openai_key")

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Analyze AAPL stock"}
    ]
)

print(response.choices[0].message.content)
```

---

## 🔐 密钥安全最佳实践

### ❌ 不要做的事

```python
# ❌ 硬编码在代码中
API_KEY = "abc123def456"

# ❌ 提交到 Git
git add .env
git commit -m "Add API keys"  # 危险!
```

### ✅ 正确的做法

```python
# ✅ 使用环境变量
import os
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# ✅ 使用 .env 文件 (不提交到 Git)
from dotenv import load_dotenv
load_dotenv()
```

### .gitignore 配置

```gitignore
# 环境变量
.env
.env.local
.env.production

# API 密钥文件
**/secrets.json
**/credentials.json
```

---

## 📊 API 使用统计和监控

### Alpha Vantage

```python
import requests
import time

def check_api_usage():
    """检查 API 使用情况"""
    # Alpha Vantage 在响应头中包含速率限制信息
    response = requests.get(
        "https://www.alphavantage.co/query",
        params={
            "function": "GLOBAL_QUOTE",
            "symbol": "AAPL",
            "apikey": API_KEY
        }
    )

    print(f"Status: {response.status_code}")
    print(f"Headers: {response.headers}")

    if response.status_code == 429:
        print("⚠️ API 速率限制已达上限")
        return False

    return True
```

### 实现速率限制

```python
from functools import wraps
import time

def rate_limit(calls_per_minute=5):
    """装饰器: 限制 API 调用频率"""
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)

            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

@rate_limit(calls_per_minute=5)
def fetch_stock_data(symbol):
    # API 调用
    pass
```

---

## 🔄 API 轮换策略

如果免费额度不够，可以轮换多个 API:

```python
import os

class StockDataFetcher:
    def __init__(self):
        self.alpha_vantage_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        self.finnhub_key = os.getenv("FINNHUB_API_KEY")

    def get_stock_price(self, symbol):
        """尝试多个数据源"""

        # 优先使用 Yahoo Finance (免费无限制)
        try:
            return self._fetch_from_yfinance(symbol)
        except Exception as e:
            print(f"Yahoo Finance failed: {e}")

        # 备用: Alpha Vantage
        try:
            return self._fetch_from_alphavantage(symbol)
        except Exception as e:
            print(f"Alpha Vantage failed: {e}")

        # 备用: Finnhub
        try:
            return self._fetch_from_finnhub(symbol)
        except Exception as e:
            print(f"Finnhub failed: {e}")

        raise Exception("All data sources failed")

    def _fetch_from_yfinance(self, symbol):
        import yfinance as yf
        ticker = yf.Ticker(symbol)
        return ticker.info['currentPrice']

    def _fetch_from_alphavantage(self, symbol):
        # 实现 Alpha Vantage 调用
        pass

    def _fetch_from_finnhub(self, symbol):
        # 实现 Finnhub 调用
        pass
```

---

## 📝 总结

### 推荐组合（完全免费）

```bash
# 主要数据源
✅ Yahoo Finance (yfinance) - 无限制
✅ Alpha Vantage - 500 请求/天
✅ Finnhub - 60 请求/分钟

# 可选
✅ OpenAI - $5 免费额度
✅ Upstash Redis - 10K 命令/天
```

### 每日请求预算

假设您的应用有 100 个用户，每天:

```
Yahoo Finance: 无限制 ✅
Alpha Vantage: 500 请求 (够用) ✅
Finnhub: 86,400 请求 (60/min * 1440 min) ✅
```

**结论**: 免费额度足够小到中型应用使用! 🎉

---

## 🆘 获取帮助

- Alpha Vantage 支持: https://www.alphavantage.co/support/
- Finnhub 文档: https://finnhub.io/docs/api
- OpenAI 社区: https://community.openai.com/

---

**更新时间**: 2024-03-10
