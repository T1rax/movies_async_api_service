from functools import lru_cache
from typing import Optional
import logging

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут

logging.getLogger().setLevel(logging.INFO)

class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    #Get specific film by id
    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get('movies', film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None

        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(film.uuid, film.json(), FILM_CACHE_EXPIRE_IN_SECONDS)
        
    #All films on path /
    async def get_all_films(self, sort: str, genre: str, page_number: int, page_size: int) -> Optional[Film]:
        if genre is not None:
            query = 'genre:'+genre
        else:
            query = '*'

        films = None #await self._film_from_cache(film_id)
        if not films:
            films = await self._get_search_from_elastic(query=query, 
                                                        sort=sort,
                                                        page_number=page_number, 
                                                        page_size=page_size)
            if not films:
                return None
            #await self._put_film_to_cache(film)

        return films

    # Searches /seach
    async def get_by_search(self, q: str, page_number: int, page_size: int) -> Optional[list[Film]]:
        films = None #await self._film_from_cache(film_id)
        if not films:
            films = await self._get_search_from_elastic(q=q, 
                                                        sort = None,
                                                        page_number=page_number, 
                                                        page_size=page_size)
            if not films:
                return None
            #await self._put_film_to_cache(film)

        return films
    
    async def _get_search_from_elastic(self, sort: str, page_number: int, page_size: int, query: str = None, q: str = None) -> Optional[list[Film]]:
        try:
            doc = await self.elastic.search(index='movies', 
                                            query=query, 
                                            q=q, 
                                            sort=sort, 
                                            size=page_size, 
                                            from_=((page_number - 1)*page_size))
        except NotFoundError:
            return None
        
        data = list()
        for item in doc['hits']['hits']:
            data.append(Film(**item['_source']))
        return data

    async def _search_from_cache(self, query: str) -> Optional[Film]:
        data = await self.redis.get(query)
        if not data:
            return None

        film = Film.parse_raw(data)
        return film

    async def _put_search_to_cache(self, film: Film):
        await self.redis.set(film.uuid, film.json(), FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
