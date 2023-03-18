from functools import lru_cache
from orjson import orjson
import logging

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre
from core import config


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_genres(self) -> list[Genre] | None:
        genres = await self._genres_from_cache()
        if not genres:
            genres = await self._get_genres_from_elastic()
            if not genres:
                return None
            await self._put_genres_to_cache(genres)
        return genres

    async def get_by_id(self, genre_id: str) -> Genre | None:
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return None
            await self._put_genre_to_cache(genre)

        return genre

    async def _get_genre_from_elastic(self, genre_id: str) -> Genre | None:
        try:
            doc = await self.elastic.get('genres', genre_id)
        except NotFoundError:
            return None
        return Genre(**doc['_source'])

    async def _get_genres_from_elastic(self) -> list[Genre]:
        try:
            query = {'query': {"match_all": {}}}
            doc = await self.elastic.search(index='genres',
                                            body=query,
                                            )
        except NotFoundError:
            return None

        data = list()
        for item in doc['hits']['hits']:
            data.append(Genre(**item['_source']))
        return data

    async def _genres_from_cache(self) -> list[Genre]:
        data = await self.redis.get('get_genres_films')
        if not data:
            return
        logging.info('Redis key to read %s', 'get_genres_films')
        genres = [Genre.parse_raw(item) for item in orjson.loads(data)]
        return genres

    async def _genre_from_cache(self, genre_id: str) -> Genre | None:
        data = await self.redis.get(f'genre_uuid_{genre_id}')
        if not data:
            return None
        logging.info('Redis key to read %s', f'genre_uuid_{genre_id}')
        genre = Genre.parse_raw(data)
        return genre

    async def _put_genres_to_cache(self, genres: list[Genre]) -> None:
        logging.info('Redis key to write %s', 'get_genres_films')
        await self.redis.set(
            'get_genres_films',
            orjson.dumps([genre.json(by_alias=True) for genre in genres]),
            config.REDIS_CACHE
        )

    async def _put_genre_to_cache(self, genre: Genre) -> None:
        logging.info('Redis key to write %s', f'genre_uuid_{genre.uuid}')
        await self.redis.set(f'genre_uuid_{genre.uuid}', genre.json(), config.REDIS_CACHE)


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
