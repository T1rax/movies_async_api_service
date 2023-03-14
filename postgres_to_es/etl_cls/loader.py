import elasticsearch.exceptions
from elasticsearch import helpers, ConnectionError

from modules.conn import elasticsearch_conn
from modules.backoff import backoff
from modules.index import settings


class ElasticsearchLoader:
    """Cls for loading data to Elasticsearch through pydantic"""

    def __init__(self, elastic_dsn, logger, pool) -> None:
        self.dsn = elastic_dsn
        self.logger = logger
        self.mappings = pool.mappings
        self.index = pool.index

    @backoff()
    def create_index(self, index_name: str) -> None:
        with elasticsearch_conn(self.dsn) as es:
            if not es.ping():
                raise elasticsearch.exceptions.ConnectionError

            if not es.indices.exists(index=index_name):
                es.indices.create(index=self.index, settings=settings, mappings=self.mappings)
                self.logger.info(f'Create index {index_name}')

    def load(self, data) -> None:
        actions = [{'_index': self.index, '_id': row.id, '_source': row.json()} for row in data]
        with elasticsearch_conn(self.dsn) as es:
            helpers.bulk(es, actions, stats_only=True)
            self.logger.info(f'Loaded {len(data)} rows')
