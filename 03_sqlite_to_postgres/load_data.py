import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from contextlib import contextmanager

from constants import TABLES_VS_DATACLASSES
from transfer_data_preparation import PostgresSaver, SQLiteLoader


@contextmanager
def sqlite3_conn_context(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    yield conn

    conn.close()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection, batch_size: int):
    """Main function to transfer data from SQLite to Postgres"""

    tables = TABLES_VS_DATACLASSES.keys()
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    data_generator = sqlite_loader.load_movies(tables, batch_size)
    for batch in data_generator:
        postgres_saver.save_all_data(TABLES_VS_DATACLASSES, batch)


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

    with sqlite3_conn_context('db.sqlite') as sqlite_conn, psycopg2.connect(
        **dsl, cursor_factory=DictCursor
    ) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn, batch_size)
