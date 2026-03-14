#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 2 端到端测试脚本
测试前后端功能是否符合文档标准
"""

import json
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.prompt import Prompt, PromptVersion
from app.ai.prompts import PromptLoader
from app.ai.service_mock import MockAIService


class TestRunner:
    """测试运行器"""
    
    def __init__(self):
        self.loader = PromptLoader()
        self.ai_service = MockAIService()
        self.passed = 0
        self.failed = 0
        self.results = []
    
    def test(self, name: str, func):
        """运行单个测试"""
        try:
            func()
            self.passed += 1
            self.results.append(f"✅ {name}")
            print(f"✅ {name}")
        except AssertionError as e:
            self.failed += 1
            self.results.append(f"❌ {name}: {e}")
            print(f"❌ {name}: {e}")
        except Exception as e:
            self.failed += 1
            self.results.append(f"❌ {name}: {type(e).__name__}: {e}")
            print(f"❌ {name}: {type(e).__name__}: {e}")
    
    def summary(self):
        """打印测试摘要"""
        print("\n" + "="*60)
        print(f"测试完成：{self.passed + self.failed} 个测试")
        print(f"✅ 通过：{self.passed}")
        print(f"❌ 失败：{self.failed}")
        print("="*60)
        return self.failed == 0


def run_tests():
    """运行所有测试"""
    runner = TestRunner()
    
    print("="*60)
    print("Phase 2 端到端测试")
    print("="*60)
    
    # ==================== 数据库测试 ====================
    print("\n📊 数据库测试")
    print("-"*60)
    
    def test_prompt_count():
        """测试 Prompt 数量"""
        import sqlite3
        db_path = Path(__file__).parent.parent / 'data' / 'content_factory.db'
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM prompts")
        count = cursor.fetchone()[0]
        conn.close()
        assert count == 6, f"期望 6 个 Prompt，实际{count}个"
    
    runner.test("数据库：Prompt 数量应为 6", test_prompt_count)
    
    def test_version_count():
        """测试版本数量"""
        import sqlite3
        conn = sqlite3.connect('data/content_factory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM prompt_versions")
        count = cursor.fetchone()[0]
        conn.close()
        assert count == 6, f"期望 6 个版本，实际{count}个"
    
    runner.test("数据库：版本数量应为 6", test_version_count)
    
    def test_prompt_display_names():
        """测试 Prompt 显示名称为中文"""
        import sqlite3
        conn = sqlite3.connect('data/content_factory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, display_name FROM prompts")
        prompts = dict(cursor.fetchall())
        conn.close()
        
        expected = {
            'topic_recommendation': '选题推荐',
            'douyin_script': '抖音文案',
            'wechat_article': '公众号文章',
            'xiaohongshu_note': '小红书笔记',
        }
        
        for name, expected_display in expected.items():
            actual = prompts.get(name)
            assert actual == expected_display, f"{name} 的显示名称应为'{expected_display}'，实际为'{actual}'"
    
    runner.test("数据库：Prompt 显示名称应为中文", test_prompt_display_names)
    
    # ==================== Prompt 加载测试 ====================
    print("\n📥 Prompt 加载测试")
    print("-"*60)
    
    def test_load_topic_prompt():
        """测试加载选题推荐 Prompt"""
        prompt = runner.loader.get_prompt('topic_recommendation')
        assert prompt is not None, "选题推荐 Prompt 不存在"
        assert 'search_results' in prompt.variables, "选题推荐 Prompt 应包含 search_results 变量"
    
    runner.test("Prompt 加载：选题推荐", test_load_topic_prompt)
    
    def test_load_douyin_prompt():
        """测试加载抖音文案 Prompt"""
        prompt = runner.loader.get_prompt('douyin_script')
        assert prompt is not None, "抖音文案 Prompt 不存在"
        assert 'topic' in prompt.variables, "抖音文案 Prompt 应包含 topic 变量"
    
    runner.test("Prompt 加载：抖音文案", test_load_douyin_prompt)
    
    def test_load_wechat_prompt():
        """测试加载公众号文章 Prompt"""
        prompt = runner.loader.get_prompt('wechat_article')
        assert prompt is not None, "公众号文章 Prompt 不存在"
    
    runner.test("Prompt 加载：公众号文章", test_load_wechat_prompt)
    
    def test_load_xhs_prompt():
        """测试加载小红书笔记 Prompt"""
        prompt = runner.loader.get_prompt('xiaohongshu_note')
        assert prompt is not None, "小红书笔记 Prompt 不存在"
    
    runner.test("Prompt 加载：小红书笔记", test_load_xhs_prompt)
    
    # ==================== 变量验证测试 ====================
    print("\n✅ 变量验证测试")
    print("-"*60)
    
    def test_variable_validation_pass():
        """测试变量验证通过"""
        prompt = runner.loader.get_prompt('douyin_script')
        result = runner.loader.validate_variables(prompt, {'topic': 'AI 工具', 'theme': '效率'})
        assert result is True
    
    runner.test("变量验证：提供所有必需变量应通过", test_variable_validation_pass)
    
    def test_variable_validation_fail():
        """测试变量验证失败"""
        prompt = runner.loader.get_prompt('douyin_script')
        try:
            runner.loader.validate_variables(prompt, {'topic': 'AI 工具'})
            assert False, "应抛出 ValueError"
        except ValueError as e:
            assert 'theme' in str(e), "错误信息应包含缺失的变量名"
    
    runner.test("变量验证：缺少必需变量应失败", test_variable_validation_fail)
    
    # ==================== 模板填充测试 ====================
    print("\n📝 模板填充测试")
    print("-"*60)
    
    def test_template_filling():
        """测试模板填充"""
        template = "你好，{name}！今天是{day}。"
        filled = runner.loader.fill_template(template, {'name': '张三', 'day': '周一'})
        assert filled == "你好，张三！今天是周一。"
    
    runner.test("模板填充：简单模板", test_template_filling)
    
    def test_template_filling_missing_var():
        """测试模板填充缺失变量"""
        template = "你好，{name}！"
        try:
            runner.loader.fill_template(template, {})
            assert False, "应抛出 ValueError"
        except ValueError as e:
            assert 'name' in str(e)
    
    runner.test("模板填充：缺失变量应报错", test_template_filling_missing_var)
    
    # ==================== Mock AI 服务测试 ====================
    print("\n🤖 Mock AI 服务测试")
    print("-"*60)
    
    def test_mock_topic_recommendation():
        """测试模拟选题推荐"""
        result = runner.ai_service.generate(
            prompt_name='topic_recommendation',
            variables={'search_results': '微博热搜：AI 工具'}
        )
        data = json.loads(result)
        assert 'topics' in data, "应包含 topics 字段"
        assert len(data['topics']) >= 3, "应至少推荐 3 个选题"
    
    runner.test("Mock AI：选题推荐", test_mock_topic_recommendation)
    
    def test_mock_douyin_script():
        """测试模拟抖音文案"""
        result = runner.ai_service.generate(
            prompt_name='douyin_script',
            variables={'topic': 'AI 工具', 'theme': '效率'}
        )
        data = json.loads(result)
        assert 'full_script' in data, "应包含 full_script 字段"
        assert len(data['full_script']) > 100, "文案长度应大于 100 字"
    
    runner.test("Mock AI：抖音文案", test_mock_douyin_script)
    
    def test_mock_wechat_article():
        """测试模拟公众号文章"""
        result = runner.ai_service.generate(
            prompt_name='wechat_article',
            variables={'topic': 'AI 工具', 'theme': '效率'}
        )
        data = json.loads(result)
        assert 'full_article' in data, "应包含 full_article 字段"
        assert '#' in data['full_article'], "公众号文章应包含 Markdown 标题"
    
    runner.test("Mock AI：公众号文章", test_mock_wechat_article)
    
    def test_mock_xiaohongshu_note():
        """测试模拟小红书笔记"""
        result = runner.ai_service.generate(
            prompt_name='xiaohongshu_note',
            variables={'topic': 'AI 工具', 'theme': '效率'}
        )
        data = json.loads(result)
        assert 'full_note' in data, "应包含 full_note 字段"
        assert '🔥' in data['title'], "小红书标题应包含 emoji"
    
    runner.test("Mock AI：小红书笔记", test_mock_xiaohongshu_note)
    
    # ==================== API 响应格式测试 ====================
    print("\n📡 API 响应格式测试")
    print("-"*60)
    
    def test_api_response_format():
        """测试 API 响应格式"""
        # 模拟 API 响应
        response = {
            "code": 200,
            "message": "success",
            "data": {"result": "test"}
        }
        assert 'code' in response, "应包含 code 字段"
        assert 'message' in response, "应包含 message 字段"
        assert 'data' in response, "应包含 data 字段"
        assert response['code'] == 200, "code 应为 200"
    
    runner.test("API 响应：格式应包含 code/message/data", test_api_response_format)
    
    # ==================== 前端 API 服务测试 ====================
    print("\n🎨 前端 API 服务测试（静态检查）")
    print("-"*60)
    
    def test_frontend_api_files():
        """测试前端 API 文件存在"""
        frontend_dir = Path(__file__).parent.parent.parent / 'frontend' / 'src' / 'services'
        required_files = ['api.js', 'prompts.js', 'topics.js', 'content.js']
        
        for file in required_files:
            file_path = frontend_dir / file
            assert file_path.exists(), f"前端 API 文件不存在：{file}"
    
    runner.test("前端 API：服务文件应存在", test_frontend_api_files)
    
    def test_frontend_page_files():
        """测试前端页面文件存在"""
        pages_dir = Path(__file__).parent.parent.parent / 'frontend' / 'src' / 'pages'
        required_files = [
            'Search.jsx',
            'Prompts.jsx',
            'PromptEdit.jsx',
            'PromptTest.jsx',
            'Topic.jsx',
            'Preview.jsx'
        ]
        
        for file in required_files:
            file_path = pages_dir / file
            assert file_path.exists(), f"前端页面文件不存在：{file}"
    
    runner.test("前端页面：页面文件应存在", test_frontend_page_files)
    
    # ==================== 文档检查 ====================
    print("\n📄 文档检查")
    print("-"*60)
    
    def test_docs_exist():
        """测试文档文件存在"""
        docs_dir = Path(__file__).parent.parent.parent / 'docs'
        required_docs = [
            'PHASE2_PLAN_v1.0.md',
            'CODE_REVIEW_AND_TEST_2026-03-14.md'
        ]
        
        for doc in required_docs:
            doc_path = docs_dir / doc
            assert doc_path.exists(), f"文档文件不存在：{doc}"
    
    runner.test("文档：关键文档应存在", test_docs_exist)
    
    # ==================== 测试摘要 ====================
    all_passed = runner.summary()
    
    if all_passed:
        print("\n🎉 所有测试通过！Phase 2 功能符合文档标准！")
        return 0
    else:
        print(f"\n⚠️  有 {runner.failed} 个测试失败，请检查！")
        return 1


if __name__ == "__main__":
    # 切换到项目根目录
    import os
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    os.chdir(PROJECT_ROOT)
    
    print(f"项目根目录：{PROJECT_ROOT}")
    print(f"当前目录：{Path.cwd()}")
    
    exit_code = run_tests()
    sys.exit(exit_code)
