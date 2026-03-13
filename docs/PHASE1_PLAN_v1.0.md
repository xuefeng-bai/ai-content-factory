# 📅 AI 内容工厂 v1.0.0 - Phase 1 细化开发计划

**文档版本：** v1.0.0  
**创建日期：** 2026-03-12  
**文档作者：** 虾虾（项目经理）🦐📋  
**阶段目标：** 完成 MVP 核心功能开发  
**时间周期：** 2026-03-13 ~ 2026-03-20（8 天）

---

## 📋 Phase 1 目标

**核心功能：**
- ✅ AI 联网搜索（微博 + 知乎）
- ✅ 选题推荐（3-5 个）
- ✅ 内容生成（抖音 + 公众号 + 小红书）
- ✅ 配图生成（最多 3 张）
- ✅ 历史管理

**交付物：** 可演示 MVP 版本

---

## 📊 每日开发计划

### 第 1 天（3.13 周五）：爬虫开发

#### 任务清单

| 任务 | 负责人 | 优先级 | 预计工时 | 交付物 |
|------|--------|--------|---------|--------|
| 微博热搜爬虫开发 | 后端开发虾 | P0 | 4h | `weibo.py` |
| 知乎热榜爬虫开发 | 后端开发虾 | P0 | 3h | `zhihu.py` |
| 爬虫测试（Windows） | 测试运维虾 | P0 | 2h | 测试报告 |
| 爬虫测试（Linux） | 测试运维虾 | P0 | 2h | 测试报告 |

#### 详细要求

**微博热搜爬虫：**
```python
# 文件：backend/app/crawler/weibo.py
# 目标 URL：https://s.weibo.com/top/summary
# 返回格式：List[Dict]
# 字段：rank, title, hot_value, url, is_new, is_hot

# 反爬对策：
# 1. User-Agent 轮换（至少 5 个）
# 2. 请求间隔：3 秒
# 3. 超时设置：10 秒
# 4. 错误重试：3 次
```

**知乎热榜爬虫：**
```python
# 文件：backend/app/crawler/zhihu.py
# 目标 URL：https://www.zhihu.com/hot
# 返回格式：List[Dict]
# 字段：rank, title, hot_value, url, answer_count

# 反爬对策：
# 1. Cookie 管理（手动登录获取）
# 2. 请求间隔：5 秒
# 3. 超时设置：10 秒
```

#### 验收标准

- [ ] 微博热搜能正常爬取 Top50
- [ ] 知乎热榜能正常爬取 Top50
- [ ] Windows 环境测试通过
- [ ] Linux 环境测试通过
- [ ] 成功率 > 90%

---

### 第 2 天（3.14 周六）：爬虫优化 + AI 集成准备

#### 任务清单

| 任务 | 负责人 | 优先级 | 预计工时 | 交付物 |
|------|--------|--------|---------|--------|
| 爬虫反爬优化 | 后端开发虾 | P0 | 3h | 优化代码 |
| 数据清洗和格式化 | 后端开发虾 | P0 | 3h | 格式化模块 |
| DashScope SDK 集成 | 后端开发虾 | P0 | 2h | SDK 集成代码 |
| API Key 配置测试 | 测试运维虾 | P0 | 1h | 配置文档 |

#### 详细要求

**数据格式化：**
```python
# 文件：backend/app/crawler/formatter.py
# 统一返回格式：
{
    "source": "weibo" | "zhihu",
    "rank": int,
    "title": str,
    "hot_value": str | int,
    "url": str,
    "extra": Dict  # 额外信息
}
```

**DashScope 集成：**
```python
# 文件：backend/app/ai/client.py
# 初始化：
from dashscope import Generation

# 配置 API Key：
import dashscope
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
```

#### 验收标准

- [ ] 爬虫稳定性 > 90%
- [ ] 数据格式统一（JSON）
- [ ] DashScope SDK 集成完成
- [ ] API Key 配置正确

---

### 第 3 天（3.15 周日）：AI 集成（搜索 + 选题）

#### 任务清单

| 任务 | 负责人 | 优先级 | 预计工时 | 交付物 |
|------|--------|--------|---------|--------|
| AI 搜索集成 | 后端开发虾 | P0 | 4h | `search.py` |
| 选题推荐 Prompt 开发 | 后端开发虾 | P0 | 3h | Prompt 模板 |
| 选题推荐测试 | 测试运维虾 | P0 | 2h | 测试报告 |

