# 🤝 AI 内容工厂 v1.0.0 - 技术对齐会议纪要

**会议时间：** 2026-03-12 20:00  
**会议类型：** 技术对齐会（接口 + 数据库）  
**主持人：** 虾虾（项目经理）🦐📋  
**参会人员：** 架构设计虾、后端开发虾、前端开发虾、测试运维虾  
**记录人：** 虾虾🦐📋

---

## 📋 会议议程

1. 数据库设计对齐（表结构、字段、类型）
2. API 接口对齐（接口定义、请求/响应格式）
3. 数据格式对齐（JSON 结构、枚举值）
4. 跨平台适配对齐（路径、编码规范）

---

## 📊 数据库设计对齐

### 表 1：content_history（内容历史表）

| 字段名 | 类型 | 长度 | 必填 | 默认值 | 说明 | 示例值 |
|--------|------|------|------|--------|------|--------|
| id | INT | - | ✅ | AUTO_INCREMENT | 主键 | 1 |
| theme | VARCHAR | 200 | ✅ | - | 主题 | "AI 效率工具" |
| selected_topic | TEXT | - | ✅ | - | 选中的选题 | "这 3 个 AI 工具让我每天准点下班" |
| template_name | VARCHAR | 100 | ❌ | NULL | 模板名称 | "AI 干货型" |
| template_config | JSON | - | ❌ | NULL | 模板配置（JSON） | `{"douyin": {...}}` |
| platform | VARCHAR | 20 | ❌ | NULL | 平台 | "douyin" |
| content | TEXT | - | ✅ | - | 生成内容 | "打工人必看！..." |
| image_urls | JSON | - | ❌ | NULL | 配图 URLs（JSON 数组） | `["url1", "url2"]` |
| word_count | INT | - | ❌ | NULL | 字数统计 | 580 |
| status | VARCHAR | 20 | ❌ | "success" | 状态 | "success" |
| error_message | TEXT | - | ❌ | NULL | 错误信息 | - |
| created_at | DATETIME | - | ✅ | CURRENT_TIMESTAMP | 创建时间 | 2026-03-12 20:00:00 |
| updated_at | DATETIME | - | ✅ | CURRENT_TIMESTAMP ON UPDATE | 更新时间 | 2026-03-12 20:00:00 |

**索引：**
- PRIMARY KEY (id)
- INDEX idx_theme (theme)
- INDEX idx_created_at (created_at)
- INDEX idx_status (status)

---

### 表 2：search_history（搜索历史表）

| 字段名 | 类型 | 长度 | 必填 | 默认值 | 说明 | 示例值 |
|--------|------|------|------|--------|------|--------|
| id | INT | - | ✅ | AUTO_INCREMENT | 主键 | 1 |
| theme | VARCHAR | 200 | ✅ | - | 搜索主题 | "AI 效率工具" |
| search_results | JSON | - | ✅ | - | 搜索结果（JSON） | `{"weibo": [...], "zhihu": [...]}` |
| recommended_topics | JSON | - | ✅ | - | 推荐选题（JSON 数组） | `[{"title": "..."}]` |
| created_at | DATETIME | - | ✅ | CURRENT_TIMESTAMP | 创建时间 | 2026-03-12 20:00:00 |

**索引：**
- PRIMARY KEY (id)
- INDEX idx_theme (theme)
- INDEX idx_created_at (created_at)

---

### 表 3：prompt_templates（提示词模板表）- Phase 2

| 字段名 | 类型 | 长度 | 必填 | 默认值 | 说明 | 示例值 |
|--------|------|------|------|--------|------|--------|
| id | INT | - | ✅ | AUTO_INCREMENT | 主键 | 1 |
| name | VARCHAR | 100 | ✅ | - | 模板名称 | "AI 干货型" |
| platform | VARCHAR | 20 | ✅ | - | 平台 | "douyin" |
| base_prompt | TEXT | - | ✅ | - | 基础提示词 | "你是专业的短视频口播文案创作者..." |
| custom_prompt | JSON | - | ❌ | NULL | 自定义提示词（JSON） | `{"target_audience": "打工人"}` |
| style_template | VARCHAR | 50 | ❌ | NULL | 风格模板 | "干货型" |
| is_preset | BOOLEAN | - | ❌ | FALSE | 是否预设模板 | TRUE |
| created_at | DATETIME | - | ✅ | CURRENT_TIMESTAMP | 创建时间 | 2026-03-12 20:00:00 |
| updated_at | DATETIME | - | ✅ | CURRENT_TIMESTAMP ON UPDATE | 更新时间 | 2026-03-12 20:00:00 |

