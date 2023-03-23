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
