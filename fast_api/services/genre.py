import backoff
from functools import lru_cache
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from cache.cache import AsyncCacheStorage
from cache.genre import cache
from models.genre import Genre
from core.config import configs


class GenreService:
    def __init__(self, cache_cli: AsyncCacheStorage, elastic: AsyncElasticsearch):
        self.cache_cli = cache_cli
        self.elastic = elastic

    @backoff.on_exception(backoff.expo, configs.cfg.excepts, max_time=configs.cfg.max_time)
    @cache.cache_name
    async def get_genres(self) -> list[Genre] | None:
        data = await self._get_genres_from_elastic()
        if not data:
            return None
        return data

    @backoff.on_exception(backoff.expo, configs.cfg.excepts, max_time=configs.cfg.max_time)
    @cache.cache_id
    async def get_by_id(self, genre_id: str) -> Genre | None:
        data = await self._get_genre_from_elastic(genre_id)
        if not data:
            return None
        return data

    async def _get_genre_from_elastic(self, genre_id: str) -> Genre | None:
        try:
            doc = await self.elastic.get('genres', genre_id)
        except NotFoundError:
            return None
        return Genre(**doc['_source'])

    async def _get_genres_from_elastic(self) -> list[Genre] | None:
        try:
            query = {'query': {"match_all": {}}}
            doc = await self.elastic.search(index='genres',
                                            body=query)
        except NotFoundError:
            return None

        return [Genre(**item['_source']) for item in doc['hits']['hits']]


@lru_cache()
def get_genre_service(
        cache_cli: AsyncCacheStorage = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(cache_cli, elastic)
