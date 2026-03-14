/**
 * History API 服务
 */
import api from './api';

export const historyApi = {
  /**
   * 获取历史列表
   * @param {Object} params - 查询参数
   * @param {number} params.page - 页码
   * @param {number} params.page_size - 每页数量
   * @param {string} params.platform - 平台筛选
   * @param {string} params.keyword - 搜索关键词
   */
  getList: (params) => api.get('/history', { params }),

  /**
   * 获取历史详情
   * @param {number} id - 历史 ID
   */
  getById: (id) => api.get(`/history/${id}`),

  /**
   * 删除历史
   * @param {number} id - 历史 ID
   */
  delete: (id) => api.delete(`/history/${id}`),

  /**
   * 搜索历史
   * @param {Object} params - 查询参数
   * @param {string} params.keyword - 搜索关键词
   * @param {number} params.page - 页码
   * @param {number} params.page_size - 每页数量
   */
  search: (params) => api.get('/history/search', { params }),
};

export default historyApi;
