#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的 DashScope API 测试脚本
直接调用 API 测试 Key 是否有效
"""

import dashscope
from dashscope import Generation

# ==================== 配置 ====================
# 在这里填入你的 API Key
API_KEY = "sk-sp-215c5f115f0b42aa82afa6f28e12fbd7"

# 使用的模型
MODEL = "qwen3.5-plus"

# ==================== 测试函数 ====================

def test_api(prompt: str) -> str:
    """
    调用 DashScope API 生成内容
    
    Args:
        prompt: 提示词
        
    Returns:
        生成的内容
    """
    # 设置 API Key
    dashscope.api_key = API_KEY
    
    try:
        print(f"正在调用 {MODEL} 模型...")
        print(f"提示词：{prompt[:100]}...")
        print()
        
        # 调用 API
        response = Generation.call(
            model=MODEL,
            prompt=prompt,
            max_tokens=2000,
            temperature=0.7,
            result_format='message'
        )
        
        # 检查响应
        if response.status_code == 200:
            content = response.output.choices[0].message.content
            return content
        else:
            error_msg = f"API 错误：{response.status_code} - {response.message}"
            print(f"❌ {error_msg}")
            return error_msg
            
    except Exception as e:
        error_msg = f"调用失败：{e}"
        print(f"❌ {error_msg}")
        return error_msg


# ==================== 主程序 ====================

if __name__ == "__main__":
    print("="*60)
    print("  DashScope API 简单测试")
    print("="*60)
    print()
    
    # 测试 1：简单对话
    print("【测试 1】简单对话")
    print("-"*60)
    prompt1 = "你好，请介绍一下你自己。"
    result1 = test_api(prompt1)
    print(f"\n✅ 生成结果：\n{result1}")
    print("\n" + "="*60 + "\n")
    
    # 测试 2：创作内容
    print("【测试 2】创作抖音文案")
    print("-"*60)
    prompt2 = """你是一位抖音爆款内容创作者。

请根据以下信息创作一篇抖音口播文案：
- 选题：AI 编程助手
- 主题：提升编程效率

要求：
1. 开头要有强吸引力的钩子（前 3 秒抓住观众）
2. 正文分点阐述，每点简洁有力
3. 结尾引导点赞、评论、关注
4. 全文 150-200 字，口语化表达
5. 加入合适的 emoji 表情
6. 提供 3-5 个相关话题标签

请返回 JSON 格式。"""
    
    result2 = test_api(prompt2)
    print(f"\n✅ 生成结果：\n{result2}")
    print("\n" + "="*60 + "\n")
    
    # 测试 3：自由输入
    print("【测试 3】自由输入提示词")
    print("-"*60)
    user_prompt = input("请输入你的提示词（直接回车跳过）：\n> ")
    
    if user_prompt.strip():
        result3 = test_api(user_prompt)
        print(f"\n✅ 生成结果：\n{result3}")
    else:
        print("跳过自由输入测试")
    
    print("\n" + "="*60)
    print("测试完成！")
    print("="*60)
