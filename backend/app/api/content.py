# Content Generation API Routes

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime

from app.utils.db import get_db
from app.models.generation import ContentGeneration
from app.models.item import ContentItem
from app.models.cover import CoverImage
from app.models.template import PromptTemplate
from app.services.generator import ContentGeneratorService

router = APIRouter()


@router.post("/generate")
async def generate_content(
    topic: str,
    template_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    一键生成 4 平台内容
    
    **请求参数：**
    - topic: 生成主题（1-500 字）
    - template_id: 提示词模板 ID（可选，不传则使用默认）
    
    **返回：**
    - generation_id: 生成任务 ID
    - message: 提示信息
    """
    try:
        # 创建生成任务
        generation = ContentGeneration(
            topic=topic,
            status="pending",
            template_id=template_id,
            created_by="admin",
            updated_by="admin"
        )
        db.add(generation)
        db.commit()
        db.refresh(generation)
        
        # 异步启动生成任务（实际应该用 Celery 等任务队列）
        # 这里简化为同步生成
        generator = ContentGeneratorService(db)
        await generator.generate_all_platforms(
            generation_id=generation.id,
            topic=topic,
            template_id=template_id
        )
        
        return {
            "code": 200,
            "message": "生成任务已创建，请稍后查看结果",
            "data": {
                "generation_id": generation.id
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{generation_id}")
async def get_generation_detail(
    generation_id: int,
    db: Session = Depends(get_db)
):
    """
    获取生成内容详情
    
    **返回：**
    - 生成任务信息
    - 4 个平台的内容项
    - 封面图 URL
    """
    generation = db.query(ContentGeneration).filter(
        ContentGeneration.id == generation_id,
        ContentGeneration.is_deleted == 0
    ).first()
    
    if not generation:
        raise HTTPException(status_code=404, detail="生成记录不存在")
    
    # 获取所有内容项
    items = db.query(ContentItem).filter(
        ContentItem.generation_id == generation_id,
        ContentItem.is_deleted == 0,
        ContentItem.is_latest == 1
    ).all()
    
    # 获取封面图
    cover_images = []
    for item in items:
        cover = db.query(CoverImage).filter(
            CoverImage.content_id == item.id,
            CoverImage.is_deleted == 0
        ).first()
        if cover:
            cover_images.append({
                "platform": item.platform,
                "url": cover.image_url,
                "width": cover.image_width,
                "height": cover.image_height
            })
    
    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": generation.id,
            "topic": generation.topic,
            "status": generation.status,
            "created_at": generation.created_at.isoformat(),
            "items": [
                {
                    "id": item.id,
                    "platform": item.platform,
                    "title": item.title,
                    "content": item.content,
                    "version": item.version,
                    "status": item.status,
                    "error_message": item.error_message,
                    "cover_image_url": next(
                        (c["url"] for c in cover_images if c["platform"] == item.platform),
                        None
                    )
                }
                for item in items
            ]
        }
    }


@router.put("/{generation_id}")
async def update_content(
    generation_id: int,
    platform: str,
    content: str,
    title: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    更新内容（Markdown 编辑）
    
    **业务规则：**
    - 更新后创建新版本，version+1
    - 旧版本 is_latest=0
    """
    # 获取最新的内容项
    old_item = db.query(ContentItem).filter(
        ContentItem.generation_id == generation_id,
        ContentItem.platform == platform,
        ContentItem.is_latest == 1,
        ContentItem.is_deleted == 0
    ).first()
    
    if not old_item:
        raise HTTPException(status_code=404, detail="内容项不存在")
    
    # 创建新版本
    new_item = ContentItem(
        generation_id=generation_id,
        platform=platform,
        title=title or old_item.title,
        content=content,
        version=old_item.version + 1,
        is_latest=1,
        status="success",
        created_by="admin",
        updated_by="admin"
    )
    db.add(new_item)
    
    # 将旧版本设置为非最新
    old_item.is_latest = 0
    db.commit()
    
    return {
        "code": 200,
        "message": "更新成功"
    }


@router.post("/{generation_id}/regenerate")
async def regenerate_platform(
    generation_id: int,
    platform: str,
    template_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    重新生成某平台内容
    
    **业务规则：**
    - 重新生成不限制次数
    - 保留原版本为历史记录
    """
    generation = db.query(ContentGeneration).filter(
        ContentGeneration.id == generation_id
    ).first()
    
    if not generation:
        raise HTTPException(status_code=404, detail="生成记录不存在")
    
    # 启动重新生成
    generator = ContentGeneratorService(db)
    await generator.generate_single_platform(
        generation_id=generation_id,
        platform=platform,
        topic=generation.topic,
        template_id=template_id
    )
    
    return {
        "code": 200,
        "message": "重新生成任务已创建"
    }


@router.get("/history")
async def get_history(
    page: int = 1,
    page_size: int = 20,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    获取历史记录列表
    
    **支持：**
    - 分页
    - 按主题搜索
    """
    query = db.query(ContentGeneration).filter(
        ContentGeneration.is_deleted == 0
    )
    
    if keyword:
        query = query.filter(ContentGeneration.topic.like(f"%{keyword}%"))
    
    # 按创建时间倒序
    query = query.order_by(ContentGeneration.created_at.desc())
    
    # 分页
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "code": 200,
        "message": "success",
        "data": {
            "total": total,
            "list": [
                {
                    "id": item.id,
                    "topic": item.topic,
                    "status": item.status,
                    "created_at": item.created_at.isoformat()
                }
                for item in items
            ]
        }
    }


@router.delete("/{generation_id}")
async def delete_generation(
    generation_id: int,
    db: Session = Depends(get_db)
):
    """
    删除生成记录（软删除）
    """
    generation = db.query(ContentGeneration).filter(
        ContentGeneration.id == generation_id
    ).first()
    
    if not generation:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    generation.is_deleted = 1
    db.commit()
    
    return {
        "code": 200,
        "message": "删除成功"
    }
