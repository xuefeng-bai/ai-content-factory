# 🚨 紧急修复 - dashscope 导入错误

**错误时间：** 2026-03-15 09:43  
**错误信息：** `ModuleNotFoundError: No module named 'dashscope.aigc.image_synthesis'`

---

## ⚠️ 问题原因

**你的 dashscope 版本不支持 `ImageSynthesis` 模块！**

可能原因：
1. dashscope 版本太旧（< 1.10.0）
2. dashscope 版本太新（API 已变更）
3. 安装不完整

---

## ✅ 立即修复步骤

### 步骤 1：停止后端服务

按 `Ctrl+C` 停止当前运行的后端

### 步骤 2：卸载旧版本

```bash
cd D:\bxf\ai-content-factory\backend

# 如果有虚拟环境
venv\Scripts\activate

# 卸载旧版本
pip uninstall dashscope -y
```

### 步骤 3：安装指定版本

```bash
# 安装 1.14.1 版本
pip install dashscope==1.14.1 -i https://mirrors.aliyun.com/pypi/simple/
```

### 步骤 4：验证安装

```bash
python -c "from dashscope import ImageSynthesis; print('✅ 安装成功')"
```

### 步骤 5：重启后端

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🔍 如果仍然失败

### 方案 A：使用备用导入（代码已修复）

**最新代码已修复兼容性导入：**

```python
# backend/app/ai/service.py
try:
    from dashscope import ImageSynthesis
except (ImportError, ModuleNotFoundError):
    try:
        from dashscope.aigc.image_synthesis import ImageSynthesis
    except (ImportError, ModuleNotFoundError):
        ImageSynthesis = None
        print("Warning: ImageSynthesis not available")
```

**拉取最新代码：**
```bash
cd D:\bxf\ai-content-factory
git pull origin main
```

### 方案 B：检查 Python 版本

```bash
python --version
```

**要求：** Python 3.8 或 3.9

### 方案 C：使用国内镜像源

```bash
pip install dashscope==1.14.1 -i https://mirrors.aliyun.com/pypi/simple/
```

---

## 📝 完整命令清单（复制粘贴执行）

```bash
# 1. 进入后端目录
cd D:\bxf\ai-content-factory\backend

# 2. 激活虚拟环境（如果有）
venv\Scripts\activate

# 3. 卸载旧版本
pip uninstall dashscope -y

# 4. 安装指定版本
pip install dashscope==1.14.1 -i https://mirrors.aliyun.com/pypi/simple/

# 5. 验证安装
python -c "from dashscope import ImageSynthesis; print('✅ 成功')"

# 6. 重启后端
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🎯 预期输出

**安装成功：**
```
Successfully installed dashscope-1.14.1
```

**导入成功：**
```
✅ 成功
```

**后端启动成功：**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

---

## 📞 如果还有问题

**提供以下信息：**

1. **Python 版本：** `python --version`
2. **dashscope 版本：** `pip show dashscope`
3. **完整错误信息**
4. **操作系统：** Windows 版本

---

*紧急修复指南生成时间：2026-03-15 09:45*
