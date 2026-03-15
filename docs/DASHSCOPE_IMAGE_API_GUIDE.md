# 🎨 DashScope 文生图 API 配置教程

**更新时间：** 2026-03-15  
**适用模型：** 通义万相 - 文生图（wanx-v1）  
**项目：** AI 内容工厂 v2.0

---

## 📋 目录

1. [注册阿里云账号](#1-注册阿里云账号)
2. [开通 DashScope 服务](#2-开通-dashscope-服务)
3. [获取 API Key](#3-获取-api-key)
4. [配置项目环境](#4-配置项目环境)
5. [测试 API](#5-测试-api)
6. [常见问题](#6-常见问题)

---

## 1. 注册阿里云账号

### 步骤

1. **访问阿里云官网**
   - 网址：https://www.aliyun.com/
   - 点击右上角"登录/注册"

2. **注册账号**
   - 使用手机号注册
   - 完成实名认证（需要身份证）
   - 绑定支付宝（用于支付，新用户有免费额度）

3. **完成实名认证**
   - 个人认证：身份证 + 人脸识别
   - 企业认证：营业执照 + 法人身份证
   - 认证时间：通常 5-10 分钟

---

## 2. 开通 DashScope 服务

### 步骤

1. **访问 DashScope 控制台**
   - 网址：https://dashscope.console.aliyun.com/
   - 或：https://www.aliyun.com/product/dashscope

2. **开通服务**
   - 点击"立即开通"
   - 同意服务协议
   - 完成开通

3. **开通通义万相（文生图）**
   - 在控制台左侧菜单选择"模型广场"
   - 搜索"通义万相"或"wanx"
   - 点击"开通模型"

---

## 3. 获取 API Key

### 步骤

1. **进入 API Key 管理**
   - 访问：https://dashscope.console.aliyun.com/apiKey
   - 或在控制台点击"API Key 管理"

2. **创建新的 API Key**
   - 点击"创建新的 API Key"
   - 输入名称（如"AI 内容工厂"）
   - 点击"确定"

3. **复制 API Key**
   - API Key 格式：`sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - **重要：** API Key 只显示一次，请立即复制保存！
   - 如果丢失，可以删除后重新创建

---

## 4. 配置项目环境

### 步骤

1. **编辑 `.env` 文件**
   
   打开 `backend/.env`，修改以下配置：
   
   ```bash
   # AI 配置（DashScope 阿里云百炼）
   DASHSCOPE_API_KEY=sk-your-new-api-key-here
   AI_MODEL=qwen-plus
   
   # AI 调用超时配置（秒）
   AI_TEXT_TIMEOUT=30
   AI_IMAGE_TIMEOUT=60
   ```

2. **验证配置**
   
   在项目根目录运行：
   
   ```bash
   cd backend
   source venv/bin/activate
   python -c "from app.config import config; print('API Key:', config.DASHSCOPE_API_KEY[:20] + '...')"
   ```

---

## 5. 测试 API

### 5.1 测试文本生成

```bash
cd backend
source venv/bin/activate

python -c "
from app.ai.service import AIService

ai = AIService()
result = ai.generate_text(
    prompt_name='douyin_script',
    variables={'topic': 'AI 工具', 'theme': '效率提升'}
)
print('文本生成成功!')
print(result[:200])
"
```

### 5.2 测试图片生成

```bash
cd backend
source venv/bin/activate

python -c "
from app.ai.service import AIService

ai = AIService()
result = ai.generate_image(
    prompt='一只可爱的猫咪，卡通风格，彩色',
    title='测试图片',
    aspect_ratio='16:9',
    platform='wechat'
)
print('图片生成成功!')
print('图片 URL:', result['image_url'])
"
```

### 5.3 测试 API 接口

启动后端服务：

```bash
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

调用图片生成接口：

```bash
curl -X POST http://localhost:8000/api/images/generate \
  -H "Content-Type: application/json" \
  -d '{
    "content": "AI 效率工具",
    "title": "AI 工具提升效率",
    "aspect_ratio": "16:9",
    "platform": "wechat"
  }'
```

---

## 6. 常见问题

### Q1: API Key 无效（401 错误）

**原因：**
- API Key 输入错误
- API Key 已被删除或禁用
- 账号未实名认证

**解决方案：**
1. 检查 `.env` 文件中的 API Key 是否正确
2. 在控制台重新创建 API Key
3. 完成实名认证

### Q2: 余额不足（402 错误）

**原因：**
- 免费额度已用完
- 账号余额不足

**解决方案：**
1. 查看免费额度：https://dashscope.console.aliyun.com/overview
2. 充值账号：https://usercenter2.aliyun.com/account/recharge
3. 新用户通常有 1000-2000 积分免费额度（约 100-200 次生成）

### Q3: 图片生成超时

**原因：**
- 图片生成需要 10-30 秒
- 网络问题

**解决方案：**
1. 增加超时时间：修改 `.env` 中的 `AI_IMAGE_TIMEOUT=60`
2. 检查网络连接
3. 重试生成

### Q4: 图片无法保存

**原因：**
- `data/images` 目录不存在
- 权限问题

**解决方案：**
```bash
cd backend
mkdir -p data/images
chmod 755 data/images
```

---

## 💰 价格说明

### 免费额度

- **新用户：** 1000-2000 积分（约 100-200 次图片生成）
- **有效期：** 开通后 30 天
- **查询：** https://dashscope.console.aliyun.com/overview

### 超出免费额度后

| 模型 | 价格 | 说明 |
|------|------|------|
| 通义万相 - 文生图 | 0.1-0.2 元/张 | 根据分辨率 |
| Qwen-Plus（文本） | 0.004 元/1K tokens | 约 0.01 元/次 |

---

## 🔗 相关链接

- **DashScope 官网：** https://www.aliyun.com/product/dashscope
- **控制台：** https://dashscope.console.aliyun.com/
- **API 文档：** https://help.aliyun.com/zh/dashscope/
- **通义万相文档：** https://help.aliyun.com/zh/dashscope/developer-reference/quick-call
- **价格详情：** https://www.aliyun.com/price/product#/dashscope/detail

---

## 📞 技术支持

遇到问题？

1. **查看文档：** https://help.aliyun.com/zh/dashscope/
2. **提交工单：** https://workorder.console.aliyun.com/
3. **社区论坛：** https://developer.aliyun.com/group/

---

*最后更新：2026-03-15*  
*AI 内容工厂 - 让内容创作更高效！*
