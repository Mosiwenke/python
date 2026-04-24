"""
第28章: 网络编程
=============================

Python网络编程基础.
- socket
- HTTP请求
- URL处理
"""

import socket
import urllib.request
import urllib.parse
from typing import Optional


# ============== socket基础 ==============

def socket_basic():
    """socket基础"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"socket创建: {s}")
    s.close()


# ============== 主机名解析 ==============

def hostname_resolution():
    """主机名解析"""
    hostname = socket.gethostname()
    print(f"主机名: {hostname}")
    
    ip = socket.gethostbyname(hostname)
    print(f"IP: {ip}")


# ============== HTTP请求 ==============

def http_request():
    """HTTP请求"""
    try:
        response = urllib.request.urlopen("https://httpbin.org/get")
        print(f"状态: {response.status}")
        response.close()
    except Exception as e:
        print(f"请求失败: {e}")


# ============== URL解析 ==============

def url_parse():
    """URL解析"""
    url = "https://example.com/path?query=value"
    parsed = urllib.parse.urlparse(url)
    
    print(f"scheme: {parsed.scheme}")
    print(f"netloc: {parsed.netloc}")
    print(f"path: {parsed.path}")
    print(f"query: {parsed.query}")


# ============== URL构建 ==============

def url_build():
    """URL构建"""
    params = {"query": "python", "page": 1}
    query = urllib.parse.urlencode(params)
    url = f"https://example.com/search?{query}"
    print(f"URL: {url}")


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("28. 网络编程")
    print("=" * 50)
    
    print("\n--- 1. socket基础 ---")
    socket_basic()
    
    print("\n--- 2. 主机名解析 ---")
    hostname_resolution()
    
    print("\n--- 3. HTTP请求 ---")
    http_request()
    
    print("\n--- 4. URL解析 ---")
    url_parse()
    
    print("\n--- 5. URL构建 ---")
    url_build()
    
    print("\n" + "=" * 50)
    print("网络编程学习完成!")
    print("=" * 50)