from psycopg2.extras import execute_batch
from dataclasses import astuple
from .dataclasses import (
    Movie, Person, Genre,
    PersonFilmwork, GenreFilmwork,
)


def get_names(cls):
    names = ' ,'.join([i for i in cls.__annotations__.keys()])
    return names


def set_number(cls):
    names = [i for i in cls.__annotations__.keys()]
    number = ' ,'.join(['%s' for s in range(0, len(names))])
    return number


def make_one_letter(row):
    if isinstance(row, Movie):
        if row.type == 'movie':
            row.type = 'M'
    elif isinstance(row, PersonFilmwork):
        if row.role == 'director':
            row.role = 'M'
        elif row.role == 'writer':
            row.role = 'W'
        elif row.role == 'actor':
            row.role = 'A'
    return row


class PostgresSaver:
    def __init__(self, pg_conn):
        self.pg_conn = pg_conn

    def save_data(self, data: list, cls, table: str, batch_size: int = 25):
        with self.pg_conn.cursor() as cursor:
            cmd = f'INSERT INTO content.{table} ({get_names(cls)}) ' \
                  f'VALUES ({set_number(cls)}) ON CONFLICT (id) DO NOTHING;'
            imp = [astuple(row) for row in data]
            execute_batch(cursor, cmd, imp, page_size=batch_size)
            self.pg_conn.commit()


class PostgresExtractor:
    def __init__(self, pg_conn):
        self.pg_conn = pg_conn

    def is_table_not_empty(self, table: str):
        with self.pg_conn.cursor() as cursor:
            cursor.execute(f'SELECT * FROM content.{table};')
            if cursor.rowcount > 0:
                return True
            else:
                return False