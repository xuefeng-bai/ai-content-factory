# Windows 安装指南（Python 3.9.11）

## 📦 环境要求

- **Python:** 3.9.11（必须）
- **Node.js:** 18.x 或更高
- **Git:** 最新版

---

## 🚀 安装步骤

### 1. 安装 Python 3.9.11

**下载地址：** https://www.python.org/downloads/release/python-3911/

**安装选项：**
- ✅ 勾选 "Add Python 3.9 to PATH"
- ✅ 勾选 "Install launcher for all users"
- ✅ 勾选 "Precompile standard library"

**验证安装：**
```powershell
python --version
# 应该显示：Python 3.9.11
```

---

### 2. 克隆项目

```powershell
# 进入项目目录
cd D:\bxf

# 克隆仓库（如果还没有）
git clone https://github.com/xuefeng-bai/ai-content-factory.git

# 进入项目
cd ai-content-factory
```

---

### 3. 安装后端依赖

```powershell
# 进入 backend 目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
.\venv\Scripts\activate

# 升级 pip
python -m pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt

# 验证安装
pip list | Select-String "fastapi|sqlalchemy|pydantic"
```

**预期输出：**
```
fastapi             0.100.0
pydantic            2.5.0
sqlalchemy          2.0.0
```

---

### 4. 初始化数据库

```powershell
# 在 backend 目录下
python -m app.utils.init_db
```

**预期输出：**
```
🔧 开始初始化数据库...
✅ 数据库表创建完成！

📊 已创建的表：
  - content_generations
  - content_items
  - cover_images
  - prompt_templates
  - system_configs

📝 插入默认提示词模板...
✅ 默认模板插入完成！

✨ 数据库初始化完成！
```

---

### 5. 启动后端

```powershell
# 在 backend 目录下
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**访问 API 文档：** http://localhost:8000/docs

---

### 6. 安装前端依赖

```powershell
# 新终端窗口
cd D:\bxf\ai-content-factory\frontend

# 安装依赖
npm install

# 验证安装
npm list --depth=0
```

---

### 7. 启动前端

```powershell
# 在 frontend 目录下
npm run dev
```

**访问前端：** http://localhost:3000

---

## 🐛 常见问题

### 问题 1：pip install 失败

**错误：** 无法下载依赖包

**解决方案：**
```powershell
# 使用国内镜像
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install -r requirements.txt
```

---

### 问题 2：ModuleNotFoundError

**错误：** `No module named 'app'`

**解决方案：**
```powershell
# 确保在 backend 目录下
cd D:\bxf\ai-content-factory\backend

# 使用 -m 参数运行
python -m app.utils.init_db
```

---

### 问题 3：端口被占用

**错误：** `Address already in use`

**解决方案：**
```powershell
# 查找占用端口的进程
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# 终止进程（替换 PID）
taskkill /F /PID <PID>
```

---

### 问题 4：虚拟环境激活失败

**错误：** 无法加载脚本

**解决方案：**
```powershell
# 以管理员身份运行 PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 重新激活
.\venv\Scripts\activate
```

---

## ✅ 验证清单

- [ ] Python 版本是 3.9.11
- [ ] 虚拟环境已激活
- [ ] 依赖已安装（fastapi, sqlalchemy, pydantic）
- [ ] 数据库初始化成功
- [ ] 后端可以启动（http://localhost:8000/docs）
- [ ] 前端可以启动（http://localhost:3000）

---

**祝安装顺利！** 🎉
