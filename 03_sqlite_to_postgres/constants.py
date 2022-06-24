"""Constants for 03_sqlite_to_postgres project."""
TABLES = [
    'genre',
    'person',
    'film_work',
    'genre_film_work',
    'person_film_work',
]

# format: field_sqlite: field_postgres;
SQLITE_POSTGRES_FIELDS_DIFF = {
    'created_at': 'created',
    'updated_at': 'modified',
}
