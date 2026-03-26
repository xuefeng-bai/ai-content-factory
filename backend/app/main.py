# AI Content Factory - FastAPI Backend

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Content Factory API",
    description="AI 驱动的多平台内容生成工具",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """根路径 - 健康检查"""
    return {
        "message": "AI Content Factory API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "service": "ai-content-factory"
    }


# 导入并注册 API 路由
from app.api import content, templates, configs

app.include_router(content.router, prefix="/api/v1/content", tags=["内容生成"])
app.include_router(templates.router, prefix="/api/v1/templates", tags=["模板管理"])
app.include_router(configs.router, prefix="/api/v1/configs", tags=["系统配置"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
