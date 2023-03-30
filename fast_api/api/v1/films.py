from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Query
from models.film import Film
from services.film import FilmService, get_film_service
from core.pagination import PaginatedParams


router = APIRouter()


# Внедряем FilmService с помощью Depends(get_film_service)
@router.get('/',
            response_model=list[Film],
            description='Show information about all films')
async def film_query(sort: str | None = None,
                     genre: str | None = None,
                     pagination_data: PaginatedParams = Depends(PaginatedParams),
                     film_service: FilmService = Depends(get_film_service)) -> Film:
    films = await film_service.get_all_films(sort=sort,
                                             genre=genre,
                                             page_number=pagination_data.page_number,
                                             page_size=pagination_data.page_size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Films not found')
    return films


@router.get('/search',
            response_model=list[Film],
            description='Search for the film')
async def film_search(query: str | None = None,
                      pagination_data: PaginatedParams = Depends(PaginatedParams),
                      film_service: FilmService = Depends(get_film_service)) -> Film:
    films = await film_service.get_by_search(q=query,
                                             page_number=pagination_data.page_number,
                                             page_size=pagination_data.page_size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Films not found')
    return films


@router.get('/{film_id}',
            response_model=Film,
            description='Show information about the film')
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id=film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Film not found')

    return Film(uuid=film.uuid, title=film.title, imdb_rating=film.imdb_rating)