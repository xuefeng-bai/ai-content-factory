import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import {
  SearchOutlined,
  ThunderboltOutlined,
  PictureOutlined,
  HistoryOutlined,
  SettingOutlined,
} from '@ant-design/icons';

import SearchPage from './pages/Search';
import PromptsPage from './pages/Prompts';
import PromptEditPage from './pages/PromptEditPage';
import PromptTestPage from './pages/PromptTestPage';
import TopicPage from './pages/Topic';
import PreviewPage from './pages/Preview';

const { Header, Content, Footer } = Layout;

/**
 * 主应用组件
 */
const App = () => {
  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Header style={{ display: 'flex', alignItems: 'center' }}>
          <div style={{ color: 'white', fontSize: '20px', fontWeight: 'bold', marginRight: '40px' }}>
            🎨 AI 内容工厂
          </div>
          <Menu
            theme="dark"
            mode="horizontal"
            defaultSelectedKeys={['search']}
            items={[
              {
                key: 'search',
                icon: <SearchOutlined />,
                label: <Link to="/">搜索</Link>,
              },
              {
                key: 'prompts',
                icon: <SettingOutlined />,
                label: <Link to="/prompts">Prompt 管理</Link>,
              },
              {
                key: 'topic',
                icon: <ThunderboltOutlined />,
                label: <Link to="/topic">选题</Link>,
              },
              {
                key: 'content',
                icon: <PictureOutlined />,
                label: <Link to="/content">内容生成</Link>,
              },
              {
                key: 'history',
                icon: <HistoryOutlined />,
                label: <Link to="/history">历史</Link>,
              },
            ]}
          />
        </Header>
        <Content style={{ padding: '0 50px', marginTop: '20px' }}>
          <Routes>
            <Route path="/" element={<SearchPage />} />
            <Route path="/prompts" element={<PromptsPage />} />
            <Route path="/prompts/:id/edit" element={<PromptEditPage />} />
            <Route path="/prompts/test" element={<PromptTestPage />} />
            <Route path="/topic" element={<TopicPage />} />
            <Route path="/content" element={<PreviewPage />} />
            <Route path="/history" element={<div style={{ padding: '40px', textAlign: 'center' }}>历史模块开发中...</div>} />
          </Routes>
        </Content>
        <Footer style={{ textAlign: 'center' }}>
          AI 内容工厂 v2.0.0 - Phase 2 开发中
        </Footer>
      </Layout>
    </Router>
  );
};

export default App;
