# Windows 环境下安装前端依赖指南

**更新时间：** 2026-03-14 20:15  
**适用系统：** Windows 10/11

---

## 📦 问题说明

**错误信息：**
```
Module not found: Error: Can't resolve 'react-markdown'
Module not found: Error: Can't resolve 'axios'
```

**原因：** package.json 中已添加依赖，但未执行 `npm install` 安装。

---

## ✅ 解决方案

### 步骤 1：打开 PowerShell

按 `Win + X`，选择 **Windows PowerShell** 或 **终端**

---

### 步骤 2：进入前端目录

```powershell
cd D:\bxf\ai-content-factory\frontend
```

---

### 步骤 3：安装依赖

**使用淘宝镜像（推荐，速度快）：**

```powershell
npm install --registry=https://registry.npmmirror.com
```

**或使用官方源：**

```powershell
npm install
```

---

### 步骤 4：等待安装完成

**预期输出：**
```bash
added 1500 packages in 3m

found 0 vulnerabilities
```

**安装时间：** 3-5 分钟（取决于网络速度）

---

### 步骤 5：启动前端服务

```powershell
npm start
```

**预期输出：**
```bash
Compiled successfully!

You can now view ai-content-factory-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

---

## 🔧 常见问题

### 问题 1：npm 安装失败

**错误：** `npm : 无法将"npm"识别为 cmdlet、函数、脚本程序或可运行文件`

**解决方案：** 安装 Node.js

1. 访问 https://nodejs.org/
2. 下载 LTS 版本（推荐 18.x）
3. 安装完成后重启 PowerShell

---

### 问题 2：安装速度慢

**解决方案：** 使用淘宝镜像

```powershell
# 临时使用淘宝镜像
npm install --registry=https://registry.npmmirror.com

# 永久设置淘宝镜像
npm config set registry https://registry.npmmirror.com

# 验证配置
npm config get registry
```

---

### 问题 3：权限错误

**错误：** `EPERM: operation not permitted`

**解决方案：**

1. 关闭所有使用前端目录的程序（VSCode、浏览器等）
2. 以管理员身份运行 PowerShell
3. 重新执行安装命令

---

### 问题 4：node_modules 冲突

**错误：** 各种奇怪的编译错误

**解决方案：** 清理重装

```powershell
# 删除 node_modules
rmdir /s /q node_modules

# 删除 package-lock.json
del package-lock.json

# 清空 npm 缓存
npm cache clean --force

# 重新安装
npm install --registry=https://registry.npmmirror.com
```

---

## 📋 验证安装

安装完成后，检查以下文件是否存在：

```powershell
# 检查 axios
ls node_modules\axios

# 检查 react-markdown
ls node_modules\react-markdown
```

如果目录存在，说明安装成功。

---

## 🎯 快速命令汇总

```powershell
# 进入项目目录
cd D:\bxf\ai-content-factory\frontend

# 安装依赖（淘宝镜像）
npm install --registry=https://registry.npmmirror.com

# 启动开发服务器
npm start

# 构建生产版本
npm run build

# 运行测试
npm test
```

---

## 📝 依赖清单

**新增依赖：**
- axios ^1.6.0 - HTTP 客户端
- react-markdown ^9.0.0 - Markdown 渲染

**已有依赖：**
- react ^18.2.0
- react-dom ^18.2.0
- react-router-dom ^6.20.0
- antd ^5.12.0
- @ant-design/icons ^5.2.6
- react-scripts 5.0.1

---

## ✅ 成功标志

安装成功后，访问 http://localhost:3000 应该看到：

- ✅ 前端页面正常加载
- ✅ 无编译错误
- ✅ 可以正常访问各个页面

---

**安装完成后，请截图反馈！** 🦐
