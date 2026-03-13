import React, { useState } from 'react';
import {
  SearchOutlined,
  WeiboOutlined,
  BookOutlined,
  LoadingOutlined,
  ExclamationCircleOutlined,
} from '@ant-design/icons';
import {
  Input,
  Button,
  List,
  Typography,
  Spin,
  Alert,
  Card,
  Space,
  Tag,
  Divider,
} from 'antd';

const { Title } = Typography;
const { TextArea } = Input;

/**
 * 搜索页面组件
 * 功能：搜索微博热搜和知乎热榜
 */
const SearchPage = () => {
  const [searchTheme, setSearchTheme] = useState('');
  const [loading, setLoading] = useState(false);
  const [searchResults, setSearchResults] = useState(null);
  const [error, setError] = useState(null);

  /**
   * 执行搜索
   */
  const handleSearch = async () => {
    if (!searchTheme.trim()) {
      setError('请输入搜索主题');
      return;
    }

    setLoading(true);
    setError(null);
    setSearchResults(null);

    try {
      const response = await fetch('http://localhost:8000/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          theme: searchTheme,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      
      if (data.code === 200) {
        setSearchResults(data.data);
      } else {
        setError(data.message || '搜索失败');
      }
    } catch (err) {
      console.error('搜索错误:', err);
      setError(`搜索失败：${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  /**
   * 处理回车键搜索
   */
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  /**
   * 渲染搜索项
   */
  const renderSearchItem = (item, index) => (
    <List.Item
      key={index}
      actions={[
        <a
          key="link"
          href={item.url}
          target="_blank"
          rel="noopener noreferrer"
        >
          查看详情 →
        </a>,
      ]}
    >
      <List.Item.Meta
        avatar={
          <Tag color={item.source === 'weibo' ? 'red' : 'blue'}>
            {item.source === 'weibo' ? '微博' : '知乎'}
          </Tag>
        }
        title={
          <Space>
            <span>#{item.rank}</span>
            <span>{item.title}</span>
          </Space>
        }
        description={item.hot_value}
      />
    </List.Item>
  );

  return (
    <div style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto' }}>
      {/* 搜索区域 */}
      <Card style={{ marginBottom: '24px' }}>
        <Title level={2}>
          <SearchOutlined /> 热门话题搜索
        </Title>
        
        <Space.Compact style={{ width: '100%' }}>
          <TextArea
            value={searchTheme}
            onChange={(e) => setSearchTheme(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="输入搜索主题，例如：AI 效率工具、人工智能、职场发展..."
            style={{ flex: 1 }}
            rows={2}
            disabled={loading}
          />
          <Button
            type="primary"
            icon={loading ? <LoadingOutlined /> : <SearchOutlined />}
            onClick={handleSearch}
            loading={loading}
            size="large"
          >
            {loading ? '搜索中...' : '搜索'}
          </Button>
        </Space.Compact>
      </Card>

      {/* 错误提示 */}
      {error && (
        <Alert
          message="搜索失败"
          description={error}
          type="error"
          showIcon
          icon={<ExclamationCircleOutlined />}
          style={{ marginBottom: '24px' }}
        />
      )}

      {/* 搜索结果 */}
      {searchResults && (
        <Space direction="vertical" style={{ width: '100%' }} size="large">
          {/* 微博热搜 */}
          <Card
            title={
              <Space>
                <WeiboOutlined style={{ color: '#e6162d' }} />
                <span>微博热搜 Top 50</span>
              </Space>
            }
            size="small"
          >
            <List
              dataSource={searchResults.weibo_hot_search || []}
              renderItem={renderSearchItem}
              size="small"
              pagination={{
                pageSize: 10,
                showSizeChanger: false,
              }}
              locale={{ emptyText: '暂无数据' }}
            />
          </Card>

          <Divider />

          {/* 知乎热榜 */}
          <Card
            title={
              <Space>
                <BookOutlined style={{ color: '#0084ff' }} />
                <span>知乎热榜 Top 50</span>
              </Space>
            }
            size="small"
          >
            <List
              dataSource={searchResults.zhihu_hot_list || []}
              renderItem={renderSearchItem}
              size="small"
              pagination={{
                pageSize: 10,
                showSizeChanger: false,
              }}
              locale={{ emptyText: '暂无数据' }}
            />
          </Card>
        </Space>
      )}

      {/* 初始状态提示 */}
      {!searchResults && !loading && !error && (
        <Card>
          <div style={{ textAlign: 'center', padding: '40px', color: '#999' }}>
            <SearchOutlined style={{ fontSize: '48px', marginBottom: '16px' }} />
            <p>输入搜索主题，获取微博热搜和知乎热榜</p>
          </div>
        </Card>
      )}
    </div>
  );
};

export default SearchPage;
