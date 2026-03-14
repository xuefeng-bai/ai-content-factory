/**
 * API 基础配置
 */
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// 创建 axios 实例
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    const data = response.data;
    // 统一处理响应码
    if (data.code === 200 || data.code === 201) {
      return data.data;
    } else {
      return Promise.reject(new Error(data.message || '请求失败'));
    }
  },
  (error) => {
    console.error('API Error:', error);
    const message = error.response?.data?.message || error.message || '网络错误';
    return Promise.reject(new Error(message));
  }
);

export default api;
