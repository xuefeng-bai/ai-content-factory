# Prompt Template API Routes

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app.utils.db import get_db
from app.models.template import PromptTemplate

router = APIRouter()


@router.get("")
async def get_templates(
    platform: Optional[str] = None,
    is_default: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    获取提示词模板列表
    
    **支持筛选：**
    - platform: 按平台筛选
    - is_default: 是否系统默认
    """
    query = db.query(PromptTemplate).filter(
        PromptTemplate.is_deleted == 0
    )
    
    if platform:
        query = query.filter(PromptTemplate.platform == platform)
    
    if is_default is not None:
        query = query.filter(PromptTemplate.is_default == is_default)
    
    # 按排序顺序
    query = query.order_by(PromptTemplate.sort_order, PromptTemplate.id)
    
    templates = query.all()
    
    return {
        "code": 200,
        "message": "success",
        "data": [
            {
                "id": t.id,
                "name": t.name,
                "platform": t.platform,
                "template_content": t.template_content,
                "is_default": t.is_default,
                "is_active": t.is_active,
                "sort_order": t.sort_order
            }
            for t in templates
        ]
    }


@router.post("")
async def create_template(
    name: str,
    platform: str,
    template_content: str,
    is_active: int = 1,
    sort_order: int = 0,
    db: Session = Depends(get_db)
):
    """
    创建提示词模板
    """
    template = PromptTemplate(
        name=name,
        platform=platform,
        template_content=template_content,
        is_default=0,
        is_active=is_active,
        sort_order=sort_order,
        created_by="admin",
        updated_by="admin"
    )
    db.add(template)
    db.commit()
    db.refresh(template)
    
    return {
        "code": 200,
        "message": "创建成功",
        "data": {
            "id": template.id
        }
    }


@router.put("/{template_id}")
async def update_template(
    template_id: int,
    name: Optional[str] = None,
    template_content: Optional[str] = None,
    is_active: Optional[int] = None,
    sort_order: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    更新提示词模板
    """
    template = db.query(PromptTemplate).filter(
        PromptTemplate.id == template_id,
        PromptTemplate.is_deleted == 0
    ).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")
    
    # 系统默认模板不可修改
    if template.is_default == 1:
        raise HTTPException(status_code=403, detail="系统默认模板不可修改")
    
    # 更新字段
    if name is not None:
        template.name = name
    if template_content is not None:
        template.template_content = template_content
    if is_active is not None:
        template.is_active = is_active
    if sort_order is not None:
        template.sort_order = sort_order
    
    template.updated_by = "admin"
    db.commit()
    
    return {
        "code": 200,
        "message": "更新成功"
    }


@router.delete("/{template_id}")
async def delete_template(
    template_id: int,
    db: Session = Depends(get_db)
):
    """
    删除提示词模板
    
    **业务规则：**
    - 系统默认模板不可删除，只能禁用
    """
    template = db.query(PromptTemplate).filter(
        PromptTemplate.id == template_id,
        PromptTemplate.is_deleted == 0
    ).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")
    
    # 系统默认模板不可删除
    if template.is_default == 1:
        raise HTTPException(status_code=403, detail="系统默认模板不可删除，只能禁用")
    
    # 软删除
    template.is_deleted = 1
    db.commit()
    
    return {
        "code": 200,
        "message": "删除成功"
    }
