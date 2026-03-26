# AI 内容工厂 v1.0 - 技术方案设计文档

**文档版本：** V1.0  
**创建时间：** 2026-03-25  
**负责人：** 架构设计虾 🏗️

---

## 1. 技术架构

### 1.1 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                      用户浏览器                          │
│              (Next.js 14 + React 18 前端应用)            │
│                   ┌──────────────┐                      │
│                   │ Markdown 编辑器│                     │
│                   │ 实时预览      │                      │
│                   └──────────────┘                      │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/HTTPS
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  后端 API 服务 (FastAPI)                 │
│  ┌─────────────┬─────────────┬─────────────────────┐   │
│  │  内容模块   │  模板模块   │    配置模块         │   │
│  └─────────────┴─────────────┴─────────────────────┘   │
│                         │                               │
│         ┌───────────────┼───────────────┐              │
│         ▼               ▼               ▼              │
│    ┌────────┐    ┌────────┐    ┌────────┐             │
│    │ 抖音   │    │ 视频号 │    │ 公众号 │  ← 逐一生成  │
│    └────────┘    └────────┘    └────────┘             │
│         │               │               │              │
│         ▼                                               │
│    ┌────────┐                                           │
│    │小红书  │                                           │
│    └────────┘                                           │
└─────────┬──────────────┬─────────────────┬─────────────┘
          │              │                 │
          ▼              ▼                 ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────────┐
│  SQLite/     │ │  Claude API  │ │   通义千问 API   │
│   MySQL      │ │  (内容生成)  │ │   (内容生成)     │
└──────────────┘ └──────────────┘ └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   通义万相 API   │
                    │   (封面图生成)   │
                    └──────────────────┘
