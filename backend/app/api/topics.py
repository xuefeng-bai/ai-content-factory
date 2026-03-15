# -*- coding: utf-8 -*-
"""
Topic Recommendation API
Recommend topics based on search results.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# 使用 Mock AI 服务（避免 dashscope 依赖）
try:
    from app.ai.service import AIService
except ImportError:
    from app.ai.service_mock import MockAIService as AIService

router = APIRouter(prefix="/api/topics", tags=["Topics"])


# ==================== Models ====================

class TopicRecommendRequest(BaseModel):
    """Topic recommendation request."""
    search_results: List[Dict[str, Any]] = Field(
        ...,
        description="Search results from Weibo and Zhihu"
    )
    theme: Optional[str] = Field(None, description="Theme")


class TopicRecommendResponse(BaseModel):
    """Topic recommendation response."""
    code: int = 200
    message: str = "success"
    data: Dict[str, Any]


# ==================== API Endpoints ====================

@router.post("/recommend", response_model=TopicRecommendResponse)
async def recommend_topics(request: TopicRecommendRequest):
    """
    Recommend topics based on search results.
    
    - **search_results**: Search results from Weibo and Zhihu
    - **theme**: Theme (optional)
    
    Returns 3-5 recommended topics.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"[Topics API] Received request with {len(request.search_results)} search results")
        
        # 如果没有搜索结果，返回示例数据
        if not request.search_results or len(request.search_results) == 0:
            logger.warning("[Topics API] No search results, using mock data")
            mock_topics = {
                "topics": [
                    {
                        "title": "AI 工具提升效率的 5 个技巧",
                        "angle": "职场人必备技能",
                        "core_point": "用 AI 节省 50% 工作时间",
                        "platforms": ["douyin", "wechat", "xhs"],
                        "hot_score": 9,
                        "reason": "切中职场痛点，实用性强"
                    },
                    {
                        "title": "打工人如何用 AI 逆袭",
                        "angle": "个人成长故事",
                        "core_point": "从加班狗到效率达人",
                        "platforms": ["douyin", "xhs"],
                        "hot_score": 8,
                        "reason": "情感共鸣强，易传播"
                    }
                ]
            }
            return TopicRecommendResponse(
                code=200,
                message="Topics recommended successfully (mock data)",
                data={"topics": mock_topics}
            )
        
        ai_service = AIService()
        
        # Format search results for prompt
        search_text = format_search_results(request.search_results)
        logger.info(f"[Topics API] Formatted search results: {search_text[:200]}...")
        
        # Generate topic recommendations
        logger.info("[Topics API] Calling AI service...")
        topics_json = ai_service.generate(
            prompt_name="topic_recommendation",
            variables={"search_results": search_text},
            is_image=False
        )
        
        logger.info(f"[Topics API] AI response: {topics_json[:200]}...")
        
        return TopicRecommendResponse(
            code=200,
            message="Topics recommended successfully",
            data={"topics": topics_json}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Topics API] Error: {e}")
        logger.exception("Full traceback:")
        raise HTTPException(status_code=500, detail=f"推荐失败：{str(e)}")


def format_search_results(search_results: List[Dict[str, Any]]) -> str:
    """
    Format search results for prompt.
    
    Args:
        search_results: List of search result items
    
    Returns:
        Formatted text string
    """
    formatted = []
    
    for idx, item in enumerate(search_results[:10], 1):
        title = item.get("title", "No title")
        source = item.get("source", "unknown")
        hot_value = item.get("hot_value", "")
        
        formatted.append(
            f"{idx}. [{source}] {title} {hot_value}"
        )
    
    return "\n".join(formatted)
