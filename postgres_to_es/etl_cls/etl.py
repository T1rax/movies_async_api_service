from datetime import datetime
import logging
import psycopg2
import elasticsearch

from etl_cls.extractor import PostgresExtractor
from etl_cls.transformer import DataTransform
from etl_cls.loader import ElasticsearchLoader
from modules.backoff import backoff
from state import State, JsonFileStorage


@backoff(elasticsearch.exceptions.ConnectionError)
@backoff(psycopg2.OperationalError)
def etl(
    logger: logging.Logger,
    extractor: PostgresExtractor,
    transformer: DataTransform,
    state: State,
    loader: ElasticsearchLoader,
) -> None:
    """Extracting, transforming and loading data"""

    start_timestamp = datetime.now()
    modified = state.get_state("modified")
    logger.info(f"Last sync {modified}")
    params = modified or datetime.min

    for extracted_part in extractor.extract(params):
        data = transformer.transform(extracted_part)
        loader.load(data)
        state.set_state("modified", str(start_timestamp))
