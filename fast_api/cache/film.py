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
            key = 'film__' + \
                  str(func.__name__) + '_' + \
                  str(kwargs.get('genre')) + '_' + \
                  str(kwargs.get('page_number')) + '_' + \
                  str(kwargs.get('page_size')) + '_' + \
                  str(kwargs.get('sort'))
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
            key = 'film__' + \
                  str(func.__name__) + '_' + \
                  str(kwargs.get('film_id'))
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
            key = 'film__' + \
                  str(func.__name__) + '_' + \
                  str(kwargs.get('q')) + '_' + \
                  str(kwargs.get('page_number')) + '_' + \
                  str(kwargs.get('page_size'))
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