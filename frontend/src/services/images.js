/**
 * Images API 服务
 */
import api from './api';

export const imagesApi = {
  /**
   * 生成配图
   * @param {Object} data - 请求数据
   * @param {string} data.content - 内容
   * @param {string} data.title - 标题
   * @param {string} data.aspect_ratio - 比例（16:9 或 3:4）
   * @param {string} data.platform - 平台（wechat/xhs）
   */
  generate: (data) => api.post('/images/generate', data),

  /**
   * 获取图片详情
   * @param {string} id - 图片 ID
   */
  getById: (id) => api.get(`/images/${id}`),

  /**
   * 获取图片列表
   * @param {Object} params - 查询参数
   * @param {number} params.page - 页码
   * @param {number} params.page_size - 每页数量
   * @param {string} params.platform - 平台筛选
   */
  getList: (params) => api.get('/images', { params }),
};

export default imagesApi;
