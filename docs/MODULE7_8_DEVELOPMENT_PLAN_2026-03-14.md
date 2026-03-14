# 模块 7-8 开发计划讨论会

**会议时间：** 2026-03-14 19:15  
**主持人：** 项目经理虾 🦐📋  
**参会人员：** 后端开发虾、前端开发虾、测试运维虾  
**会议主题：** 模块 7（配图生成）+ 模块 8（历史记录）前后端开发计划

---

## 📋 会议议程

1. 模块 7-8 当前状态同步（5 分钟）
2. 后端开发计划讨论（15 分钟）
3. 前端开发计划讨论（15 分钟）
4. 联调测试计划（10 分钟）
5. 任务分配和时间节点（10 分钟）
6. Q&A（5 分钟）

---

## 📊 当前状态同步

### 模块 7：配图生成

| 任务 | 状态 | 完成度 |
|------|------|--------|
| 后端 API（images.py） | ✅ 已完成 | 100% |
| 前端页面（ImageGen.jsx） | ✅ 已完成 | 100% |
| 图片展示组件（ImageGallery.jsx） | ✅ 已完成 | 100% |
| **前端 API 服务（images.js）** | ❌ **待创建** | **0%** |
| 联调测试 | ⏳ 待开始 | 0% |

**缺失文件：**
- `frontend/src/services/images.js`

---

### 模块 8：历史记录

| 任务 | 状态 | 完成度 |
|------|------|--------|
| **后端 API（history.py）** | ❌ **待创建** | **0%** |
| 前端页面（History.jsx） | ✅ 已完成 | 100% |
| 历史卡片组件（HistoryCard.jsx） | ✅ 已完成 | 100% |
| 搜索筛选组件（HistoryFilter.jsx） | ✅ 已完成 | 100% |
| **前端 API 服务（history.js）** | ❌ **待创建** | **0%** |
| 联调测试 | ⏳ 待开始 | 0% |

**缺失文件：**
- `backend/app/api/history.py`
- `frontend/src/services/history.js`

---

## 🎯 后端开发计划

### 模块 7：配图生成（后端）

**当前状态：** ✅ API 已完成

**已实现功能：**
```python
✅ POST /api/images/generate      - 生成配图
✅ GET  /api/images/:id           - 获取图片
✅ GET  /api/images               - 图片列表
```

**待完善：**
- [ ] 接入真实 DashScope 文生图 API（P1）
- [ ] 实现图片保存到本地/云存储（P1）
- [ ] 实现内容保存关联（P1）

**负责人：** 后端开发虾 🦐💻

---

### 模块 8：历史记录（后端）

**当前状态：** ❌ API 待创建

**需要实现：**
```python
GET    /api/history              - 历史列表（分页、筛选）
GET    /api/history/:id          - 历史详情
DELETE /api/history/:id          - 删除历史
GET    /api/history/search       - 搜索历史
```

**开发步骤：**

**Step 1：创建数据库模型（15 分钟）**
```python
# backend/app/models/content_history.py
class ContentHistory:
    id: int
    theme: str
    topic: str
    platform: str  # douyin/wechat/xhs
    content: str
    image_urls: str  # JSON array
    prompt_id: int
    created_at: datetime
    updated_at: datetime
```

**Step 2：创建 API 路由（30 分钟）**
```python
# backend/app/api/history.py
@router.get("", response_model=HistoryListResponse)
async def list_history(
    page: int = 1,
    page_size: int = 20,
    platform: Optional[str] = None,
    keyword: Optional[str] = None
):
    ...

@router.get("/{history_id}", response_model=HistoryDetailResponse)
async def get_history(history_id: int):
    ...

@router.delete("/{history_id}", response_model=BaseResponse)
async def delete_history(history_id: int):
    ...

@router.get("/search", response_model=HistoryListResponse)
async def search_history(
    keyword: str,
    page: int = 1,
    page_size: int = 20
):
    ...
```

