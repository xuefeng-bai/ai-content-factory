#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DashScope API 测试脚本
测试 API Key 有效性和额度
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from app.config import config
from app.ai.service import AIService


def print_header(title: str):
    """打印标题"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def test_api_key():
    """测试 API Key"""
    print_header("1. 测试 API Key")
    
    api_key = config.DASHSCOPE_API_KEY
    
    if not api_key:
        print("❌ 错误：DASHSCOPE_API_KEY 未配置")
        print("   请编辑 backend/.env 文件，添加 API Key")
        return False
    
    print(f"✅ API Key 已配置")
    print(f"   Key: {api_key[:20]}...{api_key[-8:]}")
    print(f"   长度：{len(api_key)}")
    
    return True


def test_text_generation():
    """测试文本生成"""
    print_header("2. 测试文本生成（Qwen-Plus）")
    
    try:
        ai = AIService()
        result = ai.generate_text(
            prompt_name='douyin_script',
            variables={'topic': 'AI 工具', 'theme': '效率提升'}
        )
        
        print("✅ 文本生成成功!")
        print(f"   生成字数：{len(result)}")
        print(f"   内容预览：{result[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 文本生成失败：{e}")
        
        # 错误类型判断
        error_msg = str(e)
        if "401" in error_msg or "InvalidApiKey" in error_msg:
            print("   原因：API Key 无效")
            print("   解决方案：请检查 API Key 是否正确，或重新创建")
        elif "402" in error_msg or "InsufficientBalance" in error_msg:
            print("   原因：余额不足")
            print("   解决方案：请充值或等待免费额度刷新")
        elif "timeout" in error_msg.lower():
            print("   原因：请求超时")
            print("   解决方案：请检查网络连接，或增加超时时间")
        
        return False


def test_image_generation():
    """测试图片生成"""
    print_header("3. 测试图片生成（通义万相）")
    
    try:
        ai = AIService()
        result = ai.generate_image(
            prompt='一只可爱的猫咪，卡通风格，彩色，高质量',
            title='测试图片',
            aspect_ratio='16:9',
            platform='wechat'
        )
        
        print("✅ 图片生成成功!")
        print(f"   图片 URL: {result['image_url']}")
        print(f"   尺寸：{result.get('size', 'unknown')}")
        print(f"   宽高比：{result['aspect_ratio']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 图片生成失败：{e}")
        
        # 错误类型判断
        error_msg = str(e)
        if "401" in error_msg or "InvalidApiKey" in error_msg:
            print("   原因：API Key 无效")
            print("   解决方案：请检查 API Key 是否正确，或重新创建")
        elif "402" in error_msg or "InsufficientBalance" in error_msg:
            print("   原因：余额不足")
            print("   解决方案：请充值或等待免费额度刷新")
        elif "timeout" in error_msg.lower():
            print("   原因：请求超时（图片生成需要 10-30 秒）")
            print("   解决方案：请检查网络连接，或增加 AI_IMAGE_TIMEOUT")
        
        return False


def check_quota():
    """检查额度（需要访问控制台 API，这里只显示查询链接）"""
    print_header("4. 查询额度")
    
    print("💡 免费额度查询：")
    print("   访问：https://dashscope.console.aliyun.com/overview")
    print()
    print("📊 新用户额度：")
    print("   - 文本生成：约 1000-2000 次（Qwen-Plus）")
    print("   - 图片生成：约 100-200 张（通义万相）")
    print("   - 有效期：开通后 30 天")
    print()
    print("💰 超出后价格：")
    print("   - 文本生成：约 0.01 元/次")
    print("   - 图片生成：约 0.1-0.2 元/张")


def main():
    """主函数"""
    print_header("DashScope API 测试工具")
    print(f"项目：AI 内容工厂 v2.0")
    print(f"日期：2026-03-15")
    
    # 1. 测试 API Key
    if not test_api_key():
        print("\n❌ API Key 未配置，无法继续测试")
        print("\n📝 配置步骤：")
        print("   1. 访问 https://dashscope.console.aliyun.com/apiKey")
        print("   2. 创建新的 API Key")
        print("   3. 编辑 backend/.env，添加 DASHSCOPE_API_KEY=sk-xxx")
        return 1
    
    print()
    
    # 2. 测试文本生成
    text_ok = test_text_generation()
    print()
    
    # 3. 测试图片生成
    image_ok = test_image_generation()
    print()
    
    # 4. 查询额度
    check_quota()
    print()
    
    # 总结
    print_header("测试总结")
    
    if text_ok and image_ok:
        print("✅ 所有测试通过！API 配置正确，可以正常使用。")
        return 0
    elif text_ok and not image_ok:
        print("⚠️  文本生成正常，图片生成失败。")
        print("   可能原因：图片生成需要额外开通通义万相模型")
        print("   解决方案：访问控制台开通通义万相模型")
        return 1
    else:
        print("❌ 测试失败，请检查 API Key 和网络连接。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
