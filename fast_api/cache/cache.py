import abc


class AsyncCacheStorage(abc.ABC):
    @abc.abstractmethod
    async def get(self, key: str, **kwargs):
        pass

    @abc.abstractmethod
    async def set(self, key: str, value: str, ex: int, **kwargs):
        pass

    @abc.abstractmethod
    async def exists(self, *keys: str, **kwargs):
        pass


class Cache(abc.ABC):
    @abc.abstractmethod
    def cache_name(self):
        pass

    @abc.abstractmethod
    def cache_id(self):
        pass

    @abc.abstractmethod
    def cache_search(self):
        pass

    def create_key(self, name, kwargs):
        return '___'.join([str(name),
                           str(kwargs.get('film_id')),
                           str(kwargs.get('genre_id')),
                           str(kwargs.get('person_id')),
                           str(kwargs.get('q')),
                           str(kwargs.get('genre')),
                           str(kwargs.get('page_number')),
                           str(kwargs.get('page_size')),
                           str(kwargs.get('sort'))])