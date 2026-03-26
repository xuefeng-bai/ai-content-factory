# Content Generation Model

from sqlalchemy import Column, BigInteger, String, DateTime, Integer, SmallInteger, text
from sqlalchemy.sql import func
from .base import Base


class ContentGeneration(Base):
    """内容生成记录表 - 存储生成任务主记录"""
    
    __tablename__ = "content_generations"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键 ID")
    topic = Column(String(500), nullable=False, comment="生成主题")
    status = Column(String(20), nullable=False, default="pending", comment="状态：pending/processing/completed/failed/partial")
    template_id = Column(BigInteger, nullable=True, comment="使用的提示词模板 ID")
    created_by = Column(String(50), nullable=False, default="admin", comment="创建人")
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    updated_by = Column(String(50), nullable=False, default="admin", comment="修改人")
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="修改时间")
    is_deleted = Column(SmallInteger, nullable=False, default=0, comment="删除标记：0=未删除，1=已删除")
    remark = Column(String(500), nullable=True, comment="备注")
    
    def __repr__(self):
        return f"<ContentGeneration(id={self.id}, topic='{self.topic}', status='{self.status}')>"
