# -*- coding: utf-8 -*-
"""
Mock AI Service for Testing
用于测试的 Mock AI 服务（不依赖 dashscope）
"""

import json
import time
from typing import Dict, Any, Optional
from pathlib import Path
import sys

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.ai.prompts import PromptLoader


class MockAIService:
    """
    Mock AI Service for testing.
    返回模拟数据用于前端测试。
    """
    
    def __init__(self):
        self.loader = PromptLoader()
    
    def generate(
        self,
        prompt_name: str,
        variables: Dict[str, Any],
        **kwargs
    ) -> str:
        """
        Generate mock content.
        根据 prompt_name 返回模拟数据。
        """
        # 加载 Prompt
        prompt = self.loader.get_prompt(prompt_name)
        if not prompt:
            raise ValueError(f"Prompt not found: {prompt_name}")
        
        # 模拟 AI 响应
        if prompt_name == 'topic_recommendation':
            return self._mock_topic_recommendation(variables)
        elif prompt_name == 'douyin_script':
            return self._mock_douyin_script(variables)
        elif prompt_name == 'wechat_article':
            return self._mock_wechat_article(variables)
        elif prompt_name == 'xiaohongshu_note':
            return self._mock_xiaohongshu_note(variables)
        else:
            return f"Mock response for {prompt_name}"
    
    def _mock_topic_recommendation(self, variables: Dict[str, Any]) -> str:
        """模拟选题推荐"""
        return json.dumps({
            "topics": [
                {
                    "title": "AI 工具提升效率的 5 个技巧",
                    "angle": "职场人必备技能",
                    "core_point": "用 AI 节省 50% 工作时间",
                    "platforms": ["douyin", "wechat", "xhs"],
                    "hot_score": 9,
                    "reason": "切中职场痛点，实用性强"
                },
                {
                    "title": "打工人如何用 AI 逆袭",
                    "angle": "个人成长故事",
                    "core_point": "从加班狗到效率达人",
                    "platforms": ["douyin", "xhs"],
                    "hot_score": 8,
                    "reason": "情感共鸣强，易传播"
                },
                {
                    "title": "这 3 个 AI 工具让我准时下班",
                    "angle": "工具测评",
                    "core_point": "实测有效的效率工具",
                    "platforms": ["wechat", "xhs"],
                    "hot_score": 7,
                    "reason": "干货内容，收藏率高"
                }
            ]
        }, ensure_ascii=False)
    
    def _mock_douyin_script(self, variables: Dict[str, Any]) -> str:
        """模拟抖音文案"""
        topic = variables.get('topic', 'AI 工具')
        return json.dumps({
            "title": f"{topic}的 5 个技巧",
            "hook": "你敢信吗？用对 AI 工具，工作效率提升 10 倍！",
            "body": f"""
第一个技巧：用 AI 写邮件
每天花 1 小时写邮件？试试 AI，3 分钟搞定！

第二个技巧：用 AI 做总结
开会记录太多？AI 帮你自动总结重点。

第三个技巧：用 AI 写文案
朋友圈、公众号、小红书，AI 一键生成。

第四个技巧：用 AI 做翻译
英文文档看不懂？AI 实时翻译，比谷歌还准。

第五个技巧：用 AI 写代码
不会编程？AI 帮你写脚本，自动化办公。
""",
            "ending": "关注我，分享更多 AI 效率技巧！点赞收藏，我们下期见！",
            "full_script": """你敢信吗？用对 AI 工具，工作效率提升 10 倍！

第一个技巧：用 AI 写邮件
每天花 1 小时写邮件？试试 AI，3 分钟搞定！

第二个技巧：用 AI 做总结
开会记录太多？AI 帮你自动总结重点。

第三个技巧：用 AI 写文案
朋友圈、公众号、小红书，AI 一键生成。

第四个技巧：用 AI 做翻译
英文文档看不懂？AI 实时翻译，比谷歌还准。

第五个技巧：用 AI 写代码
不会编程？AI 帮你写脚本，自动化办公。

关注我，分享更多 AI 效率技巧！点赞收藏，我们下期见！""",
            "hashtags": ["#AI 工具", "#效率提升", "#职场技能"],
            "word_count": 180
        }, ensure_ascii=False)
    
    def _mock_wechat_article(self, variables: Dict[str, Any]) -> str:
        """模拟公众号文章"""
        topic = variables.get('topic', 'AI 工具')
        return json.dumps({
            "titles": [
                f"{topic}：打工人逆袭的必备神器",
                f"用{topic}，工作效率提升 10 倍的秘密",
                f"深度测评：{topic}到底好不好用？",
                f"{topic}完全指南：从入门到精通",
                f"为什么高手都在用{topic}？"
            ],
            "intro": f"在这个 AI 时代，不会用{topic}，你真的out 了。今天，我们就来深度聊聊这个让无数人效率翻倍的神器。",
            "sections": [
                {
                    "subtitle": "一、什么是 AI 工具？",
                    "content": f"""简单来说，{topic}就是利用人工智能技术，帮助我们更高效地完成工作的工具。

它可以是写作助手，帮你生成文案、文章；
它可以是翻译工具，帮你实时翻译外文资料；
它也可以是数据分析工具，帮你快速处理 Excel 表格。

**总之，{topic}的核心价值就是：让你少加班，多生活。**"""
                },
                {
                    "subtitle": "二、为什么需要用 AI 工具？",
                    "content": f"""让我给你讲个真实的故事。

我有个朋友小李，在某互联网公司做运营。每天的工作就是写文案、做报表、回复用户消息。

以前，他每天都要加班到晚上 9 点。自从用了{topic}，他的工作效率提升了 3 倍，现在下午 6 点就能准时下班。

**这就是 AI 工具的力量。**

具体来说，{topic}能帮你：
1. 节省时间：重复性工作交给 AI
2. 提升质量：AI 生成的内容更专业
3. 减少错误：AI 不会疲劳，不会出错"""
                },
                {
                    "subtitle": "三、如何使用 AI 工具？",
                    "content": f"""使用{topic}其实很简单，就三步：

**第一步：明确需求**
你要让 AI 做什么？写文案？做总结？还是翻译？

**第二步：提供上下文**
给 AI 足够的背景信息，它才能生成更好的内容。

**第三步：迭代优化**
AI 生成的内容不满意？调整一下提示词，再来一次。

**记住：AI 不是万能的，但用好了，它就是你的超级助手。**"""
                }
            ],
            "ending": f"""最后，我想说：

{topic}再好，也只是工具。真正决定你价值的，是你如何使用它。

所以，别犹豫了，现在就行动起来，让{topic}成为你的效率神器吧！

**如果你觉得这篇文章有用，欢迎点赞、在看、转发，让更多人受益！**""",
            "full_article": f"""# {topic}：打工人逆袭的必备神器

在这个 AI 时代，不会用{topic}，你真的 out 了。今天，我们就来深度聊聊这个让无数人效率翻倍的神器。

## 一、什么是 AI 工具？

简单来说，{topic}就是利用人工智能技术，帮助我们更高效地完成工作的工具。

它可以是写作助手，帮你生成文案、文章；
它可以是翻译工具，帮你实时翻译外文资料；
它也可以是数据分析工具，帮你快速处理 Excel 表格。

**总之，{topic}的核心价值就是：让你少加班，多生活。**

## 二、为什么需要用 AI 工具？

让我给你讲个真实的故事。

我有个朋友小李，在某互联网公司做运营。每天的工作就是写文案、做报表、回复用户消息。

以前，他每天都要加班到晚上 9 点。自从用了{topic}，他的工作效率提升了 3 倍，现在下午 6 点就能准时下班。

**这就是 AI 工具的力量。**

具体来说，{topic}能帮你：
1. 节省时间：重复性工作交给 AI
2. 提升质量：AI 生成的内容更专业
3. 减少错误：AI 不会疲劳，不会出错

## 三、如何使用 AI 工具？

使用{topic}其实很简单，就三步：

**第一步：明确需求**
你要让 AI 做什么？写文案？做总结？还是翻译？

**第二步：提供上下文**
给 AI 足够的背景信息，它才能生成更好的内容。

**第三步：迭代优化**
AI 生成的内容不满意？调整一下提示词，再来一次。

**记住：AI 不是万能的，但用好了，它就是你的超级助手。**

## 结语

最后，我想说：

{topic}再好，也只是工具。真正决定你价值的，是你如何使用它。

所以，别犹豫了，现在就行动起来，让{topic}成为你的效率神器吧！

**如果你觉得这篇文章有用，欢迎点赞、在看、转发，让更多人受益！**""",
            "word_count": 800
        }, ensure_ascii=False)
    
    def _mock_xiaohongshu_note(self, variables: Dict[str, Any]) -> str:
        """模拟小红书笔记"""
        topic = variables.get('topic', 'AI 工具')
        return json.dumps({
            "title": f"🔥{topic}｜打工人效率翻倍的秘密武器",
            "body": f"""姐妹们！今天必须给你们安利这个超好用的{topic}！💖

用了它之后，我真的准时下班了！😭

✨ 我的使用体验：
1️⃣ 写文案超快，5 分钟搞定一篇
2️⃣ 质量超高，领导都夸我进步了
3️⃣ 操作简单，小白也能上手

💡 使用小技巧：
• 给 AI 足够的背景信息
• 多尝试几次，找到最佳提示词
• 结合自己的想法，不要完全依赖

真心推荐给所有职场姐妹！用了就回不去了！💪

#职场干货 #效率工具 #AI 工具 #打工人 #职场成长""",
            "tags": [
                "#职场干货",
                "#效率工具",
                "#AI 工具",
                "#打工人",
                "#职场成长",
                "#准时下班",
                "#工作效率"
            ],
            "full_note": f"""🔥{topic}｜打工人效率翻倍的秘密武器

姐妹们！今天必须给你们安利这个超好用的{topic}！💖

用了它之后，我真的准时下班了！😭

✨ 我的使用体验：
1️⃣ 写文案超快，5 分钟搞定一篇
2️⃣ 质量超高，领导都夸我进步了
3️⃣ 操作简单，小白也能上手

💡 使用小技巧：
• 给 AI 足够的背景信息
• 多尝试几次，找到最佳提示词
• 结合自己的想法，不要完全依赖

真心推荐给所有职场姐妹！用了就回不去了！💪

#职场干货 #效率工具 #AI 工具 #打工人 #职场成长""",
            "word_count": 180
        }, ensure_ascii=False)
    
    def test_prompt(
        self,
        prompt_id: int,
        variables: Dict[str, Any]
    ) -> Dict[str, Any]:
        """测试 Prompt（返回填充后的模板）"""
        prompt = self.loader.get_prompt_by_id(prompt_id)
        if not prompt:
            raise ValueError(f"Prompt not found: {prompt_id}")
        
        start_time = time.time()
        
        # 填充模板
        filled_template = prompt.template.format(**variables)
        
        duration_ms = int((time.time() - start_time) * 1000)
        
        return {
            "prompt_id": prompt_id,
            "prompt_name": prompt.name,
            "filled_template": filled_template,
            "input_vars": variables,
            "note": "Mock mode - AI call not executed"
        }


# 导出 Mock 服务
__all__ = ['MockAIService']
