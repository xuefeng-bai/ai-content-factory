# 🎨 AI 内容工厂 - AI Content Factory

**版本号：** v1.0.0  
**创建日期：** 2026-03-12  
**项目状态：** 开发中（Phase 1）

---

## 📋 项目简介

AI 驱动的全流程内容创作系统，实现一次选题多平台内容自动生成。

**核心价值：** 每次创作节省约 3.5 小时！

---

## 🎯 功能特性

- ✅ **AI 联网搜索** - 微博热搜 + 知乎热榜
- ✅ **智能选题推荐** - 3-5 个选题角度
- ✅ **多平台内容生成** - 抖音 + 公众号 + 小红书
- ✅ **AI 配图生成** - 最多 3 张智能配图
- ✅ **历史内容管理** - 随时查看和复用
- ✅ **跨平台支持** - Windows + Linux + Mac

---

## 🚀 快速开始

### 环境要求

- Python 3.9+
- MySQL 8.0
- Node.js 18+（前端）

### 后端启动

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 启动服务
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm start
```

---

## 📁 项目结构

```
ai-content-factory/
├── backend/                 # 后端（Python + FastAPI）
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── models/         # 数据库模型
│   │   ├── services/       # 业务逻辑
│   │   ├── crawler/        # 爬虫模块
│   │   └── ai/             # AI 服务
│   ├── data/               # 数据库文件
│   ├── tests/              # 测试代码
│   └── requirements.txt    # Python 依赖
├── frontend/               # 前端（React + Ant Design）
│   ├── src/
│   │   ├── components/     # 组件
│   │   ├── pages/          # 页面
│   │   ├── stores/         # 状态管理
│   │   └── services/       # API 服务
│   └── package.json        # Node 依赖
├── docs/                   # 文档
├── scripts/                # 脚本工具
└── README.md              # 项目说明
```

---

## 📅 开发计划

| 阶段 | 时间 | 功能 | 状态 |
|------|------|------|------|
| **Phase 1** | 3.12-3.20 | MVP（微博 + 知乎搜索 + 内容生成） | 🔄 进行中 |
| **Phase 2** | 3.20-4.02 | 优化（模板管理 + 批量生成） | ⏳ 待开始 |
| **Phase 3** | 4.02-4.09 | 自动化（API 对接 + 定时发布） | ⏳ 待开始 |

---

## 📊 里程碑

| 里程碑 | 日期 | 交付物 | 状态 |
|--------|------|--------|------|
| 项目启动 | 3.12 | 技术文档 + 环境就绪 | ✅ 已完成 |
| 爬虫完成 | 3.14 | 微博 + 知乎爬虫 | ⏳ 待完成 |
| AI 集成完成 | 3.15 | 搜索 + 选题 + 内容生成 | ⏳ 待完成 |
| 前后端完成 | 3.19 | 完整功能开发 | ⏳ 待完成 |
| MVP 演示 | 3.20 | 可演示版本 | ⏳ 待完成 |

---

## 🛠️ 技术栈

### 后端
- Python 3.9+
- FastAPI
- SQLAlchemy 2.0
- MySQL 8.0
- DashScope SDK

### 前端
- React 18
- Ant Design 5
- Zustand（状态管理）
- react-markdown

### AI 服务
- DashScope Qwen-Plus（内容生成）
- DashScope 文生图（配图生成）

---

## 📝 文档

| 文档 | 说明 | 状态 |
|------|------|------|
| [PRD_v1.0.md](docs/PRD_v1.0.md) | 产品需求文档 | ✅ 已完成 |
| [ARCHITECTURE_v1.0.md](docs/ARCHITECTURE_v1.0.md) | 技术架构文档 | ✅ 已完成 |
| [BACKEND_DEV_v1.0.md](docs/BACKEND_DEV_v1.0.md) | 后端开发文档 | ✅ 已完成 |
| [FRONTEND_DEV_v1.0.md](docs/FRONTEND_DEV_v1.0.md) | 前端开发文档 | ✅ 已完成 |
| [TEST_PLAN_v1.0.md](docs/TEST_PLAN_v1.0.md) | 测试计划文档 | ✅ 已完成 |
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

## 📞 联系方式

**项目负责人：** 虾虾（项目经理）  
**邮箱：** [待填写]  
**GitHub：** [待填写]

---

*AI 内容工厂 - 让内容创作更高效！* 🚀
