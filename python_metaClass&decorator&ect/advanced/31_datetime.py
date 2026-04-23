"""
第31章: 日期时间处理
=============================

Python日期时间处理.
- datetime
- time
- timedelta
"""

import datetime
import time
import calendar
from typing import Optional


# ============== datetime ==============

def datetime_demo():
    """datetime演示"""
    now = datetime.datetime.now()
    print(f"现在: {now}")
    print(f"日期: {now.date()}")
    print(f"时间: {now.time()}")


# ============== 时间戳 ==============

def timestamp_demo():
    """时间戳"""
    now = datetime.datetime.now()
    timestamp = now.timestamp()
    print(f"时间戳: {timestamp}")
    
    dt = datetime.datetime.fromtimestamp(timestamp)
    print(f"转换: {dt}")


# ============== timedelta ==============

def timedelta_demo():
    """timedelta演示"""
    delta = datetime.timedelta(days=1, hours=2)
    print(f"delta: {delta}")
    print(f"秒: {delta.total_seconds()}")
    
    now = datetime.datetime.now()
    future = now + delta
    print(f"未来: {future}")


# ============== time ==============

def time_module():
    """time模块"""
    print(f"time: {time.time()}")
    print(f"sleep: 不阻塞")
    time.sleep(0.01)


# ============== calendar ==============

def calendar_demo():
    """calendar"""
    cal = calendar.month(2024, 1)
    print(cal)


# ============== 时区 ==============

def timezone_demo():
    """时区"""
    utc = datetime.timezone.utc
    now_utc = datetime.datetime.now(utc)
    print(f"UTC: {now_utc}")


if __name__ == "__main__":
    print("=" * 50)
    print("31. 日期时间处理")
    print("=" * 50)
    
    print("\n--- 1. datetime ---")
    datetime_demo()
    
    print("\n--- 2. 时间戳 ---")
    timestamp_demo()
    
    print("\n--- 3. timedelta ---")
    timedelta_demo()
    
    print("\n--- 4. time ---")
    time_module()
    
    print("\n--- 5. calendar ---")
    calendar_demo()
    
    print("\n--- 6. timezone ---")
    timezone_demo()
    
    print("\n" + "=" * 50)
    print("日期时间学习完成!")
    print("=" * 50)