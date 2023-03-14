from collections import namedtuple
from modules.query import movies_query, genres_query
from modules.index import mappings_movies, mappings_genres


QueryIndex = namedtuple('QueryIndex', ['index', 'mappings', 'query', 'file'])

movies = QueryIndex(
    'movies',
    mappings_movies,
    movies_query,
    'movies.json'
)

genres = QueryIndex(
    'genres',
    mappings_genres,
    genres_query,
    'genres.json'
)

data_pool = [movies, genres]