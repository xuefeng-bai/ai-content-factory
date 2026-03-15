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
  recommend: async (data) => {
    console.log('[Topics API] Calling recommend with:', data);
    try {
      const result = await api.post('/topics/recommend', data);
      console.log('[Topics API] Response:', result);
      return result;
    } catch (error) {
      console.error('[Topics API] Error:', error);
      throw error;
    }
  },
};

export default topicsApi;
