import functools
from orjson import orjson

from models.genre import Genre
from core.config import configs
from cache.cache import Cache


class GenreCache(Cache):
    def cache_name(self, func) -> list[Genre] | None:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> list[Genre] | None:
            key = self.create_key(func.__name__, kwargs)
            c = args[0].cache_cli
            if await c.exists(key):
                result = await c.get(key)
                return [Genre.parse_raw(item) for item in orjson.loads(result)]
            else:
                result = await func(*args, **kwargs)
                if result is None:
                    return None

                await c.set(
                    key,
                    orjson.dumps([genre.json(by_alias=True) for genre in result]),
                    configs.cache.exp)
                return result
        return wrapper

    def cache_id(self, func) -> Genre | None:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Genre | None:
            print(args)
            key = self.create_key(func.__name__, kwargs)
            c = args[0].cache_cli
            if await c.exists(key):
                result = await c.get(key)
                return Genre.parse_raw(result)
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

    def cache_search(self):
        pass


cache = GenreCache()