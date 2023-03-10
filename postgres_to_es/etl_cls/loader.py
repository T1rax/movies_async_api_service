import json
import elasticsearch.exceptions
from elasticsearch import helpers, ConnectionError

from modules.conn import elasticsearch_conn
from modules.pd_cls import ElasticsearchData
from modules.backoff import backoff
from modules.index import settings, mappings


class ElasticsearchLoader:
    """Cls for loading data to Elasticsearch through pydantic"""

    def __init__(self, elastic_dsn, logger) -> None:
        self.dsn = elastic_dsn
        self.logger = logger
        self.create_index('movies')

    @backoff()
    def create_index(self, index_name: str) -> None:
        with elasticsearch_conn(self.dsn) as es:
            if not es.ping():
                raise elasticsearch.exceptions.ConnectionError

            if not es.indices.exists(index='movies'):
                es.indices.create(index=index_name, settings=settings, mappings=mappings)
                self.logger.info(f'Create index {index_name} with:'
                                 f'{json.dumps(settings, indent=2)} and {json.dumps(mappings, indent=2)}')

    def load(self, data: list[ElasticsearchData]) -> None:
        actions = [{'_index': 'movies', '_id': row.id, '_source': row.json()} for row in data]
        with elasticsearch_conn(self.dsn) as es:
            helpers.bulk(es, actions, stats_only=True)
            self.logger.info(f'Loaded {len(data)} rows')