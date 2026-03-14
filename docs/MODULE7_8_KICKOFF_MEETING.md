# Phase 2 模块 7-8 开发启动会

**会议时间：** 2026-03-14 11:45  
**主持人：** 项目经理虾 🦐📋  
**参会人员：** 全体团队成员  
**会议主题：** 模块 7（配图生成）+ 模块 8（历史记录）开发说明

---

## 📋 会议议程

1. Phase 2 当前进度同步（5 分钟）
2. 模块 7-8 功能说明（10 分钟）
3. 技术规范和注意事项（10 分钟）
4. 任务分配和时间节点（5 分钟）
5. Q&A（5 分钟）

---

## 📊 Phase 2 当前进度

### 已完成模块（95%）

| 模块 | 负责人 | 状态 | 完成度 |
|------|--------|------|--------|
| 模块 1：Prompt 数据库 | 后端虾 | ✅ 完成 | 100% |
| 模块 2：Prompt 管理 API | 后端虾 | ✅ 完成 | 100% |
| 模块 3：AIService | 后端虾 | ✅ 完成 | 100% |
| 模块 4：Prompt 管理前端 | 前端虾 | ✅ 完成 | 100% |
| 模块 5：选题推荐前端 | 前端虾 | ✅ 完成 | 100% |
| 模块 6：内容生成前端 | 前端虾 | ✅ 完成 | 100% |
| **模块 7：配图生成** | **待定** | ⏳ **待开始** | **0%** |
| **模块 8：历史记录** | **待定** | ⏳ **待开始** | **0%** |

### 测试结果

- ✅ 后端 API 测试：10/10 通过
- ✅ 数据库测试：3/3 通过
- ✅ Mock AI 测试：4/4 通过
- ⚠️ 前端服务：依赖修复中

---

## 🎯 模块 7-8 功能说明

### 模块 7：配图生成（预计 1 天）

#### 后端任务

**API 接口：**
```python
POST /api/images/generate      - 生成配图
GET  /api/images/:id           - 获取图片信息
GET  /api/images               - 图片列表
```

**功能要求：**
1. ✅ 调用 DashScope 文生图 API
2. ✅ 支持两种比例：16:9（公众号）、3:4（小红书）
3. ✅ 图片存储到本地或云存储
4. ✅ 返回图片 URL 或 base64
5. ✅ 记录生成历史

**技术要点：**
- 使用 `app/ai/image.py` 封装图片生成服务
- 图片保存到 `backend/data/images/` 目录
- 数据库记录保存到 `content_history` 表

---

#### 前端任务

**页面组件：**
```jsx
pages/ImageGen.jsx         - 配图生成页
components/ImageGallery.jsx - 图片展示组件
services/images.js         - Images API 服务
```

**功能要求：**
1. ✅ 选择内容类型（公众号/小红书）
2. ✅ 输入文章标题/内容
3. ✅ 调用 AI 生成配图
4. ✅ 图片预览（放大/下载）
5. ✅ 历史图片列表

**技术要点：**
- 使用 Ant Design Upload 组件
- 图片预览使用 Modal 组件
- 下载功能使用 blob URL

---

### 模块 8：历史记录（预计 1 天）

#### 后端任务

**API 接口：**
```python
GET    /api/history              - 历史列表（分页）
GET    /api/history/:id          - 历史详情
DELETE /api/history/:id          - 删除历史
GET    /api/history/search       - 搜索历史
```

**功能要求：**
1. ✅ 查询历史记录（分页、筛选）
2. ✅ 按主题/平台/日期筛选
3. ✅ 查看历史详情
4. ✅ 删除历史记录
5. ✅ 搜索功能

**技术要点：**
- 使用 `content_history` 表
- 支持多字段筛选
- 搜索使用 LIKE 查询

---

#### 前端任务

**页面组件：**
```jsx
pages/History.jsx        - 历史列表页
services/history.js      - History API 服务
components/HistoryCard.jsx - 历史卡片组件
```

**功能要求：**
1. ✅ 历史列表展示（卡片/表格）
2. ✅ 分页功能
3. ✅ 搜索/筛选（主题、平台、日期）
4. ✅ 查看详情（弹窗或跳转）
5. ✅ 删除确认

**技术要点：**
- 使用 Ant Design Table 或 Card
- 搜索防抖处理
- 删除操作二次确认

---

## ⚠️ 开发注意事项

### 后端注意事项

#### 1. API 设计规范

**必须遵守：**
```python
# ✅ 统一响应格式
{
    "code": 200,
    "message": "success",
    "data": {...}
}

# ✅ 错误处理
try:
    ...
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

# ✅ 参数验证
class ImageGenerateRequest(BaseModel):
    content: str = Field(..., min_length=10)
    aspect_ratio: str = Field("16:9", regex="^(16:9|3:4)$")
```