#### 详细要求

**AI 搜索集成：**
```python
# 文件：backend/app/ai/search.py
# 功能：聚合微博 + 知乎数据，调用 AI 分析热点

# 输入：
{
    "weibo": List[Dict],
    "zhihu": List[Dict]
}

# 输出：
{
    "summary": str,  # 热点总结
    "keywords": List[str],  # 关键词
    "trends": List[str]  # 趋势分析
}
```

**选题推荐 Prompt：**
```python
# 文件：backend/app/ai/prompts/topic_recommend.py

PROMPT = """
你是专业的内容策划专家。请根据以下搜索素材，推荐 3-5 个选题角度。

搜索素材：
{search_results}

请按以下 JSON 格式输出：
{{
    "topics": [
        {{
            "title": "选题标题",
            "type": "工具推荐 | 认知差 | 案例分享 | 观点输出",
            "advantage": "优势说明",
            "recommend_level": 1-5
        }}
    ]
}}

要求：
1. 选题要有吸引力
2. 类型要多样化
3. 优势要具体
"""
```

#### 验收标准

- [ ] AI 搜索能正常调用
- [ ] 能生成 3-5 个选题
- [ ] 选题质量可用（>80%）
- [ ] JSON 格式解析正确

---

### 第 4 天（3.16 周一）：AI 集成（内容生成）

#### 任务清单

| 任务 | 负责人 | 优先级 | 预计工时 | 交付物 |
|------|--------|--------|---------|--------|
| 抖音口播文案 Prompt | 后端开发虾 | P0 | 3h | Prompt 模板 |
| 公众号文章 Prompt | 后端开发虾 | P0 | 3h | Prompt 模板 |
| 小红书笔记 Prompt | 后端开发虾 | P0 | 3h | Prompt 模板 |
| 内容生成测试 | 测试运维虾 | P0 | 2h | 测试报告 |

#### 详细要求

**抖音口播 Prompt：**
```python
# 文件：backend/app/ai/prompts/douyin_script.py

PROMPT = """
你是专业的短视频口播文案创作者。

要求：
1. 口语化表达，适合朗读
2. 开头要有钩子（前 3 秒吸引注意力）
3. 结尾要有金句（引发传播）
4. 字数：500-600 字（约 60 秒口播）
5. 段落清晰，每段不超过 3 句

主题：{topic}
目标受众：{target_audience}
内容风格：{content_style}
"""
```

**公众号文章 Prompt：**
```python
# 文件：backend/app/ai/prompts/wechat_article.py

PROMPT = """
你是资深新媒体编辑。

要求：
1. 结构清晰，使用 Markdown 格式
2. 包含 H1/H2/H3 标题
3. 字数：2000 字左右
4. 标注配图位置：![配图](url)
5. 有引言、正文、总结

主题：{topic}
文章类型：{article_type}
"""
```

**小红书笔记 Prompt：**
```python
# 文件：backend/app/ai/prompts/xiaohongshu_note.py

PROMPT = """
你是小红书爆款内容创作者。

要求：
1. 标题吸引眼球，带 emoji（最多 20 字）
2. 正文种草风格，分段清晰
3. 带 emoji（每段 1-2 个）
4. 带话题标签（3-5 个）
5. 字数：300-500 字

主题：{topic}
内容类型：{content_type}
目标人群：{target_audience}
"""
```

#### 验收标准

- [ ] 抖音文案：口语化，500-600 字
- [ ] 公众号文章：Markdown 格式，2000 字
- [ ] 小红书笔记：带 emoji 和标签
- [ ] 内容质量可用（>80%）

---

### 第 5 天（3.17 周二）：AI 集成（配图生成）

#### 任务清单

| 任务 | 负责人 | 优先级 | 预计工时 | 交付物 |
|------|--------|--------|---------|--------|
| 配图生成 Prompt 开发 | 后端开发虾 | P0 | 3h | Prompt 模板 |
| 公众号配图（16:9） | 后端开发虾 | P0 | 2h | 测试图片 |
| 小红书封面（3:4） | 后端开发虾 | P0 | 2h | 测试图片 |
| 配图生成测试 | 测试运维虾 | P0 | 2h | 测试报告 |

