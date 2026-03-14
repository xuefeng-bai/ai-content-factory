/**
 * Content API 服务
 */
import api from './api';

export const contentApi = {
  /**
   * 生成多平台内容
   * @param {Object} data - 请求数据
   * @param {string} data.topic - 选题
   * @param {string} data.theme - 主题
   * @param {Array<string>} data.platforms - 平台列表
   */
  generate: (data) => api.post('/content/generate', data),

  /**
   * 生成抖音文案
   * @param {Object} data - 请求数据
   * @param {string} data.topic - 选题
   * @param {string} data.theme - 主题
   */
  generateDouyin: (data) => api.post('/content/generate/douyin', data, { params: data }),

  /**
   * 生成公众号文章
   * @param {Object} data - 请求数据
   * @param {string} data.topic - 选题
   * @param {string} data.theme - 主题
   */
  generateWechat: (data) => api.post('/content/generate/wechat', data, { params: data }),

  /**
   * 生成小红书笔记
   * @param {Object} data - 请求数据
   * @param {string} data.topic - 选题
   * @param {string} data.theme - 主题
   */
  generateXiaohongshu: (data) => api.post('/content/generate/xhs', data, { params: data }),
};

export default contentApi;
