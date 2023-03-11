movies_query = '''
SELECT
   fw.id,
   fw.title,
   fw.description,
   fw.rating,
   fw.type,
   fw.created_at,
   fw.updated_at,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'person_role', pfw.role,
               'person_id', p.id,
               'person_name', p.full_name
           )
       ) FILTER (WHERE p.id is not null),
       '[]'
   ) as persons,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'genre_id', g.id,
               'genre_name', g.name
           )
       ) FILTER (WHERE g.id is not null),
       '[]'
   ) as genres
FROM content.film_work fw
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
WHERE fw.updated_at > %s OR p.updated_at > %s OR g.updated_at > %s
GROUP BY fw.id
ORDER BY fw.updated_at DESC
'''

persons_query = '''
SELECT
    p.id,
    p.full_name,
    COALESCE (
        json_agg(
            DISTINCT jsonb_build_object(
                'film_id', fw.id,
                'film_title', fw.title,
                'film_rating', fw.rating,
                'film_roles', array_agg(pfw.role)
            )
        ) FILTER (WHERE fw.id is not null),
        '[]'
    ) AS films,
    p.updated_at
FROM content.person AS p
LEFT JOIN content.person_film_work AS pfw 
    ON pfw.person_id = p.id
LEFT JOIN content.film_work AS fw
    ON fw.id = pfw.film_work_id
WHERE p.updated_at > %s
GROUP BY p.id
ORDER BY p.updated_at, p.id ASC
'''