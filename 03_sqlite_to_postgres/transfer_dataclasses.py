"""Dataclasses for data transfer for 03_sqlite_to_postgres project."""
from dataclasses import dataclass, field

from constants import SQLITE_POSTGRES_FIELDS_DIFF as FIELDS_DIFF


def datacls_wrapper(fields_diff: dict):
    """Implements a decorator to substitute the SQLite fields by the PostgreSQL fields."""
    def datacls_field_adapter(cls: dataclass):
        def adapter(**kwargs):
            for f_sqlite, f_postgres in fields_diff.items():
                if kwargs.get(f_sqlite, None):
                    kwargs[f_postgres] = kwargs.pop(f_sqlite)
            return cls(**kwargs)
        return adapter
    return datacls_field_adapter


@dataclass(frozen=True, kw_only=True)
class TimeStamped:
    created: str
    modified: str


@dataclass(frozen=True, kw_only=True)
class UUIDField:
    id: str


@datacls_wrapper(FIELDS_DIFF)
@dataclass(frozen=True, kw_only=True)
class Filmwork(UUIDField, TimeStamped):
    title: str
    file_path: str
    description: str
    creation_date: str
    rating: float
    type: str = field(default='')
    certificate: str = field(default='')


@datacls_wrapper(FIELDS_DIFF)
@dataclass(frozen=True, kw_only=True)
class Person(UUIDField, TimeStamped):
    full_name: str
    gender: str = field(default='')


@datacls_wrapper(FIELDS_DIFF)
@dataclass(frozen=True, kw_only=True)
class PersonFilmwork(UUIDField):
    film_work_id: str
    person_id: str
    role: str
    created: str


@datacls_wrapper(FIELDS_DIFF)
@dataclass(frozen=True, kw_only=True)
class Genre(UUIDField, TimeStamped):
    name: str
    description: str


@datacls_wrapper(FIELDS_DIFF)
@dataclass(frozen=True, kw_only=True)
class GenreFilmwork(UUIDField):
    film_work_id: str
    genre_id: str
    created: str


DATACLASSES = [
    Genre,
    Person,
    Filmwork,
    GenreFilmwork,
    PersonFilmwork,
]
