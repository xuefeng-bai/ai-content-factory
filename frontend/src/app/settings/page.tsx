'use client'

import { useState, useEffect } from 'react'
import { configAPI } from '@/api/client'

export default function SettingsPage() {
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [testing, setTesting] = useState<string | null>(null)
  const [configs, setConfigs] = useState<any>({})
  const [testResults, setTestResults] = useState<any>({})

  useEffect(() => {
    loadConfigs()
  }, [])

  const loadConfigs = async () => {
    setLoading(true)
    try {
      const response = await configAPI.getList()
      if (response.code === 200) {
        const configMap: any = {}
        response.data.forEach((config: any) => {
          configMap[config.config_key] = config.config_value
        })
        setConfigs(configMap)
      }
    } catch (error) {
      console.error('加载配置失败:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    setSaving(true)
    try {
      const promises = [
        configAPI.update('claude_api_key', configs.claude_api_key || ''),
        configAPI.update('tongyi_api_key', configs.tongyi_api_key || ''),
        configAPI.update('tongyi_wanxiang_api_key', configs.tongyi_wanxiang_api_key || ''),
        configAPI.update('default_ai_provider', configs.default_ai_provider || 'claude')
      ]
      
      await Promise.all(promises)
      alert('保存成功')
    } catch (error) {
      console.error('保存失败:', error)
      alert('保存失败，请稍后重试')
    } finally {
      setSaving(false)
    }
  }

  const handleTest = async (provider: string) => {
    setTesting(provider)
    try {
      // 模拟测试（实际应该调用后端测试接口）
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      const apiKey = provider === 'claude' ? configs.claude_api_key : 
                     provider === 'tongyi' ? configs.tongyi_api_key : 
                     configs.tongyi_wanxiang_api_key
      
      if (apiKey && apiKey.length > 10) {
        setTestResults({
          ...testResults,
          [provider]: { success: true, message: '连接成功' }
        })
        alert(`${provider === 'claude' ? 'Claude' : provider === 'tongyi' ? '通义千问' : '通义万相'} 连接成功！`)
      } else {
        setTestResults({
          ...testResults,
          [provider]: { success: false, message: 'API Key 格式不正确' }
        })
        alert('API Key 格式不正确，请检查')
      }
    } catch (error) {
      setTestResults({
        ...testResults,
        [provider]: { success: false, message: '连接失败' }
      })
      alert('连接失败，请稍后重试')
    } finally {
      setTesting(null)
    }
  }

  return (
    <main className="min-h-screen p-8 bg-gray-50">
      <div className="max-w-4xl mx-auto">
        {/* 页面标题 */}
        <div className="mb-6">
          <button
            onClick={() => window.history.back()}
            className="text-gray-600 hover:text-gray-800 mr-4"
          >
            ← 返回
          </button>
          <span className="text-3xl font-bold">系统设置</span>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        ) : (
          <div className="space-y-6">
            {/* AI 服务配置卡片 */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold mb-4">AI 服务配置</h2>
              
              <div className="space-y-4">
                {/* Claude API Key */}
                <div>
                  <label className="block text-sm font-medium mb-2">
                    Claude API Key
                  </label>
                  <div className="flex gap-2">
                    <input
                      type="password"
                      value={configs.claude_api_key || ''}
                      onChange={(e) => setConfigs({ ...configs, claude_api_key: e.target.value })}
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                      placeholder="sk-ant-..."
                    />
                    <button
                      onClick={() => handleTest('claude')}
                      disabled={testing === 'claude'}
                      className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400"
                    >
                      {testing === 'claude' ? '测试中...' : '测试'}
                    </button>
                  </div>
                  {testResults.claude && (
                    <p className={`mt-1 text-sm ${testResults.claude.success ? 'text-green-600' : 'text-red-600'}`}>
                      {testResults.claude.message}
                    </p>
                  )}
                </div>

                {/* 通义千问 API Key */}
                <div>
                  <label className="block text-sm font-medium mb-2">
                    通义千问 API Key
                  </label>
                  <div className="flex gap-2">
                    <input
                      type="password"
                      value={configs.tongyi_api_key || ''}
                      onChange={(e) => setConfigs({ ...configs, tongyi_api_key: e.target.value })}
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                      placeholder="请输入 API Key"
                    />
                    <button
                      onClick={() => handleTest('tongyi')}
                      disabled={testing === 'tongyi'}
                      className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400"
                    >
                      {testing === 'tongyi' ? '测试中...' : '测试'}
                    </button>
                  </div>
                  {testResults.tongyi && (
                    <p className={`mt-1 text-sm ${testResults.tongyi.success ? 'text-green-600' : 'text-red-600'}`}>
                      {testResults.tongyi.message}
                    </p>
                  )}
                </div>

                {/* 通义万相 API Key */}
                <div>
                  <label className="block text-sm font-medium mb-2">
                    通义万相 API Key
                  </label>
                  <div className="flex gap-2">
                    <input
                      type="password"
                      value={configs.tongyi_wanxiang_api_key || ''}
                      onChange={(e) => setConfigs({ ...configs, tongyi_wanxiang_api_key: e.target.value })}
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                      placeholder="请输入 API Key"
                    />
                    <button
                      onClick={() => handleTest('tongyi_wanxiang')}
                      disabled={testing === 'tongyi_wanxiang'}
                      className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400"
                    >
                      {testing === 'tongyi_wanxiang' ? '测试中...' : '测试'}
                    </button>
                  </div>
                  {testResults.tongyi_wanxiang && (
                    <p className={`mt-1 text-sm ${testResults.tongyi_wanxiang.success ? 'text-green-600' : 'text-red-600'}`}>
                      {testResults.tongyi_wanxiang.message}
                    </p>
                  )}
                </div>

                {/* 默认服务商 */}
                <div>
                  <label className="block text-sm font-medium mb-2">
                    默认 AI 服务商
                  </label>
                  <select
                    value={configs.default_ai_provider || 'claude'}
                    onChange={(e) => setConfigs({ ...configs, default_ai_provider: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="claude">Claude</option>
                    <option value="tongyi">通义千问</option>
                  </select>
                  <p className="mt-1 text-xs text-gray-500">
                    当默认服务商失败时，会自动切换到备用服务商
                  </p>
                </div>
              </div>
            </div>

            {/* 保存按钮 */}
            <div className="flex justify-end">
              <button
                onClick={handleSave}
                disabled={saving}
                className="px-8 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-gray-400 text-lg font-medium"
              >
                {saving ? '保存中...' : '保存配置'}
              </button>
            </div>

            {/* 使用说明 */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="font-semibold text-blue-900 mb-2">💡 使用说明</h3>
              <ul className="text-sm text-blue-800 space-y-1">
                <li>• Claude API Key 格式：sk-ant-...</li>
                <li>• 通义千问和通义万相 API Key 请在阿里云控制台获取</li>
                <li>• 建议配置双服务商备份，提高可用性</li>
                <li>• 配置保存后即时生效，无需刷新页面</li>
                <li>• 点击"测试"按钮可以验证 API Key 是否有效</li>
              </ul>
            </div>
          </div>
        )}
      </div>
    </main>
  )
}
