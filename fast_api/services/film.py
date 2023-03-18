from functools import lru_cache
from typing import Optional
import logging
import json

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film
from services.config import FilmHelper
from core.config import RedisConfig


class FilmService(FilmHelper):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        FilmHelper.__init__(self)
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
        data = await self.redis.get(f'film__{film_id}')
        if not data:
            return None
        logging.info('Redis key to read %s', f'film__{film_id}')
        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        logging.info('Redis key to write %s', f'film__{film.uuid}')
        await self.redis.set(
            f'film__{film.uuid}',
            film.json(),
            RedisConfig().REDIS_CACHE)
        
    #All films on path /
    async def get_all_films(self, sort: str, genre: str, page_number: int, page_size: int) -> Optional[Film]:
        self._set_class_attr(func_name='all_films', sort=sort, page_number=page_number, page_size=page_size)
        self._generate_genre_query(genre)
        self._convert_sort_field(sort)

        films = await self._search_from_cache()
        if not films:
            films = await self._get_search_from_elastic()
            if not films:
                return None
            await self._put_search_to_cache(films=films)

        return films

    # Searches /seach
    async def get_by_search(self, q: str, page_number: int, page_size: int) -> Optional[list[Film]]:
        self._set_class_attr(func_name='search', q=q, page_number=page_number, page_size=page_size)

        films = await self._search_from_cache()
        if not films:
            films = await self._get_search_from_elastic()
            if not films:
                return None
            await self._put_search_to_cache(films=films)

        return films
    
    async def _get_search_from_elastic(self) -> Optional[list[Film]]:
        try:
            doc = await self.elastic.search(index='movies', 
                                            body=self.es_query,
                                            q=self.q, 
                                            sort=self.es_sort, 
                                            size=self.page_size, 
                                            from_=((self.page_number - 1)*self.page_size))
        except NotFoundError:
            return None
        
        data = list()
        for item in doc['hits']['hits']:
            data.append(Film(**item['_source']))
        return data

    async def _search_from_cache(self) -> Optional[list[Film]]:
        redis_key = self._generate_redis_key()
        logging.info('Redis key to read %s', redis_key)
        
        data = await self.redis.get(redis_key)
        if not data:
            return None
        
        films = list()
        for film in json.loads(data.decode('utf-8')):
            films.append(Film.parse_raw(film))
        
        return films

    async def _put_search_to_cache(self, films: list[Film]):
        redis_key = self._generate_redis_key()
        logging.info('Redis key to write %s', redis_key)

        redis_list = []
        for film in films:
            redis_list.append(film.json())

        await self.redis.set(redis_key, json.dumps(redis_list), RedisConfig().REDIS_CACHE)


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
