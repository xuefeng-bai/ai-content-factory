# -*- coding: utf-8 -*-
"""
Prompt Loader
Load prompts from database with caching support.
"""

import json
import time
from typing import Dict, Optional, List, Any
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import sqlite3

from app.config import config


@dataclass
class Prompt:
    """Prompt data structure."""
    id: int
    name: str
    display_name: str
    description: Optional[str]
    template: str
    variables: List[str]
    output_format: Optional[str]
    model: str
    max_tokens: int
    temperature: float
    is_active: bool
    is_system: bool
    category: Optional[str]
    created_at: datetime
    updated_at: datetime


class PromptLoader:
    """
    Load prompts from database with caching support.
    
    Features:
    - Cache prompts in memory
    - Auto-expire cache after TTL
    - Validate variables
    - Fill prompt templates
    """
    
    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize Prompt Loader.
        
        Args:
            db_path: Database file path (default: from config)
        """
        if db_path is None:
            # Parse database path from DATABASE_URL
            db_url = config.DATABASE_URL
            if db_url.startswith("sqlite:///"):
                db_path = Path(db_url.replace("sqlite:///", ""))
            else:
                db_path = Path("./data/content_factory.db")
        
        self.db_path = db_path
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.cache_timestamps: Dict[str, float] = {}
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn
    
    def _is_cache_valid(self, key: str) -> bool:
        """
        Check if cache is valid.
        
        Args:
            key: Cache key
        
        Returns:
            True if cache is valid
        """
        if not config.PROMPT_CACHE_ENABLED:
            return False
        
        if key not in self.cache_timestamps:
            return False
        
        age = time.time() - self.cache_timestamps[key]
        return age < config.PROMPT_CACHE_TTL
    
    def get_prompt(self, name: str) -> Optional[Prompt]:
        """
        Get prompt by name (with caching).
        
        Args:
            name: Prompt name (e.g., "douyin_script")
        
        Returns:
            Prompt object or None if not found
        """
        # Check cache
        cache_key = f"prompt:{name}"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]["prompt"]
        
        # Load from database
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM prompts 
            WHERE name = ? AND is_active = 1
        """, (name,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        # Parse prompt
        prompt = Prompt(
            id=row["id"],
            name=row["name"],
            display_name=row["display_name"],
            description=row["description"],
            template=row["template"],
            variables=json.loads(row["variables"]),
            output_format=row["output_format"],
            model=row["model"] or config.AI_MODEL,
            max_tokens=row["max_tokens"] or config.AI_MAX_TOKENS,
            temperature=row["temperature"] or config.AI_TEMPERATURE,
            is_active=bool(row["is_active"]),
            is_system=bool(row["is_system"]),
            category=row["category"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
        
        # Update cache
        if config.PROMPT_CACHE_ENABLED:
            self.cache[cache_key] = {"prompt": prompt}
            self.cache_timestamps[cache_key] = time.time()
        
        return prompt
    
    def get_prompt_by_id(self, prompt_id: int) -> Optional[Prompt]:
        """
        Get prompt by ID.
        
        Args:
            prompt_id: Prompt ID
        
        Returns:
            Prompt object or None if not found
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM prompts 
            WHERE id = ? AND is_active = 1
        """, (prompt_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return Prompt(
            id=row["id"],
            name=row["name"],
            display_name=row["display_name"],
            description=row["description"],
            template=row["template"],
            variables=json.loads(row["variables"]),
            output_format=row["output_format"],
            model=row["model"] or config.AI_MODEL,
            max_tokens=row["max_tokens"] or config.AI_MAX_TOKENS,
            temperature=row["temperature"] or config.AI_TEMPERATURE,
            is_active=bool(row["is_active"]),
            is_system=bool(row["is_system"]),
            category=row["category"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
    
    def validate_variables(self, prompt: Prompt, variables: Dict[str, Any]) -> bool:
        """
        Validate that all required variables are provided.
        
        Args:
            prompt: Prompt object
            variables: Variables dictionary
        
        Returns:
            True if valid
        
        Raises:
            ValueError: If variables are missing
        """
        missing = []
        for var in prompt.variables:
            if var not in variables:
                missing.append(var)
        
        if missing:
            raise ValueError(f"Missing required variables: {', '.join(missing)}")
        
        return True
    
    def fill_template(self, template: str, variables: Dict[str, Any]) -> str:
        """
        Fill prompt template with variables.
        
        Args:
            template: Prompt template
            variables: Variables dictionary
        
        Returns:
            Filled prompt
        """
        try:
            return template.format(**variables)
        except KeyError as e:
            raise ValueError(f"Missing variable in template: {e}")
    
    def clear_cache(self, name: Optional[str] = None) -> None:
        """
        Clear cache.
        
        Args:
            name: Specific prompt name to clear (None for all)
        """
        if name:
            cache_key = f"prompt:{name}"
            self.cache.pop(cache_key, None)
            self.cache_timestamps.pop(cache_key, None)
        else:
            self.cache.clear()
            self.cache_timestamps.clear()
    
    def list_prompts(self, category: Optional[str] = None) -> List[Prompt]:
        """
        List all active prompts.
        
        Args:
            category: Filter by category (optional)
        
        Returns:
            List of Prompt objects
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if category:
            cursor.execute("""
                SELECT * FROM prompts 
                WHERE is_active = 1 AND category = ?
                ORDER BY sort_order, id
            """, (category,))
        else:
            cursor.execute("""
                SELECT * FROM prompts 
                WHERE is_active = 1
                ORDER BY sort_order, id
            """)
        
        rows = cursor.fetchall()
        conn.close()
        
        prompts = []
        for row in rows:
            prompts.append(Prompt(
                id=row["id"],
                name=row["name"],
                display_name=row["display_name"],
                description=row["description"],
                template=row["template"],
                variables=json.loads(row["variables"]),
                output_format=row["output_format"],
                model=row["model"] or config.AI_MODEL,
                max_tokens=row["max_tokens"] or config.AI_MAX_TOKENS,
                temperature=row["temperature"] or config.AI_TEMPERATURE,
                is_active=bool(row["is_active"]),
                is_system=bool(row["is_system"]),
                category=row["category"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            ))
        
        return prompts
