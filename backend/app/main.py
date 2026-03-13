# -*- coding: utf-8 -*-
"""
AI 内容工厂 - FastAPI 后端入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sys

# 添加项目根目录到 Python 路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# 导入 API 路由
from app.api.search import router as search_router
from app.api.prompts import router as prompts_router
from app.api.content import router as content_router
from app.api.topics import router as topics_router

# 创建 FastAPI 应用
app = FastAPI(
    title="AI 内容工厂 API",
    description="AI-driven content creation system",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# 配置 CORS（允许前端跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(search_router)
app.include_router(prompts_router)
app.include_router(content_router)
app.include_router(topics_router)


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "AI 内容工厂 API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
