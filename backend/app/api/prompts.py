# -*- coding: utf-8 -*-
"""
Prompt Management API
Provides CRUD operations for prompts.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
import sqlite3
from pathlib import Path


router = APIRouter(prefix="/api/prompts", tags=["Prompts"])


# ==================== Models ====================

class PromptBase(BaseModel):
    """Base prompt model."""
    display_name: str = Field(..., description="Display name")
    description: Optional[str] = Field(None, description="Description")
    template: str = Field(..., description="Prompt template")
    variables: List[str] = Field(..., description="Variable list")
    output_format: Optional[str] = Field(None, description="Output format")
    model: Optional[str] = Field("qwen-plus", description="AI model")
    max_tokens: Optional[int] = Field(2000, description="Max tokens")
    temperature: Optional[float] = Field(0.7, description="Temperature")
    category: Optional[str] = Field(None, description="Category")
    sort_order: Optional[int] = Field(0, description="Sort order")


class PromptCreate(PromptBase):
    """Prompt creation model."""
    name: str = Field(..., description="Prompt identifier")


class PromptUpdate(BaseModel):
    """Prompt update model."""
    display_name: Optional[str] = None
    description: Optional[str] = None
    template: Optional[str] = None
    variables: Optional[List[str]] = None
    output_format: Optional[str] = None
    model: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    category: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None


class Prompt(PromptBase):
    """Prompt response model."""
    id: int
    name: str
    is_active: bool
    is_system: bool
    created_at: datetime
    updated_at: datetime
    published_version_id: Optional[int] = None

    class Config:
        from_attributes = True


class PromptListResponse(BaseModel):
    """Prompt list response."""
    code: int = 200
    message: str = "success"
    data: Dict[str, Any]


# ==================== Database Helper ====================

def get_db_connection() -> sqlite3.Connection:
    """Get database connection."""
    db_path = Path(__file__).parent.parent.parent / "data" / "content_factory.db"
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def row_to_dict(row: sqlite3.Row) -> dict:
    """Convert sqlite3.Row to dict."""
    if row is None:
        return None
    result = dict(row)
    
    # Parse JSON fields
    if 'variables' in result and result['variables']:
        try:
            result['variables'] = json.loads(result['variables'])
        except (json.JSONDecodeError, TypeError):
            # If already a string or invalid JSON, keep as is
            pass
    
    return result


# ==================== API Endpoints ====================

@router.get("", response_model=PromptListResponse)
async def list_prompts(
    category: Optional[str] = Query(None, description="Filter by category"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Page size")
):
    """
    List prompts with pagination.
    
    - **category**: Filter by category (topic/douyin/wechat/xhs/image)
    - **is_active**: Filter by active status
    - **page**: Page number (default: 1)
    - **page_size**: Page size (default: 20, max: 100)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build query
    query = "SELECT * FROM prompts WHERE 1=1"
    count_query = "SELECT COUNT(*) FROM prompts WHERE 1=1"
    params = []
    
    if category:
        query += " AND category = ?"
        count_query += " AND category = ?"
        params.append(category)
    
    if is_active is not None:
        query += " AND is_active = ?"
        count_query += " AND is_active = ?"
        params.append(1 if is_active else 0)
    
    # Get total count
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    
    # Get paginated results
    offset = (page - 1) * page_size
    query += " ORDER BY sort_order, id LIMIT ? OFFSET ?"
    params.extend([page_size, offset])
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    prompts = [row_to_dict(row) for row in rows]
    
    conn.close()
    
    return PromptListResponse(
        code=200,
        message="success",
        data={
            "list": prompts,
            "total": total,
            "page": page,
            "page_size": page_size
        }
    )


