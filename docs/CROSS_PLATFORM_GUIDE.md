# 🔄 跨平台适配补充说明

**创建日期：** 2026-03-12  
**文档作者：** 架构设计虾 🦐🏗️  
**优先级：** P0（老板要求）

---

## 📋 跨平台适配要求

**目标：** 代码在 Windows 和 Linux 上都能正常运行

---

## ✅ 必须遵守的规则

### 1. 文件路径处理

**✅ 正确做法：**
```python
from pathlib import Path

# 使用 pathlib 自动适配路径分隔符
db_path = Path(__file__).parent / "data" / "daily_brief.db"
config_path = Path.cwd() / "config" / "settings.json"

# 或使用 os.path
import os
db_path = os.path.join(os.path.dirname(__file__), "data", "daily_brief.db")
```

**❌ 错误做法：**
```python
# 硬编码 Linux 路径
db_path = "/home/admin/data/daily_brief.db"

# 硬编码 Windows 路径
db_path = "C:\\Users\\admin\\data\\daily_brief.db"

# 混用路径分隔符
db_path = "data/daily_brief.db"  # Windows 可能不兼容
```

---

### 2. 命令行调用

**✅ 正确做法：**
```python
import sys
import subprocess

# 使用 sys.executable 获取当前 Python 解释器
subprocess.run([sys.executable, "script.py"])

# 或使用 python 命令（不指定版本）
subprocess.run(["python", "script.py"])
```

**❌ 错误做法：**
```python
# 指定 Python 版本（Windows 上可能没有）
subprocess.run(["python3", "script.py"])
subprocess.run(["python3.9", "script.py"])

# 使用绝对路径
subprocess.run(["/usr/bin/python3", "script.py"])
```

---

### 3. 文件编码

**✅ 正确做法：**
```python
# 明确指定 UTF-8 编码
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()

with open("file.txt", "w", encoding="utf-8") as f:
    f.write("内容")
```

**❌ 错误做法：**
```python
# 使用默认编码（Windows 是 GBK，Linux 是 UTF-8）
with open("file.txt", "r") as f:
    content = f.read()

# 在代码中使用中文注释（配置文件）
# requirements.txt 中：
# fastapi==0.109  # 快速 API 框架  ❌ 中文注释会导致 Windows 安装失败
```

---

### 4. 环境变量

**✅ 正确做法：**
```python
import os

# 使用 os.getenv 获取环境变量
db_url = os.getenv("DATABASE_URL", "sqlite:///./data/daily_brief.db")

# 使用 pathlib 处理路径
data_dir = Path(os.getenv("DATA_DIR", Path.cwd() / "data"))
```

**❌ 错误做法：**
```python
# 硬编码路径
db_url = "sqlite:////home/admin/data/daily_brief.db"

# 依赖特定环境变量
db_url = os.environ["DATABASE_URL"]  # 如果未设置会报错
```

---

### 5. 换行符处理

**✅ 正确做法：**
```python
# 使用 Python 自动处理换行符
with open("file.txt", "w", newline=None) as f:
    f.write("内容")

# 或使用 os.linesep
import os
content = f"第一行{os.linesep}第二行"
```

**❌ 错误做法：**
```python
# 硬编码 Linux 换行符
content = "第一行\n第二行"

# 硬编码 Windows 换行符
content = "第一行\r\n第二行"
```

---

## 📋 跨平台测试清单

### 开发环境测试

| 测试项 | Windows | Linux | 状态 |
|--------|---------|-------|------|
| Python 环境搭建 | ✅ | ✅ | 待测试 |
| 依赖安装 | ✅ | ✅ | 待测试 |
| 数据库初始化 | ✅ | ✅ | 待测试 |
| 爬虫运行 | ✅ | ✅ | 待测试 |
| AI 内容生成 | ✅ | ✅ | 待测试 |
| 配图生成 | ✅ | ✅ | 待测试 |

### 代码审查检查点

| 检查项 | 说明 | 状态 |
|--------|------|------|
| 路径处理 | 使用 pathlib 或 os.path | ⏳ |
| 命令行调用 | 使用 sys.executable | ⏳ |
| 文件编码 | 明确指定 UTF-8 | ⏳ |
| 中文注释 | 配置文件无中文 | ⏳ |
| 环境变量 | 使用 os.getenv | ⏳ |

---

## 🛠️ 开发工具推荐

### Windows 开发环境

```bash
# 使用 Git Bash 或 WSL（避免 PowerShell 编码问题）
# 或使用 VSCode 内置终端

# 设置默认编码为 UTF-8
# 系统环境变量：PYTHONUTF8=1
```

### Linux 开发环境

```bash
# 默认 UTF-8 编码，无需额外配置
# 确保 Python 3.9+
python --version
```

---

## 📞 团队承诺

**架构设计虾：**
> "我会在代码审查中严格检查跨平台适配，发现一个硬编码路径就打回！"

**后端开发虾：**
> "我会使用 pathlib 处理所有路径，确保 Windows 和 Linux 都能运行！"

**前端开发虾：**
> "前端代码本身跨平台，但我会注意文件路径和构建脚本的兼容性！"

**测试运维虾：**
> "我会在 Windows 和 Linux 上都进行测试，确保跨平台兼容性！"

---

**创建时间：** 2026-03-12 19:30  
**优先级：** P0（老板要求）

---

**所有开发人员必须遵守以上跨平台适配规则！** 🦐💪
