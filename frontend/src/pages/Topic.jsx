import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Card,
  Button,
  List,
  Typography,
  Tag,
  Space,
  message,
  Alert,
  Spin,
} from 'antd';
import {
  ThunderboltOutlined,
  CheckCircleOutlined,
} from '@ant-design/icons';
import topicsApi from '../services/topics';

const { Title } = Typography;

/**
 * 选题推荐页面
 */
const TopicPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [topics, setTopics] = useState([]);
  const [error, setError] = useState(null);

  // 获取选题推荐（从搜索结果或示例数据）
  const loadTopics = async () => {
    setLoading(true);
    setError(null);

    try {
      // TODO: 从搜索结果获取，这里先用示例数据
      const mockSearchResults = [
        { title: 'AI 工具提升效率', source: 'weibo', hot_value: '500w' },
        { title: '职场人必备技能', source: 'zhihu', hot_value: '300w' },
      ];

      const data = await topicsApi.recommend({
        search_results: mockSearchResults,
        theme: 'AI 效率工具',
      });

      // 解析 AI 返回的 JSON
      let topicsData;
      try {
        topicsData = typeof data.topics === 'string' 
          ? JSON.parse(data.topics) 
          : data.topics;
      } catch (e) {
        topicsData = data.topics;
      }

      setTopics(topicsData || []);
      message.success('选题推荐成功');
    } catch (err) {
      setError(err.message);
      message.error(`推荐失败：${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // 选择选题
  const handleSelectTopic = (topic) => {
    // 跳转到内容生成页，传递选题数据
    navigate('/content', { 
      state: { 
        selectedTopic: topic 
      } 
    });
  };

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <div style={{ marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Title level={2} style={{ margin: 0 }}>
            <ThunderboltOutlined /> 选题推荐
          </Title>
          <Button
            type="primary"
            icon={<ThunderboltOutlined />}
            onClick={loadTopics}
            loading={loading}
            size="large"
          >
            AI 推荐选题
          </Button>
        </div>

        {/* 错误提示 */}
        {error && (
          <Alert
            message="推荐失败"
            description={error}
            type="error"
            showIcon
            style={{ marginBottom: '16px' }}
          />
        )}

        {/* 选题列表 */}
        {loading ? (
          <div style={{ textAlign: 'center', padding: '40px' }}>
            <Spin size="large" tip="AI 正在分析热搜数据，推荐选题..." />
          </div>
        ) : topics.length > 0 ? (
          <List
            grid={{ gutter: 16, column: 2 }}
            dataSource={topics}
            renderItem={(topic) => (
              <List.Item>
                <Card
                  hoverable
                  title={topic.title}
                  extra={
                    <Tag color={getHotColor(topic.hot_score)}>
                      热度：{topic.hot_score}
                    </Tag>
                  }
                  actions={[
                    <Button
                      type="primary"
                      icon={<CheckCircleOutlined />}
                      onClick={() => handleSelectTopic(topic)}
                    >
                      选择此选题
                    </Button>,
                  ]}
                >
                  <p><strong>角度：</strong>{topic.angle}</p>
                  <p><strong>核心观点：</strong>{topic.core_point}</p>
                  <div style={{ marginTop: '8px' }}>
                    {topic.platforms?.map((p) => (
                      <Tag key={p} color={getPlatformColor(p)}>
                        {getPlatformName(p)}
                      </Tag>
                    ))}
                  </div>
                  <p style={{ marginTop: '8px', color: '#666' }}>
                    <strong>推荐理由：</strong>{topic.reason}
                  </p>
                </Card>
              </List.Item>
            )}
          />
        ) : (
          <div style={{ textAlign: 'center', padding: '40px', color: '#999' }}>
            <ThunderboltOutlined style={{ fontSize: '48px', marginBottom: '16px' }} />
            <p>点击"AI 推荐选题"按钮，获取 3-5 个精选选题</p>
          </div>
        )}
      </Card>
    </div>
  );
};

const getPlatformName = (platform) => {
  const names = {
    douyin: '抖音',
    wechat: '公众号',
    xhs: '小红书',
  };
  return names[platform] || platform;
};

const getPlatformColor = (platform) => {
  const colors = {
    douyin: 'red',
    wechat: 'blue',
    xhs: 'pink',
  };
  return colors[platform] || 'default';
};

const getHotColor = (score) => {
  if (score >= 9) return 'red';
  if (score >= 7) return 'orange';
  if (score >= 5) return 'blue';
  return 'default';
};

export default TopicPage;
