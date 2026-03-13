# 📝 AI 内容工厂 - 产品需求文档 v2.0

**文档版本：** v2.0.0  
**创建日期：** 2026-03-13  
**更新日期：** 2026-03-13  
**文档作者：** 虾虾（产品经理）🦐📋  
**项目阶段：** Phase 2 - Prompt 配置化 + 内容生成

---

## 📋 项目概览

### 产品名称
AI 内容工厂（AI Content Factory）

### 产品定位
AI 驱动的全流程内容创作系统，实现一次选题多平台内容自动生成。

### 核心价值
- 🎯 **智能选题** - AI 根据热点推荐优质选题
- ✍️ **一键生成** - 一次输入，多平台内容自动生成
- 🎨 **智能配图** - AI 生成匹配内容的配图
- 📊 **历史管理** - 完整的内容创作历史记录
- ⚙️ **Prompt 可配置** - 数据库存储，支持动态调整

### 目标用户
- 内容创作者
- 新媒体运营
- 自媒体从业者
- 营销团队

---

## 🎯 Phase 2 功能范围

### 核心功能

| 模块 | 功能 | 优先级 | 说明 |
|------|------|--------|------|
| **Prompt 管理** | Prompt 数据库存储 | P0 | 支持动态配置、版本控制 |
| **Prompt 管理** | Prompt 在线编辑 | P0 | 支持修改、测试、发布 |
| **Prompt 管理** | Prompt 版本历史 | P1 | 支持版本追溯、回滚 |
| **选题推荐** | AI 推荐选题 | P0 | 根据热点推荐 3-5 个选题 |
| **内容生成** | 抖音文案 | P0 | 500-600 字口播文案 |
| **内容生成** | 公众号文章 | P0 | 2000 字深度文章 |
| **内容生成** | 小红书笔记 | P0 | 带 emoji 和标签 |
| **配图生成** | 公众号配图 | P1 | 16:9 比例封面 |
| **配图生成** | 小红书封面 | P1 | 3:4 比例封面 |
| **历史记录** | 历史列表 | P1 | 分页展示 |
| **历史记录** | 历史详情 | P1 | 查看完整内容 |
| **历史记录** | 搜索筛选 | P2 | 按主题/平台筛选 |

---

## 📊 功能详细设计

### 1. Prompt 管理

#### 1.1 Prompt 存储

**存储方式：** 数据库存储

**数据表：**
- `prompts` - Prompt 主表
- `prompt_versions` - 版本历史表
- `prompt_test_logs` - 测试日志表

**Prompt 字段：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| name | TEXT | 标识名（如 "douyin_script"） |
| display_name | TEXT | 显示名称（如 "抖音文案"） |
| description | TEXT | 描述说明 |
| template | TEXT | Prompt 模板（支持{变量}） |
| variables | TEXT | 变量列表 JSON |
| output_format | TEXT | 输出格式（json/text/markdown） |
| model | TEXT | AI 模型（默认 qwen-plus） |
| max_tokens | INTEGER | 最大 token 数 |
| temperature | REAL | 温度参数（0-1） |
| is_active | BOOLEAN | 是否启用 |
| is_system | BOOLEAN | 是否系统内置 |
| category | TEXT | 分类（topic/douyin/wechat/xhs/image） |

#### 1.2 Prompt 管理界面

**功能：**
- 查看 Prompt 列表
- 编辑 Prompt 模板
- 测试 Prompt 效果
- 查看版本历史
- 发布新版本

**界面：**
- `/admin/prompts` - Prompt 列表页
- `/admin/prompts/:id` - Prompt 详情页
- `/admin/prompts/:id/edit` - Prompt 编辑页
- `/admin/prompts/:id/test` - Prompt 测试页
- `/admin/prompts/:id/versions` - 版本历史页

---

### 2. 选题推荐

#### 2.1 功能描述

根据微博热搜和知乎热榜，AI 推荐 3-5 个有吸引力的选题。

#### 2.2 用户流程

```
1. 用户输入搜索主题（可选）
2. 系统获取微博热搜 + 知乎热榜
3. 调用 AI 推荐选题
4. 展示选题列表（标题、类型、优势、推荐度）
5. 用户选择选题
```

#### 2.3 选题信息

| 字段 | 类型 | 说明 |
|------|------|------|
| title | TEXT | 选题标题 |
| type | TEXT | 选题类型（干货/观点/故事/测评） |
| advantage | TEXT | 选题优势 |
| rating | INTEGER | 推荐度（1-5 星） |

---

### 3. 内容生成

#### 3.1 抖音文案

**要求：**
- 字数：500-600 字
- 风格：口语化、接地气
- 结构：开头 3 秒痛点 + 中间干货 + 结尾引导互动
- 适合真人出镜口播

#### 3.2 公众号文章

**要求：**
- 字数：2000 字左右
- 格式：Markdown
- 结构：引言 + 正文（3-5 个小标题）+ 结语
- 适合微信公众号阅读体验

