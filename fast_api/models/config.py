import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class ConfigMixin(BaseModel):
    """Base config for models"""
    class Config:
        json_loads = orjson.loads   # переопределяем json-преобразователь
        json_dumps = orjson_dumps   # в json
        allow_population_by_field_name = True   # позволяет использовать алиасы