**严格禁止：**
```python
# ❌ 直接返回数据
return {"result": data}

# ❌ 不处理异常
data = generate_image(...)
return data

# ❌ 不验证参数
def generate(content, ratio):
    ...
```

---

#### 2. 数据库操作

**必须遵守：**
```python
# ✅ 参数化查询
cursor.execute("SELECT * FROM history WHERE theme = ?", (theme,))

# ✅ 使用事务
conn.execute("BEGIN")
try:
    cursor.execute(...)
    conn.commit()
except:
    conn.rollback()
    raise

# ✅ 关闭连接
conn.close()
```

**严格禁止：**
```python
# ❌ SQL 注入风险
cursor.execute(f"SELECT * FROM history WHERE theme = '{theme}'")

# ❌ 不使用事务
cursor.execute("INSERT INTO ...")
cursor.execute("INSERT INTO ...")

# ❌ 不关闭连接
conn = sqlite3.connect(...)
```

---

#### 3. AI 服务调用

**必须遵守：**
```python
# ✅ 设置超时
response = dashscope.ImageSynthesis.call(
    prompt=prompt,
    timeout=60
)

# ✅ 添加重试
for attempt in range(3):
    try:
        response = call_ai()
        break
    except:
        if attempt == 2:
            raise
        time.sleep(2 ** attempt)

# ✅ 记录日志
logger.info(f"Image generated: {image_id}")
```

**严格禁止：**
```python
# ❌ 无超时调用
response = dashscope.call(...)  # 可能永久等待

# ❌ 不处理异常
response = dashscope.call(...)
image_url = response.url

# ❌ 不记录日志
```

---

### 前端注意事项

#### 1. API 调用规范

**必须遵守：**
```javascript
// ✅ 统一错误处理
try {
  const data = await imagesApi.generate({...});
  message.success('生成成功');
} catch (error) {
  message.error(`生成失败：${error.message}`);
}

// ✅ Loading 状态
const [loading, setLoading] = useState(false);
<Button loading={loading} onClick={handleGenerate}>
  {loading ? '生成中...' : '生成'}
</Button>

// ✅ 表单验证
<Form.Item
  name="content"
  rules={[{ required: true, message: '请输入内容' }]}
>
  <TextArea />
</Form.Item>
```

**严格禁止：**
```javascript
// ❌ 不处理错误
const data = await imagesApi.generate({...});

// ❌ 不提供反馈
<Button onClick={handleGenerate}>生成</Button>
// 用户不知道是否成功

// ❌ 不验证表单
<Form.Item name="content">
  <TextArea />
</Form.Item>
```

---

#### 2. 组件开发规范

**必须遵守：**
```jsx
// ✅ 提取通用组件
const ImageCard = ({ image, onDownload, onDelete }) => {
  return (
    <Card
      cover={<img src={image.url} alt={image.title} />}
      actions={[
        <DownloadOutlined key="download" onClick={onDownload} />,
        <DeleteOutlined key="delete" onClick={onDelete} />
      ]}
    />
  );
};

// ✅ 使用 PropTypes 或 TypeScript
ImageCard.propTypes = {
  image: PropTypes.shape({
    url: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired
  }).isRequired,
  onDownload: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
};
```

**严格禁止：**
```jsx
// ❌ 重复代码
// 在多个文件中复制相同的卡片组件

// ❌ 硬编码样式
<div style={{color: 'red', fontSize: '14px'}}>
  标题
</div>

// ❌ 不使用 Ant Design 组件
<button className="my-button">点击</button>
```

---

#### 3. 性能优化

**必须遵守：**
```javascript
// ✅ 防抖搜索
const handleSearch = useMemo(() => 
  debounce((value) => {
    setSearchQuery(value);
  }, 300),
[]);

// ✅ 分页加载
const loadHistory = async (page = 1) => {
  const data = await historyApi.getList({ page, page_size: 20 });
  setHistory(data.list);
};

// ✅ 图片懒加载
<img loading="lazy" src={image.url} alt={image.title} />
```

**严格禁止：**
```javascript
// ❌ 每次输入都查询
onChange={(e) => handleSearch(e.target.value)}
// 导致频繁 API 调用

// ❌ 一次性加载所有数据
const allHistory = await historyApi.getList();
// 数据量大时卡顿

// ❌ 图片不懒加载
<img src={image.url} />
// 大量图片同时加载
```

---

## 📋 任务分配

### 模块 7：配图生成