```

### 1.2 技术栈选型

| 层级 | 技术 | 版本 | 选型理由 |
|------|------|------|----------|
| **前端框架** | React + Next.js | 18.x + 14.x | 生态成熟、SEO 友好、App Router |
| **UI 组件库** | Shadcn/ui | 最新 | 组件美观、可定制、基于 Tailwind |
| **样式方案** | Tailwind CSS | 3.x | 原子化 CSS、开发效率高 |
| **Markdown 编辑器** | @uiw/react-md-editor | 最新 | 美观、功能全、实时预览 |
| **后端框架** | FastAPI | 0.100+ | 性能好、自动文档、异步支持 |
| **编程语言** | Python | 3.9.11 | AI 生态丰富 |
| **ORM 框架** | SQLAlchemy | 2.0+ | 功能强大、支持异步 |
| **数据库** | SQLite/MySQL | 3.x/8.0+ | SQLite 用于本地，MySQL 用于生产 |
| **AI 服务** | Claude API + 通义千问 | - | 双备份、保证可用 |
| **图片生成** | 通义万相 | - | 中文支持好 |

---

## 2. 数据库设计

### 2.1 数据库表总览

| 序号 | 表名 | 中文名 | 说明 |
|------|------|--------|------|
| 1 | content_generations | 内容生成记录表 | 存储生成任务主记录 |
| 2 | content_items | 内容项表 | 存储各平台生成的内容 |
| 3 | cover_images | 封面图表 | 存储封面图 URL |
| 4 | prompt_templates | 提示词模板表 | 存储 AI 生成提示词模板 |
| 5 | system_configs | 系统配置表 | 存储系统配置信息 |

### 2.2 表结构详细设计

#### 2.2.1 content_generations - 内容生成记录表

| 字段名 | 数据类型 | 长度 | 必填 | 默认值 | 说明 |
|--------|----------|------|------|--------|------|
| id | BIGINT | - | 是 | AUTO_INCREMENT | 主键 ID |
| topic | VARCHAR | 500 | 是 | - | 生成主题 |
| status | VARCHAR | 20 | 是 | pending | 状态：pending/processing/completed/failed/partial |
| template_id | BIGINT | - | 否 | NULL | 使用的提示词模板 ID |
| created_by | VARCHAR | 50 | 是 | 'admin' | 创建人 |
| created_at | DATETIME | - | 是 | CURRENT_TIMESTAMP | 创建时间 |
| updated_by | VARCHAR | 50 | 是 | 'admin' | 修改人 |
| updated_at | DATETIME | - | 是 | CURRENT_TIMESTAMP ON UPDATE | 修改时间 |
| is_deleted | TINYINT | 1 | 是 | 0 | 删除标记：0=未删除，1=已删除 |
| remark | VARCHAR | 500 | 否 | NULL | 备注 |

**索引：**
- PRIMARY KEY (id)
- KEY idx_status (status)
- KEY idx_created_at (created_at)

#### 2.2.2 content_items - 内容项表

| 字段名 | 数据类型 | 长度 | 必填 | 默认值 | 说明 |
|--------|----------|------|------|--------|------|
| id | BIGINT | - | 是 | AUTO_INCREMENT | 主键 ID |
| generation_id | BIGINT | - | 是 | - | 生成任务 ID（外键） |
| platform | VARCHAR | 20 | 是 | - | 平台：douyin/video_account/wechat/xiaohongshu |
| title | VARCHAR | 200 | 否 | NULL | 标题 |
| content | TEXT | - | 是 | - | 内容正文（Markdown 格式） |
| version | INT | - | 是 | 1 | 版本号 |
| is_latest | TINYINT | 1 | 是 | 1 | 是否最新版本：1=是，0=否 |
| status | VARCHAR | 20 | 是 | success | 状态：success/failed/pending |
| error_message | VARCHAR | 500 | 否 | NULL | 失败错误信息 |
| created_by | VARCHAR | 50 | 是 | 'admin' | 创建人 |
| created_at | DATETIME | - | 是 | CURRENT_TIMESTAMP | 创建时间 |
| updated_by | VARCHAR | 50 | 是 | 'admin' | 修改人 |
| updated_at | DATETIME | - | 是 | CURRENT_TIMESTAMP ON UPDATE | 修改时间 |
| is_deleted | TINYINT | 1 | 是 | 0 | 删除标记 |
| remark | VARCHAR | 500 | 否 | NULL | 备注 |

**索引：**
- PRIMARY KEY (id)
- KEY idx_generation_id (generation_id)
- KEY idx_platform (platform)

#### 2.2.3 cover_images - 封面图表

| 字段名 | 数据类型 | 长度 | 必填 | 默认值 | 说明 |
|--------|----------|------|------|--------|------|
| id | BIGINT | - | 是 | AUTO_INCREMENT | 主键 ID |
| content_id | BIGINT | - | 是 | - | 内容项 ID（外键） |
| platform | VARCHAR | 20 | 是 | - | 平台 |
| image_url | VARCHAR | 500 | 是 | - | 图片 URL |
| image_width | INT | - | 否 | NULL | 图片宽度 |
| image_height | INT | - | 否 | NULL | 图片高度 |
| status | VARCHAR | 20 | 是 | success | 状态：success/failed/pending |
| created_by | VARCHAR | 50 | 是 | 'admin' | 创建人 |
| created_at | DATETIME | - | 是 | CURRENT_TIMESTAMP | 创建时间 |
| updated_by | VARCHAR | 50 | 是 | 'admin' | 修改人 |
| updated_at | DATETIME | - | 是 | CURRENT_TIMESTAMP ON UPDATE | 修改时间 |
| is_deleted | TINYINT | 1 | 是 | 0 | 删除标记 |
| remark | VARCHAR | 500 | 否 | NULL | 备注 |

**索引：**
- PRIMARY KEY (id)
- KEY idx_content_id (content_id)

#### 2.2.4 prompt_templates - 提示词模板表

| 字段名 | 数据类型 | 长度 | 必填 | 默认值 | 说明 |
|--------|----------|------|------|--------|------|
| id | BIGINT | - | 是 | AUTO_INCREMENT | 主键 ID |
| name | VARCHAR | 100 | 是 | - | 模板名称 |
| platform | VARCHAR | 20 | 是 | - | 适用平台：all/douyin/video_account/wechat/xiaohongshu |
| template_content | TEXT | - | 是 | - | 模板内容（支持参数：{topic},{style},{word_count}） |
| is_default | TINYINT | 1 | 是 | 0 | 是否系统默认：1=是，0=否 |
| is_active | TINYINT | 1 | 是 | 1 | 是否启用：1=是，0=否 |
| sort_order | INT | - | 是 | 0 | 排序顺序 |
| created_by | VARCHAR | 50 | 是 | 'admin' | 创建人 |
| created_at | DATETIME | - | 是 | CURRENT_TIMESTAMP | 创建时间 |
| updated_by | VARCHAR | 50 | 是 | 'admin' | 修改人 |
| updated_at | DATETIME | - | 是 | CURRENT_TIMESTAMP ON UPDATE | 修改时间 |
| is_deleted | TINYINT | 1 | 是 | 0 | 删除标记 |
| remark | VARCHAR | 500 | 否 | NULL | 备注 |

**索引：**
- PRIMARY KEY (id)
- KEY idx_platform (platform)
- KEY idx_is_default (is_default)

#### 2.2.5 system_configs - 系统配置表

| 字段名 | 数据类型 | 长度 | 必填 | 默认值 | 说明 |
|--------|----------|------|------|--------|------|
| id | BIGINT | - | 是 | AUTO_INCREMENT | 主键 ID |
| config_key | VARCHAR | 100 | 是 | - | 配置键（如：claude_api_key） |
| config_value | TEXT | - | 是 | - | 配置值（加密存储） |
| config_type | VARCHAR | 20 | 是 | 'string' | 配置类型：string/number/boolean/json |
| description | VARCHAR | 500 | 否 | NULL | 配置说明 |
| is_encrypted | TINYINT | 1 | 是 | 0 | 是否加密：1=是，0=否 |
| created_by | VARCHAR | 50 | 是 | 'admin' | 创建人 |
| created_at | DATETIME | - | 是 | CURRENT_TIMESTAMP | 创建时间 |
| updated_by | VARCHAR | 50 | 是 | 'admin' | 修改人 |
| updated_at | DATETIME | - | 是 | CURRENT_TIMESTAMP ON UPDATE | 修改时间 |
| is_deleted | TINYINT | 1 | 是 | 0 | 删除标记 |
| remark | VARCHAR | 500 | 否 | NULL | 备注 |

**索引：**
- PRIMARY KEY (id)
- UNIQUE KEY uk_config_key (config_key)

---

## 3. API 接口设计

### 3.1 接口总览

| 模块 | 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|------|
| **内容** | 生成内容 | POST | /api/v1/content/generate | 一键生成 4 平台内容 |
| **内容** | 获取详情 | GET | /api/v1/content/{id} | 获取生成内容详情 |
| **内容** | 更新内容 | PUT | /api/v1/content/{id} | 更新内容（编辑） |
| **内容** | 重新生成 | POST | /api/v1/content/{id}/regenerate | 重新生成某平台内容 |
| **内容** | 历史记录 | GET | /api/v1/content/history | 获取历史记录列表 |
| **内容** | 删除记录 | DELETE | /api/v1/content/{id} | 删除生成记录 |
| **模板** | 获取模板列表 | GET | /api/v1/templates | 获取提示词模板列表 |
| **模板** | 创建模板 | POST | /api/v1/templates | 创建提示词模板 |
| **模板** | 更新模板 | PUT | /api/v1/templates/{id} | 更新提示词模板 |
| **模板** | 删除模板 | DELETE | /api/v1/templates/{id} | 删除提示词模板 |
| **配置** | 获取配置 | GET | /api/v1/configs | 获取系统配置列表 |
| **配置** | 更新配置 | PUT | /api/v1/configs/{key} | 更新系统配置 |

### 3.2 响应格式规范

#### 成功响应
```json
{
  "code": 200,
  "message": "success",
  "data": { ... }
}
```

#### 错误响应
```json
{
  "code": 错误码,
  "message": "错误描述",
  "data": null
}
```

#### 错误码定义
| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |
| 503 | 服务不可用 |

---

## 4. 项目目录结构

### 4.1 后端目录结构
```
backend/
├── app/
│   ├── main.py              # FastAPI 入口
│   ├── api/                 # API 路由
│   │   ├── __init__.py
│   │   ├── content.py       # 内容生成接口
│   │   ├── templates.py     # 模板管理接口
│   │   └── configs.py       # 配置管理接口
│   ├── models/              # 数据库模型
│   │   ├── __init__.py
│   │   ├── base.py          # Base 类定义
│   │   ├── generation.py    # content_generations 表
│   │   ├── item.py          # content_items 表
│   │   ├── cover.py         # cover_images 表
│   │   ├── template.py      # prompt_templates 表
│   │   └── config.py        # system_configs 表
│   ├── services/            # 业务逻辑
│   │   ├── __init__.py
│   │   ├── generator.py     # 内容生成服务
│   │   ├── ai_service.py    # AI 服务对接
│   │   └── image_service.py # 封面图生成
│   └── utils/               # 工具函数
│       ├── __init__.py
│       ├── db.py            # 数据库连接
│       └── init_db.py       # 初始化脚本
├── tests/                   # 测试用例
├── requirements.txt
├── .env.example
└── README.md
```

### 4.2 前端目录结构
```
frontend/
├── src/
│   ├── app/                 # Next.js 14 App Router
│   │   ├── layout.tsx       # 根布局
│   │   ├── page.tsx         # 首页（创作页）
│   │   ├── result/          # 结果页
│   │   │   └── page.tsx
│   │   ├── history/         # 历史记录页
│   │   │   └── page.tsx
│   │   ├── templates/       # 模板管理页
│   │   │   └── page.tsx
│   │   └── settings/        # 系统设置页
│   │       └── page.tsx
│   ├── components/          # 可复用组件
│   │   ├── ui/              # 基础 UI 组件
│   │   ├── MarkdownEditor/  # Markdown 编辑器
│   │   ├── PlatformCard/    # 平台内容卡片
│   │   └── TemplateSelector/# 模板选择器
│   ├── api/                 # API 客户端
│   │   └── client.ts        # Axios 封装
│   └── styles/              # 全局样式
│       └── globals.css
├── public/                  # 静态资源
├── package.json
├── tailwind.config.js
├── next.config.js
└── README.md
```

---

## 5. 核心业务流程

### 5.1 一键生成 4 平台流程

```
用户输入主题 → 选择模板 → POST /api/v1/content/generate
                                      ↓
                              创建生成任务 (pending)
                                      ↓
                        逐一生成：抖音 → 视频号 → 公众号 → 小红书
                                      ↓
                              每个平台：
                        1. 调用 AI 服务生成内容
                        2. 调用通义万相生成封面图
                        3. 保存到数据库
                                      ↓
                              更新任务状态 (completed/partial)
                                      ↓
                              返回生成任务 ID