#### 详细要求

**配图生成 Prompt：**
```python
# 文件：backend/app/ai/prompts/image_generation.py

# 公众号配图（16:9 横版）
WECHAT_PROMPT = """
科技感，商务风格，AI 人工智能主题，蓝色调，简洁大气，16:9 横版
关键词：{keywords}
"""

# 小红书封面（3:4 竖版）
XIAOHONGSHU_PROMPT = """
小红书爆款风格，大字报，醒目文字，橙色调，吸引眼球，3:4 竖版
标题文字：{title}
"""
```

**图片生成服务：**
```python
# 文件：backend/app/ai/image.py
from dashscope import ImageSynthesis

# 生成图片
response = ImageSynthesis.call(
    prompt=prompt,
    n=1,
    size="1024*1024"  # 或"1024*768"等
)
```

#### 验收标准

- [ ] 公众号配图：16:9 比例，质量合格
- [ ] 小红书封面：3:4 比例，带文字
- [ ] 图片生成时间 < 10 秒/张
- [ ] 图片质量可用（>80%）

---

### 第 6 天（3.18 周三）：后端 API 开发

#### 任务清单

| 任务 | 负责人 | 优先级 | 预计工时 | 交付物 |
|------|--------|--------|---------|--------|
| 搜索 API | 后端开发虾 | P0 | 3h | `/api/search` |
| 选题 API | 后端开发虾 | P0 | 3h | `/api/topics/recommend` |
| 内容生成 API | 后端开发虾 | P0 | 4h | `/api/content/generate` |
| 历史 API | 后端开发虾 | P0 | 2h | `/api/history` |
| API 文档（Swagger） | 后端开发虾 | P1 | 2h | Swagger UI |

#### 详细要求

**搜索 API：**
```python
# 文件：backend/app/api/search.py
@router.post("/search")
async def search(request: SearchRequest):
    """
    AI 联网搜索
    
    请求：
    - theme: 搜索主题
    
    响应：
    - search_id: 搜索记录 ID
    - weibo_hot_search: 微博热搜列表
    - zhihu_hot_list: 知乎热榜列表
    """
```

**选题 API：**
```python
# 文件：backend/app/api/topics.py
@router.post("/topics/recommend")
async def recommend_topics(request: TopicRecommendRequest):
    """
    推荐选题
    
    请求：
    - search_id: 搜索记录 ID（可选）
    - search_results: 搜索结果（可选）
    
    响应：
    - topics: 选题列表（3-5 个）
    """
```

**内容生成 API：**
```python
# 文件：backend/app/api/content.py
@router.post("/content/generate")
async def generate_content(request: ContentGenerateRequest):
    """
    生成内容
    
    请求：
    - topic: 选题
    - platform: 平台（douyin/wechat/xiaohongshu）
    - template_config: 模板配置
    - generate_images: 是否生成配图
    - image_count: 配图数量（1-3）
    
    响应：
    - content_id: 内容记录 ID
    - content: 生成内容
    - images: 配图列表
    - word_count: 字数统计
    """
```

**历史 API：**
```python
# 文件：backend/app/api/history.py
@router.get("/history")
async def get_history(
    page: int = 1,
    page_size: int = 20,
    theme: str = None,
    platform: str = None
):
    """
    获取历史列表
    
    响应：
    - total: 总数
    - page: 页码
    - page_size: 每页数量
    - items: 历史列表
    """

@router.get("/history/{id}")
async def get_history_detail(id: int):
    """
    获取历史详情
    
    响应：
    - 完整内容记录
    """
```

#### 验收标准

- [ ] 所有 API 能正常调用
- [ ] API 响应时间 < 2 秒
- [ ] Swagger 文档完整
- [ ] 错误处理完善

---

### 第 7 天（3.19 周四）：前端开发

#### 任务清单

| 任务 | 负责人 | 优先级 | 预计工时 | 交付物 |
|------|--------|--------|---------|--------|
| 首页（模板选择 + 主题输入） | 前端开发虾 | P0 | 4h | `Home.jsx` |
| 搜索结果页（热点 + 选题） | 前端开发虾 | P0 | 4h | `Search.jsx` |
| 内容预览页（三平台内容） | 前端开发虾 | P0 | 4h | `Preview.jsx` |
| 历史列表页 | 前端开发虾 | P0 | 2h | `History.jsx` |
| 前端测试 | 测试运维虾 | P0 | 2h | 测试报告 |

