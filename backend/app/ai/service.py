# -*- coding: utf-8 -*-
"""
AI Service
Unified interface for AI generation with retry and timeout support.
"""

import time
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

import dashscope
from dashscope import Generation

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
    - Call DashScope AI with retry and timeout
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
        Call DashScope AI.
        
        Args:
            prompt: Filled prompt
            model: AI model
            max_tokens: Max tokens
            temperature: Temperature
            timeout: Timeout in seconds
        
        Returns:
            Generated content
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
