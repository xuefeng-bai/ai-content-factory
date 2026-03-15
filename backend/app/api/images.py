# -*- coding: utf-8 -*-
"""
Image Generation API
Generate images for content using DashScope AI.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import json
import os
from pathlib import Path
import uuid
from datetime import datetime
import requests

from app.ai.service import AIService
from app.config import config

router = APIRouter(prefix="/api/images", tags=["Images"])


# ==================== Models ====================

class ImageGenerateRequest(BaseModel):
    """Image generation request."""
    content: str = Field(..., description="Content for generating image prompt")
    title: str = Field(..., description="Title for the image")
    aspect_ratio: str = Field("16:9", description="Image aspect ratio (16:9 or 3:4)")
    platform: str = Field("wechat", description="Platform (wechat/xhs)")


class ImageGenerateResponse(BaseModel):
    """Image generation response."""
    code: int = 200
    message: str = "success"
    data: Dict[str, Any]


class ImageInfo(BaseModel):
    """Image information."""
    id: str
    url: str
    title: str
    aspect_ratio: str
    platform: str
    prompt: str
    created_at: str


# ==================== Image Storage ====================

def get_image_storage_dir() -> Path:
    """Get image storage directory."""
    # 使用项目根目录的 data/images 文件夹
    base_dir = Path(__file__).parent.parent.parent
    image_dir = base_dir / "data" / "images"
    image_dir.mkdir(parents=True, exist_ok=True)
    return image_dir


def save_image_from_url(image_url: str, image_id: str) -> str:
    """
    Download and save image from URL.
    
    Args:
        image_url: Remote image URL
        image_id: Local image ID (filename)
    
    Returns:
        Local file path
    """
    try:
        # 下载图片
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        
        # 保存到本地
        image_dir = get_image_storage_dir()
        image_path = image_dir / f"{image_id}.png"
        
        with open(image_path, 'wb') as f:
            f.write(response.content)
        
        return str(image_path)
        
    except Exception as e:
        raise Exception(f"Failed to save image: {e}")


# ==================== API Endpoints ====================

@router.post("/generate", response_model=ImageGenerateResponse)
async def generate_image(request: ImageGenerateRequest):
    """
    Generate image for content using DashScope AI.
    
    - **content**: Content for generating image prompt
    - **title**: Title for the image
    - **aspect_ratio**: Image aspect ratio (16:9 or 3:4)
    - **platform**: Platform (wechat/xhs)
    
    Returns image URL and metadata.
    """
    try:
        # 初始化 AI 服务
        ai_service = AIService()
        
        # 生成图片提示词
        platform_style = {
            "wechat": "professional, clean, modern cover image for WeChat Official Account",
            "xhs": "vibrant, eye-catching, cartoon-style cover image for Xiaohongshu"
        }
        
        style_desc = platform_style.get(request.platform, platform_style["wechat"])
        
        # 构建详细的图片生成提示词
        image_prompt = (
            f"{style_desc}. "
            f"Title: {request.title}. "
            f"Theme: {request.content}. "
            f"Style: clean, modern, professional, high quality, 4K. "
            f"Color scheme: vibrant and eye-catching. "
            f"Composition: centered title with decorative elements."
        )
        
        # 调用 AI 生成图片
        result = ai_service.generate_image(
            prompt=image_prompt,
            title=request.title,
            aspect_ratio=request.aspect_ratio,
            platform=request.platform
        )
        
        # 生成唯一 ID
        image_id = str(uuid.uuid4())
        
        # 保存本地副本
        try:
            local_path = save_image_from_url(result["image_url"], image_id)
            local_url = f"/api/images/{image_id}"
        except Exception as e:
            # 保存失败时使用远程 URL
            local_url = result["image_url"]
        
        return ImageGenerateResponse(
            code=200,
            message="Image generated successfully",
            data={
                "id": image_id,
                "url": local_url,
                "remote_url": result["image_url"],  # 保留远程 URL 备用
                "title": request.title,
                "aspect_ratio": request.aspect_ratio,
                "platform": request.platform,
                "prompt": image_prompt,
                "size": result.get("size", "1024x1024"),
                "created_at": datetime.now().isoformat()
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        # 详细错误日志
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Image generation failed: {e}")
        logger.exception("Full traceback:")
        
        raise HTTPException(
            status_code=500,
            detail=f"Image generation failed: {str(e)}. Please check your DashScope API key."
        )


@router.get("/{image_id}", response_model=ImageGenerateResponse)
async def get_image(image_id: str):
    """
    Get image by ID.
    
    - **image_id**: Image ID
    
    Returns image file or metadata.
    """
    try:
        image_dir = get_image_storage_dir()
        image_path = image_dir / f"{image_id}.png"
        
        if not image_path.exists():
            raise HTTPException(status_code=404, detail="Image not found")
        
        # 返回图片文件（FastAPI 会自动处理文件响应）
        from fastapi.responses import FileResponse
        
        return FileResponse(
            path=str(image_path),
            media_type="image/png",
            filename=f"{image_id}.png"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=ImageGenerateResponse)
async def list_images(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Page size"),
    platform: Optional[str] = Query(None, description="Filter by platform")
):
    """
    List images with pagination.
    
    - **page**: Page number (default: 1)
    - **page_size**: Page size (default: 20, max: 100)
    - **platform**: Filter by platform (wechat/xhs)
    """
    try:
        image_dir = get_image_storage_dir()
        
        # 获取所有图片文件
        image_files = list(image_dir.glob("*.png"))
        
        # 按平台筛选（根据文件名无法判断，暂时返回全部）
        # TODO: 未来可以从数据库或元数据文件读取
        
        # 转换为图片信息
        images = []
        for img_path in image_files:
            image_id = img_path.stem  # 不含扩展名的文件名
            stat = img_path.stat()
            
            images.append({
                "id": image_id,
                "url": f"/api/images/{image_id}",
                "title": f"Generated Image {image_id[:8]}",
                "aspect_ratio": "16:9",  # TODO: 从元数据读取
                "platform": "wechat",  # TODO: 从元数据读取
                "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "size_bytes": stat.st_size
            })
        
        # 按创建时间倒序
        images.sort(key=lambda x: x["created_at"], reverse=True)
        
        # 分页
        total = len(images)
        start = (page - 1) * page_size
        end = start + page_size
        paginated_images = images[start:end]
        
        return ImageGenerateResponse(
            code=200,
            message="success",
            data={
                "list": paginated_images,
                "total": total,
                "page": page,
                "page_size": page_size
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{image_id}", response_model=ImageGenerateResponse)
async def delete_image(image_id: str):
    """
    Delete image by ID.
    
    - **image_id**: Image ID
    """
    try:
        image_dir = get_image_storage_dir()
        image_path = image_dir / f"{image_id}.png"
        
        if not image_path.exists():
            raise HTTPException(status_code=404, detail="Image not found")
        
        # 删除文件
        image_path.unlink()
        
        return ImageGenerateResponse(
            code=200,
            message="Image deleted successfully",
            data={"id": image_id}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
