import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from contextlib import contextmanager

from transfer_data_preparation import PostgresSaver, SQLiteLoader
from transfer_dataclasses import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


@contextmanager
def sqlite3_conn_context(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    yield conn

    conn.close()


def load_from_sqlite(
    connection: sqlite3.Connection, pg_conn: _connection, tables_and_datacls: dict, fields_diff: dict, batch_size: int
):
    """Main function to transfer data from SQLite to Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    data = sqlite_loader.load_movies(['film_work'], batch_size)
    for batch in data:
        postgres_saver.save_all_data(tables_and_datacls, fields_diff, batch)


if __name__ == '__main__':
    import os

    from dotenv import load_dotenv

    load_dotenv()
    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': '127.0.0.1',
        'port': os.environ.get('DB_PORT'),
    }
    batch_size = 200
    sqlite_vs_datacls = {
        'film_work': Filmwork,
        'genre_film_work': GenreFilmwork,
        'person_film_work': PersonFilmwork,
        'genre': Genre,
        'person': Person,
    }

    fields_diff = {'created_at': 'created', 'updated_at': 'modified'}

    with sqlite3_conn_context('db.sqlite') as sqlite_conn, psycopg2.connect(
        **dsl, cursor_factory=DictCursor
    ) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn, sqlite_vs_datacls, fields_diff, batch_size)
