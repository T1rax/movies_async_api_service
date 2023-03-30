import functools
from orjson import orjson

from models.person import Person, PersonFilmList
from core.config import configs
from cache.cache import Cache


class PersonCache(Cache):
    def cache_name(self, func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            key = self.create_key(func.__name__, kwargs)
            c = args[0].cache_cli
            if await c.exists(key):
                result = await c.get(key)
                return [PersonFilmList.parse_raw(item) for item in orjson.loads(result)]
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

    def cache_id(self, func) -> Person | None:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Person | None:
            key = self.create_key(func.__name__, kwargs)
            c = args[0].cache_cli
            if await c.exists(key):
                result = await c.get(key)
                return Person.parse_raw(result)
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

    def cache_search(self, func) -> list[Person] | None:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> list[Person] | None:
            key = self.create_key(func.__name__, kwargs)
            c = args[0].cache_cli
            if await c.exists(key):
                result = await c.get(key)
                return [Person.parse_raw(item) for item in orjson.loads(result)]
            else:
                result = await func(*args, **kwargs)
                if result is None:
                    return None

                await c.set(
                    key,
                    orjson.dumps([item.json() for item in result]),
                    configs.cache.exp)
                return result
        return wrapper


cache = PersonCache()