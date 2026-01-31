import json
import time
import requests
from confluent_kafka import Producer

# setup kafka configuration

kakfa_config = {
    'bootstrap.servers': 'localhost:9092'
}
producer = Producer(kakfa_config)

