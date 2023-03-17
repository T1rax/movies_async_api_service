from pydantic import Field
from models.config import ConfigMixin


class Film(ConfigMixin):
    """Model for films"""
    uuid: str = Field(..., alias='id')
    title: str
    imdb_rating: float | None
