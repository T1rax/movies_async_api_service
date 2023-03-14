import os
from contextlib import contextmanager
from psycopg2.extras import DictCursor
from psycopg2.extensions import connection as _connection
import psycopg2
import sqlite3
from modules.sql import SqlExtractor
from modules.pg import PostgresSaver, PostgresExtractor
from modules.dataclasses import (
    Movie, Person, Genre,
    PersonFilmwork, GenreFilmwork,
)
from dotenv import load_dotenv


load_dotenv()

# Настройки подключения к БД
sqlite = os.path.join(os.getcwd(), os.environ.get('SQL_PATH'))
dsl = {'dbname': os.environ.get('DB_NAME'),
       'user': os.environ.get('DB_USER'),
       'password': os.environ.get('DB_PASSWORD'),
       'host': os.environ.get('DB_HOST'),
       'port': os.environ.get('DB_PORT'),}


# Dataclasses - Table
tables = [(Movie, 'film_work'),
          (Genre, 'genre'),
          (Person, 'person'),
          (GenreFilmwork, 'genre_film_work'),
          (PersonFilmwork, 'person_film_work')]


@contextmanager
def conn_context(db_path: str):
    """Добавление в общий контекст подключения к SQLite"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def pg_conn_context(dsl: dict):
    """Добавление в общий контекст подключения к postgres"""
    pg_conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    try:
        yield pg_conn
    finally:
        pg_conn.close()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в extractor.py"""

    postgres_saver = PostgresSaver(pg_conn)
    postgres_extractor = PostgresExtractor(pg_conn)
    sqlite_extractor = SqlExtractor(connection)

    for row in tables:
        data_cls, table = row

        # Check if table already has data
        if postgres_extractor.is_table_not_empty(table):
            print("Table %s already has data" % (table))
            continue

        print("Transfer data from SQLite to PG for table - %s" % (table))
        for data in sqlite_extractor.get_data(data_cls, table):
            postgres_saver.save_data(data, data_cls, table)
        print("Data transfered - %s" % (table))


if __name__ == '__main__':
    with conn_context(sqlite) as sqlite_conn, pg_conn_context(dsl) as pg_conn:
        """Запуск основной функции переноса данных"""
        load_from_sqlite(sqlite_conn, pg_conn)
        sqlite_conn.close()
        pg_conn.close()