#### 详细要求

**首页：**
```jsx
// 文件：frontend/src/pages/Home.jsx
// 功能：
// 1. 模板选择（3 套预设模板）
// 2. 主题输入框
// 3. 【开始创作】按钮

// 状态管理（Zustand）：
const useStore = create((set) => ({
  selectedTemplate: null,
  theme: '',
  setTemplate: (template) => set({ selectedTemplate: template }),
  setTheme: (theme) => set({ theme }),
}))
```

**搜索结果页：**
```jsx
// 文件：frontend/src/pages/Search.jsx
// 功能：
// 1. 显示微博热搜 Top10
// 2. 显示知乎热榜 Top10
// 3. 显示 AI 推荐的 3-5 个选题
// 4. 【选择此选题】按钮
```

**内容预览页：**
```jsx
// 文件：frontend/src/pages/Preview.jsx
// 功能：
// 1. 标签页切换（抖音 | 公众号 | 小红书）
// 2. 显示生成内容
// 3. 显示配图（缩略图）
// 4. 【复制】按钮
// 5. 【下载】按钮
```

**历史列表页：**
```jsx
// 文件：frontend/src/pages/History.jsx
// 功能：
// 1. 历史列表（分页）
// 2. 搜索框（按主题搜索）
// 3. 筛选（按平台筛选）
// 4. 【查看】按钮
```

#### 验收标准

- [ ] 页面能正常访问
- [ ] 交互流畅
- [ ] UI 美观（Ant Design）
- [ ] 无控制台错误

---

### 第 8 天（3.20 周五）：集成测试 + MVP 演示

#### 任务清单

| 任务 | 负责人 | 优先级 | 预计工时 | 交付物 |
|------|--------|--------|---------|--------|
| 前后端集成测试 | 测试运维虾 | P0 | 4h | 测试报告 |
| Bug 修复 | 全体 | P0 | 3h | Bug 清单 |
| MVP 演示准备 | 项目经理虾 | P0 | 2h | 演示脚本 |
| MVP 演示 | 全体 | P0 | 2h | 演示视频 |

#### 详细要求

**集成测试用例：**
```markdown
# P0 测试用例（必须 100% 通过）

## TC-001: 完整流程测试
1. 打开首页
2. 选择模板"AI 干货型"
3. 输入主题"AI 效率工具"
4. 点击【开始创作】
5. 验证：能正常搜索微博/知乎
6. 验证：能生成 3-5 个选题
7. 选择选题 1
8. 验证：能生成三平台内容
9. 验证：能生成配图
10. 验证：能保存到历史
11. 验证：能查看历史

## TC-002: 跨平台测试
1. Windows 环境测试
2. Linux 环境测试
3. 验证：都能正常运行

## TC-003: 异常处理测试
1. 搜索失败（模拟网络错误）
2. 验证：有友好错误提示
3. AI 生成失败（模拟 API 错误）
4. 验证：有友好错误提示
```

#### 验收标准

- [ ] 所有 P0 用例通过（100%）
- [ ] 严重 Bug 为 0
- [ ] 一般 Bug < 5 个
- [ ] MVP 演示成功

---

## ⚠️ 研发注意事项

### 1. 跨平台适配（❗❗❗ 最重要）

**文件路径处理：**
```python
# ✅ 正确：使用 pathlib
from pathlib import Path
db_path = Path(__file__).parent / "data" / "daily_brief.db"

# ❌ 错误：硬编码路径
db_path = "/home/admin/data/daily_brief.db"  # Linux
db_path = "C:\\Users\\admin\\data\\daily_brief.db"  # Windows
```

**文件编码：**
```python
# ✅ 正确：明确指定 UTF-8
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()

# ❌ 错误：使用默认编码
with open("file.txt", "r") as f:  # Windows 默认 GBK
    content = f.read()
```

**命令行调用：**
```python
# ✅ 正确：使用 sys.executable
import sys
subprocess.run([sys.executable, "script.py"])

# ❌ 错误：指定版本
subprocess.run(["python3", "script.py"])  # Windows 无 python3
```

