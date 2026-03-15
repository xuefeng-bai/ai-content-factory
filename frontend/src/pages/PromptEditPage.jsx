import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Form,
  Input,
  Button,
  Select,
  InputNumber,
  Card,
  Space,
  message,
  Typography,
  Divider,
  Switch,
  Alert,
} from 'antd';
import { SaveOutlined, CloseOutlined } from '@ant-design/icons';
import promptsApi from '../services/prompts';

const { Title } = Typography;
const { TextArea } = Input;
const { Option } = Select;

/**
 * Prompt 编辑页面
 */
const PromptEditPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [isSystem, setIsSystem] = useState(false);
  const [promptData, setPromptData] = useState(null);

  // 加载 Prompt 详情
  useEffect(() => {
    if (id) {
      loadPrompt(id);
    }
  }, [id]);

  const loadPrompt = async (id) => {
    setLoading(true);
    try {
      const data = await promptsApi.getById(id);
      setPromptData(data);
      setIsSystem(data.is_system);
      
      // 填充表单数据 - 处理 variables 可能是字符串或数组
      let variablesStr = '';
      if (Array.isArray(data.variables)) {
        variablesStr = data.variables.join(', ');
      } else if (typeof data.variables === 'string') {
        // 如果已经是字符串（可能从数据库直接返回），直接使用
        variablesStr = data.variables;
      }
      
      form.setFieldsValue({
        ...data,
        variables: variablesStr,
      });
    } catch (error) {
      message.error(`加载失败：${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  // 保存
  const handleSave = async (values) => {
    if (isSystem) {
      message.warning('系统内置 Prompt 不可修改');
      return;
    }

    try {
      const submitData = {
        ...values,
        variables: values.variables?.split(',').map((v) => v.trim()).filter(Boolean),
      };

      await promptsApi.update(id, submitData);
      message.success('更新成功');
      navigate('/prompts');
    } catch (error) {
      message.error(`保存失败：${error.message}`);
    }
  };

  // 取消
  const handleCancel = () => {
    navigate('/prompts');
  };

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <div style={{ marginBottom: '24px' }}>
          <Title level={2}>
            {id ? '编辑 Prompt' : '新建 Prompt'}
          </Title>
        </div>

        {isSystem && (
          <Alert
            message="系统内置 Prompt"
            description="系统内置 Prompt 仅供查看，不可修改。如需使用，请复制后创建新的 Prompt。"
            type="warning"
            showIcon
            style={{ marginBottom: '24px' }}
          />
        )}

        <Form
          form={form}
          layout="vertical"
          onFinish={handleSave}
          disabled={isSystem || loading}
        >
          <Form.Item
            name="name"
            label="标识符"
            rules={[{ required: true, message: '请输入标识符' }]}
            extra="英文标识符，用于代码引用（如：douyin_script）"
          >
            <Input placeholder="例如：douyin_script" disabled />
          </Form.Item>

          <Form.Item
            name="display_name"
            label="显示名称"
            rules={[{ required: true, message: '请输入显示名称' }]}
          >
            <Input placeholder="例如：抖音文案" />
          </Form.Item>

          <Form.Item
            name="description"
            label="描述"
          >
            <TextArea
              rows={2}
              placeholder="描述此 Prompt 的用途"
            />
          </Form.Item>

          <Form.Item
            name="template"
            label="Prompt 模板"
            rules={[{ required: true, message: '请输入模板' }]}
            extra="使用 {variable} 作为占位符，例如：{topic}, {search_results}"
          >
            <TextArea
              rows={12}
              placeholder="你是一位资深内容专家..."
              style={{ fontFamily: 'monospace' }}
            />
          </Form.Item>

          <Form.Item
            name="variables"
            label="变量列表"
            rules={[{ required: true, message: '请输入变量' }]}
            extra="用逗号分隔，例如：topic, search_results"
          >
            <Input placeholder="topic, search_results" />
          </Form.Item>

          <Divider />

          <Form.Item label="高级配置">
            <Space direction="vertical" style={{ width: '100%' }} size="large">
              <Space>
                <Form.Item
                  name="category"
                  label="分类"
                  noStyle
                >
                  <Select style={{ width: 200 }} placeholder="选择分类">
                    <Option value="topic">选题</Option>
                    <Option value="douyin">抖音</Option>
                    <Option value="wechat">公众号</Option>
                    <Option value="xhs">小红书</Option>
                    <Option value="image">配图</Option>
                  </Select>
                </Form.Item>

                <Form.Item
                  name="output_format"
                  label="输出格式"
                  noStyle
                >
                  <Select style={{ width: 150 }} placeholder="选择格式">
                    <Option value="text">纯文本</Option>
                    <Option value="json">JSON</Option>
                    <Option value="markdown">Markdown</Option>
                  </Select>
                </Form.Item>
              </Space>

              <Space>
                <Form.Item
                  name="model"
                  label="AI 模型"
                  noStyle
                >
                  <Select style={{ width: 150 }}>
                    <Option value="qwen-plus">Qwen-Plus</Option>
                    <Option value="qwen-max">Qwen-Max</Option>
                  </Select>
                </Form.Item>

                <Form.Item
                  name="max_tokens"
                  label="最大 Token"
                  noStyle
                >
                  <InputNumber min={100} max={8000} step={100} />
                </Form.Item>

                <Form.Item
                  name="temperature"
                  label="温度"
                  noStyle
                >
                  <InputNumber min={0} max={2} step={0.1} />
                </Form.Item>
              </Space>

              <Form.Item
                name="is_active"
                label="启用状态"
                valuePropName="checked"
                noStyle
              >
                <Switch checkedChildren="启用" unCheckedChildren="禁用" />
              </Form.Item>
            </Space>
          </Form.Item>

          <Divider />

          <Form.Item>
            <Space>
              <Button
                type="primary"
                htmlType="submit"
                icon={<SaveOutlined />}
                disabled={isSystem}
              >
                保存
              </Button>
              <Button
                icon={<CloseOutlined />}
                onClick={handleCancel}
              >
                取消
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default PromptEditPage;
