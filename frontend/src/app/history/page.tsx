'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { contentAPI } from '@/api/client'

export default function HistoryPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(true)
  const [deleting, setDeleting] = useState<number | null>(null)
  const [history, setHistory] = useState<any[]>([])
  const [pagination, setPagination] = useState({
    page: 1,
    page_size: 20,
    total: 0
  })
  const [filters, setFilters] = useState({
    keyword: '',
    platform: '',
    status: ''
  })

  useEffect(() => {
    loadHistory()
  }, [pagination.page, filters])

  const loadHistory = async () => {
    setLoading(true)
    try {
      const response = await contentAPI.getHistory(
        pagination.page,
        pagination.page_size,
        filters.keyword || undefined
      )
      
      if (response.code === 200) {
        setHistory(response.data.list)
        setPagination({
          ...pagination,
          total: response.data.total
        })
      }
    } catch (error) {
      console.error('加载历史记录失败:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = () => {
    setPagination({ ...pagination, page: 1 })
    loadHistory()
  }

  const handleDelete = async (id: number) => {
    if (!confirm('确定要删除这条记录吗？此操作不可恢复。')) {
      return
    }

    setDeleting(id)
    try {
      const response = await contentAPI.delete(id)
      if (response.code === 200) {
        alert('删除成功')
        loadHistory()
      }
    } catch (error) {
      console.error('删除失败:', error)
      alert('删除失败，请稍后重试')
    } finally {
      setDeleting(null)
    }
  }

  const handlePageChange = (newPage: number) => {
    setPagination({ ...pagination, page: newPage })
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

  const getStatusText = (status: string) => {
    const map: any = {
      'pending': '等待中',
      'processing': '生成中',
      'completed': '已完成',
      'failed': '失败',
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

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('zh-CN')
  }

  return (
    <main className="min-h-screen p-8 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        {/* 页面标题 */}
        <div className="mb-6">
          <button
            onClick={() => router.push('/')}
            className="text-gray-600 hover:text-gray-800 mb-4"
          >
            ← 返回首页
          </button>
          <h1 className="text-3xl font-bold">历史记录</h1>
        </div>

        {/* 搜索栏 */}
        <div className="bg-white rounded-lg shadow p-4 mb-6">
          <div className="flex gap-4">
            <input
              type="text"
              value={filters.keyword}
              onChange={(e) => setFilters({ ...filters, keyword: e.target.value })}
              placeholder="搜索主题..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            />
            <select
              value={filters.platform}
              onChange={(e) => setFilters({ ...filters, platform: e.target.value })}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            >
              <option value="">所有平台</option>
              <option value="douyin">抖音</option>
              <option value="video_account">视频号</option>
              <option value="wechat">公众号</option>
              <option value="xiaohongshu">小红书</option>
            </select>
            <select
              value={filters.status}
              onChange={(e) => setFilters({ ...filters, status: e.target.value })}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            >
              <option value="">所有状态</option>
              <option value="completed">已完成</option>
              <option value="processing">生成中</option>
              <option value="pending">等待中</option>
              <option value="failed">失败</option>
              <option value="partial">部分成功</option>
            </select>
            <button
              onClick={handleSearch}
              className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
            >
              搜索
            </button>
          </div>
        </div>

        {/* 历史记录列表 */}
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        ) : history.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-12 text-center text-gray-500">
            <p className="text-lg">暂无历史记录</p>
            <button
              onClick={() => router.push('/')}
              className="mt-4 px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
            >
              去创建
            </button>
          </div>
        ) : (
          <>
            <div className="bg-white rounded-lg shadow overflow-hidden">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      主题
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      平台
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      状态
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      创建时间
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      操作
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {history.map((item) => (
                    <tr
                      key={item.id}
                      className="hover:bg-gray-50 cursor-pointer"
                      onClick={() => router.push(`/result?id=${item.id}`)}
                    >
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">
                          {item.topic || '无主题'}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                          {getPlatformName(item.platform)}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-${getStatusColor(item.status)}-100 text-${getStatusColor(item.status)}-800`}>
                          {getStatusText(item.status)}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {formatDate(item.created_at)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            router.push(`/result?id=${item.id}`)
                          }}
                          className="text-primary-600 hover:text-primary-900 mr-4"
                        >
                          查看
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            handleDelete(item.id)
                          }}
                          disabled={deleting === item.id}
                          className="text-red-600 hover:text-red-900 disabled:text-gray-400"
                        >
                          {deleting === item.id ? '删除中...' : '删除'}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* 分页 */}
            <div className="bg-white rounded-lg shadow px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6 mt-4">
              <div className="flex-1 flex justify-between sm:hidden">
                <button
                  onClick={() => handlePageChange(pagination.page - 1)}
                  disabled={pagination.page === 1}
                  className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:bg-gray-100"
                >
                  上一页
                </button>
                <button
                  onClick={() => handlePageChange(pagination.page + 1)}
                  disabled={pagination.page >= Math.ceil(pagination.total / pagination.page_size)}
                  className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:bg-gray-100"
                >
                  下一页
                </button>
              </div>
              <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
                <div>
                  <p className="text-sm text-gray-700">
                    共 <span className="font-medium">{pagination.total}</span> 条记录
                  </p>
                </div>
                <div>
                  <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                    <button
                      onClick={() => handlePageChange(pagination.page - 1)}
                      disabled={pagination.page === 1}
                      className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:bg-gray-100"
                    >
                      上一页
                    </button>
                    <button className="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50">
                      第 {pagination.page} 页
                    </button>
                    <button
                      onClick={() => handlePageChange(pagination.page + 1)}
                      disabled={pagination.page >= Math.ceil(pagination.total / pagination.page_size)}
                      className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:bg-gray-100"
                    >
                      下一页
                    </button>
                  </nav>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </main>
  )
}
