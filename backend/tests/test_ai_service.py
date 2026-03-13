# -*- coding: utf-8 -*-
"""
Unit tests for AI Service
"""

import pytest
from unittest.mock import Mock, patch
from app.ai.service import AIService
from app.ai.prompts import PromptLoader, Prompt
from app.config import config


class TestAIService:
    """Test cases for AIService."""
    
    def test_init(self):
        """Test AIService initialization."""
        service = AIService()
        assert service.api_key == config.DASHSCOPE_API_KEY
        assert service.max_retries == config.AI_MAX_RETRIES
    
    def test_generate_douyin_script(self):
        """Test Douyin script generation."""
        service = AIService()
        # Mock the _call_ai method
        with patch.object(service, '_call_ai', return_value="测试文案"):
            result = service.generate(
                prompt_name="douyin_script",
                variables={"topic": "AI 工具", "theme": "效率"}
            )
            assert len(result) > 0
    
    def test_validate_variables_complete(self):
        """Test variable validation with complete variables."""
        loader = PromptLoader()
        prompt = loader.get_prompt("douyin_script")
        assert prompt is not None
        
        variables = {"topic": "AI", "theme": "效率"}
        assert loader.validate_variables(prompt, variables) is True
    
    def test_validate_variables_missing(self):
        """Test variable validation with missing variables."""
        loader = PromptLoader()
        prompt = loader.get_prompt("douyin_script")
        assert prompt is not None
        
        # Missing variables should raise ValueError
        with pytest.raises(ValueError):
            loader.validate_variables(prompt, {})
    
    def test_fill_template_success(self):
        """Test template filling with all variables."""
        loader = PromptLoader()
        template = "Hello {name}, welcome to {place}!"
        variables = {"name": "Alice", "place": "Wonderland"}
        
        result = loader.fill_template(template, variables)
        assert result == "Hello Alice, welcome to Wonderland!"
    
    def test_fill_template_missing_var(self):
        """Test template filling with missing variables."""
        loader = PromptLoader()
        template = "Hello {name}, welcome to {place}!"
        variables = {"name": "Alice"}
        
        with pytest.raises(ValueError):
            loader.fill_template(template, variables)
    
    def test_cache_mechanism(self):
        """Test prompt caching."""
        loader = PromptLoader()
        
        # First call should load from database
        prompt1 = loader.get_prompt("douyin_script")
        assert prompt1 is not None
        
        # Second call should use cache
        prompt2 = loader.get_prompt("douyin_script")
        assert prompt2 is not None
        assert prompt1.id == prompt2.id
    
    def test_clear_cache(self):
        """Test cache clearing."""
        loader = PromptLoader()
        
        # Load a prompt to cache it
        loader.get_prompt("douyin_script")
        
        # Clear cache
        loader.clear_cache("douyin_script")
        
        # Cache should be empty for this prompt
        cache_key = "prompt:douyin_script"
        assert cache_key not in loader.cache
    
    def test_retry_mechanism(self):
        """Test retry mechanism with mock."""
        service = AIService()
        
        # Mock _call_ai to fail twice, then succeed
        call_count = [0]
        
        def mock_call(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] < 3:
                raise Exception("Simulated failure")
            return "Success"
        
        with patch.object(service, '_call_ai', side_effect=mock_call):
            result = service.generate(
                prompt_name="douyin_script",
                variables={"topic": "AI", "theme": "效率"}
            )
            assert result == "Success"
            assert call_count[0] == 3
    
    def test_config_timeout(self):
        """Test timeout configuration."""
        service = AIService()
        assert service.timeout == config.AI_TEXT_TIMEOUT
        assert service.image_timeout == config.AI_IMAGE_TIMEOUT
    
    def test_config_retry(self):
        """Test retry configuration."""
        service = AIService()
        assert service.max_retries == config.AI_MAX_RETRIES
        assert service.retry_base_delay == config.AI_RETRY_BASE_DELAY
    
    def test_generate_text_helper(self):
        """Test generate_text helper method."""
        service = AIService()
        
        with patch.object(service, 'generate', return_value="Text") as mock_gen:
            result = service.generate_text(
                prompt_name="wechat_article",
                variables={"topic": "AI", "theme": "效率"}
            )
            assert result == "Text"
            mock_gen.assert_called_once()
