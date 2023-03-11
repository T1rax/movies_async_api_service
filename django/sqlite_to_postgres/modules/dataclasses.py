from dataclasses import dataclass, field, astuple
import uuid
import datetime


@dataclass
class Movie:
    title: str
    description: str
    creation_date: datetime.date
    created_at: datetime.date
    updated_at: datetime.date
    file_path: str
    type: str
    rating: float = field(default=0.0)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Genre:
    name: str
    description: str
    created_at: datetime.date
    updated_at: datetime.date
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Person:
    full_name: str
    created_at: datetime.date
    updated_at: datetime.date
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class PersonFilmwork:
    role: str
    created_at: datetime.date
    person_id: uuid.UUID
    film_work_id: uuid.UUID
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class GenreFilmwork:
    created_at: datetime.date
    genre_id: uuid.UUID
    film_work_id: uuid.UUID
    id: uuid.UUID = field(default_factory=uuid.uuid4)
