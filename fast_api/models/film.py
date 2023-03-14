from pydantic import Field
from models.config import ConfigMixin
from models.genre import ElasticGenre
from models.person import ElasticPerson


class Film(ConfigMixin):
    """Model for films"""
    uuid: str = Field(..., alias='id')
    title: str
    imdb_rating: float | None


class FilmDetail(Film):
    """Detailed model for film"""
    description: str | None
    genre: list[ElasticGenre] | None
    actors: list[ElasticPerson] | None
    writers: list[ElasticPerson] | None
    directors: list[ElasticPerson] | None


class ElasticFilm(Film):
    """From Elasticserch"""
    description: str | None
    # genre: list[str] | None
    genre: list[ElasticGenre] | None
    # director: list[str] | None
    directors: list[ElasticPerson] | None
    actors: list[ElasticPerson] | None
    # actors_names: list[str] | None
    writers: list[ElasticPerson] | None
    # writers_names: list[str] | None