```

### 5.2 容错机制

- **单平台失败：** 标记为"生成失败"，显示重试按钮，不影响其他平台
- **全部失败：** 提示"服务繁忙，请稍后重试"
- **封面图失败：** 显示默认占位图，不影响内容使用

---

## 6. 部署方案

### 6.1 本地部署（开发环境）

**后端：**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 配置 API Key
python app/utils/init_db.py
python app/main.py
```

**前端：**
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

### 6.2 生产部署（Linux）

**后端：**
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**前端：**
```bash
npm run build
# 使用 Nginx 托管静态文件
```

**Nginx 配置：**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /var/www/html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 7. 安全与性能

### 7.1 安全措施
- API 密钥加密存储
- 本地部署默认无需认证，远程访问需配置 Token
- 敏感配置信息加密存储
- 本地词库敏感词检测

### 7.2 性能优化
- 页面加载时间 < 2 秒
- 生成平均耗时 < 120 秒（4 个平台总时长）
- API 响应时间 < 500ms（除生成接口外）
- 并发支持 5 QPS（单机使用）

---

## 8. 开发规范

### 8.1 代码规范
- **Python：** PEP 8 + Black 格式化
- **TypeScript：** ESLint + Prettier
- **Git 提交：** Conventional Commits

### 8.2 跨平台适配
- **路径处理：** 使用 pathlib，禁止硬编码路径
- **文件编码：** 统一使用 UTF-8
- **命令行调用：** 使用 sys.executable

---

**文档结束**

*最后更新：2026-03-25 17:35*
