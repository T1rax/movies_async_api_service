from datetime import datetime
from typing import Iterator

from modules.conn import postgres_conn
from modules.query import movies_query


class PostgresExtractor:
    """Cls for extracting data from Postgres"""

    def __init__(self, postgres_dsn, batch_size: int, storage_state, logger, index, query) -> None:
        self.batch_size = batch_size
        self.state = storage_state
        self.dsn = postgres_dsn
        self.logger = logger
        self.index = index
        self.query = query

    def extract(self, modified: datetime) -> Iterator:
        with postgres_conn(self.dsn) as pg_conn, pg_conn.cursor() as cursor:
            if self.index == 'movies':
                select_query = cursor.mogrify(self.query, (modified, ) * 3)
            else:
                select_query = cursor.mogrify(self.query, (modified, ))

            cursor.execute(select_query)
            self.logger.info(f'Extracting index {self.index}')
            while True:
                rows = cursor.fetchmany(self.batch_size)

                if not rows:
                    self.logger.info('No changes detected')
                    break

                self.logger.info(f'Extracted {len(rows)} rows')
                yield rows
