/**
 * Topics API 服务
 */
import api from './api';

export const topicsApi = {
  /**
   * 推荐选题
   * @param {Object} data - 请求数据
   * @param {Array} data.search_results - 搜索结果
   * @param {string} data.theme - 主题
   */
  recommend: (data) => api.post('/topics/recommend', data),
};

export default topicsApi;
