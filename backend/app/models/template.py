# Prompt Template Model

from sqlalchemy import Column, BigInteger, String, DateTime, Integer, SmallInteger, Text, text
from sqlalchemy.sql import func
from .base import Base


class PromptTemplate(Base):
    """提示词模板表 - 存储 AI 生成提示词模板"""
    
    __tablename__ = "prompt_templates"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键 ID")
    name = Column(String(100), nullable=False, comment="模板名称")
    platform = Column(String(20), nullable=False, comment="适用平台：all/douyin/video_account/wechat/xiaohongshu")
    template_content = Column(Text, nullable=False, comment="模板内容（支持参数：{topic},{style},{word_count}）")
    is_default = Column(SmallInteger, nullable=False, default=0, comment="是否系统默认：1=是，0=否")
    is_active = Column(SmallInteger, nullable=False, default=1, comment="是否启用：1=是，0=否")
    sort_order = Column(Integer, nullable=False, default=0, comment="排序顺序")
    created_by = Column(String(50), nullable=False, default="admin", comment="创建人")
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    updated_by = Column(String(50), nullable=False, default="admin", comment="修改人")
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="修改时间")
    is_deleted = Column(SmallInteger, nullable=False, default=0, comment="删除标记")
    remark = Column(String(500), nullable=True, comment="备注")
    
    def __repr__(self):
        return f"<PromptTemplate(id={self.id}, name='{self.name}', platform='{self.platform}')>"