| 任务 | 负责人 | 预计时间 | 交付物 |
|------|--------|----------|--------|
| 后端：Images API | 后端虾 | 2 小时 | `app/api/images.py` |
| 后端：图片生成服务 | 后端虾 | 1 小时 | `app/ai/image.py` |
| 前端：配图生成页 | 前端虾 | 2 小时 | `pages/ImageGen.jsx` |
| 前端：图片展示组件 | 前端虾 | 1 小时 | `components/ImageGallery.jsx` |
| 联调测试 | 测试虾 | 1 小时 | 测试报告 |

**小计：** 7 小时（1 天）

---

### 模块 8：历史记录

| 任务 | 负责人 | 预计时间 | 交付物 |
|------|--------|----------|--------|
| 后端：History API | 后端虾 | 2 小时 | `app/api/history.py` |
| 后端：数据库查询优化 | 后端虾 | 1 小时 | 索引优化 |
| 前端：历史列表页 | 前端虾 | 2 小时 | `pages/History.jsx` |
| 前端：搜索/筛选组件 | 前端虾 | 1 小时 | `components/HistoryFilter.jsx` |
| 联调测试 | 测试虾 | 1 小时 | 测试报告 |

**小计：** 7 小时（1 天）

---

## 📅 时间节点

| 里程碑 | 时间 | 负责人 |
|--------|------|--------|
| 模块 7 后端完成 | 今天 18:00 | 后端虾 |
| 模块 7 前端完成 | 今天 20:00 | 前端虾 |
| 模块 7 联调完成 | 今天 21:00 | 测试虾 |
| 模块 8 后端完成 | 明天 12:00 | 后端虾 |
| 模块 8 前端完成 | 明天 18:00 | 前端虾 |
| 模块 8 联调完成 | 明天 20:00 | 测试虾 |
| **MVP 演示** | **3.20 15:00** | **全体** |

---

## 🎯 质量要求

### 代码质量

- ✅ 所有 API 必须有完整文档字符串
- ✅ 所有函数必须有类型注解
- ✅ 所有错误必须处理并记录日志
- ✅ 所有数据库操作必须使用参数化查询
- ✅ 所有前端组件必须使用 Ant Design

### 测试覆盖

- ✅ 所有 API 接口必须测试
- ✅ 所有错误路径必须测试
- ✅ 前后端联调必须测试
- ✅ 边界条件必须测试

### 文档完整

- ✅ API 接口必须有 Swagger 文档
- ✅ 新功能必须更新 README
- ✅ 数据库变更必须更新 schema.sql
- ✅ 配置文件必须更新 .env.example

---

## 💡 开发建议

### 后端建议

1. **先写 API 文档** - 使用 Swagger 定义接口
2. **再实现业务逻辑** - 按照文档开发
3. **最后写单元测试** - 保证代码质量
4. **及时提交代码** - 每个功能完成后 commit

### 前端建议

1. **先设计组件结构** - 画出组件树
2. **再实现页面框架** - 搭建路由和布局
3. **然后填充功能** - 调用 API 实现业务
4. **最后优化体验** - Loading、错误处理

### 测试建议

1. **先写测试用例** - 明确测试范围
2. **再执行自动化测试** - 使用 pytest
3. **然后手动测试** - 验证用户体验
4. **最后写测试报告** - 记录测试结果

---

## 📝 沟通机制

### 每日站会

- **时间：** 每天 9:00、18:00
- **形式：** 飞书群视频
- **内容：** 进度同步、问题反馈

### 代码审查

- **时间：** 每次提交前
- **形式：** GitHub Pull Request
- **要求：** 至少 1 人 review

### 问题反馈

- **渠道：** 飞书群或私聊
- **响应：** 30 分钟内
- **升级：** 2 小时未解决找项目经理

---

## 🎉 激励措施

### 提前完成奖励

- **提前 1 天：** 下午茶 + 咖啡券
- **提前 2 天：** 团队聚餐
- **提前 3 天：** 额外半天假期

### 质量奖励

- **0 Bug：** 代码质量奖（红包）
- **最佳设计：** 架构设计奖（书籍）
- **最佳测试：** 测试达人奖（周边）

---

## 📋 会议总结

### 关键信息

1. **模块 7-8 开发周期：** 2 天（今天 + 明天）
2. **MVP 演示时间：** 3 月 20 日 15:00
3. **质量要求：** 0 严重 Bug，API 100% 测试
4. **沟通机制：** 每日站会 + 代码审查

### 下一步行动

1. **后端虾：** 开始模块 7 后端开发
2. **前端虾：** 等待前端服务启动后开始模块 7 前端
3. **测试虾：** 准备测试用例和测试数据
4. **项目经理：** 跟踪进度，协调资源

---

**会议结束！** 🦐

**大家加油，确保模块 7-8 高质量完成！** 💪
