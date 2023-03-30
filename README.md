## How to start the project:

Create and set env according to .env.example in root directory.

### Run docker-compose with this command:
```
docker-compose up --build
```
or background mode:
```
docker-compose up --build -d
```

When you initialize the project, it will automatically load data from Sqlite into Postgres, migrate to Django, and set up a superuser. After that the ETL process (transform, extract, load) will start, data will transfer from Postgres to Elasticsearch.

### To check the result:
- Full-text search for movies - http://127.0.0.1:9200/movies/_search
- Opening an administrative site - http://127.0.0.1:80/admin/
- Django API - http://127.0.0.1:80/api/v1/movies/


## How to run tests

Create and set env according to .env.example in root directory.

### Navigate to tests folder - tests/functional

### Run docker-compose with this command:
```
docker-compose up --build
```
or background mode:
```
docker-compose up --build -d
```
