# 🎨 AI 内容工厂 - AI Content Factory

**版本号：** v2.0.0  
**创建日期：** 2026-03-12  
**更新日期：** 2026-03-13  
**项目状态：** 开发中（Phase 2 - Prompt 配置化）

---

## 📋 项目简介

AI 驱动的全流程内容创作系统，实现一次选题多平台内容自动生成。

**核心价值：** 每次创作节省约 3.5 小时！

**核心特性：**
- ✅ **Prompt 配置化** - 数据库存储，支持动态管理、版本控制
- ✅ **AI 联网搜索** - 微博热搜 + 知乎热榜
- ✅ **智能选题推荐** - 3-5 个选题角度
- ✅ **多平台内容生成** - 抖音 + 公众号 + 小红书
- ✅ **AI 配图生成** - 公众号 16:9 + 小红书 3:4
- ✅ **历史内容管理** - 完整创作历史记录

---

## 🚀 快速开始

### 环境要求

- Python 3.9+
- Node.js 18+（前端）
- SQLite（内置，无需安装）

### 后端启动

```bash
cd backend

# 安装依赖
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件（配置 DASHSCOPE_API_KEY）

# 初始化数据库
python -m app.data.migrate_v1

# 启动服务
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端启动

```bash
cd frontend

# 配置淘宝镜像
npm config set registry https://registry.npmmirror.com

# 安装依赖
npm install

