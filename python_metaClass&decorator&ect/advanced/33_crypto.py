"""
第33章: 哈希与加密
=============================

Python哈希与加密.
- hashlib
- hmac
- base64
"""

import hashlib
import hmac
import base64
from typing import Optional


# ============== hashlib ==============

def hashlib_demo():
    """hashlib演示"""
    data = b"hello"
    
    md5 = hashlib.md5(data).hexdigest()
    sha1 = hashlib.sha1(data).hexdigest()
    sha256 = hashlib.sha256(data).hexdigest()
    
    print(f"MD5: {md5}")
    print(f"SHA1: {sha1}")
    print(f"SHA256: {sha256}")


# ============== hmac ==============

def hmac_demo():
    """hmac演示"""
    key = b"secret"
    message = b"message"
    
    mac = hmac.new(key, message, hashlib.sha256).hexdigest()
    print(f"HMAC: {mac}")


# ============== base64 ==============

def base64_demo():
    """base64演示"""
    data = b"hello"
    
    encoded = base64.b64encode(data).decode()
    decoded = base64.b64decode(encoded).decode()
    
    print(f"编码: {encoded}")
    print(f"解码: {decoded}")


# ============== 密码哈希 ==============

def password_hash():
    """密码哈希"""
    password = "password123"
    
    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        b"salt",
        100000
    ).hex()
    
    print(f"哈希: {hashed[:20]}...")


if __name__ == "__main__":
    print("=" * 50)
    print("33. 哈希与加密")
    print("=" * 50)
    
    print("\n--- 1. hashlib ---")
    hashlib_demo()
    
    print("\n--- 2. hmac ---")
    hmac_demo()
    
    print("\n--- 3. base64 ---")
    base64_demo()
    
    print("\n--- 4. 密码哈希 ---")
    password_hash()
    
    print("\n" + "=" * 50)
    print("哈希与加密学习完成!")
    print("=" * 50)