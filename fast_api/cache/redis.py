import abc


class RedisCache:
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
                           str(kwargs.get('q')),
                           str(kwargs.get('genre')),
                           str(kwargs.get('page_number')),
                           str(kwargs.get('page_size')),
                           str(kwargs.get('sort'))])