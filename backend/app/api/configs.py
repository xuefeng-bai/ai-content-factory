# System Config API Routes

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.utils.db import get_db
from app.models.config import SystemConfig

router = APIRouter()


@router.get("")
async def get_configs(db: Session = Depends(get_db)):
    """
    获取系统配置列表
    """
    configs = db.query(SystemConfig).filter(
        SystemConfig.is_deleted == 0
    ).all()
    
    return {
        "code": 200,
        "message": "success",
        "data": [
            {
                "config_key": c.config_key,
                "config_value": c.config_value if not c.is_encrypted else "***",
                "config_type": c.config_type,
                "description": c.description,
                "is_encrypted": c.is_encrypted
            }
            for c in configs
        ]
    }


@router.put("/{config_key}")
async def update_config(
    config_key: str,
    config_value: str,
    db: Session = Depends(get_db)
):
    """
    更新系统配置
    """
    config = db.query(SystemConfig).filter(
        SystemConfig.config_key == config_key,
        SystemConfig.is_deleted == 0
    ).first()
    
    if not config:
        # 创建新配置
        config = SystemConfig(
            config_key=config_key,
            config_value=config_value,
            config_type="string",
            description="",
            is_encrypted=0,
            created_by="admin",
            updated_by="admin"
        )
        db.add(config)
    else:
        config.config_value = config_value
        config.updated_by = "admin"
    
    db.commit()
    
    return {
        "code": 200,
        "message": "更新成功"
    }
