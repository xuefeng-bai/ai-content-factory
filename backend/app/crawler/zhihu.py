# -*- coding: utf-8 -*-
"""
Zhihu Hot List Crawler
Fetch Top 50 hot questions from Zhihu mobile API
"""

import requests
from typing import List, Dict
import time
import random
from pathlib import Path

# User-Agent Pool (Mobile User-Agents)
USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
]


def get_random_user_agent() -> str:
    """Randomly select a User-Agent"""
    return random.choice(USER_AGENTS)


def fetch_zhihu_hot_list(max_retries: int = 3) -> List[Dict]:
    """
    Fetch Zhihu hot list (using mobile API)
    
    Args:
        max_retries: Maximum retry attempts
        
    Returns:
        List of hot questions with rank, title, hot_value, url, answer_count
    """
    # Zhihu mobile API
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
                print("[WARNING] Zhihu API returned unexpected format")
                return []
            
            for idx, item in enumerate(data["data"], 1):
                try:
                    target = item.get("target", {})
                    question_id = target.get("id", "")
                    title = target.get("title", "No Title")
                    answer_count = target.get("answer_count", 0)
                    excerpt = target.get("excerpt", "")
                    
                    # Extract hot value (answer count)
                    hot_value = f"{answer_count}回答"
                    
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
                    print(f"[WARNING] Failed to parse hot list item {idx}: {e}")
                    continue
            
            print(f"[SUCCESS] Fetched {len(hot_list)} Zhihu hot questions")
            return hot_list
            
        except requests.RequestException as e:
            print(f"[ERROR] Failed to fetch Zhihu hot list (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                print(f"[ERROR] Max retries reached, returning empty list")
                return []
        except Exception as e:
            print(f"[ERROR] Failed to parse JSON: {e}")
            return []
    
    return []


if __name__ == "__main__":
    # Test code
    print("Testing Zhihu hot list crawler...")
    result = fetch_zhihu_hot_list()
    print(f"\nResult: {len(result)} items")
    if result:
        print("\nTop 5 hot questions:")
        for item in result[:5]:
            print(f"  {item['rank']}. {item['title']} ({item['hot_value']})")
