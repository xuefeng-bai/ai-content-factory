import React, { useState } from 'react';
import {
  Modal,
  Form,
  Input,
  Select,
  InputNumber,
  message,
  Switch,
} from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import promptsApi from '../services/prompts';

const { TextArea } = Input;
const { Option } = Select;

/**
 * 新建 Prompt 弹窗组件
 */
const PromptCreateModal = ({ visible, onCancel, onSuccess }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  // 提交新建
  const handleSubmit = async (values) => {
    setLoading(true);
    try {
      // 将 variables 字符串转换为数组
      const submitData = {
        ...values,
        variables: values.variables
          ? values.variables.split(',').map((v) => v.trim()).filter(Boolean)
          : [],
      };

      await promptsApi.create(submitData);
      message.success('Prompt 创建成功');
      form.resetFields();
      onSuccess();
    } catch (error) {
      message.error(`创建失败：${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      title={
        <span>
          <PlusOutlined /> 新建 Prompt
        </span>
      }
      open={visible}
      onCancel={onCancel}
      onOk={() => form.submit()}
      confirmLoading={loading}
      width={800}
      destroyOnClose
    >
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        initialValues={{
          model: 'qwen-plus',
          max_tokens: 2000,
          temperature: 0.7,
          output_format: 'json',
          is_active: true,
        }}
      >
        <Form.Item
          name="name"
          label="标识符"
          rules={[
            { required: true, message: '请输入标识符' },
            { pattern: /^[a-z_]+$/, message: '只能使用小写字母和下划线' },
          ]}
          extra="英文标识符，用于代码引用（如：douyin_script）"
        >
          <Input placeholder="例如：douyin_script" />
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
          rules={[{ required: true, message: '请输入描述' }]}
        >
          <TextArea rows={2} placeholder="描述此 Prompt 的用途" />
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

        <Form.Item
          name="category"
          label="分类"
          rules={[{ required: true, message: '请选择分类' }]}
        >
          <Select placeholder="选择分类">
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
          rules={[{ required: true, message: '请选择输出格式' }]}
        >
          <Select placeholder="选择格式">
            <Option value="text">纯文本</Option>
            <Option value="json">JSON</Option>
            <Option value="markdown">Markdown</Option>
          </Select>
        </Form.Item>

        <Form.Item label="AI 配置" style={{ marginBottom: 0 }}>
          <Form.Item
            name="model"
            label="AI 模型"
            style={{ display: 'inline-block', width: 'calc(33% - 8px)' }}
          >
            <Select>
              <Option value="qwen-plus">Qwen-Plus</Option>
              <Option value="qwen-max">Qwen-Max</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="max_tokens"
            label="最大 Token"
            style={{ display: 'inline-block', width: 'calc(33% - 8px)' }}
          >
            <InputNumber min={100} max={8000} step={100} />
          </Form.Item>

          <Form.Item
            name="temperature"
            label="温度"
            style={{ display: 'inline-block', width: 'calc(33% - 8px)' }}
          >
            <InputNumber min={0} max={2} step={0.1} />
          </Form.Item>
        </Form.Item>

        <Form.Item
          name="is_active"
          label="启用状态"
          valuePropName="checked"
        >
          <Switch checkedChildren="启用" unCheckedChildren="禁用" />
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default PromptCreateModal;
