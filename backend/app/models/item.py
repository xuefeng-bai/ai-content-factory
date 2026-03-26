# Content Item Model

from sqlalchemy import Column, BigInteger, String, DateTime, Integer, SmallInteger, Text, ForeignKey, text
from sqlalchemy.sql import func
from .base import Base


class ContentItem(Base):
    """内容项表 - 存储各平台生成的内容"""
    
    __tablename__ = "content_items"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键 ID")
    generation_id = Column(BigInteger, ForeignKey("content_generations.id"), nullable=False, comment="生成任务 ID（外键）")
    platform = Column(String(20), nullable=False, comment="平台：douyin/video_account/wechat/xiaohongshu")
    title = Column(String(200), nullable=True, comment="标题")
    content = Column(Text, nullable=False, comment="内容正文（Markdown 格式）")
    version = Column(Integer, nullable=False, default=1, comment="版本号")
    is_latest = Column(SmallInteger, nullable=False, default=1, comment="是否最新版本：1=是，0=否")
    status = Column(String(20), nullable=False, default="success", comment="状态：success/failed/pending")
    error_message = Column(String(500), nullable=True, comment="失败错误信息")
    created_by = Column(String(50), nullable=False, default="admin", comment="创建人")
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    updated_by = Column(String(50), nullable=False, default="admin", comment="修改人")
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="修改时间")
    is_deleted = Column(SmallInteger, nullable=False, default=0, comment="删除标记")
    remark = Column(String(500), nullable=True, comment="备注")
    
    def __repr__(self):
        return f"<ContentItem(id={self.id}, platform='{self.platform}', title='{self.title}')>"
