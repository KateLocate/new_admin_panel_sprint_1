"""Classes for data preparation."""


class SQLiteLoader:
    def __init__(self, connection):
        self.connection = connection

    def load_movies(self, sqlite_tables, batch_size):
        cursor = self.connection.cursor()
        for table in sqlite_tables:
            cursor.execute(f'select count(*) as rows_count from {table};')
            rows_count = cursor.fetchone()['rows_count']
            iter_count = rows_count // batch_size + 1 if rows_count % batch_size else rows_count // batch_size
            for _ in range(iter_count):
                cursor.execute(f'select * from {table};')
                yield {'table_name': table, 'objects': list(cursor.fetchmany(batch_size))}


class PostgresSaver:
    def __init__(self, pg_conn):
        self.pg_conn = pg_conn

    def save_all_data(self, tables_and_datacls, fields_diff, table_part) -> None:
        table_name = table_part['table_name']
        datacls = tables_and_datacls[table_name]
        objects = table_part['objects']
        datacls_intances = []
        for obj in objects:
            dict_obj = dict(obj)
            for f_sqlite, f_postgre in fields_diff.items():
                if dict_obj[f_sqlite]:
                    dict_obj[f_postgre] = dict_obj.pop(f_sqlite)
            datacls_intances.append(datacls(**dict_obj))
        print(datacls_intances[0])
        # insert_stmnt = f'INSERT INTO content.{table_name} ({keys}) VALUES ({vals}), ...; '
        pass
