import backoff
import logging
import os, sys

from elasticsearch import Elasticsearch
from redis import Redis

parent = os.path.abspath('.')
sys.path.insert(1, parent)
from settings import test_settings, ServiceNotReady

logging.getLogger('elastic_transport').setLevel(logging.ERROR)


@backoff.on_exception(backoff.expo, ServiceNotReady, jitter=backoff.full_jitter, max_time=180)
def wait_for_es():
    es_client = Elasticsearch(hosts=test_settings.es_url)

    if not es_client.ping():
        logging.info('ElasticSearch not awailable yet, wait for next try')
        raise ServiceNotReady('ElasticSearch not awailable yet')


@backoff.on_exception(backoff.expo, ServiceNotReady, jitter=backoff.full_jitter, max_time=180)
def wait_for_cache():
    cache_client = Redis(host=test_settings.cache_host, port=test_settings.cache_port)
    
    if not cache_client.ping():
        logging.info('Redis not awailable yet, wait for next try')
        raise ServiceNotReady('Redis not awailable yet')


if __name__ == '__main__':
    wait_for_es()
    wait_for_cache()