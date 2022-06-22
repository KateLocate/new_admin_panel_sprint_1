"""Dataclasses for data transfer."""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class TimeStamped:
    created: str
    modified: str


@dataclass(frozen=True)
class UUIDField:
    id: str


@dataclass(frozen=True)
class Filmwork(UUIDField, TimeStamped):
    title: str
    file_path: str
    genres: list
    description: str
    creation_date: str
    rating: float
    type: str
    certificate: str = field(default='')


@dataclass(frozen=True)
class Person(UUIDField, TimeStamped):
    full_name: str
    gender: str = field(default='')


@dataclass(frozen=True)
class PersonFilmwork(UUIDField):
    film_work: str
    person: str
    role: str
    created: str


@dataclass(frozen=True)
class Genre(UUIDField, TimeStamped):
    name: str
    description: str


@dataclass(frozen=True)
class GenreFilmwork(UUIDField):
    film_work: str
    genre: str
    created: str
