# 📝 AI 内容工厂 - 后端开发规范

**文档版本：** v1.0.0  
**创建日期：** 2026-03-13  
**文档作者：** 架构设计虾 🦐🏗️  
**适用范围：** Phase 2 及后续后端开发

---

## 一、项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置管理
│   ├── ai/                  # AI 服务层
│   │   ├── __init__.py
│   │   ├── service.py       # AIService 核心
│   │   └── prompts.py       # Prompt 加载器
│   ├── api/                 # API 接口层
│   │   ├── __init__.py
│   │   ├── prompts.py       # Prompt 管理 API
│   │   ├── topics.py        # 选题 API
│   │   ├── content.py       # 内容生成 API
│   │   └── images.py        # 配图 API
│   ├── data/                # 数据层
│   │   ├── __init__.py
│   │   ├── schema.sql       # 数据库结构
│   │   ├── seed_prompts.sql # Prompt 初始化
│   │   └── migrate_v1.py    # 迁移脚本
│   ├── models/              # 数据模型
│   │   └── __init__.py
│   ├── services/            # 业务逻辑
│   │   └── __init__.py
│   └── crawler/             # 爬虫模块
│       ├── __init__.py
│       ├── weibo.py         # 微博爬虫
│       └── zhihu.py         # 知乎爬虫
├── data/                    # 数据库文件
│   └── content_factory.db
├── tests/                   # 测试代码
│   ├── __init__.py
│   ├── test_ai_service.py
│   └── test_prompts.py
├── .env                     # 环境变量（不提交）
├── .env.example             # 环境变量模板
├── requirements.txt         # Python 依赖
└── README.md                # 后端说明
```

---

## 二、代码规范

### 1. 命名规范

**文件命名：**
- ✅ 小写字母 + 下划线：`prompt_loader.py`
- ❌ 大写字母：`PromptLoader.py`
- ❌ 驼峰命名：`promptLoader.py`

**类命名：**
- ✅ 大驼峰：`class AIService`, `class PromptLoader`
- ❌ 小写：`class aiService`

**函数命名：**
- ✅ 小写 + 下划线：`def get_prompt()`, `def validate_variables()`
- ❌ 大驼峰：`def GetPrompt()`

**常量命名：**
- ✅ 全大写 + 下划线：`AI_TEXT_TIMEOUT = 30`
- ❌ 小写：`aiTextTimeout = 30`

---

### 2. 注释规范

**所有代码必须使用英文注释！**

**模块文档字符串：**
```python
# -*- coding: utf-8 -*-
"""
AI Service
Unified interface for AI generation with retry and timeout support.
"""
```

**类文档字符串：**
```python
class AIService:
    """
    AI Service for content generation.
    
    Features:
    - Load prompts from database
    - Validate variables
    - Fill prompt templates
    - Call DashScope AI with retry and timeout
    """
```

**函数文档字符串：**
```python
def generate(
    self,
    prompt_name: str,
    variables: Dict[str, Any],
    model: Optional[str] = None,
) -> str:
    """
    Generate content using AI.
    
    Args:
        prompt_name: Prompt name (e.g., "douyin_script")
        variables: Variables dictionary
        model: AI model (optional, default from prompt)
    
    Returns:
        Generated content
    
    Raises:
        ValueError: If prompt not found or variables invalid
        Exception: If AI generation fails
    """
```

---

### 3. 类型注解

**必须使用类型注解！**

```python
# ✅ 正确
def get_prompt(self, name: str) -> Optional[Prompt]:
    pass

def validate_variables(
    self,
    prompt: Prompt,
    variables: Dict[str, Any]
) -> bool:
    pass

# ❌ 错误
def get_prompt(self, name):
    pass

def validate_variables(self, prompt, variables):
    pass
```

---

### 4. 错误处理

**必须捕获并记录异常！**

```python
# ✅ 正确
try:
    response = self._call_ai(...)
    return response
except Exception as e:
    logger.error(f"AI generation failed: {e}")
    raise

# ❌ 错误
try:
    response = self._call_ai(...)
    return response
except:
    pass
```

**使用日志记录：**
```python
logger.info(f"Calling AI (attempt {attempt + 1}/{self.max_retries})")
logger.debug(f"Prompt: {filled_prompt[:200]}...")
logger.warning(f"AI generation failed (attempt {attempt + 1}): {e}")
logger.error(f"AI generation failed after {self.max_retries} attempts")
```

---

## 三、配置管理

### 1. 环境变量

**所有配置必须通过 config.py 管理！**

```python
# ✅ 正确
from app.config import config

timeout = config.AI_TEXT_TIMEOUT
model = config.AI_MODEL

# ❌ 错误
timeout = 30  # 硬编码
model = "qwen-plus"  # 硬编码
```

### 2. .env 文件

**创建 .env 文件（不提交到 Git）：**

```bash
# 复制模板
cp .env.example .env

# 编辑 .env
DATABASE_URL=sqlite:///./data/content_factory.db
DASHSCOPE_API_KEY=sk-your-api-key
AI_TEXT_TIMEOUT=30
AI_IMAGE_TIMEOUT=60
```

### 3. 配置项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `DATABASE_URL` | sqlite:///./data/content_factory.db | 数据库连接 |
| `DASHSCOPE_API_KEY` | - | DashScope API Key |
| `AI_MODEL` | qwen-plus | AI 模型 |
| `AI_TEXT_TIMEOUT` | 30 | 文本生成超时（秒） |
| `AI_IMAGE_TIMEOUT` | 60 | 图片生成超时（秒） |
| `AI_MAX_RETRIES` | 3 | 最大重试次数 |
| `PROMPT_CACHE_ENABLED` | true | 是否启用缓存 |
| `PROMPT_CACHE_TTL` | 300 | 缓存过期时间（秒） |

---

## 四、数据库规范

### 1. 表命名

- ✅ 小写 + 下划线：`prompts`, `prompt_versions`
- ❌ 大写字母：`Prompts`
- ❌ 驼峰命名：`promptVersions`

### 2. 字段命名

- ✅ 小写 + 下划线：`created_at`, `updated_at`
- ❌ 大写字母：`CreatedAt`

### 3. SQL 注入防护

**必须使用参数化查询！**

```python
# ✅ 正确（参数化查询）
cursor.execute(
    "SELECT * FROM prompts WHERE name = ?",
    (name,)
)

