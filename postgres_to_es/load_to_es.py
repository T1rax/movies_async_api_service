import time

from configs import BaseConfig
from etl_cls.etl import etl
from etl_cls.extractor import PostgresExtractor
from etl_cls.transformer import DataTransform
from etl_cls.loader import ElasticsearchLoader
from modules.logger import get_logger
from state import State, JsonFileStorage


if __name__ == "__main__":
    """Cls initial and config. Start ETL"""

    configs = BaseConfig()
    logger = get_logger(__name__)
    state = State(JsonFileStorage(file_path="state.json"))

    extractor = PostgresExtractor(
        postgres_dsn=configs.postgres_dsn.dict(),
        batch_size=configs.batch_size,
        storage_state=state,
        logger=logger,
    )
    transformer = DataTransform()
    loader = ElasticsearchLoader(elastic_dsn=configs.elastic_dsn.hosts, logger=logger)

    while True:
        etl(logger, extractor, transformer, state, loader)
        logger.info(f"Sleep {configs.sleep_time}")
        time.sleep(configs.sleep_time)
