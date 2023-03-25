import backoff

from elasticsearch.helpers import async_bulk

class NoResultsEsception(Exception):
    "Raised when service return empty results"
    pass

class Elastic_helper:
    def __init__(self, es_client, test_config):
        self.es_client = es_client
        self.index = test_config.es_index
        self.es_id_field = test_config.es_id_field


    def get_es_bulk_query(self, data):
        
        bulk_query = []
        for row in data:
            bulk_query.append({'_index': self.index, '_id': row[self.es_id_field], '_source': row})

        return bulk_query  
    
    async def es_write_data(self, data):

        bulk_query = self.get_es_bulk_query(data)

        await self.es_client.options(ignore_status=[400,404]).indices.delete(index=self.index)

        response = await async_bulk(self.es_client, bulk_query)
        if response[1]:
            raise Exception('Ошибка записи данных в Elasticsearch')

        await self.check_index()

    @backoff.on_exception(backoff.expo, NoResultsEsception, max_time=30)
    async def check_index(self):

        result = await self.es_client.search(index=self.index, size=1)

        if result['hits']['total']['value'] == 0:
            raise NoResultsEsception


        

class Redis_helper:
    def __init__(self, redis_client, test_config):
        self.redis_client = redis_client

    
    async def clear_cache(self):
        await self.redis_client.flushall()


class Aiohttp_helper:
    def __init__(self, aiohttp_session, test_config):
        self.session = aiohttp_session

    
    async def make_get_request(self, url, path, params):
        async with self.session.get(url+path, params=params) as response:
            body = await response.json()
            headers = response.headers
            status = response.status

        if isinstance(body, list):
            length = len(body)
        else:
            length = 0

        return status, length, body, headers


class Async_helper:
    def __init__(self, event_loop, test_config):
        self.loop = event_loop
