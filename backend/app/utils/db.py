# Database Connection Utility

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os

# 数据库 URL 配置
DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ai_content_factory.db")

# SQLite 需要添加 connect_args 以支持多线程
connect_args = {}
if DATABASE_TYPE == "sqlite":
    connect_args["check_same_thread"] = False

# 异步引擎（用于 FastAPI 异步接口）
async_engine = create_async_engine(
    DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///"),
    echo=False,
    future=True
)

# 同步引擎（用于初始化脚本）
sync_engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args=connect_args
)

# 异步 Session
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    future=True
)

# 同步 Session
SessionLocal = sessionmaker(
    bind=sync_engine,
    autoflush=False,
    autocommit=False,
    future=True
)


def get_db() -> Generator[Session, None, None]:
    """获取数据库会话的依赖注入函数"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> Generator[AsyncSession, None, None]:
    """获取异步数据库会话的依赖注入函数"""
    async_db = AsyncSessionLocal()
    try:
        yield async_db
    finally:
        await async_db.close()
