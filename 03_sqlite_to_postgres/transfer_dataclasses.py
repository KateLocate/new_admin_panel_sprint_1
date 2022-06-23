"""Dataclasses for data transfer."""
from dataclasses import dataclass, field


def datacls_field_adapter(cls):
    def adapter(**kwargs):
        fields_diff = {'created_at': 'created', 'updated_at': 'modified'}
        for f_sqlite, f_postgre in fields_diff.items():
            if kwargs.get(f_sqlite, None):
                kwargs[f_postgre] = kwargs.pop(f_sqlite)
        return cls(**kwargs)
    return adapter


@dataclass(frozen=True, kw_only=True)
class TimeStamped:
    created: str
    modified: str


@dataclass(frozen=True, kw_only=True)
class UUIDField:
    id: str


@datacls_field_adapter
@dataclass(frozen=True, kw_only=True)
class Filmwork(UUIDField, TimeStamped):
    title: str
    file_path: str
    description: str
    creation_date: str
    rating: float
    type: str = field(default='')
    certificate: str = field(default='')


@datacls_field_adapter
@dataclass(frozen=True, kw_only=True)
class Person(UUIDField, TimeStamped):
    full_name: str
    gender: str = field(default='')


@datacls_field_adapter
@dataclass(frozen=True, kw_only=True)
class PersonFilmwork(UUIDField):
    film_work_id: str
    person_id: str
    role: str
    created: str


@datacls_field_adapter
@dataclass(frozen=True, kw_only=True)
class Genre(UUIDField, TimeStamped):
    name: str
    description: str


@datacls_field_adapter
@dataclass(frozen=True, kw_only=True)
class GenreFilmwork(UUIDField):
    film_work_id: str
    genre_id: str
    created: str
