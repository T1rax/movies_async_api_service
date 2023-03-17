from uuid import UUID
from pydantic import BaseModel, Field
from models.config import ConfigMixin


class FilmPerson(ConfigMixin):
    uuid: str = Field(alias='id')
    roles: list[str]
    imdb_rating: float | None
    title: str | None


class Person(ConfigMixin):
    """Model for persons"""
    uuid: str = Field(..., alias='id')
    full_name: str = Field(...)
    films: list[FilmPerson]


class PersonFilmList(ConfigMixin):
    uuid: str = Field(alias='id')
    title: str | None
    imdb_rating: float | None
