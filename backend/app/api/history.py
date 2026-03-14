# -*- coding: utf-8 -*-
"""
History API
Manage content generation history.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import json
import sqlite3
from pathlib import Path
from datetime import datetime

router = APIRouter(prefix="/api/history", tags=["History"])


# ==================== Models ====================

class HistoryListResponse(BaseModel):
    """History list response."""
    code: int = 200
    message: str = "success"
    data: Dict[str, Any]


class HistoryDetailResponse(BaseModel):
    """History detail response."""
    code: int = 200
    message: str = "success"
    data: Dict[str, Any]


# ==================== Database Helper ====================

def get_db_connection() -> sqlite3.Connection:
    """Get database connection."""
    db_path = Path(__file__).parent.parent.parent / "data" / "content_factory.db"
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def row_to_dict(row: sqlite3.Row) -> dict:
    """Convert sqlite3.Row to dict."""
    if row is None:
        return None
    return dict(row)


# ==================== API Endpoints ====================

@router.get("", response_model=HistoryListResponse)
async def list_history(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Page size"),
    platform: Optional[str] = Query(None, description="Filter by platform"),
    keyword: Optional[str] = Query(None, description="Search keyword")
):
    """
    List history with pagination.
    
    - **page**: Page number (default: 1)
    - **page_size**: Page size (default: 20, max: 100)
    - **platform**: Filter by platform (douyin/wechat/xhs)
    - **keyword**: Search keyword in topic or content
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build query
    query = "SELECT * FROM content_history WHERE 1=1"
    count_query = "SELECT COUNT(*) FROM content_history WHERE 1=1"
    params = []
    
    if platform:
        query += " AND platform = ?"
        count_query += " AND platform = ?"
        params.append(platform)
    
    if keyword:
        query += " AND (topic LIKE ? OR content LIKE ?)"
        count_query += " AND (topic LIKE ? OR content LIKE ?)"
        params.extend([f"%{keyword}%", f"%{keyword}%"])
    
    # Get total count
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    
    # Get paginated results
    offset = (page - 1) * page_size
    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([page_size, offset])
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    history_list = [row_to_dict(row) for row in rows]
    
    # Parse JSON fields
    for item in history_list:
        if item.get("image_urls"):
            try:
                item["image_urls"] = json.loads(item["image_urls"])
            except:
                item["image_urls"] = []
    
    conn.close()
    
    return HistoryListResponse(
        code=200,
        message="success",
        data={
            "list": history_list,
            "total": total,
            "page": page,
            "page_size": page_size
        }
    )


@router.get("/{history_id}", response_model=HistoryDetailResponse)
async def get_history(history_id: int):
    """
    Get history by ID.
    
    - **history_id**: History ID
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM content_history WHERE id = ?", (history_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="History not found")
    
    history = row_to_dict(row)
    
    # Parse JSON fields
    if history.get("image_urls"):
        try:
            history["image_urls"] = json.loads(history["image_urls"])
        except:
            history["image_urls"] = []
    
    conn.close()
    
    return HistoryDetailResponse(
        code=200,
        message="success",
        data=history
    )


@router.delete("/{history_id}", response_model=HistoryListResponse)
async def delete_history(history_id: int):
    """
    Delete history by ID.
    
    - **history_id**: History ID
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if exists
    cursor.execute("SELECT id FROM content_history WHERE id = ?", (history_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="History not found")
    
    # Delete
    cursor.execute("DELETE FROM content_history WHERE id = ?", (history_id,))
    conn.commit()
    conn.close()
    
    return HistoryListResponse(
        code=200,
        message="History deleted successfully",
        data={"id": history_id}
    )


@router.get("/search", response_model=HistoryListResponse)
async def search_history(
    keyword: str = Query(..., description="Search keyword"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Page size")
):
    """
    Search history by keyword.
    
    - **keyword**: Search keyword in topic or content
    - **page**: Page number (default: 1)
    - **page_size**: Page size (default: 20, max: 100)
    """
    # Reuse list_history with keyword filter
    return await list_history(page=page, page_size=page_size, keyword=keyword)
