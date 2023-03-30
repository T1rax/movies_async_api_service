import functools
from orjson import orjson

from models.film import Film
from core.config import configs
from cache.cache import Cache


class FilmCache(Cache):
    def cache_name(self, func) -> list[Film] | None:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> list[Film] | None:
            key = self.create_key(func.__name__, kwargs)
            c = args[0].cache_cli
            if await c.exists(key):
                result = await c.get(key)
                return [Film.parse_raw(item) for item in orjson.loads(result)]
            else:
                result = await func(*args, **kwargs)
                if result is None:
                    return None

                await c.set(
                    key,
                    orjson.dumps([item.json(by_alias=True) for item in result]),
                    configs.cache.exp)
                return result
        return wrapper

    def cache_id(self, func) -> Film | None:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Film | None:
            key = self.create_key(func.__name__, kwargs)
            c = args[0].cache_cli
            if await c.exists(key):
                result = await c.get(key)
                return Film.parse_raw(result)
            else:
                result = await func(*args, **kwargs)
                if result is None:
                    return None

                await c.set(
                    key,
                    result.json(),
                    configs.cache.exp)
                return result
        return wrapper

    def cache_search(self, func) -> list[Film] | None:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> list[Film] | None:
            key = self.create_key(func.__name__, kwargs)
            c = args[0].cache_cli
            if await c.exists(key):
                result = await c.get(key)
                return [Film.parse_raw(item) for item in orjson.loads(result)]
            else:
                result = await func(*args, **kwargs)
                if result is None:
                    return None

                await c.set(
                    key,
                    orjson.dumps([item.json(by_alias=True) for item in result]),
                    configs.cache.exp)
                return result
        return wrapper


cache = FilmCache()