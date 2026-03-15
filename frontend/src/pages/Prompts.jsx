import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Table,
  Button,
  Space,
  Tag,
  Input,
  Select,
  Modal,
  message,
  Typography,
  Card,
} from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  ExperimentOutlined,
  SearchOutlined,
} from '@ant-design/icons';
import promptsApi from '../services/prompts';
import PromptCreateModal from '../components/PromptCreateModal';

const { Title } = Typography;
const { TextArea } = Input;
const { Option } = Select;

/**
 * Prompt 管理列表页
 */
const PromptsPage = () => {
  const [prompts, setPrompts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchText, setSearchText] = useState('');
  const [categoryFilter, setCategoryFilter] = useState(null);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [createModalVisible, setCreateModalVisible] = useState(false);

  // 加载 Prompt 列表
  const loadPrompts = async () => {
    setLoading(true);
    try {
      const params = {
        page,
        page_size: pageSize,
      };
      if (categoryFilter) params.category = categoryFilter;
      
      const data = await promptsApi.getList(params);
      setPrompts(data.list || []);
      setTotal(data.total || 0);
    } catch (error) {
      message.error(`加载失败：${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPrompts();
  }, [page, pageSize, categoryFilter]);

  // 删除 Prompt
  const handleDelete = (record) => {
    Modal.confirm({
      title: '确认删除',
      content: `确定要删除 Prompt "${record.display_name}" 吗？`,
      onOk: async () => {
        try {
          await promptsApi.delete(record.id);
          message.success('删除成功');
          loadPrompts();
        } catch (error) {
          message.error(`删除失败：${error.message}`);
        }
      },
    });
  };

  // 表格列定义
  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      width: 60,
    },
    {
      title: '名称',
      dataIndex: 'display_name',
      key: 'display_name',
      ellipsis: true,
    },
    {
      title: '标识符',
      dataIndex: 'name',
      width: 200,
      render: (text) => <code>{text}</code>,
    },
    {
      title: '分类',
      dataIndex: 'category',
      width: 100,
      render: (text) => (
        <Tag color={getCategoryColor(text)}>{text || '未分类'}</Tag>
      ),
    },
    {
      title: '状态',
      width: 80,
      render: (_, record) => (
        <>
          {record.is_system && <Tag color="blue">系统</Tag>}
          {record.is_active ? (
            <Tag color="green">启用</Tag>
          ) : (
            <Tag color="red">禁用</Tag>
          )}
        </>
      ),
    },
    {
      title: '操作',
      key: 'action',
      width: 250,
      render: (_, record) => (
        <Space>
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            编辑
          </Button>
          <Button
            type="link"
            icon={<ExperimentOutlined />}
            onClick={() => handleTest(record)}
          >
            测试
          </Button>
          {!record.is_system && (
            <Button
              type="link"
              danger
              icon={<DeleteOutlined />}
              onClick={() => handleDelete(record)}
            >
              删除
            </Button>
          )}
        </Space>
      ),
    },
  ];

  const getCategoryColor = (category) => {
    const colors = {
      topic: 'purple',
      douyin: 'red',
      wechat: 'blue',
      xhs: 'pink',
      image: 'cyan',
    };
    return colors[category] || 'default';
  };

  const handleEdit = (record) => {
    // 跳转到编辑页
    navigate(`/prompts/${record.id}/edit`);
  };

  const handleTest = (record) => {
    // 跳转到测试页，并传递 Prompt ID
    navigate(`/prompts/test?prompt_id=${record.id}`);
  };

  const handleCreateSuccess = () => {
    setCreateModalVisible(false);
    loadPrompts();
  };

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <div style={{ marginBottom: '16px', display: 'flex', justifyContent: 'space-between' }}>
          <Title level={2} style={{ margin: 0 }}>
            Prompt 管理
          </Title>
          <Button 
            type="primary" 
            icon={<PlusOutlined />}
            onClick={() => setCreateModalVisible(true)}
          >
            新建 Prompt
          </Button>
        </div>

        {/* 筛选区 */}
        <Space style={{ marginBottom: '16px' }}>
          <Input
            placeholder="搜索名称..."
            prefix={<SearchOutlined />}
            style={{ width: 200 }}
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
          />
          <Select
            placeholder="分类筛选"
            allowClear
            style={{ width: 120 }}
            value={categoryFilter}
            onChange={setCategoryFilter}
          >
            <Option value="topic">选题</Option>
            <Option value="douyin">抖音</Option>
            <Option value="wechat">公众号</Option>
            <Option value="xhs">小红书</Option>
            <Option value="image">配图</Option>
          </Select>
        </Space>

        {/* 表格 */}
        <Table
          columns={columns}
          dataSource={prompts}
          rowKey="id"
          loading={loading}
          pagination={{
            current: page,
            pageSize,
            total,
            showSizeChanger: true,
            showTotal: (total) => `共 ${total} 条`,
            onChange: (page, pageSize) => {
              setPage(page);
              setPageSize(pageSize);
            },
          }}
        />
      </Card>

      {/* 新建 Prompt 弹窗 */}
      <PromptCreateModal
        visible={createModalVisible}
        onCancel={() => setCreateModalVisible(false)}
        onSuccess={handleCreateSuccess}
      />
    </div>
  );
};

export default PromptsPage;
