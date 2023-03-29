from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Query
from models.person import Person, PersonFilmList
from services.person import PersonService, get_person_service


router = APIRouter()


@router.get('/search',
            response_model=list[Person],
            description="Search for the person")
async def person_search(query: str | None = None,
                        page_number: int = Query(default=1, gt=0, le=100),
                        page_size: int = Query(default=50, gt=0, le=100),
                        person_service: PersonService = Depends(get_person_service)
                        ) -> Person:
    persons = await person_service.get_by_search(q=query,
                                                 page_number=page_number,
                                                 page_size=page_size)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=f'Persons not found')
    return persons


@router.get('/{person_id}',
            response_model=Person,
            description="Show information about the person")
async def person_details(person_id: str,
                         person_service: PersonService = Depends(get_person_service)
                         ) -> Person:
    person = await person_service.get_by_id(person_id=person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Person not found')
    return Person(uuid=person.uuid, full_name=person.full_name, films=person.films)


@router.get('/{person_id}/film',
            response_model=list[PersonFilmList],
            description="Show information about person's films")
async def person_films(person_id: str,
                       person_service: PersonService = Depends(get_person_service)
                       ) -> Person:
    person = await person_service.get_persons_films(person_id=person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Person not found')
    return person