**索引：**
- PRIMARY KEY (id)
- INDEX idx_name (name)
- INDEX idx_platform (platform)
- INDEX idx_is_preset (is_preset)

---

## 🔌 API 接口对齐

### 接口 1：AI 联网搜索

**接口定义：**
```
POST /api/search
```

**请求参数：**
```json
{
  "theme": "AI 效率工具"
}
```

**响应格式：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "search_id": 1,
    "theme": "AI 效率工具",
    "weibo_hot_search": [
      {
        "rank": 1,
        "title": "AI 工具推荐",
        "hot_value": "500 万",
        "url": "https://..."
      }
    ],
    "zhihu_hot_list": [
      {
        "rank": 1,
        "title": "有哪些好用的 AI 工具？",
        "hot_value": 10000,
        "url": "https://..."
      }
    ]
  }
}
```

**字段说明：**
- `search_id`: 搜索记录 ID（用于后续选题推荐）
- `weibo_hot_search`: 微博热搜列表（Top50）
- `zhihu_hot_list`: 知乎热榜列表（Top50）

---

### 接口 2：选题推荐

**接口定义：**
```
POST /api/topics/recommend
```

**请求参数：**
```json
{
  "search_id": 1,
  "search_results": {...}  // 搜索结果（可选，如不传则从数据库查）
}
```

**响应格式：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "topics": [
      {
        "id": 1,
        "title": "这 3 个 AI 工具让我每天准点下班",
        "type": "工具推荐",
        "advantage": "有数据、有案例、易共鸣",
        "recommend_level": 5
      },
      {
        "id": 2,
        "title": "90% 的人都不知道 AI 可以这样用",
        "type": "认知差",
        "advantage": "好奇心驱动、易传播",
        "recommend_level": 4
      }
    ]
  }
}
```

**字段说明：**
- `topics`: 推荐选题列表（3-5 个）
- `type`: 选题类型（工具推荐/认知差/案例分享/观点输出）
- `recommend_level`: 推荐度（1-5 星）

---

### 接口 3：内容生成

**接口定义：**
```
POST /api/content/generate
```

**请求参数：**
```json
{
  "topic": "这 3 个 AI 工具让我每天准点下班",
  "platform": "douyin",
  "template_config": {
    "target_audience": "打工人",
    "content_style": "干货型",
    "duration": "60 秒"
  },
  "generate_images": true,
  "image_count": 3
}
```

**响应格式：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "content_id": 1,
    "platform": "douyin",
    "content": "打工人必看！这 3 个 AI 工具让我每天准点下班...\n\n（完整文案）",
    "word_count": 580,
    "images": [
      {
        "type": "cover",
        "url": "https://...",
        "width": 1080,
        "height": 1920
      }
    ],
    "created_at": "2026-03-12T20:00:00"
  }
}
```

**字段说明：**
- `platform`: 平台（douyin/wechat/xiaohongshu）
- `content`: 生成内容（抖音文案/公众号文章/小红书笔记）
- `images`: 配图列表（公众号 1-5 张，小红书封面 1 张）

---

### 接口 4：历史列表

**接口定义：**
```
GET /api/history
```

**请求参数：**
```
GET /api/history?page=1&page_size=20&theme=AI&platform=douyin
```

**响应格式：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 100,
    "page": 1,
    "page_size": 20,
    "items": [
      {
        "id": 1,
        "theme": "AI 效率工具",
        "topic": "这 3 个 AI 工具让我每天准点下班",
        "platform": "douyin",
        "word_count": 580,
        "image_count": 3,
        "created_at": "2026-03-12T20:00:00"
      }
    ]
  }
}
```