**配置文件：**
```txt
# ✅ 正确：英文注释
# FastAPI Framework
fastapi==0.109

# ❌ 错误：中文注释
# FastAPI 框架  # Windows 安装会报错
fastapi==0.109
```

---

### 2. 代码质量

**命名规范：**
```python
# ✅ 正确：snake_case for 变量/函数
def get_user_info():
    pass

# ✅ 正确：PascalCase for 类
class UserService:
    pass

# ✅ 正确：UPPER_CASE for 常量
MAX_IMAGE_COUNT = 3
```

**注释规范：**
```python
# ✅ 正确：英文注释（公共代码）
# Get user info
def get_user_info():
    pass

# ❌ 错误：中文注释（配置文件/公共代码）
# 获取用户信息
def get_user_info():
    pass
```

**错误处理：**
```python
# ✅ 正确：完整的错误处理
try:
    result = await api_call()
except APIError as e:
    logger.error(f"API error: {e}")
    raise HTTPException(status_code=500, detail="API error")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise HTTPException(status_code=500, detail="Server error")
```

---

### 3. 性能优化

**数据库查询：**
```python
# ✅ 正确：使用索引
# 添加索引：idx_theme, idx_created_at
results = db.query(ContentHistory).filter(
    ContentHistory.theme.like(f"%{theme}%")
).all()

# ❌ 错误：全表扫描
results = db.query(ContentHistory).all()
```

**API 响应时间：**
```python
# ✅ 正确：异步处理
@app.post("/content/generate")
async def generate_content(request: ContentGenerateRequest):
    content = await ai_service.generate(request)
    return content

# ❌ 错误：同步阻塞
@app.post("/content/generate")
def generate_content(request: ContentGenerateRequest):
    content = ai_service.generate(request)  # 阻塞
    return content
```

---

### 4. 安全注意事项

**API Key 管理：**
```python
# ✅ 正确：从环境变量读取
api_key = os.getenv("DASHSCOPE_API_KEY")

# ❌ 错误：硬编码
api_key = "sk-sp-xxxxx"  # 禁止提交到 Git
```

**SQL 注入防护：**
```python
# ✅ 正确：使用 ORM
results = db.query(ContentHistory).filter(
    ContentHistory.theme == theme
).all()

# ❌ 错误：字符串拼接 SQL
sql = f"SELECT * FROM content_history WHERE theme = '{theme}'"
```

**XSS 防护：**
```python
# ✅ 正确：前端转义
from markupsafe import escape
safe_content = escape(user_content)
```

---

### 5. 日志记录

**日志级别：**
```python
logger.debug("Debug info")  # 调试
logger.info("Request received")  # 正常
logger.warning("High latency")  # 警告
logger.error("API error")  # 错误
logger.critical("System crash")  # 严重
```

**日志格式：**
```python
# ✅ 正确：包含关键信息
logger.info(f"Request: {method} {path} - {status_code} - {duration}ms")

# ❌ 错误：信息不完整
logger.info("Request received")
```

---

## 📞 沟通机制

### 日常沟通

| 时间 | 内容 | 参与人 |
|------|------|--------|
| 每天 9:00 | 站会（进度同步） | 全体 |
| 每天 18:00 | 日报（进度汇报） | 全体 |

### 问题上报

| 问题级别 | 上报方式 | 响应时间 |
|---------|---------|---------|
| P0（严重 Bug） | 立即上报 | 30 分钟内 |
| P1（一般 Bug） | 日报上报 | 24 小时内 |
| P2（优化建议） | 周会上报 | 1 周内 |

---

## 📊 进度跟踪

### 燃尽图

| 日期 | 剩余任务 | 完成百分比 |
|------|---------|-----------|
| 3.13 | 8 天 | 0% |
| 3.14 | 7 天 | 12.5% |
| 3.15 | 6 天 | 25% |
| 3.16 | 5 天 | 37.5% |
| 3.17 | 4 天 | 50% |
| 3.18 | 3 天 | 62.5% |
| 3.19 | 2 天 | 75% |
| 3.20 | 0 天 | 100% |

---

**制定时间：** 2026-03-12 21:45  
**审核人：** 架构设计虾、后端开发虾、前端开发虾、测试运维虾

---

**老板，Phase 1 细化开发计划已制定完成！** 🦐💪

**文档位置：** `docs/PHASE1_PLAN_v1.0.md`
