# AI Service - Content Generation

import httpx
import os
from typing import Optional

class AIService:
    """AI 服务 - 内容生成"""
    
    def __init__(self):
        self.claude_api_key = os.getenv("CLAUDE_API_KEY", "")
        self.tongyi_api_key = os.getenv("TONGYI_API_KEY", "")
        self.default_provider = os.getenv("DEFAULT_AI_PROVIDER", "claude")
    
    async def generate_content(
        self,
        prompt: str,
        platform: str
    ) -> str:
        """
        调用 AI 服务生成内容
        
        **双备份策略：**
        1. 优先使用默认服务商
        2. 失败时切换到备用服务商
        """
        if self.default_provider == "claude":
            try:
                return await self._generate_with_claude(prompt)
            except Exception as e:
                print(f"Claude 失败，切换到通义千问：{e}")
                return await self._generate_with_tongyi(prompt)
        else:
            try:
                return await self._generate_with_tongyi(prompt)
            except Exception as e:
                print(f"通义千问失败，切换到 Claude: {e}")
                return await self._generate_with_claude(prompt)
    
    async def _generate_with_claude(self, prompt: str) -> str:
        """使用 Claude 生成内容"""
        if not self.claude_api_key:
            raise Exception("Claude API Key 未配置")
        
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "X-API-Key": self.claude_api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        payload = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 4096,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            return data["content"][0]["text"]
    
    async def _generate_with_tongyi(self, prompt: str) -> str:
        """使用通义千问生成内容"""
        if not self.tongyi_api_key:
            raise Exception("通义千问 API Key 未配置")
        
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        headers = {
            "Authorization": f"Bearer {self.tongyi_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "qwen-max",
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            return data["output"]["text"]
