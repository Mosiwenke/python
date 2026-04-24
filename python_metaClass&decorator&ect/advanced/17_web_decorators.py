"""
第17章: Web框架装饰器应用
=============================

装饰器在Web框架中的实际应用.
- 路由装饰器
- 中间件
- 认证装饰器
- 速率限制
"""

from functools import wraps
from typing import Callable, Dict, List, Optional, Any
import time
import hashlib
import json


# ============== 简单Web框架 ==============

routes: Dict[str, Callable] = {}
middleware: List[Callable] = []


def route(path: str, methods: List[str] = None):
    """路由装饰器"""
    if methods is None:
        methods = ["GET"]
    
    def decorator(func: Callable) -> Callable:
        routes[path] = func
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        wrapper._route = path
        wrapper._methods = methods
        return wrapper
    
    return decorator


def add_middleware(func: Callable):
    """添加中间件"""
    middleware.append(func)
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    return wrapper


def route_demo():
    """路由演示"""
    
    @route("/home", ["GET"])
    def home():
        return "Welcome Home!"
    
    @route("/api/users", ["GET", "POST"])
    def users():
        return ["Alice", "Bob"]
    
    print(f"路由: {list(routes.keys())}")
    print(f"home: {routes['/home']()}")
    print(f"users: {routes['/api/users']()}")


# ============== 认证装饰器 ==============

class Auth:
    """认证管理器"""
    sessions: Dict[str, Dict] = {}
    
    @classmethod
    def create_session(cls, user_id: int) -> str:
        session_id = hashlib.sha256(
            f"{user_id}{time.time()}".encode()
        ).hexdigest()[:32]
        cls.sessions[session_id] = {
            "user_id": user_id,
            "created_at": time.time()
        }
        return session_id
    
    @classmethod
    def get_session(cls, session_id: str) -> Optional[Dict]:
        return cls.sessions.get(session_id)


def login_required(func: Callable) -> Callable:
    """登录 required装饰器"""
    
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        session_id = request.get("session_id")
        
        if not session_id:
            return {"error": "未登录", "code": 401}
        
        session = Auth.get_session(session_id)
        if not session:
            return {"error": "session无效", "code": 401}
        
        request["user"] = session
        return func(request, *args, **kwargs)
    
    return wrapper


def admin_required(func: Callable) -> Callable:
    """管理员权限装饰器"""
    
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user = request.get("user", {})
        
        if user.get("role") != "admin":
            return {"error": "权限不足", "code": 403}
        
        return func(request, *args, **kwargs)
    
    return wrapper


def auth_demo():
    """认证演示"""
    request = {"session_id": "test123"}
    
    @login_required
    def get_profile(req):
        return {"user": req["user"]}
    
    result = get_profile(request)
    print(f"结果: {result}")


# ============== 速率限制 ==============

class RateLimiter:
    """速率限制器"""
    _buckets: Dict[str, List[float]] = {}
    
    @classmethod
    def check(cls, key: str, max_requests: int, window: int) -> bool:
        now = time.time()
        
        if key not in cls._buckets:
            cls._buckets[key] = []
        
        bucket = cls._buckets[key]
        bucket[:] = [t for t in bucket if now - t < window]
        
        if len(bucket) >= max_requests:
            return False
        
        bucket.append(now)
        return True


def rate_limit(max_requests: int = 60, window: int = 60):
    """速率限制装饰器"""
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            ip = request.get("ip", "unknown")
            
            if not RateLimiter.check(ip, max_requests, window):
                return {"error": "请求过于频繁", "code": 429}
            
            return func(request, *args, **kwargs)
        
        return wrapper
    
    return decorator


def rate_limit_demo():
    """速率限制演示"""
    
    @rate_limit(max_requests=5, window=60)
    def api_endpoint(req):
        return {"success": True}
    
    for i in range(6):
        result = api_endpoint({"ip": "127.0.0.1"})
        print(f"请求{i+1}: {result.get('success', result.get('error'))}")


# ============== 请求日志 ==============

def log_request(func: Callable) -> Callable:
    """请求日志装饰器"""
    
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        start = time.perf_counter()
        
        result = func(request, *args, **kwargs)
        
        elapsed = time.perf_counter() - start
        print(f"[{request.get('path', 'unknown')}] {elapsed:.3f}s")
        
        return result
    
    return wrapper


# ============== 错误处理 ==============

def handle_errors(func: Callable) -> Callable:
    """错误处理装饰器"""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return {"error": str(e), "code": 400}
        except Exception as e:
            return {"error": "内部错误", "code": 500}
    
    return wrapper


# ============== 缓存 ==============

class ViewCache:
    """视图缓存"""
    _cache: Dict[str, tuple] = {}
    
    @classmethod
    def get(cls, key: str) -> Optional[Any]:
        if key in cls._cache:
            value, expires = cls._cache[key]
            if time.time() < expires:
                return value
        return None
    
    @classmethod
    def set(cls, key: str, value: Any, ttl: int = 300):
        cls._cache[key] = (value, time.time() + ttl)


def cache_view(ttl: int = 300):
    """视图缓存装饰器"""
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            cache_key = f"{func.__name__}:{request.get('path', '')}"
            
            cached = ViewCache.get(cache_key)
            if cached is not None:
                return cached
            
            result = func(request, *args, **kwargs)
            ViewCache.set(cache_key, result, ttl)
            
            return result
        
        return wrapper
    
    return decorator


# ============== CORS ==============

def cors(origin: str = "*"):
    """CORS装饰器"""
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            result = func(request, *args, **kwargs)
            
            if isinstance(result, dict):
                result["headers"] = {
                    "Access-Control-Allow-Origin": origin,
                    "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE",
                }
            
            return result
        
        return wrapper
    
    return decorator


# ============== 参数验证 ==============

def validate_body(schema: Dict):
    """请求体验证装饰器"""
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            body = request.get("body", {})
            
            for field, expected_type in schema.items():
                if field not in body:
                    return {"error": f"缺少字段: {field}", "code": 400}
                
                if not isinstance(body[field], expected_type):
                    return {"error": f"字段类型错误: {field}", "code": 400}
            
            return func(request, *args, **kwargs)
        
        return decorator
    
    return decorator


# ============== 链式装饰器 ==============

def chain_decorator(*decorators):
    """链式装饰器"""
    
    def decorator(func: Callable) -> Callable:
        for deco in reversed(decorators):
            func = deco(func)
        return func
    
    return decorator


def web_demo():
    """Web框架演示"""
    
    @log_request
    @handle_errors
    @cache_view(ttl=60)
    @rate_limit(max_requests=10)
    def api_handler(request):
        return {"data": "Hello!"}
    
    result = api_handler({"path": "/api"})
    print(f"结果: {result}")


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("17. Web框架装饰器应用")
    print("=" * 50)
    
    # 测试1: 路由
    print("\n--- 1. 路由 ---")
    route_demo()
    
    # 测试2: 认证
    print("\n--- 2. 认证 ---")
    auth_demo()
    
    # 测试3: 速率限制
    print("\n--- 3. 速率限制 ---")
    rate_limit_demo()
    
    # 测试4: Web
    print("\n--- 4. Web框架 ---")
    web_demo()
    
    print("\n" + "=" * 50)
    print("Web框架装饰器学习完成!")
    print("=" * 50)