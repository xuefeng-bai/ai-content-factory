# -*- coding: utf-8 -*-
"""
Prompt Database Models
SQLAlchemy models for prompt management.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import json


# ==================== Prompt 模型 ====================

class Prompt:
    """Prompt 模型（使用字典，不依赖 SQLAlchemy ORM）."""
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self) -> dict:
        """转换为字典."""
        return {
            'id': getattr(self, 'id', None),
            'name': getattr(self, 'name', None),
            'display_name': getattr(self, 'display_name', None),
            'description': getattr(self, 'description', None),
            'template': getattr(self, 'template', None),
            'variables': self._parse_variables(),
            'output_format': getattr(self, 'output_format', None),
            'model': getattr(self, 'model', 'qwen-plus'),
            'max_tokens': getattr(self, 'max_tokens', 2000),
            'temperature': getattr(self, 'temperature', 0.7),
            'category': getattr(self, 'category', None),
            'sort_order': getattr(self, 'sort_order', 0),
            'is_system': bool(getattr(self, 'is_system', False)),
            'is_active': bool(getattr(self, 'is_active', True)),
            'created_at': str(getattr(self, 'created_at', datetime.now())),
            'updated_at': str(getattr(self, 'updated_at', datetime.now())),
        }
    
    def _parse_variables(self) -> list:
        """解析 variables 字段（JSON 字符串转列表）."""
        variables = getattr(self, 'variables', '[]')
        if isinstance(variables, str):
            try:
                return json.loads(variables)
            except:
                return []
        return variables if variables else []


class PromptVersion:
    """Prompt 版本模型."""
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self) -> dict:
        """转换为字典."""
        return {
            'id': getattr(self, 'id', None),
            'prompt_id': getattr(self, 'prompt_id', None),
            'version': getattr(self, 'version', None),
            'template': getattr(self, 'template', None),
            'variables': self._parse_variables(),
            'change_log': getattr(self, 'change_log', None),
            'is_published': bool(getattr(self, 'is_published', False)),
            'created_at': str(getattr(self, 'created_at', datetime.now())),
        }
    
    def _parse_variables(self) -> list:
        """解析 variables 字段."""
        variables = getattr(self, 'variables', '[]')
        if isinstance(variables, str):
            try:
                return json.loads(variables)
            except:
                return []
        return variables if variables else []


class PromptTestLog:
    """Prompt 测试日志模型."""
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self) -> dict:
        """转换为字典."""
        return {
            'id': getattr(self, 'id', None),
            'prompt_id': getattr(self, 'prompt_id', None),
            'version_id': getattr(self, 'version_id', None),
            'input_variables': getattr(self, 'input_variables', None),
            'output': getattr(self, 'output', None),
            'model_used': getattr(self, 'model_used', None),
            'tokens_used': getattr(self, 'tokens_used', None),
            'duration_ms': getattr(self, 'duration_ms', None),
            'rating': getattr(self, 'rating', None),
            'feedback': getattr(self, 'feedback', None),
            'created_at': str(getattr(self, 'created_at', datetime.now())),
        }


class ContentHistory:
    """内容历史记录模型."""
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self) -> dict:
        """转换为字典."""
        return {
            'id': getattr(self, 'id', None),
            'theme': getattr(self, 'theme', None),
            'topic': getattr(self, 'topic', None),
            'platform': getattr(self, 'platform', None),
            'content': getattr(self, 'content', None),
            'image_urls': self._parse_image_urls(),
            'created_at': str(getattr(self, 'created_at', datetime.now())),
            'updated_at': str(getattr(self, 'updated_at', datetime.now())),
        }
    
    def _parse_image_urls(self) -> list:
        """解析 image_urls 字段."""
        image_urls = getattr(self, 'image_urls', '[]')
        if isinstance(image_urls, str):
            try:
                return json.loads(image_urls)
            except:
                return []
        return image_urls if image_urls else []