#### 3.3 小红书笔记

**要求：**
- 字数：300-500 字
- 风格：活泼、亲切、带 emoji
- 结构：标题 + 正文 + 标签（5-10 个）
- 符合小红书社区调性

---

### 4. 配图生成

#### 4.1 公众号配图

**要求：**
- 比例：16:9
- 风格：简洁、专业
- 包含文字：文章标题
- 适合微信公众号封面

#### 4.2 小红书封面

**要求：**
- 比例：3:4
- 风格：活泼、吸睛
- 包含文字：笔记标题
- 适合小红书封面

---

### 5. 历史记录

#### 5.1 数据表

```sql
CREATE TABLE content_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    theme TEXT NOT NULL,           -- 主题
    topic TEXT NOT NULL,           -- 选题
    platform TEXT NOT NULL,        -- 平台（douyin/wechat/xhs）
    content TEXT NOT NULL,         -- 内容
    image_urls TEXT,               -- 配图 URL 列表 JSON
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### 5.2 功能

- 历史列表（分页，每页 20 条）
- 历史详情（查看完整内容）
- 搜索（按主题搜索）
- 筛选（按平台筛选）

---

## 🔧 技术架构

### 后端技术栈

| 模块 | 技术 | 说明 |
|------|------|------|
| **框架** | FastAPI | Python Web 框架 |
| **数据库** | SQLite | 轻量级数据库（Phase 2） |
| **AI 服务** | DashScope | 阿里云百炼 |
| **ORM** | SQLAlchemy | 数据库 ORM |

### 前端技术栈

| 模块 | 技术 | 说明 |
|------|------|------|
| **框架** | React 18 | 前端框架 |
| **UI 库** | Ant Design 5 | UI 组件库 |
| **状态管理** | Zustand | 轻量级状态管理 |
| **Markdown 渲染** | react-markdown | Markdown 渲染 |

---

## 📐 API 接口设计

### Prompt 管理接口

```
GET    /api/prompts              - 获取 Prompt 列表
GET    /api/prompts/:id          - 获取 Prompt 详情
POST   /api/prompts              - 创建 Prompt
PUT    /api/prompts/:id          - 更新 Prompt
DELETE /api/prompts/:id          - 删除 Prompt
POST   /api/prompts/:id/versions - 创建新版本
GET    /api/prompts/:id/versions - 获取版本历史
POST   /api/prompts/:id/versions/:versionId/publish - 发布版本
POST   /api/prompts/test         - 测试 Prompt 效果
```

### 内容生成接口

```
POST   /api/search               - 搜索热门话题
POST   /api/topics/recommend     - 推荐选题
POST   /api/content/generate     - 生成内容
POST   /api/images/generate      - 生成配图
GET    /api/history              - 获取历史列表
GET    /api/history/:id          - 获取历史详情
```

---

## 📊 数据库设计

### 表结构概览

| 表名 | 说明 | Phase |
|------|------|-------|
| prompts | Prompt 主表 | Phase 2 |
| prompt_versions | Prompt 版本历史 | Phase 2 |
| prompt_test_logs | Prompt 测试日志 | Phase 2 |
| content_history | 内容历史 | Phase 2 |

---

## ✅ 验收标准

### Phase 2 交付标准

1. **功能完整性**
   - [ ] Prompt 管理功能完整
   - [ ] 选题推荐功能正常
   - [ ] 内容生成功能正常
   - [ ] 配图生成功能正常
   - [ ] 历史记录功能正常

2. **质量要求**
   - [ ] 所有功能可正常使用
   - [ ] 前后端联调通过
   - [ ] 测试用例 100% 通过
   - [ ] 代码推送到 GitHub

3. **性能要求**
   - [ ] 选题推荐 < 10 秒
   - [ ] 内容生成 < 60 秒
   - [ ] 配图生成 < 10 秒/张
   - [ ] API 响应 < 1 秒

---

## 📅 开发计划

| 阶段 | 时间 | 功能 | 状态 |
|------|------|------|------|
| **Phase 1** | 3.13 | 搜索模块（微博 + 知乎） | ✅ 已完成 |
| **Phase 2** | 3.14-3.20 | Prompt 配置化 + 内容生成 | 🔄 进行中 |
| **Phase 3** | 3.21-3.27 | 优化 + 自动化发布 | ⏳ 待开始 |

---

## 📝 修订历史

| 版本 | 日期 | 修订内容 | 修订人 |
|------|------|---------|--------|
| v1.0 | 2026-03-12 | 初始版本 | 虾虾 |
| v2.0 | 2026-03-13 | 增加 Prompt 配置化方案 | 虾虾 |

---

**文档状态：** ✅ 已审核  
**审核人：** 架构设计虾、后端开发虾、前端开发虾  
**审核时间：** 2026-03-13 11:30

---

*AI 内容工厂 - 让内容创作更高效！* 🚀
