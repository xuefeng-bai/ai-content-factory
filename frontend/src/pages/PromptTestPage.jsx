import React, { useState } from 'react';
import {
  Form,
  Input,
  Button,
  Card,
  Space,
  message,
  Typography,
  Divider,
  Alert,
  Tag,
} from 'antd';
import { ExperimentOutlined, SendOutlined } from '@ant-design/icons';
import promptsApi from '../services/prompts';

const { Title } = Typography;
const { TextArea } = Input;

/**
 * Prompt 测试页面
 */
const PromptTestPage = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // 测试 Prompt
  const handleTest = async (values) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // 解析输入变量为 JSON
      let inputVars;
      try {
        inputVars = JSON.parse(values.input_vars);
      } catch (e) {
        throw new Error('输入变量必须是有效的 JSON 格式');
      }

      const data = await promptsApi.test({
        prompt_id: parseInt(values.prompt_id),
        input_vars: inputVars,
      });

      setResult(data);
      message.success('测试成功');
    } catch (err) {
      setError(err.message);
      message.error(`测试失败：${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <Title level={2}>
          <ExperimentOutlined /> Prompt 测试
        </Title>

        <Divider />

        <Alert
          message="测试说明"
          description="输入 Prompt ID 和变量 JSON，测试 Prompt 模板填充效果。不会调用真实 AI，仅展示填充后的模板。"
          type="info"
          showIcon
          style={{ marginBottom: '24px' }}
        />

        <Form
          form={form}
          layout="vertical"
          onFinish={handleTest}
        >
          <Form.Item
            name="prompt_id"
            label="Prompt ID"
            rules={[{ required: true, message: '请输入 Prompt ID' }]}
            extra="要测试的 Prompt ID（可在 Prompt 管理页面查看）"
          >
            <Input type="number" placeholder="例如：1" style={{ width: 200 }} />
          </Form.Item>

          <Form.Item
            name="input_vars"
            label="输入变量（JSON 格式）"
            rules={[{ required: true, message: '请输入变量' }]}
            extra='例如：{"topic": "AI 工具", "search_results": "微博热搜..."}'
          >
            <TextArea
              rows={6}
              placeholder='{"topic": "AI 工具", "search_results": "..."}'
              style={{ fontFamily: 'monospace' }}
            />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              icon={<SendOutlined />}
              loading={loading}
              size="large"
            >
              {loading ? '测试中...' : '开始测试'}
            </Button>
          </Form.Item>
        </Form>

        <Divider />

        {/* 错误提示 */}
        {error && (
          <Alert
            message="测试失败"
            description={error}
            type="error"
            showIcon
            style={{ marginBottom: '16px' }}
          />
        )}

        {/* 测试结果 */}
        {result && (
          <div>
            <Title level={4}>测试结果</Title>
            
            <Space direction="vertical" style={{ width: '100%' }} size="middle">
              <Card size="small" title="基本信息">
                <Space direction="vertical" style={{ width: '100%' }}>
                  <div><strong>Prompt ID:</strong> {result.prompt_id}</div>
                  <div><strong>Prompt 名称:</strong> {result.prompt_name}</div>
                  <div><strong>输入变量:</strong></div>
                  <pre style={{ 
                    background: '#f5f5f5', 
                    padding: '12px', 
                    borderRadius: '4px',
                    overflow: 'auto'
                  }}>
                    {JSON.stringify(result.input_vars, null, 2)}
                  </pre>
                </Space>
              </Card>

              <Card size="small" title="填充后的模板">
                <TextArea
                  value={result.filled_template}
                  readOnly
                  rows={10}
                  style={{ fontFamily: 'monospace', fontSize: '12px' }}
                />
              </Card>

              {result.note && (
                <Alert
                  message="提示"
                  description={result.note}
                  type="info"
                  showIcon
                />
              )}
            </Space>
          </div>
        )}

        {/* 空状态提示 */}
        {!result && !loading && !error && (
          <div style={{ textAlign: 'center', padding: '40px', color: '#999' }}>
            <ExperimentOutlined style={{ fontSize: '48px', marginBottom: '16px' }} />
            <p>输入 Prompt ID 和变量，测试 Prompt 效果</p>
          </div>
        )}
      </Card>
    </div>
  );
};

export default PromptTestPage;
