#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 内容工厂 Phase 2 - 数据库迁移脚本
执行数据库表结构初始化和 Prompt 数据 seeding

用法:
    python -m app.data.migrate_v1

回滚:
    python -m app.data.migrate_v1 --rollback
"""

import sqlite3
import sys
import os
from pathlib import Path
from datetime import datetime


# ==================== 配置 ====================

# 数据库路径（相对于项目根目录）
DB_PATH = Path(__file__).parent.parent.parent / "data" / "content_factory.db"

# SQL 文件路径
SCHEMA_SQL = Path(__file__).parent / "schema.sql"
SEED_SQL = Path(__file__).parent / "seed_prompts.sql"


# ==================== 工具函数 ====================

def print_step(message: str):
    """打印步骤信息."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")


def execute_sql_file(conn: sqlite3.Connection, sql_file: Path):
    """执行 SQL 文件."""
    if not sql_file.exists():
        raise FileNotFoundError(f"SQL 文件不存在：{sql_file}")
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # 执行 SQL（支持多语句）
    conn.executescript(sql_content)


def verify_migration(conn: sqlite3.Connection) -> bool:
    """验证迁移是否成功."""
    cursor = conn.cursor()
    
    # 检查表是否存在
    required_tables = ['prompts', 'prompt_versions', 'prompt_test_logs', 'content_history']
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing_tables = [row[0] for row in cursor.fetchall()]
    
    for table in required_tables:
        if table not in existing_tables:
            print_step(f"❌ 表 {table} 不存在")
            return False
        print_step(f"✅ 表 {table} 存在")
    
    # 检查 Prompt 初始化
    cursor.execute("SELECT COUNT(*) FROM prompts WHERE is_system = 1")
    system_prompts_count = cursor.fetchone()[0]
    
    if system_prompts_count != 6:
        print_step(f"❌ 系统 Prompt 数量不正确：{system_prompts_count}（应为 6）")
        return False
    
    print_step(f"✅ 系统 Prompt 初始化成功：{system_prompts_count} 个")
    
    # 检查版本初始化
    cursor.execute("SELECT COUNT(*) FROM prompt_versions")
    versions_count = cursor.fetchone()[0]
    
    if versions_count != 6:
        print_step(f"❌ Prompt 版本数量不正确：{versions_count}（应为 6）")
        return False
    
    print_step(f"✅ Prompt 版本初始化成功：{versions_count} 个")
    
    # 列出所有 Prompt
    cursor.execute("SELECT name, display_name FROM prompts WHERE is_system = 1 ORDER BY sort_order")
    prompts = cursor.fetchall()
    
    print_step("\n📋 已初始化的系统 Prompt：")
    for name, display_name in prompts:
        print_step(f"   - {name} ({display_name})")
    
    return True


# ==================== 迁移函数 ====================

def migrate():
    """执行数据库迁移."""
    print_step("=" * 60)
    print_step("AI 内容工厂 Phase 2 - 数据库迁移开始")
    print_step("=" * 60)
    
    # 确保目录存在
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = None
    try:
        # 连接数据库
        print_step(f"📁 数据库路径：{DB_PATH.absolute()}")
        conn = sqlite3.connect(str(DB_PATH))
        
        # 启用外键
        conn.execute("PRAGMA foreign_keys = ON")
        
        # 开始事务
        conn.execute("BEGIN TRANSACTION")
        print_step("🔒 事务已开启")
        
        # 检查表是否已存在
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        # 执行表结构（如果表不存在）
        if 'prompts' not in existing_tables:
            print_step("📐 执行表结构初始化...")
            execute_sql_file(conn, SCHEMA_SQL)
            print_step("✅ 表结构初始化完成")
        else:
            print_step("✅ 表结构已存在，跳过")
        
        # 执行数据 seeding（使用 INSERT OR IGNORE 避免重复）
        print_step("🌱 执行 Prompt 数据初始化...")
        
        # 读取 seed SQL 并执行（跳过已存在的 Prompt）
        with open(SEED_SQL, 'r', encoding='utf-8') as f:
            seed_sql = f.read()
        
        # 分割 SQL 语句
        statements = []
        current_stmt = []
        for line in seed_sql.split('\n'):
            if line.strip().startswith('--'):
                continue
            current_stmt.append(line)
            if line.strip().endswith(';'):
                statements.append('\n'.join(current_stmt))
                current_stmt = []
        
        # 执行每个语句（跳过已存在的）
        executed = 0
        for stmt in statements:
            if not stmt.strip():
                continue
            try:
                conn.execute(stmt)
                executed += 1
            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed" in str(e):
                    # 已存在，跳过
                    pass
                else:
                    raise
        
        print_step(f"✅ Prompt 数据初始化完成（执行 {executed} 条语句）")
        
        # 验证迁移
        print_step("\n🔍 验证迁移结果...")
        if not verify_migration(conn):
            raise Exception("迁移验证失败")
        
        # 提交事务
        conn.commit()
        print_step("✅ 事务已提交")
        
        print_step("=" * 60)
        print_step("🎉 数据库迁移成功完成！")
        print_step("=" * 60)
        
        return True
        
    except Exception as e:
        if conn:
            conn.rollback()
            print_step("❌ 事务已回滚")
        
        print_step("=" * 60)
        print_step(f"❌ 迁移失败：{e}")
        print_step("=" * 60)
        return False
        
    finally:
        if conn:
            conn.close()


def rollback():
    """回滚迁移（删除所有表和数据）."""
    print_step("=" * 60)
    print_step("⚠️  警告：即将回滚数据库迁移")
    print_step("=" * 60)
    
    if not DB_PATH.exists():
        print_step("❌ 数据库文件不存在，无需回滚")
        return False
    
    confirm = input("确认回滚？(yes/no): ")
    if confirm.lower() != 'yes':
        print_step("❌ 回滚已取消")
        return False
    
    conn = None
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("BEGIN TRANSACTION")
        
        # 删除所有表
        tables = ['content_history', 'prompt_test_logs', 'prompt_versions', 'prompts']
        for table in tables:
            conn.execute(f"DROP TABLE IF EXISTS {table}")
            print_step(f"🗑️  已删除表：{table}")
        
        conn.commit()
        print_step("✅ 回滚成功完成")
        
        return True
        
    except Exception as e:
        if conn:
            conn.rollback()
        print_step(f"❌ 回滚失败：{e}")
        return False
        
    finally:
        if conn:
            conn.close()


# ==================== 主函数 ====================

if __name__ == "__main__":
    # 切换到项目根目录
    os.chdir(Path(__file__).parent.parent.parent)
    
    # 解析命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == "--rollback":
        rollback()
    else:
        migrate()
