"""Classes for data preparation."""
from dataclasses import asdict, astuple

from typing import Iterable

from psycopg2.extras import execute_values


class SQLiteLoader:
    """Representation of the logic of data extraction from the SQLite database."""

    def __init__(self, connection):
        self.connection = connection

    def load_movies(self, sqlite_tables: Iterable, batch_size: int = 100) -> dict:
        """
        Implements data extraction and returns table name and table rows.

        Parameters:
            sqlite_tables: Requires list of existing SQLite table names.
            batch_size: Function divides data into batches of the chosen size, otherwise uses the default value 100.

        Yields:
            dict: Consists of 'table_name' and 'rows' of the target table.
        """
        cursor = self.connection.cursor()

        for table in sqlite_tables:
            cursor.execute(f'SELECT * FROM {table};')

            iterate = True
            while iterate:
                batch = {'table_name': table, 'rows': list(cursor.fetchmany(batch_size))}
                if not batch['rows']:
                    iterate = False
                else:
                    yield batch


class PostgresSaver:
    """Representation of the logic of data loading to PostgreSQL database."""

    def __init__(self, pg_conn):
        self.pg_conn = pg_conn

    def save_all_data(self, tables_and_datacls: dict, table_part: dict) -> None:
        """
        Implements data validation and loading into target tables.

        Parameters:
            tables_and_datacls: Requires to specify the PostgreSQL table names matching dataclass templates.
            table_part: Takes dictionary consisting of the table name and the rows of the target table.
        """
        table_name, rows = table_part['table_name'], table_part['rows']
        datacls = tables_and_datacls[table_name]

        datacls_instances = [datacls(**row) for row in rows]
        keys = ', '.join(asdict(datacls_instances[0]).keys())
        tuple_instances = list(map(astuple, datacls_instances))

        query = f'INSERT INTO content.{table_name} ({keys}) VALUES %s ON CONFLICT(id) DO NOTHING;'
        cursor = self.pg_conn.cursor()

        execute_values(cursor, query, tuple_instances)