# 启动开发服务器
npm start
```

### 访问地址

- 🌐 前端页面：http://localhost:3000
- 📚 API 文档：http://localhost:8000/docs
- ⚙️ 后端 API：http://localhost:8000/api/*

---

## 📁 项目结构

```
ai-content-factory/
├── backend/                 # 后端（Python + FastAPI）
│   ├── app/
│   │   ├── api/            # API 路由
│   │   │   ├── prompts.py  # Prompt 管理 API
│   │   │   ├── topics.py   # 选题 API
│   │   │   ├── content.py  # 内容生成 API
│   │   │   └── images.py   # 配图 API
│   │   ├── models/         # 数据库模型
│   │   │   ├── prompt.py   # Prompt 模型
│   │   │   └── content_history.py
│   │   ├── services/       # 业务逻辑
│   │   │   └── ai.py       # AI 服务
│   │   ├── crawler/        # 爬虫模块
│   │   │   ├── weibo.py    # 微博爬虫
│   │   │   └── zhihu.py    # 知乎爬虫
│   │   └── ai/             # AI 服务
│   ├── data/               # 数据库文件
│   │   ├── schema.sql      # 数据库结构
│   │   ├── seed_prompts.sql # Prompt 初始化
│   │   └── migrate_v1.py   # 迁移脚本
│   ├── config/             # 配置文件
│   ├── tests/              # 测试代码
│   └── requirements.txt    # Python 依赖
├── frontend/               # 前端（React + Ant Design）
│   ├── src/
│   │   ├── pages/          # 页面
│   │   │   ├── Search.jsx      # 搜索页
│   │   │   ├── Preview.jsx     # 预览页
│   │   │   ├── History.jsx     # 历史页
│   │   │   └── Prompts.jsx     # Prompt 管理
│   │   ├── components/     # 组件
│   │   ├── services/       # API 服务
│   │   └── stores/         # 状态管理
│   └── package.json        # Node 依赖
├── docs/                   # 文档
├── scripts/                # 脚本工具
└── README.md              # 项目说明
```

---

## 📅 开发计划

| 阶段 | 时间 | 功能 | 状态 |
|------|------|------|------|
| **Phase 1** | 3.13 | 搜索模块（微博 + 知乎） | ✅ 已完成 |
| **Phase 2** | 3.14-3.20 | Prompt 配置化 + 内容生成 | 🔄 进行中 |
| **Phase 3** | 3.21-3.27 | 优化 + 自动化发布 | ⏳ 待开始 |

---

## 📊 里程碑

| 里程碑 | 日期 | 交付物 | 状态 |
|--------|------|--------|------|
| 项目启动 | 3.12 | 技术文档 + 环境就绪 | ✅ 已完成 |
| Phase 1 完成 | 3.13 | 搜索模块 + 代码推送 GitHub | ✅ 已完成 |
| Prompt 数据库 | 3.14 | 数据库设计 + 初始化脚本 | ⏳ 进行中 |
| AIService 重构 | 3.15 | Prompt 加载 + AI 调用 | ⏳ 待开始 |
| Prompt 管理前端 | 3.16-3.17 | Prompt 管理界面 | ⏳ 待开始 |
| 选题 + 内容生成 | 3.17-3.18 | 选题推荐 + 三平台内容 | ⏳ 待开始 |
| 配图 + 历史记录 | 3.19 | 配图生成 + 历史管理 | ⏳ 待开始 |
| MVP 演示 | 3.20 15:00 | 完整功能演示 | ⏳ 待完成 |

---

## 🛠️ 技术栈

### 后端
- Python 3.9+
- FastAPI 0.109+
- SQLAlchemy 2.0
- SQLite（Phase 2）→ MySQL（Phase 3）
- DashScope SDK 1.14+

### 前端
- React 18
- Ant Design 5
- Zustand（状态管理）
- react-markdown

### AI 服务
- DashScope Qwen-Plus（文本生成）
- DashScope 文生图（配图生成）

---

## 📝 文档

### Phase 2 文档

| 文档 | 说明 | 状态 |
|------|------|------|
| [PRD_v2.0.md](docs/PRD_v2.0.md) | 产品需求文档（Prompt 配置化） | ✅ 已更新 |
| [PHASE2_PLAN_v1.0.md](docs/PHASE2_PLAN_v1.0.md) | Phase 2 开发计划 | ✅ 已更新 |

### Phase 1 文档

| 文档 | 说明 | 状态 |
|------|------|------|
| [ARCHITECTURE_v1.0.md](docs/ARCHITECTURE_v1.0.md) | 技术架构文档 | ✅ 已完成 |
| [BACKEND_DEV_v1.0.md](docs/BACKEND_DEV_v1.0.md) | 后端开发文档 | ⏳ 待更新 |
| [FRONTEND_DEV_v1.0.md](docs/FRONTEND_DEV_v1.0.md) | 前端开发文档 | ⏳ 待更新 |
| [TEST_PLAN_v1.0.md](docs/TEST_PLAN_v1.0.md) | 测试计划文档 | ⏳ 待更新 |
| [CROSS_PLATFORM_GUIDE.md](docs/CROSS_PLATFORM_GUIDE.md) | 跨平台适配指南 | ✅ 已完成 |

---

## 👥 团队

| 角色 | 成员 | 职责 |
|------|------|------|
| 项目经理 | 虾虾🦐📋 | 项目管理、需求分析 |
| 架构设计 | 虾虾🦐🏗️ | 技术架构、代码审查 |
| 后端开发 | 虾虾🦐💻 | 后端开发、API 设计 |
| 前端开发 | 虾虾🦐🎨 | 前端开发、UI 实现 |
| 测试运维 | 虾虾🦐🔧 | 测试计划、部署运维 |

---

## 🔧 配置说明

### 后端配置

**编辑文件：** `backend/.env`

```bash
# 数据库配置
DATABASE_URL=sqlite:///./data/content_factory.db

# AI 配置（DashScope 阿里云百炼）
DASHSCOPE_API_KEY=sk-your-api-key
AI_MODEL=qwen-plus

# 服务配置
HOST=0.0.0.0
PORT=8000

# 日志级别
LOG_LEVEL=INFO
```

### 前端配置

**编辑文件：** `frontend/.env`

```bash
# API 地址（开发环境）
REACT_APP_API_URL=http://localhost:8000/api
```

---

## 📞 联系方式

**项目负责人：** 虾虾（项目经理）  
**GitHub：** https://github.com/xuefeng-bai/ai-content-factory

---

## 📄 License

MIT License

---

*AI 内容工厂 - 让内容创作更高效！* 🚀

**最后更新：** 2026-03-13 11:30
