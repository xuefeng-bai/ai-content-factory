'use client'

import { useState, useEffect } from 'react'
import { templateAPI } from '@/api/client'

export default function TemplatesPage() {
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [templates, setTemplates] = useState<any[]>([])
  const [showModal, setShowModal] = useState(false)
  const [editingTemplate, setEditingTemplate] = useState<any>(null)
  const [formData, setFormData] = useState({
    name: '',
    platform: 'douyin',
    template_content: '',
    sort_order: 0
  })

  useEffect(() => {
    loadTemplates()
  }, [])

  const loadTemplates = async () => {
    setLoading(true)
    try {
      const response = await templateAPI.getList()
      if (response.code === 200) {
        setTemplates(response.data)
      }
    } catch (error) {
      console.error('加载模板失败:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleOpenModal = (template?: any) => {
    if (template) {
      setEditingTemplate(template)
      setFormData({
        name: template.name,
        platform: template.platform,
        template_content: template.template_content,
        sort_order: template.sort_order || 0
      })
    } else {
      setEditingTemplate(null)
      setFormData({
        name: '',
        platform: 'douyin',
        template_content: '',
        sort_order: 0
      })
    }
    setShowModal(true)
  }

  const handleCloseModal = () => {
    setShowModal(false)
    setEditingTemplate(null)
  }

  const handleSubmit = async () => {
    if (!formData.name || !formData.template_content) {
      alert('请填写必填项')
      return
    }

    setSaving(true)
    try {
      if (editingTemplate) {
        const response = await templateAPI.update(editingTemplate.id, formData)
        if (response.code === 200) {
          alert('更新成功')
          handleCloseModal()
          loadTemplates()
        }
      } else {
        const response = await templateAPI.create(
          formData.name,
          formData.platform,
          formData.template_content,
          1,
          formData.sort_order
        )
        if (response.code === 200) {
          alert('创建成功')
          handleCloseModal()
          loadTemplates()
        }
      }
    } catch (error: any) {
      console.error('操作失败:', error)
      alert(error.response?.data?.message || '操作失败，请稍后重试')
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async (id: number, isDefault: number) => {
    if (isDefault === 1) {
      alert('系统默认模板不可删除，只能禁用')
      return
    }

    if (!confirm('确定要删除这个模板吗？此操作不可恢复。')) {
      return
    }

    try {
      const response = await templateAPI.delete(id)
      if (response.code === 200) {
        alert('删除成功')
        loadTemplates()
      }
    } catch (error: any) {
      console.error('删除失败:', error)
      alert(error.response?.data?.message || '删除失败，请稍后重试')
    }
  }

  const getPlatformName = (platform: string) => {
    const map: any = {
      'all': '通用',
      'douyin': '抖音',
      'video_account': '视频号',
      'wechat': '公众号',
      'xiaohongshu': '小红书'
    }
    return map[platform] || platform
  }

  return (
    <main className="min-h-screen p-8 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        {/* 页面标题 */}
        <div className="mb-6 flex items-center justify-between">
          <div>
            <button
              onClick={() => window.history.back()}
              className="text-gray-600 hover:text-gray-800 mr-4"
            >
              ← 返回
            </button>
            <span className="text-3xl font-bold">提示词模板管理</span>
          </div>
          <button
            onClick={() => handleOpenModal()}
            className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            + 新建模板
          </button>
        </div>

        {/* 模板列表 */}
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        ) : templates.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-12 text-center text-gray-500">
            <p className="text-lg">暂无模板</p>
            <button
              onClick={() => handleOpenModal()}
              className="mt-4 px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
            >
              创建第一个模板
            </button>
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    名称
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    平台
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    类型
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    排序
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    操作
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {templates.map((template) => (
                  <tr key={template.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">
                        {template.name}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                        {getPlatformName(template.platform)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {template.is_default === 1 ? (
                        <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-purple-100 text-purple-800">
                          系统默认
                        </span>
                      ) : (
                        <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800">
                          自定义
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {template.sort_order || 0}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button
                        onClick={() => handleOpenModal(template)}
                        className="text-primary-600 hover:text-primary-900 mr-4"
                      >
                        编辑
                      </button>
                      <button
                        onClick={() => handleDelete(template.id, template.is_default)}
                        disabled={template.is_default === 1}
                        className="text-red-600 hover:text-red-900 disabled:text-gray-400"
                      >
                        删除
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* 编辑/新建弹窗 */}
        {showModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col">
              {/* 弹窗头部 */}
              <div className="p-4 border-b flex items-center justify-between">
                <h2 className="text-xl font-semibold">
                  {editingTemplate ? '编辑模板' : '新建模板'}
                </h2>
                <button
                  onClick={handleCloseModal}
                  className="text-gray-500 hover:text-gray-700"
                >
                  ✕
                </button>
              </div>

              {/* 弹窗内容 */}
              <div className="p-6 overflow-y-auto flex-1">
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      模板名称 <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                      placeholder="例如：抖音干货型模板"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">
                      适用平台 <span className="text-red-500">*</span>
                    </label>
                    <select
                      value={formData.platform}
                      onChange={(e) => setFormData({ ...formData, platform: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                    >
                      <option value="all">通用</option>
                      <option value="douyin">抖音</option>
                      <option value="video_account">视频号</option>
                      <option value="wechat">公众号</option>
                      <option value="xiaohongshu">小红书</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">
                      模板内容 <span className="text-red-500">*</span>
                    </label>
                    <textarea
                      value={formData.template_content}
                      onChange={(e) => setFormData({ ...formData, template_content: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 h-40 font-mono text-sm"
                      placeholder="请输入模板内容，支持参数：{topic} {style} {word_count}"
                    />
                    <p className="mt-1 text-xs text-gray-500">
                      可用参数：{'{topic}'} = 主题，{'{style}'} = 风格，{'{word_count}'} = 字数范围
                    </p>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">
                      排序
                    </label>
                    <input
                      type="number"
                      value={formData.sort_order}
                      onChange={(e) => setFormData({ ...formData, sort_order: parseInt(e.target.value) || 0 })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                      placeholder="数字越小越靠前"
                    />
                  </div>
                </div>
              </div>

              {/* 弹窗底部 */}
              <div className="p-4 border-t flex justify-end gap-3">
                <button
                  onClick={handleCloseModal}
                  className="px-4 py-2 text-gray-600 hover:text-gray-800"
                >
                  取消
                </button>
                <button
                  onClick={handleSubmit}
                  disabled={saving}
                  className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-gray-400"
                >
                  {saving ? '保存中...' : '保存'}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  )
}
