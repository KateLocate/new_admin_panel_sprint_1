"""The transferred data consistency check for 03_sqlite_to_postgres project."""
from datetime import datetime

from constants import TABLES, SQLITE_POSTGRES_FIELDS_DIFF as FIELDS_DIFF
from load_data import sqlite3_conn_context

postgres_sqlite_diff = {v:k for k, v in FIELDS_DIFF.items()}


def rows_number_check(sqlite_conn, pg_conn):
    sqlite_cursor = sqlite_conn.cursor()
    postgres_cursor = pg_conn.cursor()

    for table in TABLES:
        sqlite_cursor.execute(f'SELECT COUNT(*) as rows FROM {table};')
        postgres_cursor.execute(f'SELECT COUNT(*) as rows FROM content.{table};')
        assert sqlite_cursor.fetchone()['rows'] == postgres_cursor.fetchone()['rows']


def rows_content_check(sqlite_conn, pg_conn, rows_num=None):
    sqlite_cursor = sqlite_conn.cursor()
    postgres_cursor = pg_conn.cursor()

    for table in TABLES:

        if not rows_num:
            sqlite_cursor.execute(f'SELECT COUNT(*) as rows FROM {table};')
            rows_num = sqlite_cursor.fetchone()['rows']

        sqlite_cursor.execute(f'SELECT * FROM {table} ORDER BY id LIMIT {rows_num};')
        sqlite_rows = sqlite_cursor.fetchall()

        postgres_cursor.execute(f'SELECT * FROM content.{table} ORDER BY id LIMIT {rows_num};')
        postgres_rows = postgres_cursor.fetchall()

        pairs = zip(sqlite_rows, postgres_rows)

        dt_format = '%Y-%m-%d %H:%M:%S'

        keys = sqlite_rows[0].keys()

        for pair in pairs:
            sqlite_row, postgres_row = pair
            sqlite_row = dict(sqlite_row)

            for key, val in postgres_row.items():
                if isinstance(val, datetime):
                    if key in postgres_sqlite_diff:
                        sqlite_k = postgres_sqlite_diff[key]
                    sqlite_val = sqlite_row[sqlite_k]
                    sqlite_row[sqlite_k] = sqlite_val.split('.')[0]
                    postgres_row[key] = val.strftime(dt_format)
            
            for key in keys:
                postgres_field = key
                if key in FIELDS_DIFF:
                    postgres_field = FIELDS_DIFF[key]
                assert sqlite_row[key] == postgres_row[postgres_field]


if __name__ == '__main__':
    import os

    import psycopg2

    from dotenv import load_dotenv
    from psycopg2.extras import DictCursor

    from load_data import load_from_sqlite

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
        **dsl, cursor_factory=DictCursor,
    ) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn, batch_size)

        rows_number_check(sqlite_conn, pg_conn)
        rows_content_check(sqlite_conn, pg_conn)
