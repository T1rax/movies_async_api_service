import time
import os, sys
from elasticsearch import Elasticsearch

parent = os.path.abspath('.')
sys.path.insert(1, parent)
from settings import test_settings

if __name__ == '__main__':
    es_client = Elasticsearch(hosts=test_settings.es_url)
    while True:
        if es_client.ping():
            print('es connected')
            break
        print('es wait next try')
        time.sleep(5)