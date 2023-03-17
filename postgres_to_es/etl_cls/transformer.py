from modules.pd_cls import ElasticsearchMovies, ElasticsearchGenres, ElasticsearchPersons


def set_names(row: dict, role: str) -> list[str]:
    names = []
    for person in row['persons']:
        if person['person_role'] == role:
            names.append(person['person_name'])
    return names


def set_persons(row: dict, role: str) -> list[dict]:
    detailed_persons = []
    for person in row['persons']:
        if person['person_role'] == role:
            detailed_persons.append(person)
    return detailed_persons


def set_genres(row: list) -> list[str]:
    genres = []
    for genre in row:
        genres.append(genre['genre_name'])
    return genres

def set_films(row: list) -> list[str]:
    films = []
    for film in row:
        film_dict = dict()
        film_dict['film_id'] = film['film_id']
        film_dict['film_title'] = film['film_title']
        film_dict['film_rating'] = film['film_rating']
        film_dict['film_roles'] = film['film_roles']
        films.append(film_dict)
    return films

class DataTransform:
    """Cls for transforming data from Postgres to pydantic"""

    def __init__(self, index):
        self.index_name = index

    def transform(self, batch: list[dict]):

        transformed_part = []

        match self.index_name:
            
            case 'movies':
                for row in batch:
                    transformed_row = ElasticsearchMovies(
                        id=row['id'],
                        imdb_rating=row['rating'],
                        genre=set_genres(row['genres']),
                        genres=row['genres'],
                        title=row['title'],
                        description=row['description'],
                        director=set_names(row, 'director'),
                        actors_names=set_names(row, 'actor'),
                        writers_names=set_names(row, 'writer'),
                        directors=set_persons(row, 'director'),
                        actors=set_persons(row, 'actor'),
                        writers=set_persons(row, 'writer'),
                        modified=row['updated_at']
                    )
                    transformed_part.append(transformed_row)
            
            case 'genres':
                for row in batch:
                    transformed_row = ElasticsearchGenres(
                        id=row['id'],
                        name=row['name'],
                        description=row['description']
                    )
                    transformed_part.append(transformed_row)
            
            case 'persons':
                for row in batch:
                    transformed_row = ElasticsearchPersons(
                        id=row['id'],
                        full_name=row['full_name'],
                        films=set_films(row['films']),
                        modified=row['updated_at']
                    )
                    transformed_part.append(transformed_row)

            case _:
                print('Index not found')
        
        return transformed_part
