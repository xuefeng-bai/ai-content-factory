# -*- coding: utf-8 -*-
"""
Weibo Hot Search Crawler
Fetch Top 50 hot searches from Weibo mobile API
"""

import requests
from typing import List, Dict
import time
import random
from pathlib import Path

# User-Agent Pool (Mobile User-Agents to bypass anti-crawling)
USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
]


def get_random_user_agent() -> str:
    """Randomly select a User-Agent"""
    return random.choice(USER_AGENTS)


def fetch_weibo_hot_search(max_retries: int = 3) -> List[Dict]:
    """
    Fetch Weibo hot search list (using mobile API)
    
    Args:
        max_retries: Maximum retry attempts
        
    Returns:
        List of hot searches with rank, title, hot_value, url
    """
    # Weibo hot search API (no login required)
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
            
            # Parse API response
            if "data" not in data:
                print("[WARNING] Weibo API returned unexpected format")
                print(f"[DEBUG] Response: {str(data)[:200]}")
                return []
            
            realtime = data["data"].get("realtime", [])
            
            for idx, item in enumerate(realtime[:50], 1):
                try:
                    title = item.get("word", "")
                    if not title:
                        continue
                    
                    # Extract hot value
                    hot_value = item.get("note", "") or f"{item.get('num', 0)}热度"
                    
                    # Generate URL
                    url = f"https://s.weibo.com/weibo?q={title}"
                    
                    hot_search_list.append({
                        "rank": idx,
                        "title": title,
                        "hot_value": hot_value,
                        "url": url,
                        "source": "weibo"
                    })
                except Exception as e:
                    print(f"[WARNING] Failed to parse hot search item: {e}")
                    continue
            
            print(f"[SUCCESS] Fetched {len(hot_search_list)} Weibo hot searches")
            return hot_search_list
            
        except requests.RequestException as e:
            print(f"[ERROR] Failed to fetch Weibo hot search (attempt {attempt + 1}/{max_retries}): {e}")
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
    print("Testing Weibo hot search crawler...")
    result = fetch_weibo_hot_search()
    print(f"\nResult: {len(result)} items")
    if result:
        print("\nTop 5 hot searches:")
        for item in result[:5]:
            print(f"  {item['rank']}. {item['title']} ({item['hot_value']})")