# ❌ 错误（字符串拼接）
cursor.execute(
    f"SELECT * FROM prompts WHERE name = '{name}'"
)
```

### 4. 数据库连接

**使用完后必须关闭连接！**

```python
# ✅ 正确
conn = self._get_connection()
try:
    cursor = conn.cursor()
    cursor.execute(...)
    row = cursor.fetchone()
finally:
    conn.close()

# ❌ 错误
conn = self._get_connection()
cursor = conn.cursor()
cursor.execute(...)  # 忘记关闭连接
```

---

## 五、API 设计规范

### 1. RESTful 风格

```
GET    /api/prompts           # 获取列表
GET    /api/prompts/:id       # 获取详情
POST   /api/prompts           # 创建
PUT    /api/prompts/:id       # 更新
DELETE /api/prompts/:id       # 删除
```

### 2. 响应格式

**统一响应格式：**

```python
{
    "code": 200,
    "message": "success",
    "data": {...}
}
```

**错误响应：**

```python
{
    "code": 404,
    "message": "Prompt not found",
    "data": null
}
```

### 3. 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 403 | 禁止访问（系统 Prompt 不可修改） |
| 404 | 资源不存在 |
| 500 | 服务器错误 |

---

## 六、测试规范

### 1. 单元测试

**每个模块必须有单元测试！**

```python
# backend/tests/test_ai_service.py
class TestAIService:
    def test_generate_douyin_script(self):
        """Test Douyin script generation"""
        service = AIService()
        result = service.generate(
            prompt_name="douyin_script",
            variables={"topic": "AI 工具", "theme": "效率"}
        )
        assert len(result) > 0
    
    def test_validate_variables(self):
        """Test variable validation"""
        loader = PromptLoader()
        prompt = loader.get_prompt("douyin_script")
        
        # Should raise ValueError for missing variables
        with pytest.raises(ValueError):
            loader.validate_variables(prompt, {})
```

### 2. 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_ai_service.py

# 查看覆盖率
pytest --cov=app
```

---

## 七、Git 提交规范

### 1. 提交信息格式

```
<type>: <subject>

<body>

<footer>
```

### 2. Type 类型

| Type | 说明 |
|------|------|
| feat | 新功能 |
| fix | Bug 修复 |
| docs | 文档更新 |
| style | 代码格式（不影响功能） |
| refactor | 重构 |
| test | 测试相关 |
| chore | 构建/工具/配置 |

### 3. 示例

```
feat: Phase 2 模块 3 - AIService 重构完成

新增内容：
- backend/app/ai/prompts.py - Prompt 加载器
- backend/app/ai/service.py - AIService 核心类

核心功能：
✅ 从数据库加载 Prompt
✅ 变量验证
✅ AI 调用（带重试和超时）

代码质量：
✅ 英文注释
✅ 类型注解
✅ 日志记录
```

---

## 八、安全检查清单

### 提交前检查

- [ ] 所有注释使用英文
- [ ] 所有函数有类型注解
- [ ] 所有函数有文档字符串
- [ ] 没有硬编码配置（使用 config.py）
- [ ] 没有 SQL 注入风险（使用参数化查询）
- [ ] 异常已捕获并记录
- [ ] 数据库连接已关闭
- [ ] 单元测试通过
- [ ] .env 文件未提交

---

## 九、性能优化建议

### 1. 数据库

- ✅ 使用索引（category, is_active）
- ✅ 避免 N+1 查询
- ✅ 使用连接池（Phase 3）

### 2. 缓存

- ✅ Prompt 缓存（5 分钟 TTL）
- ✅ 缓存验证（检查过期）
- ✅ 手动清除接口

### 3. AI 调用

- ✅ 超时控制（文本 30s，图片 60s）
- ✅ 重试机制（指数退避）
- ✅ 日志记录

---

## 十、常见问题

### Q1: 如何添加新的 Prompt？

```python
# 1. 在数据库中插入
INSERT INTO prompts (name, display_name, template, variables, ...)
VALUES ('new_prompt', '新 Prompt', '模板内容', '["var1", "var2"]', ...);

# 2. 在代码中使用
service.generate(
    prompt_name="new_prompt",
    variables={"var1": "value1", "var2": "value2"}
)
```

### Q2: 如何修改配置？

```bash
# 1. 编辑 .env 文件
vi .env

# 2. 修改配置项
AI_TEXT_TIMEOUT=60

# 3. 重启服务
python -m uvicorn app.main:app --reload
```

### Q3: 如何调试？

```python
# 1. 设置日志级别为 DEBUG
LOG_LEVEL=DEBUG

# 2. 查看日志
tail -f logs/app.log

# 3. 使用断点
import pdb; pdb.set_trace()
```

---

**文档状态：** ✅ 已审核  
**审核人：** 架构设计虾、后端开发虾、项目经理虾  
**最后更新：** 2026-03-13 17:35

---

*AI 内容工厂 - 让内容创作更高效！* 🚀
