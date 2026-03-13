# 🏗️ AI 内容工厂 v1.0.0 - 技术架构文档

**文档版本：** v1.0.0  
**创建日期：** 2026-03-12  
**文档作者：** 架构设计虾 🦐🏗️  
**审核状态：** 待审核

---

## 1. 系统架构

### 1.1 整体架构

```
┌─────────────────────────────────────────┐
│  前端：React 18 + Ant Design 5          │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  后端：Python FastAPI                   │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  AI 服务：DashScope Qwen + 文生图        │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  数据库：MySQL 8.0                      │
└─────────────────────────────────────────┘
```

### 1.2 技术栈

| 模块 | 技术选型 | 版本 |
|------|---------|------|
| 前端框架 | React | 18.x |
| UI 库 | Ant Design | 5.x |
| 状态管理 | Zustand | 4.x |
| 后端框架 | FastAPI | 0.109+ |
| 数据库 | MySQL | 8.0 |
| ORM | SQLAlchemy | 2.0 |
| AI 模型 | DashScope Qwen-Plus | 最新 |

---

## 2. 模块设计

### 2.1 搜索模块

```python
class SearchService:
    - 微博热搜爬虫
    - 知乎热榜爬虫
    - 数据清洗
    - 结果聚合
```

### 2.2 AI 模块

```python
class AIService:
    - 选题推荐
    - 内容生成
    - 配图生成
    - Prompt 管理
```

### 2.3 内容模块

```python
class ContentService:
    - 抖音文案生成
    - 公众号文章生成
    - 小红书笔记生成
```

---

## 3. 数据库设计

### 3.1 内容历史表

```sql
CREATE TABLE content_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    theme VARCHAR(200) NOT NULL,
    selected_topic TEXT,
    template_config JSON,
    template_name VARCHAR(100),
    platform VARCHAR(20),
    content TEXT,
    image_urls JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 3.2 搜索历史表

```sql
CREATE TABLE search_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    theme VARCHAR(200) NOT NULL,
    search_results JSON,
    recommended_topics JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 4. API 设计

### 4.1 核心 API

| 接口 | 方法 | 描述 |
|------|------|------|
| /api/search | POST | AI 联网搜索 |
| /api/topics/recommend | POST | 推荐选题 |
| /api/content/generate | POST | 生成内容 |
| /api/history | GET | 获取历史 |

---

## 5. 部署方案

### 5.1 MVP 部署

- 本地运行
- **跨平台支持：Windows + Linux + Mac**
- 一键启动脚本

### 5.2 跨平台适配要求

**文件路径：**
- ✅ 使用 `pathlib` 库（自动适配 `/` 和 `\`）
- ❌ 禁止硬编码路径分隔符

**命令行工具：**
- ✅ 使用 `python` 命令（不指定版本）
- ❌ 禁止使用 `python3` 或 `python3.9`

**编码格式：**
- ✅ 所有文件使用 UTF-8 编码
- ❌ 禁止使用 GBK 等非 UTF-8 编码

**依赖管理：**
- ✅ `requirements.txt` 使用英文注释
- ✅ 所有依赖在 Windows 和 Linux 上都可安装

### 5.3 Phase 3 部署

- 云服务器（Linux）
- Nginx 反向代理
- Docker 容器化

---

**审核人：** 项目经理虾、后端开发虾、前端开发虾、测试运维虾  
**审核日期：** 2026-03-12
