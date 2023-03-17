from pydantic import Field
from models.config import ConfigMixin


class Genre(ConfigMixin):
    """Model for genres"""
    uuid: str = Field(..., alias='id')
    name: str