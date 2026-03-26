# Image Service - Cover Image Generation

import httpx
import os
from typing import Optional

class ImageService:
    """图片服务 - 封面图生成"""
    
    def __init__(self):
        self.tongyi_wanxiang_api_key = os.getenv("TONGYI_WANXIANG_API_KEY", "")
    
    async def generate_cover(
        self,
        topic: str,
        platform: str
    ) -> str:
        """
        生成封面图
        
        **平台尺寸规范：**
        - 抖音/视频号：1080×1920 (9:16)
        - 公众号：900×383 (2.35:1)
        - 小红书：1242×1660 (3:4)
        """
        if not self.tongyi_wanxiang_api_key:
            # 返回默认占位图
            return self._get_placeholder_image(platform)
        
        # 构建图片生成提示词
        prompt = self._build_image_prompt(topic, platform)
        
        # 调用通义万相 API
        image_url = await self._generate_with_tongyi_wanxiang(prompt, platform)
        
        return image_url
    
    def _build_image_prompt(self, topic: str, platform: str) -> str:
        """构建图片生成提示词"""
        style_map = {
            "douyin": "现代、活力、吸引眼球",
            "video_account": "专业、清晰、有质感",
            "wechat": "商务、深度、专业",
            "xiaohongshu": "清新、时尚、生活化"
        }
        
        style = style_map.get(platform, "精美、专业")
        return f"为以下内容创作封面图，主题：{topic}。风格要求：{style}。高质量、专业设计。"
    
    async def _generate_with_tongyi_wanxiang(
        self,
        prompt: str,
        platform: str
    ) -> str:
        """使用通义万相生成图片"""
        # 通义万相 API 调用（示例）
        # 实际需要根据官方文档调整
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-to-image/generation"
        headers = {
            "Authorization": f"Bearer {self.tongyi_wanxiang_api_key}",
            "Content-Type": "application/json"
        }
        
        # 获取平台对应的尺寸
        size = self._get_platform_size(platform)
        
        payload = {
            "model": "wanx-v1",
            "input": {
                "prompt": prompt
            },
            "parameters": {
                "size": size,
                "n": 1,
                "style": "<auto>"
            }
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            # 返回图片 URL
            return data["output"]["results"][0]["url"]
    
    def _get_platform_size(self, platform: str) -> str:
        """获取平台对应的图片尺寸"""
        sizes = {
            "douyin": "1080x1920",
            "video_account": "1080x1920",
            "wechat": "900x383",
            "xiaohongshu": "1242x1660"
        }
        return sizes.get(platform, "1024x1024")
    
    def _get_placeholder_image(self, platform: str) -> str:
        """返回默认占位图"""
        # 使用 placehold.co 生成占位图
        size = self._get_platform_size(platform)
        return f"https://placehold.co/{size}/3b82f6/ffffff?text=AI+Content+Factory"
