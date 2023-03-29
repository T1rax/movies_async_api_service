class FilmHelper:
    def _generate_genre_query(self, genre):
        if genre is not None:
            query = {
                'query': {
                    'nested': {
                        'path': 'genres',
                        'query': {
                            'constant_score': {
                                'filter': {
                                    'term': {
                                        'genres.id': {
                                            'value': genre
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        else:
            query = {'query': {"match_all": {}}}

        return query

    def _convert_sort_field(self, sort):
        if sort is not None and sort[0] == '-':
            sort = sort[1:] + ':desc'
        return sort