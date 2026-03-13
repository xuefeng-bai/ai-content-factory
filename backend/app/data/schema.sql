-- AI Content Factory Database Schema
-- Version: 1.0.0
-- Created: 2026-03-13

-- ==================== Prompt Management ====================

-- Table: prompts (Prompt master table)
CREATE TABLE IF NOT EXISTS prompts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,           -- Prompt identifier (e.g., "douyin_script")
    display_name TEXT NOT NULL,          -- Display name (e.g., "抖音文案")
    description TEXT,                     -- Description
    template TEXT NOT NULL,               -- Prompt template with {variable} placeholders
    variables TEXT NOT NULL,              -- Variable list as JSON: ["topic", "theme"]
    output_format TEXT,                   -- Output format (json/text/markdown)
    model TEXT DEFAULT 'qwen-plus',       -- AI model
    max_tokens INTEGER DEFAULT 2000,      -- Max tokens to generate
    temperature REAL DEFAULT 0.7,         -- Temperature (0-1)
    is_active BOOLEAN DEFAULT 1,          -- Is enabled
    is_system BOOLEAN DEFAULT 0,          -- Is system built-in (cannot delete)
    category TEXT,                        -- Category (topic/douyin/wechat/xhs/image)
    sort_order INTEGER DEFAULT 0,         -- Sort order
    created_by TEXT,                      -- Creator
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    published_version_id INTEGER          -- Current published version ID
);

-- Indexes for prompts
CREATE INDEX IF NOT EXISTS idx_prompts_category ON prompts(category);
CREATE INDEX IF NOT EXISTS idx_prompts_is_active ON prompts(is_active);
CREATE INDEX IF NOT EXISTS idx_prompts_name ON prompts(name);

-- Table: prompt_versions (Version history)
CREATE TABLE IF NOT EXISTS prompt_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt_id INTEGER NOT NULL,           -- Reference to prompts.id
    version TEXT NOT NULL,                -- Version string (e.g., "1.0.0")
    template TEXT NOT NULL,               -- Template snapshot
    variables TEXT NOT NULL,              -- Variables snapshot
    change_log TEXT,                      -- Change description
    test_result TEXT,                     -- Test result as JSON
    created_by TEXT,                      -- Creator
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_published BOOLEAN DEFAULT 0,       -- Is published
    FOREIGN KEY (prompt_id) REFERENCES prompts(id) ON DELETE CASCADE
);

-- Indexes for prompt_versions
CREATE INDEX IF NOT EXISTS idx_versions_prompt_id ON prompt_versions(prompt_id);
CREATE INDEX IF NOT EXISTS idx_versions_is_published ON prompt_versions(is_published);

-- Table: prompt_test_logs (Test logs)
CREATE TABLE IF NOT EXISTS prompt_test_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt_id INTEGER NOT NULL,           -- Reference to prompts.id
    version_id INTEGER,                   -- Reference to prompt_versions.id
    input_variables TEXT NOT NULL,        -- Input variables as JSON
    output TEXT,                          -- AI output
    model_used TEXT,                      -- Model used
    tokens_used INTEGER,                  -- Tokens consumed
    duration_ms INTEGER,                  -- Duration in milliseconds
    rating INTEGER,                       -- Rating (1-5)
    feedback TEXT,                        -- Feedback notes
    created_by TEXT,                      -- Creator
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prompt_id) REFERENCES prompts(id) ON DELETE CASCADE
);

-- Indexes for prompt_test_logs
CREATE INDEX IF NOT EXISTS idx_logs_prompt_id ON prompt_test_logs(prompt_id);

-- ==================== Content History ====================

-- Table: content_history (Content generation history)
CREATE TABLE IF NOT EXISTS content_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    theme TEXT NOT NULL,                  -- Theme
    topic TEXT NOT NULL,                  -- Topic
    platform TEXT NOT NULL,               -- Platform (douyin/wechat/xhs)
    content TEXT NOT NULL,                -- Generated content
    image_urls TEXT,                      -- Image URLs as JSON
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for content_history
CREATE INDEX IF NOT EXISTS idx_history_platform ON content_history(platform);
CREATE INDEX IF NOT EXISTS idx_history_theme ON content_history(theme);
CREATE INDEX IF NOT EXISTS idx_history_created_at ON content_history(created_at);

-- ==================== System Info ====================

-- Table: schema_versions (Schema version tracking)
CREATE TABLE IF NOT EXISTS schema_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version TEXT NOT NULL,                -- Version string (e.g., "1.0.0")
    description TEXT,                     -- Description
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial schema version
INSERT INTO schema_versions (version, description) VALUES ('1.0.0', 'Initial schema with prompts and content history');
