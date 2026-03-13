# -*- coding: utf-8 -*-
"""
微博热搜爬虫模块
功能：爬取微博热搜榜 Top50（使用移动端 API）
"""

import requests
from typing import List, Dict
import time
import random
from pathlib import Path

# User-Agent 轮换池（使用移动端 User-Agent 绕过反爬）
USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
]


def get_random_user_agent() -> str:
    """随机选择一个 User-Agent"""
    return random.choice(USER_AGENTS)


def fetch_weibo_hot_search(max_retries: int = 3) -> List[Dict]:
    """
    爬取微博热搜榜（使用移动端 API 接口）
    
    Args:
        max_retries: 最大重试次数
        
    Returns:
        热搜列表，每条包含：rank, title, hot_value, url
    """
    # 使用微博热搜 API（无需登录）
    url = "https://weibo.com/ajax/side/hotSearch"
    params = {}
    
    headers = {
        "User-Agent": get_random_user_agent(),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "https://weibo.com/",
        "X-Requested-With": "XMLHttpRequest",
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            hot_search_list = []
            
            # 解析 API 返回数据
            if "data" not in data:
                print("[警告] 微博 API 返回数据格式异常")
                print(f"[调试] 返回数据：{str(data)[:200]}")
                return []
            
            realtime = data["data"].get("realtime", [])
            
            for idx, item in enumerate(realtime[:50], 1):
                try:
                    title = item.get("word", "")
                    if not title:
                        continue
                    
                    # 提取热度值
                    hot_value = item.get("note", "") or f"{item.get('num', 0)} 热度"
                    
                    # 生成链接
                    url = f"https://s.weibo.com/weibo?q={title}"
                    
                    hot_search_list.append({
                        "rank": idx,
                        "title": title,
                        "hot_value": hot_value,
                        "url": url,
                        "source": "weibo"
                    })
                except Exception as e:
                    print(f"[警告] 解析热搜项失败：{e}")
                    continue
            
            print(f"[成功] 爬取微博热搜 {len(hot_search_list)} 条")
            return hot_search_list
            
        except requests.RequestException as e:
            print(f"[错误] 爬取微博热搜失败 (尝试 {attempt + 1}/{max_retries}): {e}")
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
    print("开始测试微博热搜爬虫...")
    result = fetch_weibo_hot_search()
    print(f"\n爬取结果：{len(result)} 条")
    if result:
        print("\n前 5 条热搜：")
        for item in result[:5]:
            print(f"  {item['rank']}. {item['title']} ({item['hot_value']})")
