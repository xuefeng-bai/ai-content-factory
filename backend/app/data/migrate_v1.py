#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Migration Script v1.0
Initializes database schema and seed prompts for AI Content Factory.

Usage:
    python -m app.data.migrate_v1

Or:
    python migrate_v1.py
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime


def get_db_path() -> Path:
    """Get database file path."""
    # Database location: backend/data/content_factory.db
    base_dir = Path(__file__).parent.parent.parent
    db_dir = base_dir / "data"
    db_dir.mkdir(exist_ok=True)
    return db_dir / "content_factory.db"


def load_sql(file_name: str) -> str:
    """Load SQL file content."""
    sql_path = Path(__file__).parent / file_name
    with open(sql_path, "r", encoding="utf-8") as f:
        return f.read()


def migrate(db_conn: sqlite3.Connection) -> None:
    """
    Run database migration.
    
    Args:
        db_conn: SQLite database connection
    """
    cursor = db_conn.cursor()
    
    print("[INFO] Starting database migration...")
    print(f"[INFO] Database: {get_db_path()}")
    
    # Step 1: Load and execute schema
    print("\n[STEP 1] Creating database schema...")
    schema_sql = load_sql("schema.sql")
    cursor.executescript(schema_sql)
    print("[OK] Schema created successfully")
    
    # Step 2: Load and execute seed prompts
    print("\n[STEP 2] Initializing system prompts...")
    seed_sql = load_sql("seed_prompts.sql")
    cursor.executescript(seed_sql)
    
    # Count prompts
    cursor.execute("SELECT COUNT(*) FROM prompts")
    count = cursor.fetchone()[0]
    print(f"[OK] {count} prompts initialized")
    
    # Step 3: Verify migration
    print("\n[STEP 3] Verifying migration...")
    
    # Check tables
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' 
        ORDER BY name
    """)
    tables = [row[0] for row in cursor.fetchall()]
    print(f"[OK] Tables created: {', '.join(tables)}")
    
    # Check prompts by category
    cursor.execute("""
        SELECT category, COUNT(*) as count 
        FROM prompts 
        WHERE is_system=1 
        GROUP BY category
    """)
    print("\n[OK] System prompts by category:")
    for row in cursor.fetchall():
        print(f"  - {row[0]}: {row[1]} prompts")
    
    # Commit changes
    db_conn.commit()
    
    print("\n" + "="*50)
    print("[SUCCESS] Database migration completed!")
    print("="*50)
    print(f"\nDatabase location: {get_db_path()}")
    print(f"Migration time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def main():
    """Main entry point."""
    try:
        # Get database path
        db_path = get_db_path()
        
        # Connect to database
        print(f"[INFO] Connecting to database: {db_path}")
        conn = sqlite3.connect(str(db_path))
        
        # Run migration
        migrate(conn)
        
        # Close connection
        conn.close()
        
        print("\n[INFO] Database connection closed.")
        return 0
        
    except FileNotFoundError as e:
        print(f"\n[ERROR] File not found: {e}")
        return 1
        
    except sqlite3.Error as e:
        print(f"\n[ERROR] Database error: {e}")
        return 2
        
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        return 99


if __name__ == "__main__":
    sys.exit(main())
