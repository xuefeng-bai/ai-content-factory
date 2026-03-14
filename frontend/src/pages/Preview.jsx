import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Card,
  Button,
  Tabs,
  Space,
  Typography,
  message,
  Spin,
  Alert,
  Divider,
} from 'antd';
import {
  CopyOutlined,
  DownloadOutlined,
  SyncOutlined,
} from '@ant-design/icons';
import ReactMarkdown from 'react-markdown';
import contentApi from '../services/content';

const { Title } = Typography;
const { TabPane } = Tabs;

/**
 * 内容生成预览页
 */
const PreviewPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [content, setContent] = useState(null);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('douyin');

  // 从路由状态获取选题
  const selectedTopic = location.state?.selectedTopic;

  // 生成内容
  const handleGenerate = async () => {
    if (!selectedTopic) {
      message.warning('请先选择选题');
      navigate('/topic');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const data = await contentApi.generate({
        topic: selectedTopic.title,
        theme: selectedTopic.angle || '',
        platforms: ['douyin', 'wechat', 'xhs'],
      });

      setContent(data);
      message.success('内容生成成功');
    } catch (err) {
      setError(err.message);
      message.error(`生成失败：${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // 复制内容
  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
    message.success('复制成功');
  };

  // 下载内容
  const handleDownload = (platform, text) => {
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${platform}_${selectedTopic?.title || 'content'}.txt`;
    a.click();
    URL.revokeObjectURL(url);
    message.success('下载成功');
  };

  // 渲染内容
  const renderContent = (platform) => {
    if (!content) return null;

    const platformContent = content[platform];
    if (!platformContent) return '暂无内容';

    // 如果是 JSON 格式，解析并展示
    try {
      const parsed = typeof platformContent === 'string' 
        ? JSON.parse(platformContent) 
        : platformContent;

      if (platform === 'wechat') {
        // 公众号文章用 Markdown 渲染
        return (
          <div className="markdown-body">
            <ReactMarkdown>{parsed.full_article || platformContent}</ReactMarkdown>
          </div>
        );
      } else {
        // 抖音/小红书展示完整文案
        return (
          <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.8' }}>
            {parsed.full_script || parsed.full_note || platformContent}
          </div>
        );
      }
    } catch (e) {
      // 非 JSON 格式直接展示
      return <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.8' }}>{platformContent}</div>;
    }
  };

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <div style={{ marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Title level={2}>内容生成</Title>
          <Space>
            <Button
              type="primary"
              icon={<SyncOutlined spin={loading} />}
              onClick={handleGenerate}
              loading={loading}
              size="large"
            >
              {loading ? '生成中...' : '重新生成'}
            </Button>
          </Space>
        </div>

        {/* 选题信息 */}
        {selectedTopic && (
          <Alert
            message="当前选题"
            description={
              <Space>
                <strong>{selectedTopic.title}</strong>
                <span>{selectedTopic.core_point}</span>
              </Space>
            }
            type="info"
            showIcon
            style={{ marginBottom: '16px' }}
          />
        )}

        {/* 错误提示 */}
        {error && (
          <Alert
            message="生成失败"
            description={error}
            type="error"
            showIcon
            style={{ marginBottom: '16px' }}
          />
        )}

        {/* 内容展示 */}
        {loading ? (
          <div style={{ textAlign: 'center', padding: '40px' }}>
            <Spin size="large" tip="AI 正在创作内容，请稍候..." />
          </div>
        ) : content ? (
          <Tabs activeKey={activeTab} onChange={setActiveTab}>
            <TabPane
              tab={
                <Space>
                  <span style={{ fontSize: '16px' }}>🎬</span>
                  抖音文案
                </Space>
              }
              key="douyin"
              extra={
                <Space>
                  <Button
                    size="small"
                    icon={<CopyOutlined />}
                    onClick={() => handleCopy(content.douyin)}
                  >
                    复制
                  </Button>
                  <Button
                    size="small"
                    icon={<DownloadOutlined />}
                    onClick={() => handleDownload('douyin', content.douyin)}
                  >
                    下载
                  </Button>
                </Space>
              }
            >
              <Card size="small">
                {renderContent('douyin')}
              </Card>
            </TabPane>

            <TabPane
              tab={
                <Space>
                  <span style={{ fontSize: '16px' }}>📝</span>
                  公众号文章
                </Space>
              }
              key="wechat"
              extra={
                <Space>
                  <Button
                    size="small"
                    icon={<CopyOutlined />}
                    onClick={() => handleCopy(content.wechat)}
                  >
                    复制
                  </Button>
                  <Button
                    size="small"
                    icon={<DownloadOutlined />}
                    onClick={() => handleDownload('wechat', content.wechat)}
                  >
                    下载
                  </Button>
                </Space>
              }
            >
              <Card size="small">
                {renderContent('wechat')}
              </Card>
            </TabPane>

            <TabPane
              tab={
                <Space>
                  <span style={{ fontSize: '16px' }}>📕</span>
                  小红书笔记
                </Space>
              }
              key="xhs"
              extra={
                <Space>
                  <Button
                    size="small"
                    icon={<CopyOutlined />}
                    onClick={() => handleCopy(content.xhs)}
                  >
                    复制
                  </Button>
                  <Button
                    size="small"
                    icon={<DownloadOutlined />}
                    onClick={() => handleDownload('xhs', content.xhs)}
                  >
                    下载
                  </Button>
                </Space>
              }
            >
              <Card size="small">
                {renderContent('xhs')}
              </Card>
            </TabPane>
          </Tabs>
        ) : (
          <div style={{ textAlign: 'center', padding: '40px', color: '#999' }}>
            <p>点击"重新生成"按钮，为选题创作多平台内容</p>
          </div>
        )}
      </Card>
    </div>
  );
};

export default PreviewPage;
