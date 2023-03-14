from uuid import UUID
from pydantic import Field
from models.config import ConfigMixin


class Person(ConfigMixin):
    """Model for persons"""
    uuid: str = Field(..., alias='id')
    full_name: str = Field(..., alias='name')
    roles: list[str]
    film_ids: list[UUID]


class ElasticPerson(ConfigMixin):
    """From Elasticserch"""
    uuid: str = Field(..., alias='id')
    full_name: str = Field(..., alias='name')