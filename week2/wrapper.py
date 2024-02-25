from typing import Any
from functools import wraps
import time
import json

from starlette.responses import JSONResponse


class Cache:
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Cache, cls).__new__(cls)
            cls.cache = {}
        return cls._instance
    
    def get(self, key):
        return self.cache.get(key)
    
    def set(self, key, value):
        self.cache[key] = value


def log_request_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        query = kwargs.get("query")
        request = kwargs.get("request")

        client_ip = request.client.host
        url = request.url.path
        method = request.method

        start_time = time.perf_counter()
        response = await func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"{func.__name__} took {total_time} seconds")

        log = {
            "request_processing_time": total_time,
            "request_method": method,
            "request_url": url,
            "query_params": query,
            "client_ip": client_ip,
            "response_status_code": response.status_code,
        }
        print(json.dumps(log, indent=4, ensure_ascii=False))
        return response
    return wrapper


def cache_response(func) -> Any:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        query = kwargs.get("query")
        request = kwargs.get("request")

        client_ip = request.client.host
        url = request.url.path
        method = request.method
        key = f"{client_ip}:{url}:{method}:{query}"

        cache = Cache()
        if cache.get(key):
            print("Cache hit", key)
            return cache.get(key)
        response = await func(*args, **kwargs)
        cache.set(key, response)
        return response
    return wrapper


def exception_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})
    return wrapper
