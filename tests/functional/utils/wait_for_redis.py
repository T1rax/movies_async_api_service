import time
import os, sys
from redis import Redis

parent = os.path.abspath('.')
sys.path.insert(1, parent)
from settings import test_settings

if __name__ == '__main__':
    redis_client = Redis(host=test_settings.redis_host, port=test_settings.redis_port)
    while True:
        if redis_client.ping():
            print('redis connected')
            break
        print('redis wait next try')
        time.sleep(5)