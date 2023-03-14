from collections import namedtuple
from modules.query import movies_query, genres_query, persons_query
from modules.index import mappings_movies, mappings_genres, mappings_persons


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

persons = QueryIndex(
    'persons',
    mappings_persons,
    persons_query,
    'persons.json'
)

data_pool = [movies, genres, persons]