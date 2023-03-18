from functools import lru_cache
from orjson import orjson
import logging
import json

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person, PersonFilmList
from services.config import PersonHelper
from core.config import RedisConfig


class PersonService(PersonHelper):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_search(self, q: str, page_number: int, page_size: int) -> list[Person] | None:
        self._set_class_attr(func_name='search', q=q, page_number=page_number, page_size=page_size)

        persons = await self._search_from_cache()
        if not persons:
            persons = await self._get_search_from_elastic()
            if not persons:
                return None
            await self._put_search_to_cache(persons=persons)

        return persons

    async def get_by_id(self, person_id: str) -> Person | None:
        person = await self._person_from_cache(person_id)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self._put_person_to_cache(person)

        return person

    async def get_persons_films(self, person_id: str) -> Person | None:
        person = await self._persons_from_cache(person_id)
        if not person:
            person = await self._get_persons_films_from_elastic(person_id)
            if not person:
                return None
            await self._put_persons_to_cache(person_id, person)

        return person

    async def _get_search_from_elastic(self) -> list[Person]:
        try:
            query = {'query': {"match_all": {}}}
            doc = await self.elastic.search(index='persons',
                                            body=query,
                                            q=self.q,
                                            size=self.page_size,
                                            from_=((self.page_number - 1) * self.page_size))
        except NotFoundError:
            return None

        data = list()
        for item in doc['hits']['hits']:
            data.append(Person(**item['_source']))
        return data

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

    async def _search_from_cache(self) -> list[Person] | None:
        redis_key = self._generate_redis_key()
        logging.info('Redis key to read %s', redis_key)

        data = await self.redis.get(redis_key)
        if not data:
            return None

        persons = list()
        for person in json.loads(data.decode('utf-8')):
            persons.append(Person.parse_raw(person))

        return persons

    async def _person_from_cache(self, person_id: str) -> Person | None:
        data = await self.redis.get(f'detailed_person__{person_id}')
        logging.info('Redis key to read %s', f'detailed_person__{person_id}')
        if not data:
            return None
        person = Person.parse_raw(data)
        return person

    async def _persons_from_cache(self, key: str) -> list[PersonFilmList] | None:
        data = await self.redis.get(f'persons_films__{key}')
        if not data:
            return
        logging.info('Redis key to read %s', f'persons_films__{key}')
        persons = [PersonFilmList.parse_raw(item) for item in orjson.loads(data)]
        return persons

    async def _put_search_to_cache(self, persons: list[Person]):
        redis_key = self._generate_redis_key()
        logging.info('Redis key to write %s', redis_key)
        redis_list = []
        for person in persons:
            redis_list.append(person.json())

        await self.redis.set(
            redis_key,
            json.dumps(redis_list),
            RedisConfig().REDIS_CACHE)

    async def _put_person_to_cache(self, person: PersonFilmList) -> None:
        logging.info('Redis key to write %s', f'detailed_person__{person.uuid}')
        await self.redis.set(
            f'detailed_person__{person.uuid}',
            person.json(),
            RedisConfig().REDIS_CACHE)

    async def _put_persons_to_cache(self, key: str, persons: list[Person]) -> None:
        logging.info('Redis key to write %s', f'persons_films__{key}')
        await self.redis.set(
            f'persons_films__{key}',
            orjson.dumps([person.json(by_alias=True) for person in persons]),
            RedisConfig().REDIS_CACHE)


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
