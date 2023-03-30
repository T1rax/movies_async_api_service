import backoff
from functools import lru_cache
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film
from services.config import FilmHelper
from cache.cache import AsyncCacheStorage
from cache.film import cache
from core.config import configs


class FilmService(FilmHelper):
    def __init__(self, cache_cli: AsyncCacheStorage, elastic: AsyncElasticsearch):
        FilmHelper.__init__(self)
        self.cache_cli = cache_cli
        self.elastic = elastic

    @backoff.on_exception(backoff.expo, configs.cfg.excepts, max_time=configs.cfg.max_time)
    @cache.cache_name
    async def get_all_films(self, sort: str, genre: str, page_number: int, page_size: int) -> Film | None:
        body = self._generate_genre_query(genre)
        sort = self._convert_sort_field(sort)

        data = await self._get_search_from_elastic(body=body, sort=sort, page_number=page_number, page_size=page_size)
        if not data:
            return None
        return data

    @backoff.on_exception(backoff.expo, configs.cfg.excepts, max_time=configs.cfg.max_time)
    @cache.cache_id
    async def get_by_id(self, film_id: str) -> Film | None:
        data = await self._get_film_from_elastic(film_id)
        if not data:
            return None
        return data

    @backoff.on_exception(backoff.expo, configs.cfg.excepts, max_time=configs.cfg.max_time)
    @cache.cache_search
    async def get_by_search(self, q: str, page_number: int, page_size: int) -> list[Film] | None:
        films = await self._get_search_from_elastic(q=q, page_number=page_number, page_size=page_size)
        if not films:
            return None
        return films

    async def _get_film_from_elastic(self, film_id: str) -> Film | None:
        try:
            doc = await self.elastic.get('movies', film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    async def _get_search_from_elastic(self,
                                       q: str | None = None,
                                       page_number: int | None = None,
                                       page_size: int | None = None,
                                       body: str | None = None,
                                       sort: str | None = None
    ) -> list[Film] | None:
        try:
            doc = await self.elastic.search(index='movies',
                                            body=body,
                                            q=q,
                                            sort=sort,
                                            size=page_size,
                                            from_=((page_number - 1) * page_size))
        except NotFoundError:
            return None

        data = list()
        for item in doc['hits']['hits']:
            data.append(Film(**item['_source']))
        return data


@lru_cache()
def get_film_service(
        cache_cli: AsyncCacheStorage = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> FilmService:
    return FilmService(cache_cli, elastic)
