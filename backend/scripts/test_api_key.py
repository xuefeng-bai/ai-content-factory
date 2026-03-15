#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 API Key 是否有效
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import config
from app.ai.service import AIService


def print_header(title: str):
    """打印标题"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def test_api_key():
    """测试 API Key"""
    print_header("1. 测试 API Key 配置")
    
    api_key = config.DASHSCOPE_API_KEY
    base_url = config.DASHSCOPE_BASE_URL
    
    if not api_key:
        print("❌ 错误：DASHSCOPE_API_KEY 未配置")
        return False
    
    print(f"✅ API Key 已配置")
    print(f"   Key: {api_key[:20]}...{api_key[-8:]}")
    print(f"   Base URL: {base_url}")
    print(f"   模型：{config.AI_MODEL}")
    
    return True


def test_text_generation():
    """测试文本生成"""
    print_header("2. 测试文本生成（qwen3.5-plus）")
    
    try:
        ai = AIService()
        result = ai.generate_text(
            prompt_name='douyin_script',
            variables={'topic': 'AI 编程助手', 'theme': '效率提升'}
        )
        
        print("✅ 文本生成成功!")
        print(f"   生成字数：{len(result)}")
        print(f"   内容预览：{result[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 文本生成失败：{e}")
        
        # 错误类型判断
        error_msg = str(e)
        if "401" in error_msg or "InvalidApiKey" in error_msg:
            print("   原因：API Key 无效")
            print("   解决方案：请检查 API Key 是否正确")
        elif "402" in error_msg or "InsufficientBalance" in error_msg:
            print("   原因：余额不足")
            print("   解决方案：请充值或等待免费额度刷新")
        elif "timeout" in error_msg.lower():
            print("   原因：请求超时")
            print("   解决方案：请检查网络连接，或增加超时时间")
        
        return False


def test_topic_recommendation():
    """测试选题推荐"""
    print_header("3. 测试选题推荐")
    
    try:
        ai = AIService()
        search_results = """1. [weibo] AI 编程助手提升效率 500w 热度
2. [zhihu] 程序员必备工具推荐 300 万赞同
3. [weibo] 时间管理方法分享 200w 讨论"""
        
        result = ai.generate(
            prompt_name='topic_recommendation',
            variables={'search_results': search_results},
            is_image=False
        )
        
        print("✅ 选题推荐成功!")
        print(f"   生成字数：{len(result)}")
        print(f"   内容预览：{result[:300]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 选题推荐失败：{e}")
        return False


def main():
    """主函数"""
    print_header("DashScope API 测试工具")
    print(f"项目：AI 内容工厂 v2.0")
    print(f"日期：2026-03-15")
    print(f"模型：{config.AI_MODEL}")
    print(f"Base URL: {config.DASHSCOPE_BASE_URL}")
    
    # 1. 测试 API Key
    if not test_api_key():
        print("\n❌ API Key 未配置，无法继续测试")
        return 1
    
    print()
    
    # 2. 测试文本生成
    text_ok = test_text_generation()
    print()
    
    # 3. 测试选题推荐
    topic_ok = test_topic_recommendation()
    print()
    
    # 总结
    print_header("测试总结")
    
    if text_ok and topic_ok:
        print("✅ 所有测试通过！API 配置正确，可以正常使用。")
        return 0
    elif text_ok and not topic_ok:
        print("⚠️  文本生成正常，选题推荐失败。")
        return 1
    else:
        print("❌ 测试失败，请检查 API Key 和网络连接。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
