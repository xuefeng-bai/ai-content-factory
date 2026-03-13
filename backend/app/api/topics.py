# -*- coding: utf-8 -*-
"""
Topic Recommendation API
Recommend topics based on search results.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from app.ai.service import AIService

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
    try:
        ai_service = AIService()
        
        # Format search results for prompt
        search_text = format_search_results(request.search_results)
        
        # Generate topic recommendations
        topics_json = ai_service.generate(
            prompt_name="topic_recommendation",
            variables={"search_results": search_text},
            is_image=False
        )
        
        return TopicRecommendResponse(
            code=200,
            message="Topics recommended successfully",
            data={"topics": topics_json}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
