from datetime import datetime
import logging

from etl_cls.extractor import PostgresExtractor
from etl_cls.transformer import DataTransform
from etl_cls.loader import ElasticsearchLoader
from modules.backoff import backoff
from state import State
from postgres_to_es.modules.pg_queries import movies_query, persons_query


@backoff()
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

    #films pipeline
    for extracted_part in extractor.extract(params, movies_query):
        movies_data = transformer.transform_to_movies(extracted_part)
        loader.load('movies', movies_data)
    
    #clean memory
    del movies_data


    #persons pipeline
    for extracted_part in extractor.extract(params, persons_query):
        persons_data = transformer.transform_to_persons(extracted_part)
        loader.load('persons', persons_data)

    #clean memory
    del persons_data

    #if all indexes updated successfully - set new date state
    state.set_state("modified", str(start_timestamp))