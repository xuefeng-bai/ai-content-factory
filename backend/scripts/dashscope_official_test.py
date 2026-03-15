#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DashScope API 完整测试脚本
符合阿里云官方接口规范
文档：https://help.aliyun.com/zh/model-studio/

支持两种调用方式：
1. OpenAI 兼容接口（推荐）
2. DashScope 原生 SDK
"""

import sys
import json

# ==================== 配置 ====================
CONFIG = {
    # API Key（从环境变量或配置文件读取）
    "api_key": "sk-sp-215c5f115f0b42aa82afa6f28e12fbd7",
    
    # Base URL（兼容 OpenAI 协议）
    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    
    # 使用的模型
    "model": "qwen3.5-plus",
    
    # 调用方式：openai 或 dashscope
    "mode": "openai"
}

# ==================== 测试函数 ====================

def test_with_openai(prompt: str) -> str:
    """
    使用 OpenAI 兼容接口调用
    
    文档：https://help.aliyun.com/zh/model-studio/qwen-api-reference/
    """
    try:
        from openai import OpenAI
        
        print(f"【调用方式】OpenAI 兼容接口")
        print(f"【Base URL】{CONFIG['base_url']}")
        print(f"【模型】{CONFIG['model']}")
        print()
        
        # 创建客户端
        client = OpenAI(
            api_key=CONFIG["api_key"],
            base_url=CONFIG["base_url"]
        )
        
        # 调用 API
        response = client.chat.completions.create(
            model=CONFIG["model"],
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7,
            stream=False  # 非流式输出
        )
        
        # 返回结果
        return response.choices[0].message.content
        
    except ImportError:
        print("❌ 错误：缺少 openai 库")
        print("解决方案：pip install openai")
        sys.exit(1)
        
    except Exception as e:
        handle_error(e)
        raise


def test_with_dashscope(prompt: str) -> str:
    """
    使用 DashScope 原生 SDK 调用
    
    文档：https://help.aliyun.com/zh/dashscope/
    """
    try:
        import dashscope
        from dashscope import Generation
        
        print(f"【调用方式】DashScope 原生 SDK")
        print(f"【模型】{CONFIG['model']}")
        print()
        
        # 设置 API Key
        dashscope.api_key = CONFIG["api_key"]
        
        # 调用 API
        response = Generation.call(
            model=CONFIG["model"],
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7,
            result_format='message'
        )
        
        # 检查响应
        if response.status_code == 200:
            return response.output.choices[0].message.content
        else:
            raise Exception(f"API 错误：{response.status_code} - {response.message}")
        
    except ImportError:
        print("❌ 错误：缺少 dashscope 库")
        print("解决方案：pip install dashscope==1.14.1")
        sys.exit(1)
        
    except Exception as e:
        handle_error(e)
        raise


def handle_error(error: Exception):
    """
    处理 API 错误（参考阿里云官方错误码）
    文档：https://help.aliyun.com/zh/model-studio/error-code
    """
    error_msg = str(error)
    
    print("\n" + "="*60)
    print("❌ 错误详情")
    print("="*60)
    print(f"错误信息：{error_msg}")
    print()
    
    # 401 - InvalidApiKey
    if "401" in error_msg or "InvalidApiKey" in error_msg:
        print("【错误代码】InvalidApiKey")
        print("【原因】API Key 无效")
        print("【解决方案】")
        print("  1. 访问 https://dashscope.console.aliyun.com/apiKey")
        print("  2. 检查 API Key 是否正确复制（包含 sk-前缀）")
        print("  3. 确认账号已实名认证")
        print("  4. 确认套餐未过期")
        print()
    
    # 402 - Arrearage
    elif "402" in error_msg or "Arrearage" in error_msg:
        print("【错误代码】Arrearage")
        print("【原因】账号欠费")
        print("【解决方案】")
        print("  1. 访问 https://usercenter2.aliyun.com/account/recharge")
        print("  2. 充值账号")
        print("  3. 等待 5-10 分钟后重试")
        print()
    
    # 400 - InvalidParameter
    elif "400" in error_msg or "InvalidParameter" in error_msg:
        print("【错误代码】InvalidParameter")
        print("【原因】参数设置错误")
        print("【解决方案】")
        print("  1. 检查 temperature 是否在 [0.0, 2.0) 范围")
        print("  2. 检查 max_tokens 是否在合理范围")
        print("  3. 检查 messages 格式是否正确")
        print()
    
    # 500 - InternalError
    elif "500" in error_msg or "InternalError" in error_msg:
        print("【错误代码】InternalError")
        print("【原因】服务器内部错误")
        print("【解决方案】")
        print("  1. 等待 1-2 分钟后重试")
        print("  2. 检查网络连接")
        print("  3. 如持续报错，联系阿里云客服")
        print()
    
    # 其他错误
    else:
        print("【错误代码】Unknown")
        print("【解决方案】")
        print("  1. 查看完整错误信息")
        print("  2. 访问 https://help.aliyun.com/zh/model-studio/error-code")
        print("  3. 联系阿里云客服")
        print()
    
    print("="*60)


# ==================== 主程序 ====================

def main():
    """主程序"""
    print("="*60)
    print("  DashScope API 完整测试")
    print("  符合阿里云官方接口规范")
    print("="*60)
    print()
    
    # 选择调用方式
    print("请选择调用方式：")
    print("1. OpenAI 兼容接口（推荐）")
    print("2. DashScope 原生 SDK")
    choice = input("\n请输入选择（1 或 2，默认 1）：").strip()
    
    if choice == "2":
        CONFIG["mode"] = "dashscope"
        test_func = test_with_dashscope
    else:
        CONFIG["mode"] = "openai"
        test_func = test_with_openai
    
    print(f"\n已选择：{CONFIG['mode']} 模式")
    print("="*60 + "\n")
    
    # 测试 1：简单对话
    print("【测试 1】简单对话")
    print("-"*60)
    prompt1 = "你好，请介绍一下你自己。"
    print(f"提示词：{prompt1}\n")
    
    try:
        result1 = test_func(prompt1)
        print(f"\n✅ 生成成功！")
        print(f"结果：{result1[:200]}...")
    except Exception as e:
        print(f"\n❌ 测试 1 失败")
        return 1
    
    print("\n" + "="*60 + "\n")
    
    # 测试 2：创作内容
    print("【测试 2】创作抖音文案")
    print("-"*60)
    prompt2 = """你是一位抖音爆款内容创作者。

请根据以下信息创作一篇抖音口播文案：
- 选题：AI 编程助手
- 主题：提升编程效率

要求：
1. 开头要有强吸引力的钩子
2. 正文分点阐述
3. 结尾引导互动
4. 150-200 字
5. 加入 emoji
6. 提供 3-5 个话题标签

请返回 JSON 格式。"""
    print(f"提示词：{prompt2[:100]}...\n")
    
    try:
        result2 = test_func(prompt2)
        print(f"\n✅ 生成成功！")
        print(f"结果：{result2[:300]}...")
    except Exception as e:
        print(f"\n❌ 测试 2 失败")
        return 1
    
    print("\n" + "="*60 + "\n")
    
    # 测试 3：自由输入
    print("【测试 3】自由输入")
    print("-"*60)
    user_prompt = input("请输入你的提示词（回车跳过）：\n> ")
    
    if user_prompt.strip():
        try:
            result3 = test_func(user_prompt)
            print(f"\n✅ 生成成功！")
            print(f"结果：{result3}")
        except Exception as e:
            print(f"\n❌ 测试 3 失败")
            return 1
    else:
        print("跳过自由输入测试")
    
    print("\n" + "="*60)
    print("✅ 所有测试完成！")
    print("="*60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
