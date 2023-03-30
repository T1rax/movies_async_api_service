import backoff
from functools import lru_cache
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person, PersonFilmList
from cache.cache import AsyncCacheStorage
from cache.person import cache
from core.config import configs


class PersonService:
    def __init__(self, cache_cli: AsyncCacheStorage, elastic: AsyncElasticsearch):
        self.cache_cli = cache_cli
        self.elastic = elastic

    @backoff.on_exception(backoff.expo, configs.cfg.excepts, max_time=configs.cfg.max_time)
    @cache.cache_name
    async def get_persons_films(self, person_id: str) -> Person | None:
        data = await self._get_persons_films_from_elastic(person_id)
        if not data:
            return None
        return data

    @backoff.on_exception(backoff.expo, configs.cfg.excepts, max_time=configs.cfg.max_time)
    @cache.cache_id
    async def get_by_id(self, person_id: str) -> Person | None:
        data = await self._get_person_from_elastic(person_id)
        if not data:
            return None
        return data

    @backoff.on_exception(backoff.expo, configs.cfg.excepts, max_time=configs.cfg.max_time)
    @cache.cache_search
    async def get_by_search(self,
                            q: str | None = None,
                            page_number: int | None = None,
                            page_size: int | None = None
    ) -> list[Person] | None:
        data = await self._get_search_from_elastic(q=q,
                                                   page_number=page_number,
                                                   page_size=page_size)
        if not data:
            return None
        return data

    async def _get_search_from_elastic(self,
                                       q: str | None = None,
                                       page_number: int | None = None,
                                       page_size: int | None = None
    ) -> list[Person] | None:
        try:
            query = {'query': {"match_all": {}}}
            doc = await self.elastic.search(index='persons',
                                            body=query,
                                            q=q,
                                            size=page_size,
                                            from_=((page_number - 1) * page_size))
        except NotFoundError:
            return None
        return [Person(**item['_source']) for item in doc['hits']['hits']]

    async def _get_person_from_elastic(self, person_id: str) -> Person | None:
        try:
            doc = await self.elastic.get('persons', person_id)
        except NotFoundError:
            return None
        return Person(**doc['_source'])

    async def _get_persons_films_from_elastic(self, person_id: str) -> list[PersonFilmList] | None:
        try:
            doc = await self.elastic.get('persons', person_id)
        except NotFoundError:
            return None
        return [PersonFilmList(**d) for d in doc['_source']['films']]


@lru_cache()
def get_person_service(
        cache_cli: AsyncCacheStorage = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(cache_cli, elastic)