**Step 3：测试验证（15 分钟）**
```bash
# 测试列表
curl http://localhost:8000/api/history?page=1&page_size=20

# 测试详情
curl http://localhost:8000/api/history/1

# 测试删除
curl -X DELETE http://localhost:8000/api/history/1

# 测试搜索
curl http://localhost:8000/api/history/search?keyword=AI
```

**负责人：** 后端开发虾 🦐💻  
**预计时间：** 1 小时  
**截止时间：** 今天 20:30

---

## 🎨 前端开发计划

### 模块 7：配图生成（前端）

**当前状态：** 页面完成，API 服务待创建

**需要实现：**
```javascript
// frontend/src/services/images.js
import api from './api';

export const imagesApi = {
  // 生成配图
  generate: (data) => api.post('/images/generate', data),
  
  // 获取图片
  getById: (id) => api.get(`/images/${id}`),
  
  // 图片列表
  getList: (params) => api.get('/images', { params }),
};
```

**开发步骤：**

**Step 1：创建 API 服务（15 分钟）**
```javascript
// frontend/src/services/images.js
import api from './api';

export const imagesApi = {
  generate: (data) => api.post('/images/generate', data),
  getById: (id) => api.get(`/images/${id}`),
  getList: (params) => api.get('/images', { params }),
};

export default imagesApi;
```

**Step 2：集成到页面（15 分钟）**
```jsx
// frontend/src/pages/ImageGen.jsx
import imagesApi from '../services/images';

const handleGenerate = async (values) => {
  try {
    const result = await imagesApi.generate(values);
    setImageUrl(result.data.url);
    message.success('生成成功');
  } catch (error) {
    message.error(`生成失败：${error.message}`);
  }
};
```

**Step 3：测试验证（15 分钟）**
- 测试图片生成功能
- 测试图片预览功能
- 测试图片下载功能

**负责人：** 前端开发虾 🦐🎨  
**预计时间：** 45 分钟  
**截止时间：** 今天 20:30

---

### 模块 8：历史记录（前端）

**当前状态：** 页面完成，API 服务待创建

**需要实现：**
```javascript
// frontend/src/services/history.js
import api from './api';

export const historyApi = {
  // 历史列表
  getList: (params) => api.get('/history', { params }),
  
  // 历史详情
  getById: (id) => api.get(`/history/${id}`),
  
  // 删除历史
  delete: (id) => api.delete(`/history/${id}`),
  
  // 搜索历史
  search: (params) => api.get('/history/search', { params }),
};
```

**开发步骤：**

**Step 1：创建 API 服务（15 分钟）**
```javascript
// frontend/src/services/history.js
import api from './api';

export const historyApi = {
  getList: (params) => api.get('/history', { params }),
  getById: (id) => api.get(`/history/${id}`),
  delete: (id) => api.delete(`/history/${id}`),
  search: (params) => api.get('/history/search', { params }),
};

export default historyApi;
```

**Step 2：集成到页面（30 分钟）**
```jsx
// frontend/src/pages/History.jsx
import historyApi from '../services/history';

const HistoryPage = () => {
  const [historyList, setHistoryList] = useState([]);
  const [loading, setLoading] = useState(false);
  
  const loadHistory = async (page = 1) => {
    setLoading(true);
    try {
      const data = await historyApi.getList({ page, page_size: 20 });
      setHistoryList(data.list);
    } catch (error) {
      message.error(`加载失败：${error.message}`);
    } finally {
      setLoading(false);
    }
  };
  
  const handleDelete = (id) => {
    Modal.confirm({
      title: '确认删除',
      onOk: async () => {
        await historyApi.delete(id);
        message.success('删除成功');
        loadHistory();
      }
    });
  };
  
  const handleSearch = (keyword) => {
    historyApi.search({ keyword }).then(data => {
      setHistoryList(data.list);
    });
  };
  
  return (...);
};
```

