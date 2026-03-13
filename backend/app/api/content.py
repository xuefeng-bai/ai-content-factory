# -*- coding: utf-8 -*-
"""
Content Generation API
Generate multi-platform content using AI.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from app.ai.service import AIService
from app.config import config

router = APIRouter(prefix="/api/content", tags=["Content"])


# ==================== Models ====================

class ContentGenerateRequest(BaseModel):
    """Content generation request."""
    topic: str = Field(..., description="Selected topic")
    theme: str = Field(..., description="Theme")
    platforms: List[str] = Field(
        ...,
        description="Platforms to generate (douyin/wechat/xhs)"
    )


class ContentGenerateResponse(BaseModel):
    """Content generation response."""
    code: int = 200
    message: str = "success"
    data: Dict[str, str]


# ==================== API Endpoints ====================

@router.post("/generate", response_model=ContentGenerateResponse)
async def generate_content(request: ContentGenerateRequest):
    """
    Generate content for multiple platforms.
    
    - **topic**: Selected topic
    - **theme**: Theme
    - **platforms**: Platforms to generate (douyin/wechat/xhs)
    
    Returns generated content for each platform.
    """
    try:
        ai_service = AIService()
        results = {}
        
        # Platform mapping
        platform_mapping = {
            "douyin": "douyin_script",
            "wechat": "wechat_article",
            "xhs": "xiaohongshu_note"
        }
        
        # Generate content for each platform
        for platform in request.platforms:
            prompt_name = platform_mapping.get(platform)
            if not prompt_name:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported platform: {platform}"
                )
            
            try:
                content = ai_service.generate(
                    prompt_name=prompt_name,
                    variables={
                        "topic": request.topic,
                        "theme": request.theme
                    },
                    is_image=False
                )
                results[platform] = content
                
            except Exception as e:
                results[platform] = f"Error: {str(e)}"
        
        return ContentGenerateResponse(
            code=200,
            message="Content generated successfully",
            data=results
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/douyin")
async def generate_douyin(topic: str, theme: str):
    """Generate Douyin script."""
    ai_service = AIService()
    
    content = ai_service.generate(
        prompt_name="douyin_script",
        variables={"topic": topic, "theme": theme},
        is_image=False
    )
    
    return {
        "code": 200,
        "message": "success",
        "data": {
            "platform": "douyin",
            "content": content
        }
    }


@router.post("/generate/wechat")
async def generate_wechat(topic: str, theme: str):
    """Generate WeChat article."""
    ai_service = AIService()
    
    content = ai_service.generate(
        prompt_name="wechat_article",
        variables={"topic": topic, "theme": theme},
        is_image=False
    )
    
    return {
        "code": 200,
        "message": "success",
        "data": {
            "platform": "wechat",
            "content": content
        }
    }


@router.post("/generate/xhs")
async def generate_xiaohongshu(topic: str, theme: str):
    """Generate Xiaohongshu note."""
    ai_service = AIService()
    
    content = ai_service.generate(
        prompt_name="xiaohongshu_note",
        variables={"topic": topic, "theme": theme},
        is_image=False
    )
    
    return {
        "code": 200,
        "message": "success",
        "data": {
            "platform": "xhs",
            "content": content
        }
    }
