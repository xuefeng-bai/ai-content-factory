# -*- coding: utf-8 -*-
"""
搜索 API 模块
功能：提供统一的搜索接口，整合微博热搜和知乎热榜
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from pathlib import Path
import sys

# 添加项目根目录到 Python 路径
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
root_dir = parent_dir.parent
sys.path.insert(0, str(root_dir))

from app.crawler.weibo import fetch_weibo_hot_search
from app.crawler.zhihu import fetch_zhihu_hot_list

router = APIRouter(prefix="/api", tags=["搜索"])


class SearchRequest(BaseModel):
    """搜索请求模型"""
    theme: str = ""  # 搜索主题（可选，用于后续过滤）


class SearchItem(BaseModel):
    """搜索项模型"""
    rank: int
    title: str
    hot_value: str
    url: str
    source: str


class SearchResponse(BaseModel):
    """搜索响应模型"""
    code: int = 200
    message: str = "success"
    data: Dict[str, List[SearchItem]]


@router.post("/search", response_model=SearchResponse)
async def search_hot_topics(request: SearchRequest):
    """
    搜索热门话题
    
    同时获取微博热搜和知乎热榜，并根据关键词过滤
    
    Args:
        request: 搜索请求（包含 theme 主题，用于过滤）
        
    Returns:
        包含微博热搜和知乎热榜的列表（已过滤）
    """
    try:
        keyword = request.theme.strip() if request.theme else ""
        print(f"[API] 收到搜索请求，keyword: {keyword or '无（获取全部热搜）'}")
        
        # 获取微博和知乎数据
        weibo_data = fetch_weibo_hot_search()
        zhihu_data = fetch_zhihu_hot_list()
        
        # 如果有搜索关键词，进行过滤
        if keyword:
            print(f"[API] 使用关键词过滤：{keyword}")
            weibo_data = [
                item for item in weibo_data
                if keyword.lower() in item.get('title', '').lower()
            ]
            zhihu_data = [
                item for item in zhihu_data
                if keyword.lower() in item.get('title', '').lower()
            ]
            print(f"[API] 过滤后：微博{len(weibo_data)}条，知乎{len(zhihu_data)}条")
        else:
            print(f"[API] 无关键词，返回全部热搜数据")
        
        # 格式化数据
        weibo_items = [SearchItem(**item) for item in weibo_data]
        zhihu_items = [SearchItem(**item) for item in zhihu_data]
        
        response_data = {
            "weibo_hot_search": weibo_items,
            "zhihu_hot_list": zhihu_items
        }
        
        print(f"[API] 搜索完成，微博{len(weibo_items)}条，知乎{len(zhihu_items)}条")
        
        return SearchResponse(
            code=200,
            message="success",
            data=response_data
        )
        
    except Exception as e:
        print(f"[API] 搜索失败：{e}")
        raise HTTPException(status_code=500, detail=f"搜索失败：{str(e)}")


@router.get("/search/weibo", response_model=List[SearchItem])
async def get_weibo_hot_search():
    """
    单独获取微博热搜
    
    Returns:
        微博热搜列表
    """
    try:
        data = fetch_weibo_hot_search()
        return [SearchItem(**item) for item in data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取微博热搜失败：{str(e)}")


@router.get("/search/zhihu", response_model=List[SearchItem])
async def get_zhihu_hot_list():
    """
    单独获取知乎热榜
    
    Returns:
        知乎热榜列表
    """
    try:
        data = fetch_zhihu_hot_list()
        return [SearchItem(**item) for item in data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取知乎热榜失败：{str(e)}")
