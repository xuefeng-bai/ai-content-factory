# -*- coding: utf-8 -*-
"""
AI Service - Image Generation Support
支持图片生成的 AI 服务
"""

import time
import logging
import base64
from typing import Dict, Any, Optional, List
from pathlib import Path

import dashscope
from dashscope import Generation

# 兼容不同版本的 dashscope
try:
    from dashscope import ImageSynthesis
except ImportError:
    from dashscope.aigc.image_synthesis import ImageSynthesis

from app.config import config
from app.ai.prompts import PromptLoader, Prompt


# Configure logging
logger = logging.getLogger(__name__)


class AIService:
    """
    AI Service for content generation.
    
    Features:
    - Load prompts from database
    - Validate variables
    - Fill prompt templates
    - Call DashScope AI with retry and timeout (text & image)
    - Log generation history
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI Service.
        
        Args:
            api_key: DashScope API key (default: from config)
        """
        self.api_key = api_key or config.DASHSCOPE_API_KEY
        dashscope.api_key = self.api_key
        
        self.loader = PromptLoader()
        self.timeout = config.AI_TEXT_TIMEOUT
        self.image_timeout = config.AI_IMAGE_TIMEOUT
        self.max_retries = config.AI_MAX_RETRIES
        self.retry_base_delay = config.AI_RETRY_BASE_DELAY
    
    def generate(
        self,
        prompt_name: str,
        variables: Dict[str, Any],
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        is_image: bool = False
    ) -> str:
        """
        Generate content using AI.
        
        Args:
            prompt_name: Prompt name (e.g., "douyin_script")
            variables: Variables dictionary
            model: AI model (optional, default from prompt)
            max_tokens: Max tokens (optional, default from prompt)
            temperature: Temperature (optional, default from prompt)
            is_image: True for image generation prompts
        
        Returns:
            Generated content
        
        Raises:
            ValueError: If prompt not found or variables invalid
            Exception: If AI generation fails
        """
        # 1. Load prompt
        prompt = self.loader.get_prompt(prompt_name)
        if not prompt:
            raise ValueError(f"Prompt not found: {prompt_name}")
        
        # 2. Validate variables
        self.loader.validate_variables(prompt, variables)
        
        # 3. Fill template
        filled_prompt = self.loader.fill_template(prompt.template, variables)
        
        # 4. Get parameters
        model = model or prompt.model
        max_tokens = max_tokens or prompt.max_tokens
        temperature = temperature or prompt.temperature
        timeout = self.image_timeout if is_image else self.timeout
        
        # 5. Call AI with retry
        last_error = None
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Calling AI (attempt {attempt + 1}/{self.max_retries})")
                logger.debug(f"Prompt: {filled_prompt[:200]}...")
                
                if is_image:
                    # 图片生成返回的是 URL，不是文本
                    result = self._call_image_ai(
                        prompt=filled_prompt,
                        timeout=timeout
                    )
                    logger.info(f"Image generation successful, URL: {result}")
                    return result
                else:
                    # 文本生成
                    response = self._call_ai(
                        prompt=filled_prompt,
                        model=model,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        timeout=timeout
                    )
                    logger.info(f"AI generation successful, {len(response)} characters")
                    return response
                
            except Exception as e:
                last_error = e
                logger.warning(f"AI generation failed (attempt {attempt + 1}): {e}")
                
                if attempt < self.max_retries - 1:
                    delay = self.retry_base_delay * (2 ** attempt)
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
        
        # All retries failed
        logger.error(f"AI generation failed after {self.max_retries} attempts")
        raise last_error
    
    def _call_ai(
        self,
        prompt: str,
        model: str,
        max_tokens: int,
        temperature: float,
        timeout: int
    ) -> str:
        """
        Call DashScope AI for text generation.
        
        Args:
            prompt: Filled prompt
            model: AI model
            max_tokens: Max tokens
            temperature: Temperature
            timeout: Timeout in seconds
        
        Returns:
            Generated text content
        """
        try:
            response = Generation.call(
                model=model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=timeout,
                result_format='message'
            )
            
            if response.status_code == 200:
                return response.output.choices[0].message.content
            else:
                raise Exception(
                    f"AI API error: {response.status_code} - {response.message}"
                )
                
        except Exception as e:
            logger.error(f"DashScope API error: {e}")
            raise
    
    def _call_image_ai(
        self,
        prompt: str,
        size: str = "1024x1024",
        n: int = 1,
        timeout: int = 60
    ) -> str:
        """
        Call DashScope Image Synthesis API.
        
        Args:
            prompt: Image generation prompt
            size: Image size (1024x1024, 720x1280, 1280x720)
            n: Number of images to generate
            timeout: Timeout in seconds
        
        Returns:
            Image URL (first image if multiple)
        """
        try:
            logger.info(f"Calling DashScope Image Synthesis API: prompt={prompt[:100]}...")
            
            response = ImageSynthesis.call(
                model='wanx-v1',  # 通义万相文生图模型
                prompt=prompt,
                n=n,
                size=size,
                timeout=timeout
            )
            
            if response.status_code == 200:
                # 返回第一张图片的 URL
                image_url = response.output.results[0].url
                logger.info(f"Image generated successfully: {image_url}")
                return image_url
            else:
                raise Exception(
                    f"Image API error: {response.status_code} - {response.message}"
                )
                
        except Exception as e:
            logger.error(f"DashScope Image API error: {e}")
            raise
    
    def generate_image(
        self,
        prompt: str,
        title: str,
        aspect_ratio: str = "16:9",
        platform: str = "wechat",
        size: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate image with metadata.
        
        Args:
            prompt: Image generation prompt
            title: Image title
            aspect_ratio: Aspect ratio (16:9, 3:4, 1:1)
            platform: Platform (wechat/xhs)
            size: Custom size (optional, auto-calculated if not provided)
        
        Returns:
            Dictionary with image_url, title, aspect_ratio, platform, prompt
        """
        # 根据宽高比计算尺寸
        if not size:
            size_map = {
                "16:9": "1280x720",  # 公众号封面
                "3:4": "768x1024",   # 小红书封面
                "1:1": "1024x1024",  # 正方形
            }
            size = size_map.get(aspect_ratio, "1024x1024")
        
        # 生成图片
        image_url = self._call_image_ai(
            prompt=prompt,
            size=size,
            n=1,
            timeout=self.image_timeout
        )
        
        return {
            "image_url": image_url,
            "title": title,
            "aspect_ratio": aspect_ratio,
            "platform": platform,
            "prompt": prompt,
            "size": size
        }
    
    def generate_text(
        self,
        prompt_name: str,
        variables: Dict[str, Any],
        **kwargs
    ) -> str:
        """
        Generate text content.
        
        Args:
            prompt_name: Prompt name
            variables: Variables dictionary
            **kwargs: Additional parameters
        
        Returns:
            Generated text
        """
        return self.generate(
            prompt_name=prompt_name,
            variables=variables,
            is_image=False,
            **kwargs
        )
    
    def test_prompt(
        self,
        prompt_id: int,
        variables: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Test a prompt (for management interface).
        
        Args:
            prompt_id: Prompt ID
            variables: Variables dictionary
        
        Returns:
            Test result with output, tokens_used, duration_ms
        """
        prompt = self.loader.get_prompt_by_id(prompt_id)
        if not prompt:
            raise ValueError(f"Prompt not found: {prompt_id}")
        
        start_time = time.time()
        
        # Generate
        output = self.generate(
            prompt_name=prompt.name,
            variables=variables
        )
        
        duration_ms = int((time.time() - start_time) * 1000)
        
        return {
            "output": output,
            "tokens_used": len(output) // 4,  # Estimate
            "duration_ms": duration_ms,
            "model": prompt.model
        }
    
    def clear_cache(self, prompt_name: Optional[str] = None) -> None:
        """
        Clear prompt cache.
        
        Args:
            prompt_name: Specific prompt to clear (None for all)
        """
        self.loader.clear_cache(prompt_name)
