import datetime
import uuid
import random


class Elastic_mock:
    def __init__(self):
        pass

    def generate_film_data(self, n_copies):
        
        es_data = [{
            'id': str(uuid.uuid4()),
            'imdb_rating': round(random.uniform(1, 10), 1),
            'genre': ['Action', 'Sci-Fi'],
            'genres': [
                {'id': 'genre-id-1', 'name': 'Action'},
                {'id': 'genre-id-2', 'name': 'Sci-Fi'}
            ],
            'title': 'The Star',
            'description': 'New World',
            'director': ['Stan'],
            'actors_names': ['Ann', 'Bob'],
            'writers_names': ['Ben', 'Howard'],
            'directors': [
                {'id': '555', 'name': 'Stan'},
            ],
            'actors': [
                {'id': '111', 'name': 'Ann'},
                {'id': '222', 'name': 'Bob'}
            ],
            'writers': [
                {'id': '333', 'name': 'Ben'},
                {'id': '444', 'name': 'Howard'}
            ],
            'modified': datetime.datetime.now().isoformat()
        } for _ in range(n_copies)]

        return es_data
    
    def generate_film_with_id(self, id='qwerty123-5a1c-4b95-b32b-fdd89b40dddc'):
        
        es_data = [{
            'id': id,
            'imdb_rating': 8.5,
            'genre': ['Action', 'Sci-Fi'],
            'genres': [
                {'id': 'genre-id-1', 'name': 'Action'},
                {'id': 'genre-id-2', 'name': 'Sci-Fi'}
            ],
            'title': 'The Star',
            'description': 'New World',
            'director': ['Stan'],
            'actors_names': ['Ann', 'Bob'],
            'writers_names': ['Ben', 'Howard'],
            'directors': [
                {'id': '555', 'name': 'Stan'},
            ],
            'actors': [
                {'id': '111', 'name': 'Ann'},
                {'id': '222', 'name': 'Bob'}
            ],
            'writers': [
                {'id': '333', 'name': 'Ben'},
                {'id': '444', 'name': 'Howard'}
            ],
            'modified': datetime.datetime.now().isoformat()
        }]

        return es_data
    
    def generate_genre_data(self):
        
        es_data = [
            {
            'id': 'genre-id-1',
            'name': 'Action',
            'description': 'Cool genre',
            },
            {
            'id': 'genre-id-2',
            'name': 'Sci-Fi',
            'description': 'Cool genre',
            },
            {
            'id': 'genre-id-3',
            'name': 'Sci-Fi',
            'description': 'Documentary',
            },
            {
            'id': 'genre-id-4',
            'name': 'Sci-Fi',
            'description': 'Detective',
            },
            {
            'id': 'genre-id-5',
            'name': 'Sci-Fi',
            'description': 'Horror',
            },
        ]

        return es_data

    def generate_person_data(self):
        es_data = [
            {
                'id': 'person-id-1',
                'full_name': 'Edd Gee',
                'films': [
                        {
                          "id": "111",
                          "roles": [
                            "actor"
                          ],
                          "imdb_rating": 7,
                          "title": "The Star"
                        },
                        {
                          "id": "222",
                          "roles": [
                            "actor"
                          ],
                          "imdb_rating": 6.8,
                          "title": "The Wars"
                        }
                      ],
                'modified': datetime.datetime.now().isoformat()
            },
            {
                'id': 'person-id-2',
                'full_name': 'Alan Po',
                'films': [
                    {
                        "id": "333",
                        "roles": [
                            "writer"
                        ],
                        "imdb_rating": 1,
                        "title": "The Movie 2"
                    },
                    {
                        "id": "444",
                        "roles": [
                            "actor"
                        ],
                        "imdb_rating": 9,
                        "title": "Test Film 2"
                    }
                ],
                'modified': datetime.datetime.now().isoformat()
            }
        ]

        return es_data
    

es_mock = Elastic_mock()