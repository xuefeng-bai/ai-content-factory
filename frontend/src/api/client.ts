import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// 创建 axios 实例
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    // 可以在这里添加认证 token
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.error('API 请求错误:', error)
    
    if (error.response) {
      // 服务器返回错误响应
      switch (error.response.status) {
        case 400:
          console.error('请求参数错误')
          break
        case 404:
          console.error('资源不存在')
          break
        case 500:
          console.error('服务器内部错误')
          break
        case 503:
          console.error('服务不可用')
          break
        default:
          console.error('未知错误')
      }
    } else if (error.request) {
      console.error('网络错误，请检查网络连接')
    }
    
    return Promise.reject(error)
  }
)

export default apiClient

// API 调用方法
export const contentAPI = {
  // 生成内容
  generate: (topic: string, templateId?: number) => {
    return apiClient.post('/api/v1/content/generate', { topic, template_id: templateId })
  },
  
  // 获取详情
  getDetail: (id: number) => {
    return apiClient.get(`/api/v1/content/${id}`)
  },
  
  // 更新内容
  update: (id: number, platform: string, content: string, title?: string) => {
    return apiClient.put(`/api/v1/content/${id}`, { platform, content, title })
  },
  
  // 重新生成
  regenerate: (id: number, platform: string, templateId?: number) => {
    return apiClient.post(`/api/v1/content/${id}/regenerate`, { platform, template_id: templateId })
  },
  
  // 历史记录
  getHistory: (page = 1, pageSize = 20, keyword?: string) => {
    return apiClient.get('/api/v1/content/history', { params: { page, page_size: pageSize, keyword } })
  },
  
  // 删除记录
  delete: (id: number) => {
    return apiClient.delete(`/api/v1/content/${id}`)
  },
}

export const templateAPI = {
  // 获取模板列表
  getList: (platform?: string, isDefault?: number) => {
    return apiClient.get('/api/v1/templates', { params: { platform, is_default: isDefault } })
  },
  
  // 创建模板
  create: (name: string, platform: string, templateContent: string, isActive = 1, sortOrder = 0) => {
    return apiClient.post('/api/v1/templates', { name, platform, template_content: templateContent, is_active: isActive, sort_order: sortOrder })
  },
  
  // 更新模板
  update: (id: number, data: any) => {
    return apiClient.put(`/api/v1/templates/${id}`, data)
  },
  
  // 删除模板
  delete: (id: number) => {
    return apiClient.delete(`/api/v1/templates/${id}`)
  },
}

export const configAPI = {
  // 获取配置列表
  getList: () => {
    return apiClient.get('/api/v1/configs')
  },
  
  // 更新配置
  update: (key: string, value: string) => {
    return apiClient.put(`/api/v1/configs/${key}`, { config_value: value })
  },
}
