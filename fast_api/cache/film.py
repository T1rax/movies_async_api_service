import functools
from orjson import orjson

from models.film import Film
from core.config import configs
from cache.redis import RedisCache
from db.redis import get_redis


class FilmCache(RedisCache):
    def cache_name(self, func) -> list[Film] | None:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> list[Film] | None:
            key = self.create_key(func.__name__, kwargs)
            r = await get_redis()
            if await r.exists(key):
                result = await r.get(key)
                return [Film.parse_raw(item) for item in orjson.loads(result)]
            else:
                result = await func(*args, **kwargs)
                await r.set(
                    key,
                    orjson.dumps([item.json(by_alias=True) for item in result]),
                    configs.redis_config.REDIS_CACHE)
                return result
        return wrapper

    def cache_id(self, func) -> Film | None:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Film | None:
            key = self.create_key(func.__name__, kwargs)
            r = await get_redis()
            if await r.exists(key):
                result = await r.get(key)
                return Film.parse_raw(result)
            else:
                result = await func(*args, **kwargs)
                await r.set(
                    key,
                    result.json(),
                    configs.redis_config.REDIS_CACHE)
                return result
        return wrapper

    def cache_search(self, func) -> list[Film] | None:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> list[Film] | None:
            key = self.create_key(func.__name__, kwargs)
            r = await get_redis()
            if await r.exists(key):
                result = await r.get(key)
                return [Film.parse_raw(item) for item in orjson.loads(result)]
            else:
                result = await func(*args, **kwargs)
                await r.set(
                    key,
                    orjson.dumps([item.json(by_alias=True) for item in result]),
                    configs.redis_config.REDIS_CACHE)
                return result
        return wrapper


cache = FilmCache()