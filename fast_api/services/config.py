class FilmHelper:
    def __init__(self):
        self.func_name = None
        self.q = None
        self.sort = None
        self.page_number = None
        self.page_size = None
        self.genre_id = None
        self.es_query = None
        self.es_sort = None
    
    def _set_class_attr(self, func_name = None, q = None, sort = None, page_number = None, page_size = None):
        self.func_name = func_name
        self.q = q
        self.sort = sort
        self.page_number = page_number
        self.page_size = page_size

    def _generate_redis_key(self):
        redis_key = '___'.join(filter(None, map(str, 
            ['movies', self.func_name, self.genre_id, self.q, self.sort, self.page_number, self.page_size]
        )))
        return redis_key
    
    def _generate_genre_query(self, genre):
        if genre is not None:
            query = {
                'query': {
                    'nested':{
                        'path': 'genres',
                        'query': {
                            'constant_score': {
                                'filter': {
                                    'term': {
                                        'genres.id':{
                                            'value': genre
                                            } 
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
        
            self.genre_id = genre
        else:
            query = {'query':{"match_all": {}}}
        
        self.es_query = query
    
    def _convert_sort_field(self, sort):
        if sort is not None and sort[0] == '-':
            sort = sort[1:]+':desc'
        self.es_sort = sort


class PersonHelper:
    def __init__(self):
        self.func_name = None
        self.q = None
        self.page_number = None
        self.page_size = None

    def _set_class_attr(self, func_name=None, q=None, sort=None, page_number=None, page_size=None):
        self.func_name = func_name
        self.q = q
        self.page_number = page_number
        self.page_size = page_size

    def _generate_redis_key(self):
        redis_key = '___'.join(filter(None, map(str,
            ['person', self.func_name, self.q, self.page_number, self.page_size]
        )))
        return redis_key