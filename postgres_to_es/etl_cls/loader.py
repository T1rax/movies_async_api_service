import json
import elasticsearch.exceptions
from elasticsearch import helpers, ConnectionError

from modules.conn import elasticsearch_conn
from modules.pd_cls import ElasticsearchData
from modules.backoff import backoff


class ElasticsearchLoader:
    """Cls for loading data to Elasticsearch through pydantic"""

    def __init__(self, elastic_dsn, logger) -> None:
        self.dsn = elastic_dsn
        self.logger = logger

    @backoff()
    def create_index(self, index_name: str, index_settings: dict, index_mappings: dict) -> None:
        with elasticsearch_conn(self.dsn) as es:
            if not es.ping():
                raise elasticsearch.exceptions.ConnectionError

            if not es.indices.exists(index=index_name):
                es.indices.create(index=index_name, settings=index_settings, mappings=index_mappings)
                self.logger.info(f'Create index {index_name} with:'
                                 f'{json.dumps(index_settings, indent=2)} and {json.dumps(index_mappings, indent=2)}')

    def load(self, index: str, data: list[ElasticsearchData]) -> None:
        actions = [{'_index': index, '_id': row.uuid, '_source': row.json()} for row in data]
        with elasticsearch_conn(self.dsn) as es:
            helpers.bulk(es, actions, stats_only=True)
            self.logger.info(f'Loaded {len(data)} rows')