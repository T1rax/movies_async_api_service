from modules.pd_cls import ElasticsearchData


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
        film_dict['uuid'] = film['film_id']
        film_dict['roles'] = film['film_roles']
        films.append(film_dict)
    return films


def set_full_films(row: list) -> list[str]:
    films = []
    for film in row:
        film_dict = dict()
        film_dict['uuid'] = film['film_id']
        film_dict['title'] = film['film_title']
        film_dict['imdb_rating'] = film['film_rating']
        film_dict['roles'] = film['film_roles']
        films.append(film_dict)
    return films


class DataTransform:
    """Cls for transforming data from Postgres to pydantic"""

    def transform_to_movies(self, batch: list[dict]) -> list[ElasticsearchData]:

        transformed_part = []
        for row in batch:
            transformed_row = ElasticsearchData(
                uuid=row['id'],
                imdb_rating=row['rating'],
                genre=set_genres(row['genres']),
                genres=row['genres'],
                title=row['title'],
                description=row['description'],
                director=set_names(row, 'D'),
                actors_names=set_names(row, 'A'),
                writers_names=set_names(row, 'W'),
                directors=set_persons(row, 'D'),
                actors=set_persons(row, 'A'),
                writers=set_persons(row, 'W'),
                modified=row['updated_at']
            )
            transformed_part.append(transformed_row)
        
        return transformed_part
    
    
    def transform_to_persons(self, batch: list[dict]) -> list[ElasticsearchData]:

        transformed_part = []
        for row in batch:
            transformed_row = ElasticsearchData(
                uuid=row['id'],
                full_name=row['full_name'],
                films=set_films(row['films']),
                films_full=set_full_films(row['films']),
                modified=row['updated_at']
            )
            transformed_part.append(transformed_row)
        
        return transformed_part
