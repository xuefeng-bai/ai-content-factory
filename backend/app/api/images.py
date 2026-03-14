# -*- coding: utf-8 -*-
"""
Image Generation API
Generate images for content using AI.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import json
import os
from pathlib import Path
import uuid
from datetime import datetime

# 使用 Mock AI 服务（避免 dashscope 依赖）
try:
    from app.ai.service import AIService
except ImportError:
    from app.ai.service_mock import MockAIService as AIService

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


# ==================== API Endpoints ====================

@router.post("/generate", response_model=ImageGenerateResponse)
async def generate_image(request: ImageGenerateRequest):
    """
    Generate image for content.
    
    - **content**: Content for generating image prompt
    - **title**: Title for the image
    - **aspect_ratio**: Image aspect ratio (16:9 or 3:4)
    - **platform**: Platform (wechat/xhs)
    
    Returns image URL and metadata.
    """
    try:
        ai_service = AIService()
        
        # Generate image prompt
        prompt = f"Create a professional cover image for {request.platform} platform. Title: {request.title}. Content theme: {request.content}. Style: clean, modern, eye-catching."
        
        # Mock image generation (replace with real DashScope call)
        image_id = str(uuid.uuid4())
        image_filename = f"{image_id}.png"
        image_dir = Path("data/images")
        image_dir.mkdir(exist_ok=True)
        image_path = image_dir / image_filename
        
        # Save placeholder image (in real implementation, save actual generated image)
        # For now, just create a text file as placeholder
        with open(image_path, 'w') as f:
            f.write(f"Image placeholder for: {request.title}")
        
        # Mock image URL
        image_url = f"/api/images/{image_id}"
        
        return ImageGenerateResponse(
            code=200,
            message="Image generated successfully",
            data={
                "id": image_id,
                "url": image_url,
                "title": request.title,
                "aspect_ratio": request.aspect_ratio,
                "platform": request.platform,
                "prompt": prompt,
                "created_at": datetime.now().isoformat()
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{image_id}", response_model=ImageGenerateResponse)
async def get_image(image_id: str):
    """
    Get image by ID.
    
    - **image_id**: Image ID
    """
    try:
        image_dir = Path("data/images")
        image_path = image_dir / f"{image_id}.png"
        
        if not image_path.exists():
            raise HTTPException(status_code=404, detail="Image not found")
        
        # In real implementation, return actual image file
        # For now, return placeholder
        return ImageGenerateResponse(
            code=200,
            message="Image retrieved successfully",
            data={
                "id": image_id,
                "url": f"/static/images/{image_id}.png",
                "title": "Generated Image",
                "aspect_ratio": "16:9",
                "platform": "wechat",
                "created_at": datetime.now().isoformat()
            }
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
        # Mock image list (in real implementation, query from database)
        mock_images = [
            {
                "id": str(uuid.uuid4()),
                "url": f"/static/images/{uuid.uuid4()}.png",
                "title": "公众号封面图",
                "aspect_ratio": "16:9",
                "platform": "wechat",
                "created_at": datetime.now().isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "url": f"/static/images/{uuid.uuid4()}.png",
                "title": "小红书封面图",
                "aspect_ratio": "3:4",
                "platform": "xhs",
                "created_at": datetime.now().isoformat()
            }
        ]
        
        # Filter by platform
        if platform:
            mock_images = [img for img in mock_images if img["platform"] == platform]
        
        # Pagination
        total = len(mock_images)
        start = (page - 1) * page_size
        end = start + page_size
        paginated_images = mock_images[start:end]
        
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