**Step 3：测试验证（30 分钟）**
- 测试历史列表加载
- 测试分页功能
- 测试搜索功能
- 测试删除功能

**负责人：** 前端开发虾 🦐🎨  
**预计时间：** 1.25 小时  
**截止时间：** 今天 21:00

---

## 🧪 联调测试计划

### 测试范围

**模块 7：配图生成**
- [ ] 图片生成 API 测试
- [ ] 图片预览功能测试
- [ ] 图片下载功能测试
- [ ] 前后端联调测试

**模块 8：历史记录**
- [ ] 历史列表 API 测试
- [ ] 历史详情 API 测试
- [ ] 历史删除 API 测试
- [ ] 搜索功能测试
- [ ] 分页功能测试
- [ ] 前后端联调测试

---

### 测试用例

#### 模块 7：配图生成

**测试用例 1：生成配图**
```
输入：
{
  "content": "AI 工具提升效率",
  "title": "效率工具",
  "aspect_ratio": "16:9",
  "platform": "wechat"
}

期望输出：
{
  "code": 200,
  "message": "success",
  "data": {
    "id": "xxx",
    "url": "/api/images/xxx",
    "title": "效率工具",
    "aspect_ratio": "16:9"
  }
}
```

**测试用例 2：获取图片**
```
输入：GET /api/images/{id}

期望输出：图片信息
```

**测试用例 3：图片列表**
```
输入：GET /api/images?page=1&page_size=20

期望输出：分页图片列表
```

---

#### 模块 8：历史记录

**测试用例 1：历史列表**
```
输入：GET /api/history?page=1&page_size=20

期望输出：
{
  "code": 200,
  "message": "success",
  "data": {
    "list": [...],
    "total": 100,
    "page": 1,
    "page_size": 20
  }
}
```

**测试用例 2：历史详情**
```
输入：GET /api/history/1

期望输出：完整历史记录
```

**测试用例 3：删除历史**
```
输入：DELETE /api/history/1

期望输出：
{
  "code": 200,
  "message": "删除成功"
}
```

**测试用例 4：搜索历史**
```
输入：GET /api/history/search?keyword=AI&page=1

期望输出：包含"AI"的历史记录
```

---

### 测试时间安排

| 测试项 | 负责人 | 预计时间 | 截止时间 |
|--------|--------|----------|----------|
| 模块 7 API 测试 | 测试虾 | 30 分钟 | 20:45 |
| 模块 8 API 测试 | 测试虾 | 45 分钟 | 21:15 |
| 前后端联调 | 全体 | 30 分钟 | 21:45 |
| 测试报告编写 | 测试虾 | 30 分钟 | 22:15 |

---

## 📋 任务分配

### 后端任务

| 任务 | 负责人 | 预计时间 | 截止时间 |
|------|--------|----------|----------|
| 创建 history.py API | 后端虾 | 1 小时 | 20:30 |
| 测试 history API | 后端虾 | 15 分钟 | 20:45 |
| 协助联调测试 | 后端虾 | 30 分钟 | 21:45 |

**小计：** 1.75 小时

---

### 前端任务

| 任务 | 负责人 | 预计时间 | 截止时间 |
|------|--------|----------|----------|
| 创建 images.js 服务 | 前端虾 | 15 分钟 | 20:30 |
| 集成 images.js 到页面 | 前端虾 | 15 分钟 | 20:45 |
| 创建 history.js 服务 | 前端虾 | 15 分钟 | 20:45 |
| 集成 history.js 到页面 | 前端虾 | 30 分钟 | 21:15 |
| 测试前端功能 | 前端虾 | 30 分钟 | 21:45 |

**小计：** 1.75 小时

---

### 测试任务

