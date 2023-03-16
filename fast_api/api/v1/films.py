from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Request
from models.film import Film
from services.film import FilmService, get_film_service
import logging
from pydantic import BaseModel

router = APIRouter()

logging.getLogger().setLevel(logging.INFO)

# Внедряем FilmService с помощью Depends(get_film_service)
@router.get('/', response_model=list[Film])
async def film_query(sort: str | None = None,
                     genre: str | None = None,
                     page_number: int | None  = 1, 
                     page_size: int | None  = 50, 
                     film_service: FilmService = Depends(get_film_service)) -> Film:
    films = await film_service.get_all_films(sort, genre, page_number, page_size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Films not found')
    return films


# Внедряем FilmService с помощью Depends(get_film_service)
@router.get('/search', response_model=list[Film])
async def film_search(query: str | None  = None, 
                      page_number: int | None  = 1, 
                      page_size: int | None  = 50, 
                      film_service: FilmService = Depends(get_film_service)) -> Film:
    films = await film_service.get_by_search(q=query, page_number=page_number, page_size=page_size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Films not found')
    return films


# Внедряем FilmService с помощью Depends(get_film_service)
@router.get('/{film_id}', response_model=Film)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return Film(uuid=film.uuid, title=film.title, imdb_rating=film.imdb_rating)