---

### 接口 5：历史详情

**接口定义：**
```
GET /api/history/:id
```

**响应格式：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "theme": "AI 效率工具",
    "topic": "这 3 个 AI 工具让我每天准点下班",
    "platform": "douyin",
    "content": "打工人必看！...",
    "images": [...],
    "template_config": {...},
    "created_at": "2026-03-12T20:00:00"
  }
}
```

---

## 📏 数据格式对齐

### 平台枚举值

```json
{
  "platform": {
    "douyin": "抖音/视频号",
    "wechat": "公众号",
    "xiaohongshu": "小红书"
  }
}
```

### 选题类型枚举值

```json
{
  "topic_type": {
    "tool_recommend": "工具推荐",
    "knowledge_gap": "认知差",
    "case_share": "案例分享",
    "opinion_output": "观点输出"
  }
}
```

### 内容状态枚举值

```json
{
  "content_status": {
    "success": "生成成功",
    "failed": "生成失败",
    "partial": "部分成功"
  }
}
```

### 配图类型枚举值

```json
{
  "image_type": {
    "cover": "封面图",
    "inner": "内页图",
    "thumbnail": "缩略图"
  }
}
```

---

## 🛠️ 跨平台适配对齐

### 路径处理规范

**✅ 正确做法：**
```python
from pathlib import Path
db_path = Path(__file__).parent / "data" / "daily_brief.db"
```

**❌ 禁止做法：**
```python
db_path = "/home/admin/data/daily_brief.db"  # Linux 路径
db_path = "C:\\Users\\admin\\data\\daily_brief.db"  # Windows 路径
```

### 文件编码规范

**✅ 正确做法：**
```python
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

**❌ 禁止做法：**
```python
with open("file.txt", "r") as f:  # Windows 默认 GBK
    content = f.read()
```

### 命令行调用规范

**✅ 正确做法：**
```python
import sys
subprocess.run([sys.executable, "script.py"])
```

**❌ 禁止做法：**
```python
subprocess.run(["python3", "script.py"])  # Windows 无 python3 命令
```

---

## 📝 各自文档交付清单

| 角色 | 交付文档 | 截止时间 | 状态 |
|------|---------|---------|------|
| 架构设计虾 | 数据库设计文档（详细版） | 今天 21:00 | ⏳ |
| 后端开发虾 | API 接口文档（Swagger） | 今天 21:00 | ⏳ |
| 前端开发虾 | 前端数据结构文档 | 今天 21:00 | ⏳ |
| 测试运维虾 | 测试用例文档 | 明天 12:00 | ⏳ |
| 项目经理虾 | 会议纪要 + 汇总文档 | 今天 20:30 | ✅ |

---

## ✅ 会议结论

### 数据库设计
- ✅ 3 张表结构已确认（content_history、search_history、prompt_templates）
- ✅ 字段类型、长度、默认值已对齐
- ✅ 索引设计已确认

### API 接口
- ✅ 5 个核心接口已确认（搜索、选题、生成、历史列表、历史详情）
- ✅ 请求/响应格式已对齐
- ✅ 枚举值已统一

### 数据格式
- ✅ JSON 结构已统一
- ✅ 平台枚举值已统一
- ✅ 选题类型枚举值已统一

### 跨平台适配
- ✅ 路径处理规范已确认（使用 pathlib）
- ✅ 文件编码规范已确认（UTF-8）
- ✅ 命令行调用规范已确认（sys.executable）

---

## 📅 下一步行动

1. ✅ 各角色根据会议结论完善各自文档
2. ✅ 后端开发虾创建数据库表结构
3. ✅ 后端开发虾实现 API 接口
4. ✅ 前端开发虾根据接口文档开发页面
5. ✅ 测试运维虾根据接口文档编写测试用例

---

**会议结束时间：** 2026-03-12 20:30  
**会议时长：** 30 分钟

---

**所有技术细节已对齐，团队可以开始开发！** 🦐💪
