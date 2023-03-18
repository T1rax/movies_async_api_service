from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from models.person import Person, PersonFilmList
from services.person import PersonService, get_person_service


router = APIRouter()


@router.get('/search', response_model=list[Person])
async def person_search(query: str | None = None,
                        page_number: int | None = 1,
                        page_size: int | None = 50,
                        person_service: PersonService = Depends(get_person_service)) -> Person:
    persons = await person_service.get_by_search(q=query, page_number=page_number, page_size=page_size)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Persons not found')
    return persons


@router.get('/{person_id}', response_model=Person)
async def person_details(person_id: str,
                         person_service: PersonService = Depends(get_person_service)) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Person not found')
    return Person(uuid=person.uuid, full_name=person.full_name, films=person.films)


@router.get('/{person_id}/film', response_model=list[PersonFilmList])
async def person_films(person_id: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    person = await person_service.get_persons_films(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Person not found')
    return person