-- AI 内容工厂 Phase 2 - Prompt 配置化
-- 数据库表结构设计
-- 创建日期：2026-03-14

-- 启用外键约束
PRAGMA foreign_keys = ON;

-- ==================== Prompts 表 ====================
-- 存储 Prompt 基本信息
CREATE TABLE IF NOT EXISTS prompts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,              -- Prompt 标识符（英文，用于代码引用）
    display_name TEXT NOT NULL,             -- 显示名称（中文）
    description TEXT,                       -- 描述说明
    template TEXT NOT NULL,                 -- Prompt 模板（含{variable}占位符）
    variables TEXT NOT NULL,                -- 变量列表（JSON 数组：["search_results", "topic"]）
    output_format TEXT,                     -- 输出格式（text/json/markdown）
    model TEXT DEFAULT 'qwen-plus',         -- AI 模型
    max_tokens INTEGER DEFAULT 2000,        -- 最大 token 数
    temperature REAL DEFAULT 0.7,           -- 温度参数
    category TEXT,                          -- 分类（topic/douyin/wechat/xhs/image）
    sort_order INTEGER DEFAULT 0,           -- 排序顺序
    is_system INTEGER DEFAULT 0,            -- 是否系统内置（1=系统，0=用户）
    is_active INTEGER DEFAULT 1,            -- 是否启用（1=启用，0=禁用）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_prompts_category ON prompts(category);
CREATE INDEX IF NOT EXISTS idx_prompts_is_active ON prompts(is_active);
CREATE INDEX IF NOT EXISTS idx_prompts_is_system ON prompts(is_system);
CREATE INDEX IF NOT EXISTS idx_prompts_name ON prompts(name);

-- ==================== Prompt Versions 表 ====================
-- 存储 Prompt 版本历史
CREATE TABLE IF NOT EXISTS prompt_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt_id INTEGER NOT NULL,             -- 外键：prompts.id
    version INTEGER NOT NULL,               -- 版本号（v1, v2, v3...）
    template TEXT NOT NULL,                 -- 该版本的模板
    variables TEXT,                         -- 该版本的变量列表（JSON）
    changes_log TEXT,                       -- 变更说明
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_published INTEGER DEFAULT 0,         -- 是否已发布（1=发布，0=草稿）
    published_at TIMESTAMP,                 -- 发布时间
    published_by TEXT,                      -- 发布人
    FOREIGN KEY (prompt_id) REFERENCES prompts(id) ON DELETE CASCADE,
    UNIQUE(prompt_id, version)              -- 同一 Prompt 的版本号唯一
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_versions_prompt_id ON prompt_versions(prompt_id);
CREATE INDEX IF NOT EXISTS idx_versions_is_published ON prompt_versions(is_published);

-- ==================== Prompt Test Logs 表 ====================
-- 存储 Prompt 测试记录
CREATE TABLE IF NOT EXISTS prompt_test_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt_id INTEGER NOT NULL,             -- 外键：prompts.id
    version_id INTEGER,                     -- 外键：prompt_versions.id（可选）
    input_vars TEXT NOT NULL,               -- 输入变量（JSON 对象）
    output TEXT,                            -- AI 输出结果
    latency REAL,                           -- 响应时间（秒）
    tokens_used INTEGER,                    -- 消耗 token 数
    model TEXT,                             -- 使用的 AI 模型
    status TEXT DEFAULT 'success',          -- 状态（success/error/timeout）
    error_message TEXT,                     -- 错误信息
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prompt_id) REFERENCES prompts(id) ON DELETE CASCADE,
    FOREIGN KEY (version_id) REFERENCES prompt_versions(id) ON DELETE SET NULL
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_test_logs_prompt_id ON prompt_test_logs(prompt_id);
CREATE INDEX IF NOT EXISTS idx_test_logs_created_at ON prompt_test_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_test_logs_status ON prompt_test_logs(status);

-- ==================== Content History 表 ====================
-- 存储历史生成内容（模块 8 使用）
CREATE TABLE IF NOT EXISTS content_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,                    -- 选题
    platform TEXT NOT NULL,                 -- 平台（douyin/wechat/xhs）
    content TEXT NOT NULL,                  -- 生成内容
    image_urls TEXT,                        -- 配图 URL 列表（JSON 数组）
    prompt_id INTEGER,                      -- 使用的 Prompt ID
    prompt_version_id INTEGER,              -- 使用的 Prompt 版本 ID
    search_results TEXT,                    -- 原始搜索结果（JSON）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prompt_id) REFERENCES prompts(id) ON DELETE SET NULL,
    FOREIGN KEY (prompt_version_id) REFERENCES prompt_versions(id) ON DELETE SET NULL
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_history_topic ON content_history(topic);
CREATE INDEX IF NOT EXISTS idx_history_platform ON content_history(platform);
CREATE INDEX IF NOT EXISTS idx_history_created_at ON content_history(created_at);

-- ==================== 注释说明 ====================
-- 
-- 表关系：
-- - prompts (1) -> (N) prompt_versions：一个 Prompt 有多个版本
-- - prompts (1) -> (N) prompt_test_logs：一个 Prompt 有多条测试记录
-- - prompts (1) -> (N) content_history：一个 Prompt 可生成多条历史内容
--
-- 字段说明：
-- - variables: JSON 数组格式，如 ["search_results", "topic"]
-- - input_vars: JSON 对象格式，如 {"search_results": "...", "topic": "..."}
-- - image_urls: JSON 数组格式，如 ["url1", "url2"]
-- - is_system: 系统内置 Prompt 不可删除，只能禁用（is_active=0）
--
-- 使用示例：
-- INSERT INTO prompts (name, display_name, template, variables, category)
-- VALUES ('topic_recommend', '选题推荐', '你是...{search_results}...', '["search_results"]', 'topic');
