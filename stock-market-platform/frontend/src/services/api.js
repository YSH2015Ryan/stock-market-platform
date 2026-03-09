import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: `${API_URL}/api/v1`,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API methods
export const stockAPI = {
  getStocks: (params) => apiClient.get('/stocks', { params }),
  getStock: (symbol) => apiClient.get(`/stocks/${symbol}`),
  getStockPrices: (symbol, params) => apiClient.get(`/stocks/${symbol}/prices`, { params }),
  getStockAnalysis: (symbol) => apiClient.get(`/stocks/${symbol}/analysis`),
  searchStocks: (params) => apiClient.get('/stocks/search/screener', { params }),
};

export const indexAPI = {
  getIndices: (market) => apiClient.get('/indices', { params: { market } }),
  getIndex: (symbol) => apiClient.get(`/indices/${symbol}`),
  getMarketOverview: () => apiClient.get('/indices/market/overview'),
};

export const newsAPI = {
  getNews: (params) => apiClient.get('/news', { params }),
  getNewsItem: (id) => apiClient.get(`/news/${id}`),
  getSentimentSummary: (params) => apiClient.get('/news/sentiment/summary', { params }),
};

export const reportAPI = {
  getReports: (params) => apiClient.get('/reports', { params }),
  getReport: (id) => apiClient.get(`/reports/${id}`),
  getLatestDailyReport: () => apiClient.get('/reports/latest/daily'),
  generateDailyReport: () => apiClient.post('/reports/generate/daily'),
  generateWeeklyReport: () => apiClient.post('/reports/generate/weekly'),
};

export const portfolioAPI = {
  getPortfolios: (userId) => apiClient.get('/portfolios', { params: { user_id: userId } }),
  getPortfolio: (id) => apiClient.get(`/portfolios/${id}`),
  createPortfolio: (data, userId) => apiClient.post('/portfolios', data, { params: { user_id: userId } }),
  getHoldings: (portfolioId) => apiClient.get(`/portfolios/${portfolioId}/holdings`),
  addHolding: (portfolioId, data) => apiClient.post(`/portfolios/${portfolioId}/holdings`, data),
  getPerformance: (portfolioId) => apiClient.get(`/portfolios/${portfolioId}/performance`),
};

export default apiClient;
