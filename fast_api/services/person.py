from functools import lru_cache

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person, PersonFilmList
from services.config import PersonHelper


PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class PersonService(PersonHelper):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, person_id: str) -> Person | None:
        person = await self._person_from_cache(person_id)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self._put_person_to_cache(person)

        return person

    async def _get_person_from_elastic(self, person_id: str) -> Person | None:
        try:
            doc = await self.elastic.get('persons', person_id)
        except NotFoundError:
            return None
        return Person(**doc['_source'])

    async def get_persons_films(self, person_id: str) -> Person | None:
        person = None
        if not person:
            person = await self._get_persons_films_from_elastic(person_id)
            if not person:
                return None

        return person

    async def _get_persons_films_from_elastic(self, person_id: str) -> Person | None:
        try:
            doc = await self.elastic.get('persons', person_id)
        except NotFoundError:
            return None
        return [PersonFilmList(**d) for d in doc['_source']['films']]

    async def _person_from_cache(self, person_id: str) -> Person | None:
        data = await self.redis.get(person_id)
        if not data:
            return None

        person = Person.parse_raw(data)
        return person

    async def _put_person_to_cache(self, person: Person):
        await self.redis.set(person.uuid, person.json(), PERSON_CACHE_EXPIRE_IN_SECONDS)

    async def get_by_search(self, q: str, page_number: int, page_size: int) -> list[Person] | None:
        self._set_class_attr(func_name='search', q=q, page_number=page_number, page_size=page_size)

        persons = None
        if not persons:
            persons = await self._get_search_from_elastic()
            if not persons:
                return None

        return persons

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


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
