# ⚙️ AI 内容工厂 v1.0.0 - 后端开发文档

**文档版本：** v1.0.0  
**创建日期：** 2026-03-12  
**文档作者：** 后端开发虾 🦐💻  
**审核状态：** 待审核

---

## 1. 开发环境

### 1.1 环境要求

- Python 3.9+
- MySQL 8.0
- Node.js 18+（前端）

### 1.2 跨平台适配要求

**⚠️ 重要：代码必须在 Windows 和 Linux 上都能运行！**

**文件路径处理：**
```python
# ✅ 正确：使用 pathlib
from pathlib import Path
db_path = Path(__file__).parent / "data" / "daily_brief.db"

# ❌ 错误：硬编码路径分隔符
db_path = "/home/admin/data/daily_brief.db"  # Linux 路径
db_path = "C:\\Users\\admin\\data\\daily_brief.db"  # Windows 路径
```

**命令行调用：**
```python
# ✅ 正确：使用 sys.executable
import sys
subprocess.run([sys.executable, "script.py"])

# ❌ 错误：硬编码 python 命令
subprocess.run(["python3", "script.py"])  # Windows 上不行
```

**编码格式：**
```python
# ✅ 正确：明确指定 UTF-8
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()

# ❌ 错误：使用默认编码（Windows 是 GBK）
with open("file.txt", "r") as f:  # Windows 会报错
    content = f.read()
```

### 1.3 依赖安装

**Windows：**
```bash
pip install fastapi uvicorn sqlalchemy dashscope
```

**Linux：**
```bash
pip install fastapi uvicorn sqlalchemy dashscope
```

**注意：** `requirements.txt` 必须用英文注释（避免编码问题）

---

## 2. 爬虫模块

### 2.1 微博热搜爬虫

```python
class WeiboSpider:
    - URL: https://s.weibo.com/top/summary
    - 反爬对策：UA 轮换 + 间隔 3 秒
    - 输出：热搜榜列表（标题、热度、排名）
```

### 2.2 知乎热榜爬虫

```python
class ZhihuSpider:
    - URL: https://www.zhihu.com/hot
    - 反爬对策：Cookie 管理 + 间隔 5 秒
    - 输出：热榜列表（问题、热度、排名）
```

---

## 3. AI 模块

### 3.1 选题推荐 Prompt

```
你是专业的内容策划专家。请根据以下搜索素材，推荐 3-5 个选题角度。

搜索素材：
{search_results}

请按以下格式输出：
1. 选题标题
   类型：[工具推荐/认知差/案例分享/观点输出]
   优势：[一句话说明]
   推荐度：⭐⭐⭐⭐⭐
```

### 3.2 内容生成 Prompt

**抖音口播：**
```
你是专业的短视频口播文案创作者。
要求：口语化、有钩子开头、金句结尾、500-600 字。
主题：{topic}
```

**公众号文章：**
```
你是资深新媒体编辑。
要求：结构清晰、Markdown 格式、2000 字左右。
主题：{topic}
```

**小红书笔记：**
```
你是小红书爆款内容创作者。
要求：吸引眼球的标题、种草风格、带 emoji 和标签。
主题：{topic}
```

---

## 4. API 接口

### 4.1 搜索接口

```python
POST /api/search
Request: { "theme": "AI 效率" }
Response: { "results": [...], "topics": [...] }
```

### 4.2 内容生成接口

```python
POST /api/content/generate
Request: { "topic": "...", "platform": "douyin" }
Response: { "content": "...", "images": [...] }
```

---

## 5. 开发计划

| 任务 | 时间 | 状态 |
|------|------|------|
| 微博爬虫 | 2 天 | ⏳ |
| 知乎爬虫 | 1 天 | ⏳ |
| AI 集成 | 1 天 | ⏳ |
| Prompt 调优 | 3 天 | ⏳ |
| API 开发 | 3 天 | ⏳ |

---

**审核人：** 架构设计虾、测试运维虾  
**审核日期：** 2026-03-12
