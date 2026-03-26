'use client'

import { useState } from 'react'
import axios from 'axios'

export default function Home() {
  const [topic, setTopic] = useState('')
  const [templateId, setTemplateId] = useState<number | null>(null)
  const [generating, setGenerating] = useState(false)
  const [generationId, setGenerationId] = useState<number | null>(null)

  const handleGenerate = async () => {
    if (!topic.trim()) {
      alert('请输入创作主题')
      return
    }

    setGenerating(true)
    try {
      const response = await axios.post('/api/v1/content/generate', {
        topic: topic.trim(),
        template_id: templateId
      })
      
      if (response.data.code === 200) {
        setGenerationId(response.data.data.generation_id)
        // 跳转到结果页
        window.location.href = `/result?id=${response.data.data.generation_id}`
      }
    } catch (error) {
      console.error('生成失败:', error)
      alert('生成失败，请稍后重试')
    } finally {
      setGenerating(false)
    }
  }

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        {/* 标题 */}
        <h1 className="text-4xl font-bold text-center mb-2">
          AI 内容工厂 🚀
        </h1>
        <p className="text-center text-gray-600 mb-12">
          输入一个主题，一键生成 4 平台内容（抖音、视频号、公众号、小红书）
        </p>

        {/* 主题输入框 */}
        <div className="mb-6">
          <label className="block text-sm font-medium mb-2">
            创作主题
          </label>
          <textarea
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="输入创作主题，例如：如何高效时间管理..."
            className="w-full h-40 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
          />
        </div>

        {/* 模板选择器 */}
        <div className="mb-8">
          <label className="block text-sm font-medium mb-2">
            提示词模板
          </label>
          <select
            value={templateId || ''}
            onChange={(e) => setTemplateId(e.target.value ? Number(e.target.value) : null)}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">使用系统默认模板</option>
            {/* TODO: 从 API 加载模板列表 */}
            <option value="1">抖音默认模板</option>
            <option value="2">视频号默认模板</option>
            <option value="3">公众号默认模板</option>
            <option value="4">小红书默认模板</option>
          </select>
        </div>

        {/* 生成按钮 */}
        <button
          onClick={handleGenerate}
          disabled={generating}
          className="w-full py-4 px-6 bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 text-white font-semibold rounded-lg transition duration-200 ease-in-out transform hover:scale-105"
        >
          {generating ? '生成中...' : '✨ 一键生成'}
        </button>

        {/* 最近历史记录 */}
        <div className="mt-12">
          <h2 className="text-2xl font-semibold mb-4">最近历史记录</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* TODO: 从 API 加载历史记录 */}
            <div className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition cursor-pointer">
              <h3 className="font-medium mb-2">如何高效时间管理</h3>
              <p className="text-sm text-gray-500">2026-03-25 10:00</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
