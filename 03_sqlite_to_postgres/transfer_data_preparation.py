"""Classes for data preparation."""
from dataclasses import asdict, astuple

from typing import Iterable

from psycopg2.extras import execute_values


class SQLiteLoader:
    def __init__(self, connection):
        self.connection = connection

    def load_movies(self, sqlite_tables: Iterable, batch_size: int) -> dict:
        cursor = self.connection.cursor()

        for table in sqlite_tables:
            cursor.execute(f'SELECT * FROM {table};')

            iterate = True
            while iterate:
                result = {'table_name': table, 'rows': list(cursor.fetchmany(batch_size))}
                if not result['rows']:
                    iterate = False
                else:
                    yield result


class PostgresSaver:
    def __init__(self, pg_conn):
        self.pg_conn = pg_conn

    def save_all_data(self, tables_and_datacls: dict, table_part: dict) -> None:
        table_name = table_part['table_name']
        datacls = tables_and_datacls[table_name]
        rows = table_part['rows']

        datacls_instances = [datacls(**row) for row in rows]
        keys = ', '.join(asdict(datacls_instances[0]).keys())
        tuple_instances = list(map(astuple, datacls_instances))

        query = f'INSERT INTO content.{table_name} ({keys}) VALUES %s ON CONFLICT(id) DO NOTHING;'
        cursor = self.pg_conn.cursor()

        execute_values(cursor, query, tuple_instances)
