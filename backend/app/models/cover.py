# Cover Image Model

from sqlalchemy import Column, BigInteger, String, DateTime, Integer, SmallInteger, ForeignKey, text
from sqlalchemy.sql import func
from .base import Base


class CoverImage(Base):
    """封面图表 - 存储封面图 URL"""
    
    __tablename__ = "cover_images"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键 ID")
    content_id = Column(BigInteger, ForeignKey("content_items.id"), nullable=False, comment="内容项 ID（外键）")
    platform = Column(String(20), nullable=False, comment="平台")
    image_url = Column(String(500), nullable=False, comment="图片 URL")
    image_width = Column(Integer, nullable=True, comment="图片宽度")
    image_height = Column(Integer, nullable=True, comment="图片高度")
    status = Column(String(20), nullable=False, default="success", comment="状态：success/failed/pending")
    created_by = Column(String(50), nullable=False, default="admin", comment="创建人")
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    updated_by = Column(String(50), nullable=False, default="admin", comment="修改人")
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="修改时间")
    is_deleted = Column(SmallInteger, nullable=False, default=0, comment="删除标记")
    remark = Column(String(500), nullable=True, comment="备注")
    
    def __repr__(self):
        return f"<CoverImage(id={self.id}, platform='{self.platform}', url='{self.image_url}')>"
