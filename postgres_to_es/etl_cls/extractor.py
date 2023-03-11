from datetime import datetime
from typing import Iterator

from modules.conn import postgres_conn
from modules.movies_query import query


class PostgresExtractor:
    """Cls for extracting data from Postgres"""

    def __init__(self, postgres_dsn, batch_size: int, storage_state, logger) -> None:
        self.batch_size = batch_size
        self.state = storage_state
        self.dsn = postgres_dsn
        self.logger = logger

    def extract(self, modified: datetime) -> Iterator:
        with postgres_conn(self.dsn) as pg_conn, pg_conn.cursor() as cursor:
            select_query = cursor.mogrify(query, (modified, ) * 3)
            cursor.execute(select_query)

            while True:
                rows = cursor.fetchmany(self.batch_size)

                if not rows:
                    self.logger.info('No changes detected')
                    break

                self.logger.info(f'Extracted {len(rows)} rows')
                yield rows
