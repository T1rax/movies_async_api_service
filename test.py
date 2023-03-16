from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

query_body = {
    "match": {
        "title": "Qui-Gon"
    }
}

data = es.search(index="movies", q='title:Qui-Gon')

for film in data['hits']['hits']:
    print(film['_source']['title'])