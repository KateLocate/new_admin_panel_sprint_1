"""Constants for 03_sqlite_to_postgres project."""
from transfer_dataclasses import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


TABLES_VS_DATACLASSES = {
    'genre': Genre,
    'person': Person,
    'film_work': Filmwork,
    'genre_film_work': GenreFilmwork,
    'person_film_work': PersonFilmwork,
}

# format: field_sqlite: field_postgres;
SQLITE_POSTGRES_FIELDS_DIFF = {
    'created_at': 'created',
    'updated_at': 'modified',
}