@router.get("/{prompt_id}", response_model=PromptListResponse)
async def get_prompt(prompt_id: int):
    """
    Get prompt by ID.
    
    - **prompt_id**: Prompt ID
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get prompt
    cursor.execute("SELECT * FROM prompts WHERE id = ?", (prompt_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    prompt = row_to_dict(row)
    
    # Get versions
    cursor.execute(
        "SELECT * FROM prompt_versions WHERE prompt_id = ? ORDER BY created_at DESC",
        (prompt_id,)
    )
    versions = [row_to_dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    prompt["versions"] = versions
    
    return PromptListResponse(
        code=200,
        message="success",
        data=prompt
    )


@router.post("", response_model=PromptListResponse)
async def create_prompt(prompt: PromptCreate):
    """
    Create a new prompt.
    
    - **name**: Prompt identifier (unique)
    - **display_name**: Display name
    - **template**: Prompt template with {variable} placeholders
    - **variables**: Variable list
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if name exists
        cursor.execute("SELECT id FROM prompts WHERE name = ?", (prompt.name,))
        if cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=400, detail="Prompt name already exists")
        
        # Insert prompt
        cursor.execute("""
            INSERT INTO prompts 
            (name, display_name, description, template, variables, output_format, 
             model, max_tokens, temperature, category, sort_order, is_system, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 1)
        """, (
            prompt.name,
            prompt.display_name,
            prompt.description,
            prompt.template,
            json.dumps(prompt.variables),
            prompt.output_format,
            prompt.model,
            prompt.max_tokens,
            prompt.temperature,
            prompt.category,
            prompt.sort_order
        ))
        
        prompt_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return PromptListResponse(
            code=201,
            message="Prompt created successfully",
            data={"id": prompt_id}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{prompt_id}", response_model=PromptListResponse)
async def update_prompt(prompt_id: int, prompt: PromptUpdate):
    """
    Update an existing prompt.
    
    - **prompt_id**: Prompt ID
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if prompt exists
    cursor.execute("SELECT * FROM prompts WHERE id = ?", (prompt_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Check if system prompt
    if row["is_system"]:
        conn.close()
        raise HTTPException(status_code=403, detail="System prompts cannot be modified")
    
    # Build update query
    updates = []
    params = []
    
    if prompt.display_name is not None:
        updates.append("display_name = ?")
        params.append(prompt.display_name)
    if prompt.description is not None:
        updates.append("description = ?")
        params.append(prompt.description)
    if prompt.template is not None:
        updates.append("template = ?")
        params.append(prompt.template)
    if prompt.variables is not None:
        updates.append("variables = ?")
        params.append(json.dumps(prompt.variables))
    if prompt.output_format is not None:
        updates.append("output_format = ?")
        params.append(prompt.output_format)
    if prompt.model is not None:
        updates.append("model = ?")
        params.append(prompt.model)
    if prompt.max_tokens is not None:
        updates.append("max_tokens = ?")
        params.append(prompt.max_tokens)
    if prompt.temperature is not None:
        updates.append("temperature = ?")
        params.append(prompt.temperature)
    if prompt.category is not None:
        updates.append("category = ?")
        params.append(prompt.category)
    if prompt.sort_order is not None:
        updates.append("sort_order = ?")
        params.append(prompt.sort_order)
    if prompt.is_active is not None:
        updates.append("is_active = ?")
        params.append(1 if prompt.is_active else 0)
    
    if updates:
        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(prompt_id)
        
        query = f"UPDATE prompts SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
    
    conn.close()
    
    return PromptListResponse(
        code=200,
        message="Prompt updated successfully",
        data={"id": prompt_id}
    )


@router.delete("/{prompt_id}", response_model=PromptListResponse)
async def delete_prompt(prompt_id: int):
    """
    Delete a prompt.
    
    - **prompt_id**: Prompt ID
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if prompt exists
    cursor.execute("SELECT * FROM prompts WHERE id = ?", (prompt_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Check if system prompt
    if row["is_system"]:
        conn.close()
        raise HTTPException(status_code=403, detail="System prompts cannot be deleted")
    
    # Delete prompt
    cursor.execute("DELETE FROM prompts WHERE id = ?", (prompt_id,))
    conn.commit()
    conn.close()
    
    return PromptListResponse(
        code=200,
        message="Prompt deleted successfully",
        data={"id": prompt_id}
    )


# ==================== Version Management ====================

class PromptVersionCreate(BaseModel):
    """Create new prompt version."""
    template: str = Field(..., description="New template")
    variables: Optional[List[str]] = Field(None, description="Variables")
    changes_log: Optional[str] = Field(None, description="Change log")


class PromptVersionResponse(BaseModel):
    """Prompt version response."""
    id: int
    prompt_id: int
    version: str
    template: str
    variables: list
    change_log: Optional[str]
    is_published: bool
    created_at: str


@router.post("/{prompt_id}/versions", response_model=PromptListResponse)
async def create_version(prompt_id: int, version_data: PromptVersionCreate):
    """
    Create a new version for a prompt.
    
    - **prompt_id**: Prompt ID
    - **template**: New template
    - **changes_log**: Change description
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if prompt exists
    cursor.execute("SELECT * FROM prompts WHERE id = ?", (prompt_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Get max version
    cursor.execute(
        "SELECT MAX(version) FROM prompt_versions WHERE prompt_id = ?",
        (prompt_id,)
    )
    max_version = cursor.fetchone()[0]
    next_version = f"v{int(max_version[1:]) + 1}" if max_version else "v1"
    
    # Insert new version
    cursor.execute("""
        INSERT INTO prompt_versions 
        (prompt_id, version, template, variables, change_log, is_published, created_at)
        VALUES (?, ?, ?, ?, ?, 0, CURRENT_TIMESTAMP)
    """, (
        prompt_id,
        next_version,
        version_data.template,
        json.dumps(version_data.variables) if version_data.variables else row["variables"],
        version_data.changes_log or ""
    ))
    
    version_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return PromptListResponse(
        code=201,
        message=f"Version {next_version} created successfully",
        data={"version_id": version_id, "version": next_version}
    )


@router.get("/{prompt_id}/versions", response_model=PromptListResponse)
async def list_versions(prompt_id: int):
    """
    Get version history for a prompt.
    
    - **prompt_id**: Prompt ID
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM prompt_versions WHERE prompt_id = ? ORDER BY created_at DESC",
        (prompt_id,)
    )
    versions = [dict(row) for row in cursor.fetchall()]
    
    # Parse variables JSON
    for v in versions:
        if v.get("variables"):
            try:
                v["variables"] = json.loads(v["variables"])
            except:
                v["variables"] = []
    
    conn.close()
    
    return PromptListResponse(
        code=200,
        message="success",
        data={"versions": versions}
    )


@router.post("/{prompt_id}/versions/{version_id}/publish", response_model=PromptListResponse)
async def publish_version(prompt_id: int, version_id: int):
    """
    Publish a prompt version.
    
    - **prompt_id**: Prompt ID
    - **version_id**: Version ID to publish
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if version exists
    cursor.execute(
        "SELECT * FROM prompt_versions WHERE id = ? AND prompt_id = ?",
        (version_id, prompt_id)
    )
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Version not found")
    
    # Publish version
    cursor.execute("""
        UPDATE prompt_versions 
        SET is_published = 1, published_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (version_id,))
    
    # Update prompt template
    cursor.execute("""
        UPDATE prompts 
        SET template = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (row["template"], prompt_id))
    
    conn.commit()
    conn.close()
    
    return PromptListResponse(
        code=200,
        message="Version published successfully",
        data={"version_id": version_id}
    )


# ==================== Prompt Testing ====================

class PromptTestRequest(BaseModel):
    """Prompt test request."""
    prompt_id: int = Field(..., description="Prompt ID")
    input_vars: Dict[str, str] = Field(..., description="Input variables")
    version_id: Optional[int] = Field(None, description="Specific version to test")


class PromptTestResponse(BaseModel):
    """Prompt test response."""
    code: int
    message: str
    data: Dict[str, Any]


@router.post("/test", response_model=PromptTestResponse)
async def test_prompt(test_data: PromptTestRequest):
    """
    Test a prompt with given input variables.
    
    - **prompt_id**: Prompt ID to test
    - **input_vars**: Input variables (key-value pairs)
    - **version_id**: Optional specific version
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get prompt
    cursor.execute("SELECT * FROM prompts WHERE id = ?", (test_data.prompt_id,))
    prompt_row = cursor.fetchone()
    
    if not prompt_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    prompt = dict(prompt_row)
    
    # Get version if specified
    if test_data.version_id:
        cursor.execute(
            "SELECT * FROM prompt_versions WHERE id = ? AND prompt_id = ?",
            (test_data.version_id, test_data.prompt_id)
        )
        version_row = cursor.fetchone()
        if version_row:
            prompt["template"] = version_row["template"]
    
    conn.close()
    
    # Fill template variables
    template = prompt["template"]
    try:
        filled_template = template.format(**test_data.input_vars)
    except KeyError as e:
        return PromptTestResponse(
            code=400,
            message=f"Missing variable: {e}",
            data={"error": f"Template requires variable: {e}"}
        )
    
    # Call AI (placeholder - will be implemented in AIService)
    # For now, return filled template
    return PromptTestResponse(
        code=200,
        message="Prompt test successful",
        data={
            "prompt_id": test_data.prompt_id,
            "prompt_name": prompt["name"],
            "filled_template": filled_template,
            "input_vars": test_data.input_vars,
            "note": "AI call will be implemented in AIService"
        }
    )
