from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from models.genre import Genre
from services.genre import GenreService, get_genre_service


router = APIRouter()


@router.get('/', response_model=list[Genre])
async def genre_query(genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    genre = await genre_service.get_genres()
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Genres not found')
    return genre


@router.get('/{genre_id}', response_model=Genre)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Genre not found')
    return Genre(uuid=genre.uuid, name=genre.name)
