# Database Initialization Script
# 修复 Windows 兼容性：使用 -m 参数运行时自动处理路径

import sys
from pathlib import Path

# 智能路径处理：支持直接运行和 -m 模块运行
# 修复 Windows: ModuleNotFoundError: No module named 'app'
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent

# 只在不是通过 -m 运行时才添加路径
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from app.models.base import Base
from app.models.generation import ContentGeneration
from app.models.item import ContentItem
from app.models.cover import CoverImage
from app.models.template import PromptTemplate
from app.models.config import SystemConfig
from app.utils.db import sync_engine

def init_db():
    """初始化数据库 - 创建所有表"""
    print("🔧 开始初始化数据库...")
    
    # 创建所有表
    Base.metadata.create_all(bind=sync_engine)
    
    print("✅ 数据库表创建完成！")
    print("\n📊 已创建的表：")
    print("  - content_generations (内容生成记录表)")
    print("  - content_items (内容项表)")
    print("  - cover_images (封面图表)")
    print("  - prompt_templates (提示词模板表)")
    print("  - system_configs (系统配置表)")
    
    # 插入默认提示词模板
    from sqlalchemy.orm import Session
    
    with Session(sync_engine) as session:
        # 检查是否已有默认模板
        existing = session.query(PromptTemplate).filter(
            PromptTemplate.is_default == 1
        ).first()
        
        if not existing:
            print("\n📝 插入默认提示词模板...")
            
            default_templates = [
                PromptTemplate(
                    name="抖音默认模板",
                    platform="douyin",
                    template_content="请为抖音平台写一个短视频脚本，主题是：{topic}。要求：节奏快、前 3 秒抓人、强吸引力开头，{word_count}。请使用 Markdown 格式输出，包含标题和正文。",
                    is_default=1,
                    is_active=1,
                    sort_order=1
                ),
                PromptTemplate(
                    name="视频号默认模板",
                    platform="video_account",
                    template_content="请为视频号写一个短视频脚本，主题是：{topic}。要求：{style}，{word_count}。请使用 Markdown 格式输出，包含标题和正文。",
                    is_default=1,
                    is_active=1,
                    sort_order=2
                ),
                PromptTemplate(
                    name="公众号默认模板",
                    platform="wechat",
                    template_content="请为公众号写一篇图文文章，主题是：{topic}。要求：深度、专业、逻辑清晰，{word_count}。请使用 Markdown 格式输出，包含标题、小标题和正文。",
                    is_default=1,
                    is_active=1,
                    sort_order=3
                ),
                PromptTemplate(
                    name="小红书默认模板",
                    platform="xiaohongshu",
                    template_content="请为小红书写一篇图文笔记，主题是：{topic}。要求：真实分享风格、emoji 丰富、口语化，{word_count}。请使用 Markdown 格式输出，包含标题和正文。",
                    is_default=1,
                    is_active=1,
                    sort_order=4
                )
            ]
            
            session.add_all(default_templates)
            session.commit()
            print("✅ 默认模板插入完成！")
        else:
            print("\nℹ️ 默认模板已存在，跳过插入")
    
    print("\n✨ 数据库初始化完成！")


if __name__ == "__main__":
    init_db()
