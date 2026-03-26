# Windows 使用指南

## 🚀 快速开始

### 方式 1：使用启动脚本（推荐）⭐

**初始化数据库：**
```powershell
# 双击运行或在命令行执行
.\init-db.bat
```

**启动后端服务：**
```powershell
.\start-backend.bat
```

**启动前端服务：**
```powershell
.\start-frontend.bat
```

---

### 方式 2：手动启动

#### 1. 环境准备

**安装 Python 3.9+：**
```powershell
# 检查 Python 版本
python --version
# 应该显示：Python 3.9.x 或更高
```

**安装 Node.js 18+：**
```powershell
# 检查 Node.js 版本
node --version
# 应该显示：v18.x.x 或更高
```

#### 2. 后端配置

```powershell
# 进入 backend 目录
cd D:\bxf\ai-content-factory\backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
.\venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
copy .env.example .env
notepad .env
```

**.env 配置示例：**
```ini
# 数据库配置
DATABASE_TYPE=sqlite
DATABASE_URL=sqlite:///./ai_content_factory.db

# AI API 配置
CLAUDE_API_KEY=sk-ant-你的 claude 密钥
TONGYI_API_KEY=你的通义千问密钥
TONGYI_WANXIANG_API_KEY=你的通义万相密钥
DEFAULT_AI_PROVIDER=claude

# 服务器配置
HOST=0.0.0.0
PORT=8000
```

#### 3. 初始化数据库

**推荐方式（使用 -m 参数）：**
```powershell
cd backend
python -m app.utils.init_db
```

**或者使用批处理脚本：**
```powershell
.\init-db.bat
```

**预期输出：**
```
🔧 开始初始化数据库...
✅ 数据库表创建完成！

📊 已创建的表：
  - content_generations (内容生成记录表)
  - content_items (内容项表)
  - cover_images (封面图表)
  - prompt_templates (提示词模板表)
  - system_configs (系统配置表)

📝 插入默认提示词模板...
✅ 默认模板插入完成！

✨ 数据库初始化完成！
```

#### 4. 启动后端

```powershell
cd backend
.\venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**或者使用批处理脚本：**
```powershell
.\start-backend.bat
```

**访问 API 文档：** http://localhost:8000/docs

#### 5. 启动前端

```powershell
cd frontend
npm install
npm run dev
```

**或者使用批处理脚本：**
```powershell
.\start-frontend.bat
```

**访问前端：** http://localhost:3000

---

## ⚠️ 常见问题

### 问题 1：ModuleNotFoundError: No module named 'app'

**原因：** Python 路径问题

**解决方案：**
```powershell
# 使用 -m 参数运行
python -m app.utils.init_db

# 或者设置 PYTHONPATH
$env:PYTHONPATH="."
python app/utils/init_db.py
```

### 问题 2：权限错误

**原因：** PowerShell 执行策略限制

**解决方案：**
```powershell
# 以管理员身份运行 PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 然后重新激活虚拟环境
.\venv\Scripts\activate
```

### 问题 3：端口被占用

**原因：** 8000 或 3000 端口已被使用

**解决方案：**
```powershell
# 查找占用端口的进程
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# 终止进程（替换 PID）
taskkill /F /PID <PID>
```

### 问题 4：npm install 失败

**原因：** 网络问题或 Node 版本不兼容

**解决方案：**
```powershell
# 使用淘宝镜像
npm config set registry https://registry.npmmirror.com

# 重新安装
npm install
```

### 问题 5：中文乱码

**原因：** Windows 编码问题

**解决方案：**
```powershell
# 设置 UTF-8 编码
chcp 65001

# 或在 PowerShell 配置文件中添加
$PSDefaultParameterValues['Out-File:Encoding'] = 'UTF8'
```

---

## 📝 开发流程

### 1. 启动开发环境

```powershell
# 终端 1：启动后端
.\start-backend.bat

# 终端 2：启动前端
.\start-frontend.bat
```

### 2. 数据库迁移

```powershell
# 修改模型后重新初始化
.\init-db.bat
```

### 3. 运行测试

```powershell
# 后端测试（待添加）
cd backend
pytest

# 前端测试（待添加）
cd frontend
npm test
```

---

## 📦 项目结构

```
ai-content-factory/
├── init-db.bat              # 数据库初始化脚本
├── start-backend.bat        # 后端启动脚本
├── start-frontend.bat       # 前端启动脚本
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI 入口
│   │   ├── api/             # API 路由
│   │   ├── models/          # 数据库模型
│   │   ├── services/        # 业务逻辑
│   │   └── utils/           # 工具函数
│   ├── requirements.txt     # Python 依赖
│   └── .env.example         # 环境变量示例
└── frontend/
    ├── src/
    │   ├── app/             # Next.js 页面
    │   └── api/             # API 客户端
    ├── package.json         # Node 依赖
    └── tsconfig.json        # TypeScript 配置
```

---

## 🎯 下一步

1. **配置 AI 服务** - 编辑 `.env` 文件，填写 API Key
2. **测试功能** - 访问 http://localhost:3000 测试生成
3. **查看文档** - API 文档 http://localhost:8000/docs

---

## 📞 获取帮助

如有问题，请检查：
1. Python 版本 >= 3.9
2. Node.js 版本 >= 18
3. 虚拟环境已激活
4. 依赖已安装
5. 端口未被占用

---

**祝开发顺利！** 🚀
