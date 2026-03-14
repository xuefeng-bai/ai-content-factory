/**
 * Prompt API 服务
 */
import api from './api';

export const promptsApi = {
  /**
   * 获取 Prompt 列表
   * @param {Object} params - 查询参数
   * @param {string} params.category - 分类筛选
   * @param {boolean} params.is_active - 状态筛选
   * @param {number} params.page - 页码
   * @param {number} params.page_size - 每页数量
   */
  getList: (params) => api.get('/prompts', { params }),

  /**
   * 获取 Prompt 详情
   * @param {number} id - Prompt ID
   */
  getById: (id) => api.get(`/prompts/${id}`),

  /**
   * 创建 Prompt
   * @param {Object} data - Prompt 数据
   */
  create: (data) => api.post('/prompts', data),

  /**
   * 更新 Prompt
   * @param {number} id - Prompt ID
   * @param {Object} data - 更新数据
   */
  update: (id, data) => api.put(`/prompts/${id}`, data),

  /**
   * 删除 Prompt
   * @param {number} id - Prompt ID
   */
  delete: (id) => api.delete(`/prompts/${id}`),

  /**
   * 创建新版本
   * @param {number} id - Prompt ID
   * @param {Object} data - 版本数据
   */
  createVersion: (id, data) => api.post(`/prompts/${id}/versions`, data),

  /**
   * 获取版本历史
   * @param {number} id - Prompt ID
   */
  getVersions: (id) => api.get(`/prompts/${id}/versions`),

  /**
   * 发布版本
   * @param {number} id - Prompt ID
   * @param {number} versionId - 版本 ID
   */
  publishVersion: (id, versionId) => api.post(`/prompts/${id}/versions/${versionId}/publish`),

  /**
   * 测试 Prompt
   * @param {Object} data - 测试数据
   * @param {number} data.prompt_id - Prompt ID
   * @param {Object} data.input_vars - 输入变量
   */
  test: (data) => api.post('/prompts/test', data),
};

export default promptsApi;