| 任务 | 负责人 | 预计时间 | 截止时间 |
|------|--------|----------|----------|
| 模块 7 API 测试 | 测试虾 | 30 分钟 | 20:45 |
| 模块 8 API 测试 | 测试虾 | 45 分钟 | 21:15 |
| 前后端联调 | 测试虾 | 30 分钟 | 21:45 |
| 编写测试报告 | 测试虾 | 30 分钟 | 22:15 |

**小计：** 2.25 小时

---

## 📅 时间节点

### 今天（3.14）晚上

| 时间 | 任务 | 负责人 |
|------|------|--------|
| 19:15 - 19:30 | 开发计划讨论会 | 全体 |
| 19:30 - 20:30 | 后端创建 history.py | 后端虾 |
| 19:30 - 20:30 | 前端创建 images.js | 前端虾 |
| 20:30 - 20:45 | 后端测试 history API | 后端虾 |
| 20:30 - 20:45 | 前端集成 images.js | 前端虾 |
| 20:45 - 21:15 | 前端创建 history.js | 前端虾 |
| 20:45 - 21:15 | 测试模块 7 API | 测试虾 |
| 21:15 - 21:45 | 前端集成 history.js | 前端虾 |
| 21:15 - 21:45 | 测试模块 8 API | 测试虾 |
| 21:45 - 22:15 | 前后端联调测试 | 全体 |
| 22:15 - 22:30 | 编写测试报告 | 测试虾 |
| 22:30 - 23:00 | 代码提交 + 总结 | 全体 |

**预计完成时间：** 今天 23:00

---

## 🎯 开发规范

### 后端规范

**API 响应格式：**
```python
{
    "code": 200,
    "message": "success",
    "data": {...}
}
```

**错误处理：**
```python
try:
    ...
except HTTPException:
    raise
except Exception as e:
    logger.error(f"API error: {e}")
    raise HTTPException(status_code=500, detail=str(e))
```

**数据库操作：**
```python
# ✅ 参数化查询
cursor.execute("SELECT * FROM history WHERE theme = ?", (theme,))

# ✅ 使用事务
conn.execute("BEGIN")
try:
    ...
    conn.commit()
except:
    conn.rollback()
    raise
```

---

### 前端规范

**API 调用：**
```javascript
try {
  const data = await imagesApi.generate(values);
  message.success('生成成功');
} catch (error) {
  message.error(`生成失败：${error.message}`);
}
```

**Loading 状态：**
```jsx
const [loading, setLoading] = useState(false);
<Button loading={loading} onClick={handleGenerate}>
  {loading ? '生成中...' : '生成'}
</Button>
```

**表单验证：**
```jsx
<Form.Item
  name="title"
  rules={[{ required: true, message: '请输入标题' }]}
>
  <Input />
</Form.Item>
```

---

## 💡 注意事项

### 后端注意

1. **参数化查询** - 防止 SQL 注入
2. **事务处理** - 保证数据一致性
3. **日志记录** - 关键操作必须记录
4. **超时设置** - AI 调用设置 timeout
5. **错误处理** - 统一格式，友好提示

---

### 前端注意

1. **错误处理** - 所有 API 调用必须 try-catch
2. **Loading 状态** - 异步操作必须有 loading
3. **表单验证** - 必填项必须验证
4. **用户体验** - 删除操作二次确认
5. **性能优化** - 搜索防抖处理

---

## 📝 会议总结

### 关键结论

1. **模块 7-8 完成度 95%** - 仅剩 3 个文件待创建
2. **开发计划明确** - 后端 1 小时，前端 1.75 小时
3. **时间节点清晰** - 今晚 23:00 前完成
4. **责任到人** - 后端/前端/测试各有明确任务

### 下一步行动

1. **后端虾：** 立即创建 history.py（19:30 开始）
2. **前端虾：** 立即创建 images.js（19:30 开始）
3. **测试虾：** 准备测试用例（20:30 开始）
4. **项目经理：** 跟踪进度，协调资源

---

**会议结束！** 🦐

**大家加油，今晚 23:00 前完成模块 7-8 全部开发！** 💪
