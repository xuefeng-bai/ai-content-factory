# Content Generator Service

from sqlalchemy.orm import Session
from typing import Optional, List
import asyncio
from datetime import datetime

from app.models.generation import ContentGeneration
from app.models.item import ContentItem
from app.models.cover import CoverImage
from app.models.template import PromptTemplate
from app.services.ai_service import AIService
from app.services.image_service import ImageService


class ContentGeneratorService:
    """内容生成服务 - 负责 4 平台内容生成"""
    
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIService()
        self.image_service = ImageService()
    
    async def generate_all_platforms(
        self,
        generation_id: int,
        topic: str,
        template_id: Optional[int] = None
    ):
        """
        逐一生成 4 个平台的内容
        
        生成顺序：抖音 → 视频号 → 公众号 → 小红书
        """
        # 更新任务状态为 processing
        generation = self.db.query(ContentGeneration).get(generation_id)
        generation.status = "processing"
        self.db.commit()
        
        platforms = ["douyin", "video_account", "wechat", "xiaohongshu"]
        success_count = 0
        failed_count = 0
        
        for platform in platforms:
            try:
                # 逐一生成
                await self.generate_single_platform(
                    generation_id=generation_id,
                    platform=platform,
                    topic=topic,
                    template_id=template_id
                )
                success_count += 1
            except Exception as e:
                print(f"生成 {platform} 失败：{e}")
                failed_count += 1
        
        # 更新任务状态
        if failed_count == 0:
            generation.status = "completed"
        elif success_count > 0:
            generation.status = "partial"
        else:
            generation.status = "failed"
        
        self.db.commit()
    
    async def generate_single_platform(
        self,
        generation_id: int,
        platform: str,
        topic: str,
        template_id: Optional[int] = None
    ):
        """
        生成单个平台的内容
        """
        # 获取提示词模板
        template = None
        if template_id:
            template = self.db.query(PromptTemplate).filter(
                PromptTemplate.id == template_id,
                PromptTemplate.is_active == 1
            ).first()
        
        if not template:
            # 使用平台默认模板
            template = self.db.query(PromptTemplate).filter(
                PromptTemplate.platform == platform,
                PromptTemplate.is_default == 1,
                PromptTemplate.is_active == 1
            ).first()
        
        # 构建提示词
        prompt = self._build_prompt(template, topic, platform)
        
        # 调用 AI 服务生成内容
        content_text = await self.ai_service.generate_content(
            prompt=prompt,
            platform=platform
        )
        
        # 解析内容（标题 + 正文）
        title, content = self._parse_content(content_text)
        
        # 创建内容项
        item = ContentItem(
            generation_id=generation_id,
            platform=platform,
            title=title,
            content=content,
            version=1,
            is_latest=1,
            status="success",
            created_by="admin",
            updated_by="admin"
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        
        # 生成封面图
        try:
            image_url = await self.image_service.generate_cover(
                topic=topic,
                platform=platform
            )
            
            cover = CoverImage(
                content_id=item.id,
                platform=platform,
                image_url=image_url,
                status="success",
                created_by="admin",
                updated_by="admin"
            )
            self.db.add(cover)
            self.db.commit()
        except Exception as e:
            print(f"生成封面图失败：{e}")
            # 封面图失败不影响内容
        
        return item
    
    def _build_prompt(
        self,
        template: Optional[PromptTemplate],
        topic: str,
        platform: str
    ) -> str:
        """构建 AI 提示词"""
        if not template or not template.template_content:
            # 默认提示词
            default_prompts = {
                "douyin": f"请为抖音平台写一个短视频脚本，主题是：{topic}。要求：节奏快、前 3 秒抓人、强吸引力开头，200-400 字。请使用 Markdown 格式输出，包含标题和正文。",
                "video_account": f"请为视频号写一个短视频脚本，主题是：{topic}。要求：风格自然、有吸引力，200-400 字。请使用 Markdown 格式输出，包含标题和正文。",
                "wechat": f"请为公众号写一篇图文文章，主题是：{topic}。要求：深度、专业、逻辑清晰，1000-3000 字。请使用 Markdown 格式输出，包含标题、小标题和正文。",
                "xiaohongshu": f"请为小红书写一篇图文笔记，主题是：{topic}。要求：真实分享风格、emoji 丰富、口语化，300-500 字。请使用 Markdown 格式输出，包含标题和正文。"
            }
            return default_prompts.get(platform, f"请为{platform}平台创作内容，主题是：{topic}")
        
        # 使用模板，替换参数
        prompt = template.template_content
        prompt = prompt.replace("{topic}", topic)
        prompt = prompt.replace("{style}", "专业、有吸引力")
        prompt = prompt.replace("{word_count}", self._get_word_count_range(platform))
        
        return prompt
    
    def _get_word_count_range(self, platform: str) -> str:
        """获取字数范围"""
        ranges = {
            "douyin": "200-400 字",
            "video_account": "200-400 字",
            "wechat": "1000-3000 字",
            "xiaohongshu": "300-500 字"
        }
        return ranges.get(platform, "300-500 字")
    
    def _parse_content(self, content_text: str) -> tuple:
        """
        解析 AI 生成的内容
        返回：(title, content)
        """
        lines = content_text.strip().split("\n")
        title = ""
        content = content_text.strip()
        
        # 尝试提取标题（第一个非空行）
        for line in lines:
            line = line.strip()
            if line:
                # 去掉 Markdown 标题符号
                if line.startswith("# "):
                    title = line[2:].strip()
                elif line.startswith("## "):
                    title = line[3:].strip()
                else:
                    title = line
                break
        
        return title, content
