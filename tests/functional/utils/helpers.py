from typing import List

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, async_bulk


class Elastic_helper:
    def __init__(self, es_client, test_settings):
        self.es_client = es_client
        self.index = test_settings.es_index
        self.es_id_field = test_settings.es_id_field


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