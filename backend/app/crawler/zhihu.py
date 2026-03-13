# -*- coding: utf-8 -*-
"""
知乎热榜爬虫模块
功能：爬取知乎热榜 Top50（使用移动端 API）
"""

import requests
from typing import List, Dict
import time
import random
from pathlib import Path

# User-Agent 轮换池（使用移动端 User-Agent）
USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
]


def get_random_user_agent() -> str:
    """随机选择一个 User-Agent"""
    return random.choice(USER_AGENTS)


def fetch_zhihu_hot_list(max_retries: int = 3) -> List[Dict]:
    """
    爬取知乎热榜（使用移动端 API 接口）
    
    Args:
        max_retries: 最大重试次数
        
    Returns:
        热榜列表，每条包含：rank, title, hot_value, url, answer_count
    """
    # 使用知乎移动端 API
    url = "https://api.zhihu.com/topstory/hot-list"
    params = {
        "limit": 50,
        "reverse_order": "0",
    }
    
    headers = {
        "User-Agent": get_random_user_agent(),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "X-Device-Id": "web",
        "X-Client-Version": "3.0.0",
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            hot_list = []
            
            if "data" not in data:
                print("[警告] 知乎 API 返回数据格式异常")
                return []
            
            for idx, item in enumerate(data["data"], 1):
                try:
                    target = item.get("target", {})
                    question_id = target.get("id", "")
                    title = target.get("title", "无标题")
                    answer_count = target.get("answer_count", 0)
                    excerpt = target.get("excerpt", "")
                    
                    # 提取热度值（回答数）
                    hot_value = f"{answer_count} 回答"
                    
                    hot_list.append({
                        "rank": idx,
                        "title": title,
                        "hot_value": hot_value,
                        "url": f"https://www.zhihu.com/question/{question_id}",
                        "source": "zhihu",
                        "answer_count": answer_count,
                        "excerpt": excerpt[:50] + "..." if len(excerpt) > 50 else excerpt
                    })
                except Exception as e:
                    print(f"[警告] 解析第{idx}条热榜失败：{e}")
                    continue
            
            print(f"[成功] 爬取知乎热榜 {len(hot_list)} 条")
            return hot_list
            
        except requests.RequestException as e:
            print(f"[错误] 爬取知乎热榜失败 (尝试 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # 指数退避
            else:
                print(f"[错误] 达到最大重试次数，返回空列表")
                return []
        except Exception as e:
            print(f"[错误] 解析 JSON 失败：{e}")
            return []
    
    return []


if __name__ == "__main__":
    # 测试代码
    print("开始测试知乎热榜爬虫...")
    result = fetch_zhihu_hot_list()
    print(f"\n爬取结果：{len(result)} 条")
    if result:
        print("\n前 5 条热榜：")
        for item in result[:5]:
            print(f"  {item['rank']}. {item['title']} ({item['hot_value']})")
