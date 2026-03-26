'use client'

import { useState, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import MDEditor from '@uiw/react-md-editor'
import { contentAPI } from '@/api/client'

export default function ResultPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const generationId = searchParams.get('id')
  
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [generation, setGeneration] = useState<any>(null)
  const [editingPlatform, setEditingPlatform] = useState<string | null>(null)
  const [editContent, setEditContent] = useState('')
  const [editTitle, setEditTitle] = useState('')

  useEffect(() => {
    if (generationId) {
      loadGeneration()
      // 轮询检查生成状态
      const interval = setInterval(() => {
        loadGeneration()
      }, 5000)
      return () => clearInterval(interval)
    }
  }, [generationId])

  const loadGeneration = async () => {
    try {
      const response = await contentAPI.getDetail(Number(generationId))
      if (response.code === 200) {
        setGeneration(response.data)
        setLoading(false)
      }
    } catch (error) {
      console.error('加载失败:', error)
    }
  }

  const handleEdit = (item: any) => {
    setEditingPlatform(item.platform)
    setEditContent(item.content)
    setEditTitle(item.title || '')
  }

  const handleSave = async () => {
    if (!generationId || !editingPlatform) return
    
    setSaving(true)
    try {
      const response = await contentAPI.update(
        Number(generationId),
        editingPlatform,
        editContent,
        editTitle
      )
      
      if (response.code === 200) {
        alert('保存成功')
        setEditingPlatform(null)
        loadGeneration()
      }
    } catch (error) {
      console.error('保存失败:', error)
      alert('保存失败，请稍后重试')
    } finally {
      setSaving(false)
    }
  }

  const handleCopy = async (content: string, title: string) => {
    const text = `# ${title}\n\n${content}`
    try {
      await navigator.clipboard.writeText(text)
      alert('复制成功')
    } catch (error) {
      console.error('复制失败:', error)
      alert('复制失败')
    }
  }

  const handleRegenerate = async (platform: string) => {
    if (!generationId) return
    
    try {
      const response = await contentAPI.regenerate(
        Number(generationId),
        platform
      )
      
      if (response.code === 200) {
        alert('重新生成任务已创建，请稍后查看')
        loadGeneration()
      }
    } catch (error) {
      console.error('重新生成失败:', error)
      alert('重新生成失败')
    }
  }

  const getStatusText = (status: string) => {
    const map: any = {
      'pending': '等待中',
      'processing': '生成中',
      'completed': '已完成',
      'failed': '生成失败',
      'partial': '部分成功'
    }
    return map[status] || status
  }

  const getStatusColor = (status: string) => {
    const map: any = {
      'pending': 'gray',
      'processing': 'blue',
      'completed': 'green',
      'failed': 'red',
      'partial': 'yellow'
    }
    return map[status] || 'gray'
  }

  const getPlatformName = (platform: string) => {
    const map: any = {
      'douyin': '抖音',
      'video_account': '视频号',
      'wechat': '公众号',
      'xiaohongshu': '小红书'
    }
    return map[platform] || platform
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-lg text-gray-600">正在加载生成结果...</p>
        </div>
      </div>
    )
  }

  if (!generation) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-lg text-gray-600 mb-4">未找到生成记录</p>
          <button
            onClick={() => router.push('/')}
            className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            返回首页
          </button>
        </div>
      </div>
    )
  }

  return (
    <main className="min-h-screen p-8 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        {/* 返回按钮和标题 */}
        <div className="mb-6 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => router.push('/')}
              className="text-gray-600 hover:text-gray-800"
            >
              ← 返回
            </button>
            <h1 className="text-2xl font-bold">{generation.topic}</h1>
          </div>
          <div className="flex items-center gap-2">
            <span className={`px-3 py-1 rounded-full text-sm text-white bg-${getStatusColor(generation.status)}-500`}>
              {getStatusText(generation.status)}
            </span>
            <span className="text-sm text-gray-500">
              {new Date(generation.created_at).toLocaleString('zh-CN')}
            </span>
          </div>
        </div>

        {/* 4 个平台内容卡片 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {generation.items?.map((item: any) => (
            <div key={item.id} className="bg-white rounded-lg shadow-md p-6">
              {/* 卡片头部 */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <span className="text-lg font-semibold">{getPlatformName(item.platform)}</span>
                  {item.status === 'success' && (
                    <span className="px-2 py-1 bg-green-100 text-green-700 rounded text-xs">成功</span>
                  )}
                  {item.status === 'failed' && (
                    <span className="px-2 py-1 bg-red-100 text-red-700 rounded text-xs">失败</span>
                  )}
                  {item.status === 'pending' && (
                    <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">等待中</span>
                  )}
                </div>
                <div className="flex gap-2">
                  {item.status === 'success' && (
                    <>
                      <button
                        onClick={() => handleEdit(item)}
                        className="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600"
                      >
                        编辑
                      </button>
                      <button
                        onClick={() => handleCopy(item.content, item.title)}
                        className="px-3 py-1 text-sm bg-green-500 text-white rounded hover:bg-green-600"
                      >
                        复制
                      </button>
                    </>
                  )}
                  {item.status === 'failed' && (
                    <button
                      onClick={() => handleRegenerate(item.platform)}
                      className="px-3 py-1 text-sm bg-orange-500 text-white rounded hover:bg-orange-600"
                    >
                      重试
                    </button>
                  )}
                </div>
              </div>

              {/* 标题 */}
              {item.title && (
                <h3 className="text-lg font-medium mb-3">{item.title}</h3>
              )}

              {/* 封面图 */}
              {item.cover_image_url && (
                <div className="mb-4">
                  <img
                    src={item.cover_image_url}
                    alt="封面图"
                    className="w-full h-48 object-cover rounded-lg"
                  />
                </div>
              )}

              {/* 内容预览 */}
              {item.status === 'success' && (
                <div className="prose max-w-none">
                  <MDEditor.Markdown
                    source={item.content}
                    className="bg-gray-50 rounded p-4 max-h-96 overflow-y-auto"
                  />
                </div>
              )}

              {/* 错误信息 */}
              {item.status === 'failed' && item.error_message && (
                <div className="text-red-600 text-sm bg-red-50 p-4 rounded">
                  {item.error_message}
                </div>
              )}

              {/* 等待中 */}
              {item.status === 'pending' && (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-2"></div>
                  <p className="text-gray-500">正在生成...</p>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* 编辑对话框 */}
        {editingPlatform && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col">
              {/* 对话框头部 */}
              <div className="p-4 border-b flex items-center justify-between">
                <h2 className="text-xl font-semibold">
                  编辑内容 - {getPlatformName(editingPlatform)}
                </h2>
                <button
                  onClick={() => setEditingPlatform(null)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  ✕
                </button>
              </div>

              {/* 标题输入 */}
              <div className="p-4 border-b">
                <label className="block text-sm font-medium mb-2">标题</label>
                <input
                  type="text"
                  value={editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              </div>

              {/* Markdown 编辑器 */}
              <div className="flex-1 p-4 overflow-hidden">
                <MDEditor
                  value={editContent}
                  onChange={(val) => setEditContent(val || '')}
                  height={400}
                  preview="live"
                />
              </div>

              {/* 底部按钮 */}
              <div className="p-4 border-t flex justify-end gap-3">
                <button
                  onClick={() => setEditingPlatform(null)}
                  className="px-4 py-2 text-gray-600 hover:text-gray-800"
                >
                  取消
                </button>
                <button
                  onClick={handleSave}
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
