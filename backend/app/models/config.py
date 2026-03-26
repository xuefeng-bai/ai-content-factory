# System Config Model

from sqlalchemy import Column, BigInteger, String, DateTime, Integer, SmallInteger, Text, text
from sqlalchemy.sql import func
from .base import Base


class SystemConfig(Base):
    """系统配置表 - 存储系统配置信息"""
    
    __tablename__ = "system_configs"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键 ID")
    config_key = Column(String(100), nullable=False, unique=True, comment="配置键（如：claude_api_key）")
    config_value = Column(Text, nullable=False, comment="配置值（加密存储）")
    config_type = Column(String(20), nullable=False, default="string", comment="配置类型：string/number/boolean/json")
    description = Column(String(500), nullable=True, comment="配置说明")
    is_encrypted = Column(SmallInteger, nullable=False, default=0, comment="是否加密：1=是，0=否")
    created_by = Column(String(50), nullable=False, default="admin", comment="创建人")
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    updated_by = Column(String(50), nullable=False, default="admin", comment="修改人")
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="修改时间")
    is_deleted = Column(SmallInteger, nullable=False, default=0, comment="删除标记")
    remark = Column(String(500), nullable=True, comment="备注")
    
    def __repr__(self):
        return f"<SystemConfig(id={self.id}, key='{self.config_key}')>"
