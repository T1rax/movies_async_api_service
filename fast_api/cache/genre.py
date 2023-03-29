import functools
from orjson import orjson

from models.genre import Genre
from core.config import configs
from cache.redis import RedisCache
from db.redis import get_redis


class GenreCache(RedisCache):
    def cache_name(self, func) -> list[Genre] | None:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> list[Genre] | None:
            key = self.create_key(func.__name__, kwargs)
            r = await get_redis()
            if await r.exists(key):
                result = await r.get(key)
                return [Genre.parse_raw(item) for item in orjson.loads(result)]
            else:
                result = await func(*args, **kwargs)
                await r.set(
                    key,
                    orjson.dumps([genre.json(by_alias=True) for genre in result]),
                    configs.redis_config.REDIS_CACHE)
                return result
        return wrapper

    def cache_id(self, func) -> Genre | None:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Genre | None:
            print(args)
            key = self.create_key(func.__name__, kwargs)
            r = await get_redis()
            if await r.exists(key):
                result = await r.get(key)
                return Genre.parse_raw(result)
            else:
                result = await func(*args, **kwargs)
                await r.set(
                    key,
                    result.json(),
                    configs.redis_config.REDIS_CACHE)
                return result
        return wrapper

    def cache_search(self):
        pass


cache = GenreCache()