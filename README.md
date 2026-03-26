# AI 内容工厂 v1.0

**AI 驱动的多平台内容生成工具**

---

## 🚀 项目简介

AI 内容工厂是一款**AI 驱动的多平台内容生成工具**。用户只需输入一个主题，系统即可自动生成适配抖音、视频号、公众号、小红书四个主流平台的内容及封面图。

### 核心价值

- ⚡ **高效** - 5 分钟完成原本 2 小时的内容创作工作
- 🎯 **精准** - 各平台风格自适应，无需手动调整
- ✏️ **灵活** - 支持 Markdown 编辑，内容可控可调
- 🔧 **可扩展** - 支持自定义提示词模板，满足个性化需求
- 🛡️ **稳定** - 容错机制完善，单平台失败不影响整体

---

## 📦 技术栈

### 后端
- **框架:** FastAPI 0.100
- **语言:** Python 3.9.11
- **ORM:** SQLAlchemy 2.0
- **数据库:** SQLite (开发) / MySQL 8.0+ (生产)
- **AI 服务:** Claude API + 通义千问 (双备份)
- **图片生成:** 通义万相

### 前端
- **框架:** React 18 + Next.js 14
- **UI 组件:** Shadcn/ui + Tailwind CSS 3
- **Markdown 编辑器:** @uiw/react-md-editor
- **HTTP 客户端:** Axios

---

## 🏗️ 项目结构

```
ai-content-factory/
├── backend/              # 后端 FastAPI 项目
│   ├── app/
│   │   ├── main.py       # FastAPI 入口
│   │   ├── api/          # API 路由
│   │   ├── models/       # 数据库模型
│   │   ├── services/     # 业务逻辑
│   │   └── utils/        # 工具函数
│   ├── tests/            # 测试用例
│   ├── requirements.txt
│   └── .env.example
├── frontend/             # 前端 Next.js 项目
│   ├── src/
│   │   ├── app/          # Next.js 14 App Router
│   │   ├── components/   # 可复用组件
│   │   ├── api/          # API 客户端
│   │   └── styles/       # 样式文件
│   ├── public/           # 静态资源
│   ├── package.json
│   └── next.config.js
└── docs/                 # 技术文档
```

---

## 🛠️ 快速开始

### 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 复制配置文件
cp .env.example .env
# 编辑 .env 配置 API Key

# 初始化数据库
python app/utils/init_db.py

# 启动服务
python app/main.py
# 或：uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000/docs 查看 API 文档

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 配置环境变量
cp .env.local.example .env.local

# 启动开发服务
npm run dev
```

访问 http://localhost:3000

---

## 📊 数据库设计

### 5 张核心表

1. **content_generations** - 内容生成记录表（主任务）
2. **content_items** - 内容项表（各平台内容）
3. **cover_images** - 封面图表
4. **prompt_templates** - 提示词模板表
5. **system_configs** - 系统配置表

详见：`docs/TECH_DESIGN.md`

---

## 🔌 API 接口

### 内容模块
- `POST /api/v1/content/generate` - 一键生成 4 平台内容
- `GET /api/v1/content/{id}` - 获取生成内容详情
- `PUT /api/v1/content/{id}` - 更新内容（编辑）
- `POST /api/v1/content/{id}/regenerate` - 重新生成某平台内容
- `GET /api/v1/content/history` - 获取历史记录列表
- `DELETE /api/v1/content/{id}` - 删除生成记录

### 模板模块
- `GET /api/v1/templates` - 获取提示词模板列表
- `POST /api/v1/templates` - 创建提示词模板
- `PUT /api/v1/templates/{id}` - 更新提示词模板
- `DELETE /api/v1/templates/{id}` - 删除提示词模板

### 配置模块
- `GET /api/v1/configs` - 获取系统配置列表
- `PUT /api/v1/configs/{key}` - 更新系统配置

---

## 📱 功能特性

### 核心功能
- ✅ 一键生成 4 平台内容（逐一生成，容错机制）
- ✅ AI 封面图生成（各平台合规尺寸）
- ✅ Markdown 在线编辑 + 实时预览
- ✅ 单平台重新生成
- ✅ 一键复制内容
- ✅ 提示词模板管理
- ✅ AI 服务配置（双备份）

### 辅助功能
- 🟡 敏感词检测（本地词库）
- 🟡 历史记录管理（搜索、删除）

---

## 📅 开发计划

### 5 天冲刺（3.25-3.29）

| 日期 | 阶段 | 核心任务 |
|------|------|----------|
| 周三 (3.25) | 启动日 | 技术方案评审 + 项目初始化 ✅ |
| 周四 (3.26) | 开发 Day1 | 后端：数据库 + API 框架<br>前端：项目搭建 + 首页框架 |
| 周五 (3.27) | 开发 Day2 | 后端：内容生成核心逻辑<br>前端：结果页 + Markdown 编辑器 |
| 周六 (3.28) | 开发 Day3 | 后端：提示词模板 + 配置模块<br>前端：历史记录 + 模板管理页 |
| 周日 (3.29) | 收尾日 | 联调测试 + Bug 修复 + 部署演示 |

---

## 👥 项目团队（虾虾军团）

| 角色 | 昵称 | 职责 |
|------|------|------|
| 📋 项目经理 | 虾虾 | 进度跟踪、资源协调、产品验收 |
| 🏗️ 架构设计 | 架构虾 | 技术方案、数据库设计、代码审查 |
| 🔧 后端开发 | 后端虾 | FastAPI 接口、数据库、AI 服务对接 |
| 🎨 前端开发 | 前端虾 | React/Next.js 页面、Markdown 编辑器 |
| 🧪 测试运维 | 测试虾 | 测试用例、Bug 检查、部署配置 |

---

## 📝 相关文档

- [技术方案设计](docs/TECH_DESIGN.md)
- [产品需求文档](../ai-content-factory-prd-v1.2.md)

---

## ⚠️ 注意事项

1. **API Key 配置** - 请在 `.env` 文件中配置 AI 服务密钥
2. **数据库初始化** - 首次启动需运行 `init_db.py` 创建表结构
3. **CORS 配置** - 开发环境允许所有来源，生产环境需限制
4. **跨平台路径** - 代码中使用 `pathlib` 处理路径，兼容 Windows/Linux

---

## 📄 许可证

MIT License

---

**最后更新：** 2026-03-25 17:40
