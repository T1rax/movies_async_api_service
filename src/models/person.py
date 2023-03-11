from uuid import UUID
from pydantic import Field
from config import ConfigMixin


class Person(ConfigMixin):
    """Person information in the list."""
    uuid: str = Field(..., alias='id')
    full_name: str = Field(..., alias='name')
    roles: list[str]
    film_ids: list[UUID]


class ElasticPerson(ConfigMixin):
    """Person from ElasticSearch."""
    uuid: str = Field(..., alias='id')
    full_name: str = Field(..., alias='name')