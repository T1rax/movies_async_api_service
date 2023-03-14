import time

from configs import BaseConfig
from etl_cls.etl import etl
from etl_cls.extractor import PostgresExtractor
from etl_cls.transformer import DataTransform
from etl_cls.loader import ElasticsearchLoader
from modules.logger import get_logger
from modules.pool import data_pool
from state import State, JsonFileStorage


class PoolInit:
    def __init__(self, pool, configs, logger):
        self.pool = pool
        self.state = State(JsonFileStorage(file_path=pool.file))
        self.extractor = PostgresExtractor(
            postgres_dsn=configs.postgres_dsn.dict(),
            batch_size=configs.batch_size,
            storage_state=self.state,
            logger=logger,
            index=pool.index,
            query=pool.query
            )
        self.transformer = DataTransform(
            index=pool.index
            )
        self.loader = ElasticsearchLoader(elastic_dsn=configs.elastic_dsn.hosts, logger=logger, pool=pool)


if __name__ == "__main__":
    """Cls initial and config. Start ETL"""
    configs = BaseConfig()
    logger = get_logger(__name__)
    state_pool = [PoolInit(pool, configs, logger) for pool in data_pool]

    for p in state_pool:
        p.loader.create_index(p.pool.index)

    while True:
        for p in state_pool:
            etl(logger, p.extractor, p.transformer, p.state, p.loader)
        logger.info(f"Sleep {configs.sleep_time}")
        time.sleep(configs.sleep_time)
