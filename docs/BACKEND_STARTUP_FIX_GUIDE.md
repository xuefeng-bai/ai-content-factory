# 🔧 后端启动错误修复指南

**错误时间：** 2026-03-15 09:39  
**错误信息：** `ImportError: cannot import name 'ImageSynthesis' from 'dashscope'`

---

## 🐛 问题原因

**环境：** Windows (Python 3.9)  
**错误文件：** `backend/app/ai/service.py` 第 15 行

```python
from dashscope import ImageSynthesis
```

**原因：** dashscope 库版本不同，导入路径可能不同

---

## ✅ 解决方案

### 方案 1：更新 dashscope 到最新版本（推荐）

**在 Windows 后端目录执行：**

```bash
cd D:\bxf\ai-content-factory\backend

# 激活虚拟环境（如果有）
venv\Scripts\activate

# 或者使用全局 Python
# 升级 dashscope
pip install --upgrade dashscope -i https://mirrors.aliyun.com/pypi/simple/

# 或者重新安装指定版本
pip install dashscope==1.14.1 -i https://mirrors.aliyun.com/pypi/simple/
```

---

### 方案 2：修改导入方式（兼容性更好）

**修改文件：** `backend/app/ai/service.py`

**第 15 行修改：**

```python
# 原代码（第 15 行）
from dashscope import ImageSynthesis

# 修改为
from dashscope.aigc.image_synthesis import ImageSynthesis
```

**或者使用动态导入：**

```python
# 第 15-18 行修改为
try:
    from dashscope import ImageSynthesis
except ImportError:
    from dashscope.aigc.image_synthesis import ImageSynthesis
```

---

### 方案 3：检查 dashscope 版本

**查看已安装版本：**

```bash
cd D:\bxf\ai-content-factory\backend
pip show dashscope
```

**预期输出：**
```
Name: dashscope
Version: 1.14.1
Location: ...
```

**如果版本不是 1.14.1，重新安装：**

```bash
pip uninstall dashscope
pip install dashscope==1.14.1 -i https://mirrors.aliyun.com/pypi/simple/
```

---

## 📝 完整修复步骤（Windows）

### 步骤 1：停止后端服务

按 `Ctrl+C` 停止当前运行的后端服务

### 步骤 2：检查并修复 dashscope

```bash
# 进入后端目录
cd D:\bxf\ai-content-factory\backend

# 如果有虚拟环境，激活它
venv\Scripts\activate

# 查看 dashscope 版本
pip show dashscope

# 升级或重新安装
pip install --upgrade dashscope -i https://mirrors.aliyun.com/pypi/simple/
```

### 步骤 3：测试导入

```bash
python -c "from dashscope import ImageSynthesis; print('✅ 导入成功')"
```

### 步骤 4：重启后端

```bash
# 如果使用虚拟环境
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 或者直接使用 python
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🔍 验证后端启动成功

**预期输出：**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx]
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**测试 API：**

打开浏览器访问：
- http://localhost:8000/docs - Swagger API 文档
- http://localhost:8000/api/prompts - Prompt 列表

---

## 💡 预防措施

### 更新 requirements.txt

确保 `backend/requirements.txt` 包含明确版本号：

```txt
# AI Service
dashscope==1.14.1
```

### 使用虚拟环境

**创建虚拟环境（如果还没有）：**

```bash
cd D:\bxf\ai-content-factory\backend
python -m venv venv
```

**激活虚拟环境：**

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**安装依赖：**

```bash
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

---

## 📞 如果问题仍然存在

1. **提供完整错误信息**
2. **查看 dashscope 版本：** `pip show dashscope`
3. **查看 Python 版本：** `python --version`
4. **尝试手动导入测试：**
   ```bash
   python -c "import dashscope; print(dashscope.__version__)"
   python -c "from dashscope import ImageSynthesis"
   ```

---

*修复指南生成时间：2026-03-15 09:45*  
*AI 内容工厂 - 让内容创作更高效！*
