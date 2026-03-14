# AI module initialization
from app.ai.prompts import PromptLoader, Prompt

# 延迟导入 AIService（避免 dashscope 依赖问题）
try:
    from app.ai.service import AIService
    __all__ = ["AIService", "PromptLoader", "Prompt"]
except ImportError:
    # dashscope 未安装时使用 Mock
    from app.ai.service_mock import MockAIService as AIService
    __all__ = ["AIService", "PromptLoader", "Prompt", "MockAIService"]
